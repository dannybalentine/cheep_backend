from flask import Flask, jsonify, request
import json
import librosa
import os
from birdnet_functions import get_birdcall
import traceback

ALLOWED_EXTENSIONS = {'mp3', 'wav'}
app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = '/home/ubuntu/helloworld/temp'


@app.route('/hello')
def hello_world():
    data = {'message': 'Hello Jack!'}
    return jsonify(data)

@app.route('/upload_audio', methods=['POST'])
def upload_audio():

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    try:
        # Check if the POST request has the file part
        if 'audio_file' not in request.files:
            return jsonify({'error': 'No file part'})

        audio_file = request.files['audio_file']
        
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        
        
        # Check if the file is empty
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        # Check if the file has an allowed extension
        #if not allowed_file(audio_file.filename):
        #    return jsonify({'error': 'Invalid file extension'})

        # Save the file to the upload folder
        filename = os.path.join(app.config['DOWNLOAD_FOLDER'], audio_file.filename)
        audio_file.save(filename)

        birdname = get_birdcall(filename)

        
        #audio, sr = librosa.load(audio_file)

        #duration_seconds = librosa.get_duration(y=audio, sr=sr)
        return jsonify(birdname)
    except Exception as e:
        return jsonify({'error':str(e)}), 500

@app.route('/simple_post', methods=['POST'])
def simple_post():
    try:
        data = request.get_json()
        with open('received_data.txt', 'w') as file:
            file.write(json.dumps(data, indent=2))

        response_data = {'message': 'Hello Spaceman!'}
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
