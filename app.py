# app.py

from flask import Flask, request, render_template
from flask_cors import CORS
from utils import process_audio, get_surahs, get_ayahs

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/surahs', methods=['GET'])
def get_surahs_endpoint():
    return get_surahs()

@app.route('/ayahs/<int:surah_id>', methods=['GET'])
def get_ayahs_endpoint(surah_id):
    return get_ayahs(surah_id)

@app.route('/process-audio', methods=['POST'])
def process_audio_endpoint():
    return process_audio(request)

if __name__ == "__main__":
    app.run(debug=True)
