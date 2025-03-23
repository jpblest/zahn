from flask import render_template, request, jsonify
from app import app, socketio
import speech_recognition as sr
import soundfile as sf
import io
from utils import save_audio_file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio']

    try:
        # Save the audio file using the utility function
        filename = save_audio_file(audio_file.read())

        # Load the audio file using soundfile
        audio_data, samplerate = sf.read(io.BytesIO(audio_file.read()))

        # Convert the audio data to a format compatible with speech_recognition
        recognizer = sr.Recognizer()
        audio_source = sr.AudioData(audio_data.tobytes(), samplerate, 2)  # 2 for 16-bit audio

        # Perform speech recognition
        text = recognizer.recognize_google(audio_source)
        return jsonify({'text': text, 'filename': filename})
    except sr.UnknownValueError:
        return jsonify({'text': "Could not understand audio"}), 400
    except sr.RequestError:
        return jsonify({'text': "API unavailable"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Optional: Keep the socketio handler for real-time transcription (if needed)
@socketio.on('audio_stream')
def handle_audio_stream(data):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioData(data['audio'], data['sample_rate'], data['sample_width'])
    try:
        text = recognizer.recognize_google(audio_data)
        socketio.emit('transcription', {'text': text})
    except sr.UnknownValueError:
        socketio.emit('transcription', {'text': "Could not understand audio"})
    except sr.RequestError:
        socketio.emit('transcription', {'text': "API unavailable"})
