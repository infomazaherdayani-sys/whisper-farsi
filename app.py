from flask import Flask, request, jsonify
from transformers import pipeline
import whisper
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

# اضافه کردن ffmpeg به PATH
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# بارگذاری مدل Whisper
model = whisper.load_model("medium")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def convert_audio(input_path, output_path):
    """تبدیل فایل صوتی به wav تک کاناله با 16khz"""
    command = ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pipe = pipeline("automatic-speech-recognition", model="vhdm/whisper-large-fa-v1")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "فایل صوتی ارسال نشده"}), 400

    file = request.files["audio"]
    if file.filename == "":
        return jsonify({"error": "نام فایل معتبر نیست"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # تبدیل فایل
    converted_file = os.path.join(app.config["UPLOAD_FOLDER"], "converted.wav")
    convert_audio(filepath, converted_file)

    try:
        # ترنسکرایب فارسی
        # result = model.transcribe(converted_file, language="fa", task="transcribe")
        result = pipe(converted_file)
        text = result["text"]
        return jsonify({"text": text})
    finally:
        # حذف فایل موقت
        if os.path.exists(converted_file):
            os.remove(converted_file)

if __name__ == "__main__":
    app.run(debug=True)
