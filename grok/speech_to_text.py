import os
import sounddevice as sd
from scipy.io.wavfile import write
from groq import Groq
import numpy as np

# Initialize the Groq client
client = Groq()

# Recording settings
sample_rate = 44100  # Sample rate for recording
duration = 10  # Duration in seconds for the recording

# Function to record audio from the microphone
def record_audio(filename, duration, sample_rate):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait for the recording to complete
    write(filename, sample_rate, recording)  # Save as WAV file
    print(f"Recording saved to {filename}")

# Specify the path to save the recorded audio file
filename = os.path.dirname(__file__) + "/recorded_audio.wav"

# Record audio
record_audio(filename, duration, sample_rate)

# Open the audio file
with open(filename, "rb") as file:
    # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
      file=(filename, file.read()),  # Required audio file
      model="distil-whisper-large-v3-en",  # Required model to use for transcription
      prompt="Specify context or spelling",  # Optional
      response_format="json",  # Optional
      language="en",  # Optional
      temperature=0.0  # Optional
    )
    
    # Print the transcription text
    print(transcription.text)
