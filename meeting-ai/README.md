# Meeting AI — Локальный сервис для транскрибации и конспектирования встреч

Сервис автоматически транскрибирует аудио/видео записи встреч, разделяет спикеров и создаёт структурированный конспект.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
cd meeting-ai
pip install -r requirements.txt
```

### 2. Установка Ollama

**Linux/macOS:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** Скачайте установщик с https://ollama.com

### 3. Скачивание модели Ollama

```bash
ollama pull qwen2.5:7b-instruct
```

### 4. Получение Hugging Face Token

1. Зарегистрируйтесь на https://huggingface.co
2. Перейдите в Settings → Access Tokens
3. Создайте токен с правами `read`
4. Примите лицензионные соглашения моделей:
   - https://huggingface.co/pyannote/speaker-diarization-3.1
   - https://huggingface.co/pyannote/segmentation-3.0

### 5. Настройка переменных окружения

```bash
export HF_TOKEN="your_huggingface_token_here"
export OLLAMA_HOST="http://localhost:11434"
export OLLAMA_MODEL="qwen2.5:7b-instruct"
```

Или скопируйте `.env.example` в `.env` и отредактируйте.

### 6. Запуск сервиса

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Откройте http://localhost:8000 в браузере.

---

## 📋 Требования к системе

- **ОС:** Linux, macOS, Windows
- **Python:** 3.9+
- **RAM:** минимум 8GB (рекомендуется 16GB+)
- **GPU:** опционально (NVIDIA с CUDA ускорит обработку в 5-10 раз)
- **Диск:** ~5GB для моделей

---

## 🔧 Конфигурация

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `HF_TOKEN` | Токен Hugging Face для pyannote | (обязательно) |
| `OLLAMA_HOST` | Адрес Ollama API | `http://localhost:11434` |
| `OLLAMA_MODEL` | Модель для суммаризации | `qwen2.5:7b-instruct` |
| `MAX_FILE_SIZE_MB` | Макс. размер файла | `2048` |
| `PORT` | Порт сервиса | `8000` |

---

## 📡 API Endpoints

### POST /upload
Загрузка аудио/видео файла.

**Request:** `multipart/form-data` с полем `file`

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "queued"
}
```

### GET /status/{job_id}
Получение статуса обработки.

**Response:**
```json
{
  "job_id": "uuid-string",
  "filename": "meeting.mp3",
  "status": "processing|done|error",
  "progress": 45,
  "status_message": "Транскрибация: 120 сегментов",
  "transcript": [...],
  "summary": "...",
  "error": null
}
```

### GET /download/{job_id}/{type}
Скачивание результата.

**Parameters:**
- `type`: `md` (конспект) или `json` (транскрипт)

---

## 🏗️ Архитектура

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Upload    │ ──► │  Whisper STT │ ──► │  Pyannote   │
│   (FastAPI) │     │  (large-v3)  │     │  Diarization│
└─────────────┘     └──────────────┘     └─────────────┘
                                                 │
                                                 ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Output    │ ◄── │   Ollama     │ ◄── │   Align     │
│  (MD/JSON)  │     │  Summarize   │     │  Speakers   │
└─────────────┘     └──────────────┘     └─────────────┘
```

### Этапы обработки:

1. **Транскрибация (0-30%)** — faster-whisper с word_timestamps
2. **Диаризация (30-50%)** — pyannote/speaker-diarization-3.1
3. **Алигнмент (50-60%)** — сопоставление спикеров по временному перекрытию
4. **Суммаризация (60-95%)** — иерархическое суммирование через Ollama
5. **Финальная сборка (95-100%)** — формирование результата

---

## 📁 Структура проекта

```
meeting-ai/
├── main.py              # FastAPI приложение
├── pipeline.py          # Логика обработки (STT→Diarize→Align→LLM)
├── requirements.txt     # Python зависимости
├── .env.example         # Шаблон переменных окружения
├── templates/
│   └── index.html       # Веб-интерфейс
├── static/
│   └── style.css        # Стили
├── data/                # Статусы задач и результаты (авто-создание)
└── uploads/             # Временные файлы (авто-очистка)
```

---

## 🔒 Безопасность

- Все вычисления происходят локально
- Файлы загружаются только во временную папку
- Автоматическая очистка uploads/ каждые 2 часа
- Данные задач хранятся в JSON без отправки наружу

---

## ⚠️ Возможные проблемы

### Ollama не доступен
```bash
# Проверьте, запущен ли Ollama
ollama serve

# Или проверьте статус
curl http://localhost:11434/api/tags
```

### Ошибка pyannote.audio
- Убедитесь, что HF_TOKEN установлен
- Примите лицензии моделей на Hugging Face
- Проверьте интернет-соединение при первой загрузке моделей

### Недостаточно памяти
- Закройте другие приложения
- Используйте меньшие файлы
- Рассмотрите использование GPU

### Медленная обработка на CPU
- Транскрибация 1 часа аудио может занять 10-30 минут на CPU
- Рекомендуется NVIDIA GPU с CUDA
- Модель кешируется после первой загрузки

---

## 📝 Лицензии

- faster-whisper: MIT License
- pyannote.audio: MIT License
- Ollama/qwen2.5: Apache 2.0
- Этот проект: MIT License

---

## 🙏 Благодарности

- [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [Ollama](https://ollama.com/)
- [Qwen](https://huggingface.co/Qwen)
