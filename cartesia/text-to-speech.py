from pydub import AudioSegment
from pydub.playback import play
import requests
from pydub import AudioSegment
from io import BytesIO
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

# Replace with your actual API key
API_KEY = os.getenv('CARTESIA_API_KEY')

# Set up the endpoint and headers
url = "https://api.cartesia.ai/tts/bytes"
headers = {
    "Cartesia-Version": "2024-06-10",
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

val = 5
if val == 4:
    tscript = "Turning off the light."
elif val == 3:
    tscript = "Turning on the light."
elif val == 1:
    tscript = "Locking the door."
elif val == 2:
    tscript = "Unlocking the door."
elif val == 5:
    tscript = "Listening. what is your request?"
elif val == 6:
    tscript = "Showing front door camera."
elif val == 7:
    tscript = "Opening Google Calendar."
elif val == 8:
    tscript = "Showing today's weather forecast."

data = {
        "transcript": tscript,
        "model_id": "sonic-english",
        "voice": {
            "mode": "id",
            "id": "e3827ec5-697a-4b7c-9704-1a23041bbc51"
        },
        "output_format": {
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100
        }
    }
response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    # Save the raw PCM data
    with open("raw_output.pcm", "wb") as f:
        f.write(response.content)

    file_path = 'sonic.wav'  # Replace with your file name

    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

    # Convert the PCM file to WAV using FFmpeg
    subprocess.run([
        "ffmpeg", "-f", "f32le", "-ar", "44100", "-ac", "1", 
        "-i", "raw_output.pcm", "sonic.wav"
    ])
    
    # Load the WAV file with pydub and normalize
    audio = AudioSegment.from_wav("sonic.wav")

    # Save the normalized audio
    audio.export("sonic.wav", format="wav")
    print("audio saved as sonic.wav")
else:
    print(f"Error: {response.status_code} - {response.text}")

audio = AudioSegment.from_wav('sonic.wav')  # Replace with your file path

# Play the audio
play(audio)