import cv2
import threading
try:
    from fer import FER
except ImportError:
    try:
        from fer.fer import FER
    except ImportError:
        FER = None
import numpy as np

class FaceAnalyzer:
    def __init__(self):
        self.is_running = False
        self.current_frame = None
        self.emotion_log = []
        self.cap = None
        self.thread = None
        self.frame_count = 0
        self.analyze_every = 10

        # Initialize detector
        if FER is not None:
            self.detector = FER(mtcnn=False)
        else:
            self.detector = None
            print("FER not available, emotion detection disabled")

    def start(self):
        """Start webcam capture and emotion analysis."""
        self.is_running = True
        self.emotion_log = []
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop webcam capture."""
        self.is_running = False

    def get_frame(self):
        """Get current frame for display."""
        return self.current_frame

    def get_emotion_log(self):
        """Get all logged emotions."""
        return self.emotion_log

    def get_dominant_emotion(self):
        """Get most frequent emotion from log."""
        if not self.emotion_log:
            return "neutral"

        emotion_counts = {}
        for entry in self.emotion_log:
            emotion = entry["emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        return max(emotion_counts, key=emotion_counts.get)

    def _run(self):
        """Main capture and analysis loop."""
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    break

                self.frame_count += 1

                # Analyze every Nth frame
                if self.frame_count % self.analyze_every == 0:
                    self._analyze_emotion(frame)

                # Store current frame for display
                self.current_frame = frame.copy()

        except Exception as e:
            print(f"Face engine error: {e}")
        finally:
            if self.cap:
                self.cap.release()

    def _analyze_emotion(self, frame):
        """Analyze emotion in current frame."""
        if self.detector is None:
            return
        try:
            result = self.detector.detect_emotions(frame)
            if result:
                emotions = result[0]["emotions"]
                dominant = max(emotions, key=emotions.get)
                score = emotions[dominant]
                self.emotion_log.append({
                    "emotion": dominant,
                    "score": round(score, 2),
                    "frame": self.frame_count
                })
        except Exception as e:
            pass