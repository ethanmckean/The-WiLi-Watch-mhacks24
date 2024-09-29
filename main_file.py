from pydub import AudioSegment
from pydub.playback import play
import requests
from pydub import AudioSegment
from io import BytesIO
import subprocess
import os
import serial
import time
import re
import pyautogui
import sys
import webbrowser

from dotenv import load_dotenv
from speech_to_text import listen_for_request
load_dotenv()

CARTESIA_API_KEY = os.getenv('CARTESIA_API_KEY')

def open_camera():
    try:
        # Open Cheese (the default camera application)
        subprocess.run(['cheese'])
    except Exception as e:
        print(f"Error opening camera: {e}")

def speech(tscript):
    # Set up the endpoint and headers
    url = "https://api.cartesia.ai/tts/bytes"
    headers = {
        "Cartesia-Version": "2024-06-10",
        "X-API-Key": CARTESIA_API_KEY ,
        "Content-Type": "application/json"
    }
    # announce
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

    audio = AudioSegment.from_wav('sonic.wav')

    # Play the audio
    play(audio)


def main():
    print("test1")

    # Configure the serial connection
    port = '/dev/ttyACM0'  # Change this to your port
    baudrate = 9600        # Match the baud rate of your device
    raw_data_pattern = re.compile(r'Raw-Data=0x([0-9A-Fa-f]+)')

    while True:
        try:
            # Create a serial connection
            ser = serial.Serial(port, baudrate, timeout=1)

            print(f'Connected to {port} at {baudrate} baud rate.')

            while True:
                # Read a line from the serial port
                if ser.in_waiting > 0:  # Check if there's data to read
                    line = ser.readline().decode('utf-8').rstrip()
                    print(f'Received: {line}')
                    raw_data_match = raw_data_pattern.search(line)
                    if raw_data_match:
                        raw_data = raw_data_match.group(1)
                        print(f'Parsed Raw-Data: {raw_data}')

                        val = raw_data
                        print(val)
                        print("\n")
                        tscript = ""
                        requesting=False
                        camera=False
                        if val == "4":
                            print("4\n\n\n")
                            tscript = "Turning off the light."
                        elif val == "3":
                            print("3")
                            tscript = "Turning on the light."
                        elif val == "1":
                            print("1")
                            tscript = "Locking the door."
                        elif val == "2":
                            print("2")
                            tscript = "Unlocking the door."
                        elif val == "5":
                            print("5")
                            tscript = "Listening. what is your request?"
                            requesting=True
                        elif val == "6":
                            print("6")
                            tscript = "Showing front door camera."
                            camera=True
                        elif val == "7":
                            print("7")
                            tscript = "Opening Google Calendar."
                            url = 'https://calendar.google.com/calendar/u/0/r'
                            webbrowser.open(url)
                        elif val == "8":
                            print("8")
                            tscript = "Showing today's weather forecast."
                            url = 'https://www.wunderground.com/forecast/us/mi/ann-arbor'
                            webbrowser.open(url)
                        else:
                            print("???/n/n/n")

                        speech(tscript)

                        if(requesting):
                            listen_for_request()
                        if(camera):
                            open_camera()
                        
                        time.sleep(0.1)  # Small delay to avoid high CPU usage

        except serial.SerialException as e:
            print(f'Error: {e}')

        if ser.is_open:  # Correct usage here
            ser.close()
            print('Serial connection closed.')

if __name__ == "__main__":
    main()