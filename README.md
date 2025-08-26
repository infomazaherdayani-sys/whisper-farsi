# Persian Speech-to-Text Service with Flask + Whisper

This repository provides a simple API for **speech-to-text in Persian** built with Flask. It uses the Hugging Face model **`vhdm/whisper-large-fa-v1`**. Any uploaded audio file is first converted to WAV (16kHz, mono) using **FFmpeg**, and then transcribed.

---

## ✨ Features

* Persian ASR with a fine-tuned Whisper model
* Automatic conversion of input audio to WAV (16kHz, mono)
* Simple API endpoint for transcription
* Ready for development and deployment

---

## 🧰 Requirements

* **Python 3.9 – 3.12** (64-bit)
* **FFmpeg** installed and available in PATH

  * Windows: default path in code is `C:\ffmpeg\bin`
  * Linux/macOS: ensure `ffmpeg -version` works in terminal
* **Disk space** for model downloads (several GB on first run)
* (Optional) **GPU + CUDA** for faster inference

> ⚠️ First run may take a while to download model weights.

---

## 📁 Project Structure

```
.
├─ app.py                 # Main Flask application
├─ uploads/               # Temporary upload folder
├─ requirements.txt       # Dependencies
└─ README.md              # This file
```

---

## 🔧 Installation & Setup

### 1) Install FFmpeg

* **Windows**:

  1. Download FFmpeg and extract to `C:\ffmpeg`.
  2. Ensure `C:\ffmpeg\bin` exists. The code adds this path automatically:

     ```python
     os.environ["PATH"] += os.pathsep + r"C:\\ffmpeg\\bin"
     ```
  3. Update this path in `app.py` if FFmpeg is installed elsewhere.

* **Ubuntu/Debian**:

  ```bash
  sudo apt update && sudo apt install -y ffmpeg
  ```

* **macOS (Homebrew)**:

  ```bash
  brew install ffmpeg
  ```

### 2) Create and activate virtual environment

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Sample `requirements.txt`:

```txt
Flask>=3.0.0
transformers>=4.41.0
torch>=2.2.0
openai-whisper>=20231117
werkzeug>=3.0.0
numpy
```

> **Note:** The `openai-whisper` package provides `import whisper`. Without it you’ll get `ModuleNotFoundError: No module named 'whisper'`.

### 4) Run the service

```bash
python app.py
```

Expected output:

```
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

---

## 🚏 API Endpoint

### POST `/transcribe`

* **Content type:** `multipart/form-data`
* **Required field:** `audio` (the audio file)

**Successful response:**

```json
{
  "text": "recognized transcription"
}
```

**Error examples:**

```json
{"error": "No audio file uploaded"}
{"error": "Invalid filename"}
```

---

## 🧪 Quick Test

### With `curl`

```bash
curl -X POST \
  -F "audio=@/path/to/sample.mp3" \
  http://127.0.0.1:5000/transcribe
```

### With Python (requests)

```python
import requests

url = "http://127.0.0.1:5000/transcribe"
files = {"audio": open("/path/to/sample.mp3", "rb")}
r = requests.post(url, files=files)
print(r.json())
```

---

## ⚙️ Configuration Notes

* **FFmpeg path (Windows):** Update in `app.py` if not in `C:\ffmpeg\bin`.
* **Upload folder:** Configured as `uploads/`. Change in `app.py` for production.
* **Model cache:** Stored under Hugging Face cache (`~/.cache/huggingface`). Set `HF_HOME` to customize.
* **GPU support:** Requires CUDA-enabled PyTorch. Example:

  ```python
  import torch
  device = 0 if torch.cuda.is_available() else -1
  pipe = pipeline(
      "automatic-speech-recognition",
      model="vhdm/whisper-large-fa-v1",
      device=device,
  )
  ```
* **Cleanup:** The current code loads `whisper.load_model("medium")` but doesn’t use it. Safe to remove.

---

## 🛡️ Production Deployment

* **Linux**: Run with `gunicorn` behind Nginx.
* **Windows**: Use `waitress` instead of `flask run`.
* Enable logging, limit file size, secure upload folder.

Example with `gunicorn`:

```bash
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

---

## 🔍 Troubleshooting

* **`ModuleNotFoundError: No module named 'flask'`** → Ensure virtualenv is active and dependencies installed.
* **`ffmpeg not found`** → Add FFmpeg to PATH.
* **Long model download** → Happens only first run.
* **Out of memory** → Use a smaller Whisper model or GPU.
* **File errors** → Ensure field name is `audio` and file is valid.

---

## 🔒 Security Recommendations

* Validate file type, MIME, and size
* Periodically clean `uploads/`
* Disable `debug=True` in production
* Apply request size limits in reverse proxy or WSGI

---

## 📝 License

Add a license of your choice (MIT, Apache-2.0, GPL-3.0, ...).

---

## 🙌 Contributing

Contributions via Pull Requests and Issues are welcome. Please test before submitting PRs.

---

## 📣 Acknowledgments

* \[Hugging Face Transformers]
* \[OpenAI Whisper]
* Open-source community
