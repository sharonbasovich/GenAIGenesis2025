import google.generativeai as genai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import io
import base64
import PIL.Image  # For image handling

genai.configure(api_key="AIzaSyCCTK90t4X7SVmmFHHbwRtI8u5sk_b7DZE")  # Replace with your actual API key

model = genai.GenerativeModel('models/gemini-2.0-flash')
chat = model.start_chat(history=[])

print("Welcome to the Gemini Multimodal Chatbot (Audio & Image)!")

def record_audio(duration=5, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  
    print("Recording complete.")
    return recording.flatten(), fs  

def audio_to_base64(audio_data, sample_rate):
    wav_io = io.BytesIO()
    wav.write(wav_io, sample_rate, audio_data)
    audio_bytes = wav_io.getvalue()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    return audio_base64

def load_image(image_path):
    """Loads an image from the given path."""
    img = PIL.Image.open(image_path)
    return img

image_path = './menus/menu2.jpg'
img = load_image(image_path)

while True:
    user_input = input("Press 'r' to record audio, or type text ")

    if user_input == 'r':
        audio_data, sample_rate = record_audio()
        audio_base64_string = audio_to_base64(audio_data, sample_rate)
        
        audio_content = {
            "mime_type": "audio/wav",
            "data": audio_base64_string,
        }
        try:
            response = chat.send_message([audio_content, img])
            print("Bot:", response.text)
        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        try:
            response = chat.send_message([user_input, img])
            print("Bot:", response.text)
        except Exception as e:
            print(f"An error occurred: {e}")
