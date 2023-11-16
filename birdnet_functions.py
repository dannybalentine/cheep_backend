'''

Credits to birdNET ( https://github.com/kahst/BirdNET-Analyzer )
These methods interact with the BirdNET-Analyzer to recognize birdcalls
from audio. 

'''

def get_birdcall(audio_file):
    from birdnetlib import Recording
    from birdnetlib.analyzer import Analyzer
    from datetime import datetime
    import json

    today = datetime(year=2023, month=11, day=14)
    print(today)
    
    # Load and initialize the BirdNET-Analyzer models.
    analyzer = Analyzer()

    recording = Recording(
        analyzer,
        audio_file,
        date=datetime(year=2022, month=5, day=10), # use date or week_48
        min_conf=0.90)



    recording.analyze()
    #
    output = get_max_confidence_elements(recording.detections)
    print(output)
    #print(output)
    output_with_writeup = get_gpt_writeup(output)
    #json_data = json.dumps(output_with_writeup, indent=2)
    return output_with_writeup

def get_max_confidence_elements(detections):
    
    max_confidence_dict = {}
    for entry in detections:
        common_name = entry["common_name"]
        scientific_name = entry["scientific_name"]
        confidence = entry["confidence"]

        if common_name not in max_confidence_dict or confidence > max_confidence_dict[common_name]["confidence"]:
            max_confidence_dict[common_name] = {"confidence": confidence, "scientific_name": scientific_name}

    selected_common_names = [
            {"common_name": common_name, "scientific_name": values["scientific_name"], "confidence": values["confidence"]}
        for common_name, values in max_confidence_dict.items()
    ]
    sorted_names = sorted(selected_common_names, key=lambda x: x["confidence"], reverse=True)
    top_3_birds = sorted_names[:3]
    return top_3_birds



def get_gpt_writeup(detections):
    import openai
    openai.api_key = OPEN_AI_KEY
    input_data = detections

    # Initialize an empty list to store dictionaries for each bird
    result_data = []

    # Loop through each bird and generate a response
    for i, bird in enumerate(input_data, start=1):
        print("gpt_iteration")
        # Create a prompt for the current bird
        bird_prompt = f"Write a short paragraph about the bird:\n\nCommon Name: {bird['common_name']}\nScientific Name: {bird['scientific_name']}\n and make it no longer than 100 words"

        # Make the API request for the current bird
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


    print(result_data)
    return result_data

