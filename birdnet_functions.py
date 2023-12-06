'''
Written by Daniel Balentine
Contact: dannybalentine@gmail.com
Date: 2023-12-06

Credits to birdNET (https://github.com/kahst/BirdNET-Analyzer)
These methods were adapted by Daniel Balentine on 2023-12-06 for birdcall recognition
using the BirdNET-Analyzer from audio. 

For inquiries, contact Daniel Balentine at dannybalentine@gmail.com.

Note: Original BirdNET-Analyzer source can be found at https://github.com/kahst/BirdNET-Analyzer
'''

def get_birdcall(audio_file):
    # Import necessary modules
    from birdnetlib import Recording
    from birdnetlib.analyzer import Analyzer
    from datetime import datetime
    import json

    # Set a specific date (November 14, 2023)
    #today = datetime(year=2023, month=11, day=14)
    
    # Load and initialize the BirdNET-Analyzer models.
    analyzer = Analyzer()

    # Create a Recording object with specified parameters
    recording = Recording(
        analyzer,
        audio_file,
        date=datetime(year=2022, month=5, day=10), # specify date or use week_48
        min_conf=0.90
    )

    # Analyze the recording
    recording.analyze()

    # Get the 3 bird detections with the highest confidence level
    output = get_max_confidence_elements(recording.detections)

    # Generate and return GPT writeup for the top bird detections
    output_with_writeup = get_gpt_writeup(output)
    return output_with_writeup


def get_max_confidence_elements(detections):
    # Initialize a dictionary to store the maximum confidence for each bird
    max_confidence_dict = {}

    # Iterate through each detection entry
    for entry in detections:
        common_name = entry["common_name"]
        scientific_name = entry["scientific_name"]
        confidence = entry["confidence"]

        # Check and update the maximum confidence for each bird
        if common_name not in max_confidence_dict or confidence > max_confidence_dict[common_name]["confidence"]:
            max_confidence_dict[common_name] = {"confidence": confidence, "scientific_name": scientific_name}

    # Create a list of selected bird entries with common name, scientific name, and confidence
    selected_common_names = [
        {"common_name": common_name, "scientific_name": values["scientific_name"], "confidence": values["confidence"]}
        for common_name, values in max_confidence_dict.items()
    ]

    # Sort the selected bird entries by confidence in descending order
    sorted_names = sorted(selected_common_names, key=lambda x: x["confidence"], reverse=True)

    # Get the top 3 bird entries
    top_3_birds = sorted_names[:3]
    return top_3_birds


def get_gpt_writeup(detections):
    # Import necessary modules
    import openai
    import os
    from dotenv import load_dotenv
    load_dotenv()

    # Set OpenAI API key from environment variables
    api_key = os.getenv('OPEN_AI_KEY')
    openai.api_key = api_key

    # Initialize an empty list to store dictionaries for each bird
    result_data = []

    # Loop through each bird and generate a GPT prompt
    for i, bird in enumerate(detections, start=1):
        print("gpt_iteration")

        # Create a prompt for the current bird
        bird_prompt = f"Write a short paragraph about the bird:\n\nCommon Name: {bird['common_name']}\nScientific Name: {bird['scientific_name']}\n and make it no longer than 100 words"

        # Make the API request for the current bird using GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": bird_prompt}
            ],
            temperature=0.7,
            max_tokens=100,
        )

        # Extract the generated text from the response and truncate at the last period
        generated_text = response["choices"][0]["message"]["content"]
        last_period_index = generated_text.rfind('.')
        if last_period_index != -1:
            generated_text = generated_text[:last_period_index + 1]

        # Create a dictionary for the current bird with common name, scientific name, and generated prompt
        result_entry = {
            "common_name": bird["common_name"],
            "scientific_name": bird["scientific_name"],
            "generated_prompt": generated_text
        }

        # Add the dictionary to the result list
        result_data.append(result_entry)

    # Print and return the result data
    return result_data


