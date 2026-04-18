import pyaudio
import wave
import os
import tempfile
import threading
from groq import Groq
from config import GROQ_API_KEY

# Groq client for Whisper
client = Groq(api_key=GROQ_API_KEY)

# Recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 500
SILENCE_DURATION = 2

class VoiceRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.audio = None
        self.stream = None
        self.thread = None
        self.on_complete = None

    def start_recording(self, on_complete_callback):
        """Start recording audio from microphone."""
        self.on_complete = on_complete_callback
        self.is_recording = True
        self.frames = []

        self.thread = threading.Thread(target=self._record, daemon=True)
        self.thread.start()

    def stop_recording(self):
        """Manually stop recording."""
        self.is_recording = False

    def _record(self):
        """Internal recording loop."""
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )

            while self.is_recording:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                self.frames.append(data)

        except Exception as e:
            print(f"Recording error: {e}")
        finally:
            self._cleanup()
            if self.frames:
                self._transcribe()

    def _cleanup(self):
        """Clean up audio resources."""
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.audio:
                self.audio.terminate()
        except:
            pass

    def _transcribe(self):
        """Send recording to Groq Whisper for transcription."""
        temp_path = None
        try:
            # Save frames to temp WAV file
            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False
            ) as temp_file:
                temp_path = temp_file.name

            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(RATE)
                wf.writeframes(b''.join(self.frames))

            # Send to Groq Whisper
            with open(temp_path, 'rb') as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3-turbo",
                    file=audio_file,
                    response_format="text"
                )

            # Return transcription
            if self.on_complete:
                self.on_complete(str(transcription).strip(), None)

        except Exception as e:
            print(f"Transcription error: {e}")
            if self.on_complete:
                self.on_complete(None, str(e))
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)