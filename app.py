'''
Author: Daniel Balentine
Contact: dannybalentine@gmail.com
Date: 2023-12-06

Synopsis:
This Flask application serves as an API for birdcall recognition using the BirdNET-Analyzer.
It includes endpoints for simple greetings, uploading audio files, and receiving JSON data.

Note: Make sure to install the required dependencies (Flask, librosa, etc.) before running the script.
'''

from flask import Flask, jsonify, request
import os
from birdnet_functions import get_birdcall

ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = '/home/ubuntu/helloworld/temp'


@app.route('/hello')
def hello_world():
    """
    Endpoint for a simple greeting message.
    """
    data = {'message': 'Hello Jack!'}
    return jsonify(data)


@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    """
    Endpoint for uploading an audio file and obtaining birdcall recognition results.
    """
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
        
        # Save the file to the upload folder
        filename = os.path.join(app.config['DOWNLOAD_FOLDER'], audio_file.filename)
        audio_file.save(filename)

        # Perform birdcall recognition
        birdpacket = get_birdcall(filename)
        
        return jsonify(birdpacket)
    
    except Exception as e:
        # Return an error response with status code 500
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
