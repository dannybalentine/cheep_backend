'''

Credits to birdNET ( https://github.com/kahst/BirdNET-Analyzer )
These methods interact with the BirdNET-Analyzer to recognize birdcalls
from audio. 

'''

def get_birdcall(audio_file):
    from birdnetlib import Recording
    from birdnetlib.analyzer import Analyzer
    from datetime import datetime
    

    today = datetime(year=2023, month=11, day=14)
    print(today)
    
    # Load and initialize the BirdNET-Analyzer models.
    analyzer = Analyzer()

    recording = Recording(
        analyzer,
        audio_file,
        date=datetime(year=2022, month=5, day=10), # use date or week_48
        min_conf=0.50)



    recording.analyze()
    return recording.detections

