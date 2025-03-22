import whisper
import torch
import numpy as np
import sounddevice as sd
import queue

# Load Whisper Tiny model
model = whisper.load_model("tiny")  # or "tiny.en" for English only

# Check if CUDA is available, else use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Audio configuration
SAMPLE_RATE = 16000  # Whisper requires 16kHz input
CHANNELS = 1         # Mono audio
q = queue.Queue()
recording = False    # Flag to control recording

def audio_callback(indata, frames, time, status):
    """Callback function to receive live audio and put it in a queue."""
    if status:
        print(status)
    if recording:  # Only store audio if recording is active
        q.put(indata.copy())

def start_recording():
    """Start recording and transcribing."""
    global recording
    recording = True
    print("\nRecording started... Press ENTER to stop.")

def stop_recording():
    """Stop recording and process transcription."""
    global recording
    recording = False
    print("\nProcessing audio...")

    # Collect all audio chunks
    audio_data = []
    while not q.empty():
        audio_data.append(q.get())
    
    if not audio_data:
        print("No audio detected.")
        return
    
    # Convert audio chunks to NumPy array
    audio_data = np.concatenate(audio_data, axis=0)
    audio_data = np.array(audio_data, dtype=np.float32)
    print('audio', audio_data)
    # Transcribe using Whisper
    result = model.transcribe(audio_data, fp16=True)
    print("\nTranscription:", result["text"])

# Start the audio input stream
with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback):
    print("Press ENTER to start recording, and ENTER again to stop.")

    while True:
        try:
            input("Press ENTER to start recording...")  # Wait for user input
            start_recording()

            input("Press ENTER to stop recording...")  # Wait for user input
            stop_recording()

        except KeyboardInterrupt:
            print("\nExiting...")
            break
