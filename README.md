# Cheep Flask API

## Overview

This Flask application serves as an API for birdcall recognition, leveraging the BirdNET-Analyzer. The app provides endpoints for simple greetings and uploading audio files. Birdcall recognition is performed using the BirdNET-Analyzer library, and the results are returned in a JSON format.

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
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
