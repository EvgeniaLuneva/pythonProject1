import os
import json
import traceback
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime

import torch
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline as PyannotePipeline


class MeetingPipeline:
    """Пайплайн обработки встреч: STT → Диаризация → Алигнмент → LLM суммаризация"""

    def __init__(
        self,
        hf_token: str,
        ollama_host: str = "http://localhost:11434",
        ollama_model: str = "qwen2.5:7b-instruct",
    ):
        self.hf_token = hf_token
        self.ollama_host = ollama_host
        self.ollama_model = ollama_model
        
        # Определяем устройство
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Инициализируем модели (ленивая загрузка)
        self._whisper_model = None
        self._pyannote_pipeline = None
        
    @property
    def whisper_model(self):
        if self._whisper_model is None:
            self._whisper_model = WhisperModel(
                "large-v3-turbo",
                device=self.device,
                compute_type="float32" if self.device == "cpu" else "float16",
            )
        return self._whisper_model
    
    @property
    def pyannote_pipeline(self):
        if self._pyannote_pipeline is None:
            self._pyannote_pipeline = PyannotePipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.hf_token,
            )
            self._pyannote_pipeline.to(torch.device(self.device))
        return self._pyannote_pipeline

    async def process(
        self,
        audio_path: str,
        job_id: str,
        progress_callback: Callable[[int, str], None],
    ) -> Dict[str, Any]:
        """
        Полный пайплайн обработки аудиофайла.
        Возвращает транскрипт и саммари.
        """
        result = {
            "job_id": job_id,
            "transcript": [],
            "summary": "",
            "stages": {},
        }
        
        try:
            # Этап 1: Транскрибация (0-30%)
            progress_callback(5, "Запуск транскрибации...")
            whisper_segments = await self._transcribe(audio_path, progress_callback)
            progress_callback(30, "Транскрибация завершена")
            result["stages"]["transcription"] = "done"
            
            # Этап 2: Диаризация (30-50%)
            progress_callback(35, "Запуск диаризации спикеров...")
            pyannote_segments = await self._diarize(audio_path, progress_callback)
            progress_callback(50, "Диаризация завершена")
            result["stages"]["diarization"] = "done"
            
            # Этап 3: Алигнмент (50-60%)
            progress_callback(55, "Алигнмент спикеров с транскриптом...")
            aligned_transcript = self._align_speakers(whisper_segments, pyannote_segments)
            progress_callback(60, "Алигнмент завершён")
            result["stages"]["alignment"] = "done"
            result["transcript"] = aligned_transcript
            
            # Этап 4: Суммаризация через LLM (60-95%)
            progress_callback(65, "Подготовка к суммаризации...")
            summary = await self._summarize(aligned_transcript, progress_callback)
            progress_callback(95, "Суммаризация завершена")
            result["stages"]["summarization"] = "done"
            result["summary"] = summary
            
            # Этап 5: Финальная сборка (95-100%)
            progress_callback(100, "Обработка завершена")
            result["stages"]["complete"] = "done"
            
        except Exception as e:
            error_trace = traceback.format_exc()
            result["error"] = str(e)
            result["traceback"] = error_trace
            progress_callback(0, f"Ошибка: {str(e)}")
            raise
        
        return result

    async def _transcribe(
        self,
        audio_path: str,
        progress_callback: Callable[[int, str], None],
    ) -> List[Dict[str, Any]]:
        """Транскрибация аудио через faster-whisper"""
        segments, info = self.whisper_model.transcribe(
            audio_path,
            language="ru",
            word_timestamps=True,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
        )
        
        result = []
        for segment in segments:
            result.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "words": [
                    {
                        "start": w.start,
                        "end": w.end,
                        "word": w.word,
                    }
                    for w in (segment.words or [])
                ],
            })
            # Обновляем прогресс примерно по количеству сегментов
            progress_callback(
                5 + int(len(result) / max(1, len(result) + 10) * 25),
                f"Транскрибация: {len(result)} сегментов",
            )
        
        return result

    async def _diarize(
        self,
        audio_path: str,
        progress_callback: Callable[[int, str], None],
    ) -> List[Dict[str, Any]]:
        """Диаризация спикеров через pyannote"""
        diarization = self.pyannote_pipeline(audio_path)
        
        result = []
        count = 0
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            result.append({
                "speaker": speaker,
                "start": turn.start,
                "end": turn.end,
            })
            count += 1
            if count % 10 == 0:
                progress_callback(
                    30 + int(count / max(1, count + 50) * 20),
                    f"Диаризация: {count} сегментов спикеров",
                )
        
        return result

    def _align_speakers(
        self,
        whisper_segments: List[Dict[str, Any]],
        pyannote_segments: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Алигнмент спикеров к словам/сегментам whisper через максимальное временное перекрытие.
        Для каждого whisper-сегмента находим pyannote-спикера с max overlap.
        """
        aligned = []
        
        for ws in whisper_segments:
            w_start = ws["start"]
            w_end = ws["end"]
            w_duration = w_end - w_start
            
            best_speaker = "SPEAKER_00"
            best_overlap = 0.0
            
            for ps in pyannote_segments:
                p_start = ps["start"]
                p_end = ps["end"]
                
                # Вычисляем перекрытие
                overlap_start = max(w_start, p_start)
                overlap_end = min(w_end, p_end)
                
                if overlap_end > overlap_start:
                    overlap = overlap_end - overlap_start
                    overlap_ratio = overlap / w_duration if w_duration > 0 else 0
                    
                    if overlap_ratio > best_overlap:
                        best_overlap = overlap_ratio
                        best_speaker = ps["speaker"]
            
            aligned.append({
                "speaker": best_speaker,
                "text": ws["text"],
                "start": round(w_start, 2),
                "end": round(w_end, 2),
            })
        
        return aligned

    async def _summarize(
        self,
        transcript: List[Dict[str, Any]],
        progress_callback: Callable[[int, str], None],
    ) -> str:
        """
        Иерархическое суммаризирование через Ollama.
        Разбивает транскрипт на чанки по ~10 минут речи.
        """
        import httpx
        
        # Оцениваем длительность речи по транскрипту
        if not transcript:
            return "*Нет данных для суммаризации*"
        
        total_duration = transcript[-1]["end"] - transcript[0]["start"]
        
        # Разбиваем на чанки по ~600 секунд (10 минут)
        chunk_duration = 600
        chunks = []
        current_chunk = []
        current_start = transcript[0]["start"]
        
        for segment in transcript:
            current_chunk.append(segment)
            if segment["end"] - current_start >= chunk_duration:
                chunks.append(current_chunk)
                current_chunk = []
                current_start = segment["end"]
        
        if current_chunk:
            chunks.append(current_chunk)
        
        progress_callback(70, f"Разбито на {len(chunks)} чанков для суммаризации")
        
        partial_summaries = []
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            for i, chunk in enumerate(chunks):
                chunk_text = "\n".join(
                    f"[{s['speaker']}]: {s['text']}" for s in chunk
                )
                
                prompt = f"""Ты помощник для конспектирования встреч. Ниже транскрипт части встречи.
Сделай краткий конспект этой части, выделив ключевые моменты, решения и задачи.

Транскрипт:
{chunk_text}

Конспект части:"""
                
                progress_callback(
                    70 + int((i + 1) / len(chunks) * 20),
                    f"Суммаризация чанка {i+1}/{len(chunks)}",
                )
                
                try:
                    response = await client.post(
                        f"{self.ollama_host}/api/generate",
                        json={
                            "model": self.ollama_model,
                            "prompt": prompt,
                            "stream": False,
                            "options": {
                                "temperature": 0.3,
                                "top_p": 0.8,
                            },
                        },
                    )
                    response.raise_for_status()
                    data = response.json()
                    partial_summaries.append(data.get("response", ""))
                except Exception as e:
                    partial_summaries.append(f"[Ошибка суммаризации чанка {i+1}: {str(e)}]")
        
        # Финальное объединение
        if len(partial_summaries) == 1:
            final_summary = partial_summaries[0]
        else:
            combined = "\n\n---\n\n".join(partial_summaries)
            
            final_prompt = f"""Ты помощник для конспектирования встреч. Ниже конспекты отдельных частей встречи.
Объедини их в единый структурированный конспект.

Структура конспекта:
# Тема встречи
## Участники
## Ключевые обсуждения
## Принятые решения
## Задачи (с ответственным если указан)
## Открытые вопросы

Конспекты частей:
{combined}

Итоговый конспект в формате Markdown:"""
            
            progress_callback(90, "Финальное объединение конспекта")
            
            try:
                async with httpx.AsyncClient(timeout=300.0) as client:
                    response = await client.post(
                        f"{self.ollama_host}/api/generate",
                        json={
                            "model": self.ollama_model,
                            "prompt": final_prompt,
                            "stream": False,
                            "options": {
                                "temperature": 0.3,
                                "top_p": 0.8,
                            },
                        },
                    )
                    response.raise_for_status()
                    data = response.json()
                    final_summary = data.get("response", "")
            except Exception as e:
                final_summary = combined
        
        return final_summary
