import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from gtts import gTTS
import moviepy.editor as mp
import speech_recognition as sr

# Path to the Tesseract executable (change this to your installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    language = request.form.get('language', 'en')
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_ext = filename.rsplit('.', 1)[1].lower()
        extracted_text = ""
        if file_ext in ['png', 'jpg', 'jpeg']:
            # OCR for images
            try:
                extracted_text = pytesseract.image_to_string(Image.open(filepath), lang=language)
            except Exception as e:
                return f"Error during OCR: {e}", 500
        elif file_ext in ['mp4', 'mov']:
            # ASR (Automatic Speech Recognition) for video
            try:
                video = mp.VideoFileClip(filepath)
                audio_file = video.audio
                audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
                audio_file.write_audiofile(audio_path, logger=None)
                r = sr.Recognizer()
                with sr.AudioFile(audio_path) as source:
                    audio_data = r.record(source)
                extracted_text = r.recognize_google(audio_data, language=language)
                os.remove(audio_path)  # Clean up temp file
            except Exception as e:
                return f"Error during video processing: {e}", 500
        if not extracted_text:
            return "Could not extract text from the file.", 400
        # Convert extracted text to audio
        tts = gTTS(text=extracted_text, lang=language, slow=False)
        audio_filename = f"echoverse_audio_{os.path.splitext(filename)[0]}.mp3"
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        tts.save(audio_path)
        return send_file(audio_path, as_attachment=True)
    return "Invalid file type", 400

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)