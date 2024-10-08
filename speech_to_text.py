import os
import sounddevice as sd
from scipy.io.wavfile import write
from groq import Groq
import numpy as np
from dotenv import load_dotenv
import base64
import serial
# import imageio
from PIL import Image

import webbrowser
import cv2


def listen_for_request():
    from main_file import speech
    from main_file import open_camera
    load_dotenv()
    # Replace with your actual API key
    API_KEY = os.getenv('GROQ_API_KEY')

    # Initialize the Groq client
    client = Groq()

    # Initialize the webcam (0 is the default camera index)
    # reader = imageio.get_reader("/dev/video0")

    # print("Camera initialized")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
    else:
        print("Camera initialized")

    # Recording settings
    sample_rate = 44100  # Sample rate for recording
    duration = 5  # Duration in seconds for the recording

    # Function to record audio from the microphone
    def record_audio(filename, duration, sample_rate):
        print("Recording...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
        sd.wait()  # Wait for the recording to complete
        write(filename, sample_rate, recording)  # Save as WAV file
        print(f"Recording saved to {filename}")

    # Specify the path to save the recorded audio file
    filename = os.path.join(os.path.dirname(__file__), "recorded_audio.wav")

    # Record audio
    record_audio(filename, duration, sample_rate)

    # Open the audio file and create transcription
    try:
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
    finally:
        # Remove the audio file after transcription
        if os.path.exists(filename):
            os.remove(filename)
            print(f"File {filename} deleted.")


    initial_chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "As a smart assistant, your task is to listen to user requests and categorize them based on the appropriate action. Below are predefined categories and their corresponding responses. Your job is to determine which category the request fits into: [lock_door] Locking the door [unlock_door] Unlocking the door [light_on] Turning on the light [light_off] Turning off the light [door_camera] Showing front door camera [calendar] Opening/viewing Calendar [weather] Showing today's weather forecast. [other] Other (unknown request). Respond with just the text in the bracket of the category."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": transcription.text,
            }
        ],

        # The language model which will generate the completion.
        model="llama-3.1-70b-versatile",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    # Print the completion returned by the LLM.
    message_type = initial_chat_completion.choices[0].message.content
    print(f"Message type is: {message_type}")

    '''
    [lock_door]
    [unlock_door]
    [door_camera]
    [calendar]
    [weather]
    [other] 
    '''
    if message_type == "[door_camera]":
        # # Capture a frame (the first one)
        # frame = reader.get_data(0)

        # # Convert the frame to an image and save it
        # img = Image.fromarray(frame)
        # img.save("webcam_capture.jpg")

        ret, frame = cap.read()
        if ret:
            # Save the frame as an image
            cv2.imwrite("webcam_capture.jpg", frame)
            print("Captured image")
        else:
            print("Error: Could not read frame.")

        # Release the camera
        cap.release()

        # Function to encode the image
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        # Path to your image
        image_path = "webcam_capture.jpg"

        # Getting the base64 string
        base64_image = encode_image(image_path)

        front_door = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llava-v1.5-7b-4096-preview",
        )
        front_door = front_door.choices[0].message.content
        print(f"Visual response: {front_door}")
        front_door_analysis = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "The description provided is a view from the front door. Start your message with at the front door I see."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": front_door,
            }
        ],

        # The language model which will generate the completion.
        model="llama-3.1-70b-versatile",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
        )
        final_message = front_door_analysis.choices[0].message.content
        print(final_message)
        # open_camera()
        speech(front_door_analysis.choices[0].message.content)
    elif message_type == "[lock_door]":
        # Configure the serial connection
        port = '/dev/ttyACM0'  # Change this to your port
        baudrate = 9600        # Match the baud rate of your device
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f'Connected to {port} at {baudrate} baud rate.')
        value_to_send = 'lock'
        ser.write(value_to_send.encode())
        print(f'Sent: {value_to_send}')
        speech("Locking the door.")

    elif message_type == "[unlock_door]":
        # Configure the serial connection
        port = '/dev/ttyACM0'  # Change this to your port
        baudrate = 9600        # Match the baud rate of your device
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f'Connected to {port} at {baudrate} baud rate.')
        value_to_send = 'unlock'
        ser.write(value_to_send.encode())
        print(f'Sent: {value_to_send}')
        speech("Unlocking the door.")

    elif message_type == "[calendar]":
        url = 'https://calendar.google.com/calendar/u/0/r'
        webbrowser.open(url)
    elif message_type == "[weather]":
        url = 'https://www.wunderground.com/forecast/us/mi/ann-arbor'
        webbrowser.open(url)
        # Define the input message
        user_message = "What's the weather like in Ann Arbor today?"

        # Define the tool for getting current weather
        weather_tool = {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                }
            }
        }

        # Create the chat completion request
        response = client.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            tools=[weather_tool],
            tool_choice="auto"
        )
        print(response.choices[0].message.content)
        #speech(response.choices[0].message.content)
    elif message_type == "[other]":
        print("hi")
