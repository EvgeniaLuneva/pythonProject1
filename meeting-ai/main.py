import os
import json
import shutil
import uuid
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from pipeline import MeetingPipeline


# Пути
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Создаём директории
DATA_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

# Загружаем переменные окружения
HF_TOKEN = os.getenv("HF_TOKEN", "")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "2048"))

# Валидация при старте
if not HF_TOKEN:
    print("⚠️  ПРЕДУПРЕЖДЕНИЕ: HF_TOKEN не установлен. pyannote.audio не будет работать без токена.")
    print("   Получите токен: https://huggingface.co/settings/tokens")
    print("   Установите через: export HF_TOKEN=your_token")

# Инициализируем приложение
app = FastAPI(
    title="Meeting AI",
    description="Сервис для транскрибации и конспектирования встреч",
    version="1.0.0",
)

# Статика и шаблоны
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Глобальный пайплайн (ленивая инициализация)
pipeline: Optional[MeetingPipeline] = None

# Хранилище задач в памяти + на диске
jobs: Dict[str, Dict[str, Any]] = {}


def get_job_path(job_id: str) -> Path:
    return DATA_DIR / f"{job_id}.json"


def load_job(job_id: str) -> Optional[Dict[str, Any]]:
    path = get_job_path(job_id)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return jobs.get(job_id)


def save_job(job_id: str, data: Dict[str, Any]):
    jobs[job_id] = data
    path = get_job_path(job_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_job_progress(job_id: str, progress: int, status_msg: str):
    job = load_job(job_id)
    if job:
        job["progress"] = progress
        job["status_message"] = status_msg
        if progress == 100:
            job["status"] = "done"
        elif progress == 0 and "Ошибка" in status_msg:
            job["status"] = "error"
        else:
            job["status"] = "processing"
        job["updated_at"] = datetime.utcnow().isoformat()
        save_job(job_id, job)


async def process_file_task(job_id: str, file_path: str):
    """Фоновая задача обработки файла"""
    global pipeline
    
    try:
        if pipeline is None:
            pipeline = MeetingPipeline(
                hf_token=HF_TOKEN,
                ollama_host=OLLAMA_HOST,
                ollama_model=OLLAMA_MODEL,
            )
        
        def progress_callback(progress: int, message: str):
            update_job_progress(job_id, progress, message)
        
        result = await pipeline.process(file_path, job_id, progress_callback)
        
        # Сохраняем результат
        job = load_job(job_id)
        if job:
            job["transcript"] = result.get("transcript", [])
            job["summary"] = result.get("summary", "")
            job["stages"] = result.get("stages", {})
            if "error" in result:
                job["error"] = result["error"]
                job["traceback"] = result.get("traceback", "")
                job["status"] = "error"
            else:
                job["status"] = "done"
            job["completed_at"] = datetime.utcnow().isoformat()
            save_job(job_id, job)
        
        # Очищаем загруженный файл после обработки
        try:
            os.remove(file_path)
        except Exception:
            pass
            
    except Exception as e:
        job = load_job(job_id)
        if job:
            job["status"] = "error"
            job["error"] = str(e)
            job["updated_at"] = datetime.utcnow().isoformat()
            save_job(job_id, job)


def cleanup_old_files():
    """Очистка файлов старше 2 часов"""
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=2)
    
    # Очистка uploads
    for f in UPLOADS_DIR.glob("*"):
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime < cutoff:
                f.unlink()
        except Exception:
            pass
    
    # Очистка старых job-файлов (старше 24 часов)
    old_cutoff = now - timedelta(hours=24)
    for f in DATA_DIR.glob("*.json"):
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime < old_cutoff:
                f.unlink()
        except Exception:
            pass


@app.on_event("startup")
async def startup_event():
    """Проверки при старте"""
    print("🚀 Запуск Meeting AI сервиса...")
    
    # Проверка Ollama
    import httpx
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{OLLAMA_HOST}/api/tags")
            if resp.status_code == 200:
                print(f"✅ Ollama доступен: {OLLAMA_HOST}")
            else:
                print(f"⚠️  Ollama вернул статус {resp.status_code}")
    except Exception as e:
        print(f"⚠️  Ollama недоступен: {e}")
        print(f"   Убедитесь, что Ollama запущен: ollama serve")
    
    # Проверка наличия модели
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{OLLAMA_HOST}/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                if OLLAMA_MODEL not in models:
                    print(f"⚠️  Модель {OLLAMA_MODEL} не найдена. Скачайте: ollama pull {OLLAMA_MODEL}")
                else:
                    print(f"✅ Модель {OLLAMA_MODEL} доступна")
    except Exception:
        pass
    
    # Очистка старых файлов
    cleanup_old_files()
    print("📁 Директории готовы")


@app.get("/", response_class=HTMLResponse)
async def index():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Загрузка файла и запуск обработки"""
    
    # Валидация размера
    file.file.seek(0, 2)
    size_bytes = file.file.tell()
    file.file.seek(0)
    size_mb = size_bytes / (1024 * 1024)
    
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"Файл слишком большой: {size_mb:.1f} МБ (максимум {MAX_FILE_SIZE_MB} МБ)"
        )
    
    # Валидация формата
    allowed_extensions = {".mp3", ".wav", ".m4a", ".mp4", ".webm", ".ogg", ".flac"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат: {ext}. Допустимы: {', '.join(allowed_extensions)}"
        )
    
    # Создаём job
    job_id = str(uuid.uuid4())
    
    # Сохраняем файл
    file_path = UPLOADS_DIR / f"{job_id}{ext}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Создаём запись задачи
    job_data = {
        "job_id": job_id,
        "filename": file.filename,
        "status": "queued",
        "progress": 0,
        "status_message": "В очереди",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "transcript": [],
        "summary": "",
        "error": None,
    }
    save_job(job_id, job_data)
    
    # Запускаем фоновую задачу
    app.background_tasks.add_task(process_file_task, job_id, str(file_path))
    
    return {"job_id": job_id, "status": "queued"}


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Получение статуса задачи"""
    job = load_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return {
        "job_id": job["job_id"],
        "filename": job.get("filename", ""),
        "status": job.get("status", "unknown"),
        "progress": job.get("progress", 0),
        "status_message": job.get("status_message", ""),
        "transcript": job.get("transcript", []),
        "summary": job.get("summary", ""),
        "error": job.get("error"),
        "created_at": job.get("created_at"),
        "completed_at": job.get("completed_at"),
    }


@app.get("/download/{job_id}/{type}")
async def download_file(job_id: str, type: str):
    """Скачивание результата"""
    job = load_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    if job.get("status") != "done":
        raise HTTPException(status_code=400, detail="Задача ещё не завершена")
    
    filename_base = Path(job.get("filename", "meeting")).stem
    
    if type == "md":
        # Генерируем Markdown файл
        summary = job.get("summary", "Нет данных")
        content = f"# Конспект встречи\n\n{summary}\n"
        
        file_path = DATA_DIR / f"{job_id}_summary.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return FileResponse(
            file_path,
            media_type="text/markdown",
            filename=f"{filename_base}_summary.md",
        )
    
    elif type == "json":
        # Генерируем JSON с транскриптом
        transcript = job.get("transcript", [])
        content = json.dumps(transcript, ensure_ascii=False, indent=2)
        
        file_path = DATA_DIR / f"{job_id}_transcript.json"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return FileResponse(
            file_path,
            media_type="application/json",
            filename=f"{filename_base}_transcript.json",
        )
    
    else:
        raise HTTPException(status_code=400, detail="Неподдерживаемый тип. Используйте 'md' или 'json'")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
