from google.cloud import speech
import io

def transcribe_audio(audio_path):
    client = speech.SpeechClient()

    # Read the audio file
    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    
    # Configure request
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Change if needed
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Send request
    response = client.recognize(config=config, audio=audio)

    # Print results
    for result in response.results:
        print("Transcript:", result.alternatives[0].transcript)

# Example usage
transcribe_audio("audio.wav")
