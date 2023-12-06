# BirdNET Flask API

## Overview

This Flask application serves as an API for birdcall recognition, leveraging the BirdNET-Analyzer. The app provides endpoints for simple greetings and uploading audio files. Birdcall recognition is performed using the BirdNET-Analyzer library, and the results are returned in a JSON format. This API was built for the [Cheep](https://github.com/du693/cheep/blob/main/README.md) project.

## Features

- **Greeting Endpoint**: `/hello`
  - Returns a simple greeting message.
  
- **Upload Audio Endpoint**: `/upload_audio` (POST)
  - Allows users to upload an audio file for birdcall recognition.
  - Requires a file parameter named `audio_file`.
  - Optionally accepts latitude and longitude parameters for geolocation (`lat`, `lng`).
  - Returns birdcall recognition results in JSON format.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/birdnet-flask-app.git
   cd birdnet-flask-app
2. Install birdnetLib:
    
    -[birdnetlib](https://pypi.org/project/birdnetlib/)
3. Install Flask:
    ```bash
    pip install Flask
4. Run the Flask app:
    ```bash
    python app.py
The app will be accessible at http://localhost:5000.
## Usage

### Greeting Endpoint

Access the greeting endpoint at [http://localhost:5000/hello](http://localhost:5000/hello).

### Upload Audio Endpoint

Send a POST request to [http://localhost:5000/upload_audio](http://localhost:5000/upload_audio) with an audio file attached. Optionally, provide latitude and longitude parameters.

Example using `curl`:


    curl -X POST -F "audio_file=@/path/to/your/audio/file.mp3" -F "lat=37.7749" -F "lng=-122.4194" [http://localhost:5000/upload_audio](http://localhost:5000/upload_audio)

## License

This project is licensed under the [\`MIT License\`](LICENSE).




