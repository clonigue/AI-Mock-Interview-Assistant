import cv2
import customtkinter as ctk
import threading
from config import QUESTIONS_PER_SESSION
from core.question_engine import generate_question
from core.voice_engine import VoiceRecorder
from core.face_engine import FaceAnalyzer
from PIL import Image

class PlaceholderTextbox(ctk.CTkTextbox):
    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = "#AAAAAA"
        self.default_color = "#1A1A2E"
        self._placeholder_active = False
        self.set_placeholder()
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def set_placeholder(self):
        self.delete("1.0", "end")
        self.insert("1.0", self.placeholder)
        self.configure(text_color=self.placeholder_color)
        self._placeholder_active = True

    def on_focus_in(self, event):
        if self._placeholder_active:
            self.delete("1.0", "end")
            self.configure(text_color=self.default_color)
            self._placeholder_active = False

    def on_focus_out(self, event):
        if self.get("1.0", "end-1c").strip() == "":
            self.set_placeholder()

    def get_answer(self):
        if self._placeholder_active:
            return ""
        return self.get("1.0", "end-1c").strip()

    def reset(self):
        self.set_placeholder()

class InterviewScreen(ctk.CTkFrame):
    def __init__(self, parent, domain):
        super().__init__(parent, fg_color="#F0F4FF")
        self.parent = parent
        self.domain = domain

        # Session state
        self.current_question_num = 0
        self.asked_questions = []
        self.current_question = ""
        self.answers = []
        self.recorder = VoiceRecorder()
        self.is_recording = False
        self.face_analyzer = FaceAnalyzer()
        self.webcam_active = False

        self.build_ui()
        self.after(100, self.load_next_question)

    def build_ui(self):
        # ── Main Container ───────────────────────
        # Left side — interview content
        left_panel = ctk.CTkFrame(self, fg_color="#F0F4FF", corner_radius=0)
        left_panel.pack(side="left", fill="both", expand=True)

        # Right side — webcam preview
        right_panel = ctk.CTkFrame(self, fg_color="#E8EFFF", corner_radius=0, width=220)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # ── Webcam Panel ─────────────────────────
        ctk.CTkLabel(
            right_panel,
            text="📷 Live Preview",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2B5CE6"
        ).pack(pady=(20, 5))

        self.webcam_label = ctk.CTkLabel(
            right_panel,
            text="",
            width=200,
            height=150
        )
        self.webcam_label.pack(padx=10, pady=5)

        # Webcam status
        self.webcam_status = ctk.CTkLabel(
            right_panel,
            text="⏳ Starting camera...",
            font=ctk.CTkFont(size=11),
            text_color="#888888",
            wraplength=180
        )
        self.webcam_status.pack(pady=5)

        # Emotion display
        ctk.CTkLabel(
            right_panel,
            text="Current Emotion:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#1A1A2E"
        ).pack(pady=(15, 2))

        self.emotion_label = ctk.CTkLabel(
            right_panel,
            text="😐 Neutral",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2B5CE6"
        )
        self.emotion_label.pack(pady=2)

        # Tips
        tips_frame = ctk.CTkFrame(
            right_panel,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#D0D8F0"
        )
        tips_frame.pack(fill="x", padx=10, pady=15)

        ctk.CTkLabel(
            tips_frame,
            text="💡 Tips",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#2B5CE6"
        ).pack(anchor="w", padx=10, pady=(8, 2))

        ctk.CTkLabel(
            tips_frame,
            text="• Look at the camera\n• Speak clearly\n• Stay confident\n• Take your time",
            font=ctk.CTkFont(size=11),
            text_color="#444444",
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 8))

        # ── Left Panel Content ───────────────────
        # Header
        header = ctk.CTkFrame(
            left_panel, fg_color="#2B5CE6", corner_radius=0, height=70
        )
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=f"PrepAI  •  {self.domain}",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        ).place(x=20, rely=0.5, anchor="w")

        self.counter_label = ctk.CTkLabel(
            header,
            text=f"Question 0 / {QUESTIONS_PER_SESSION}",
            font=ctk.CTkFont(family="Arial", size=13),
            text_color="#C8D8FF"
        )
        self.counter_label.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(
            header,
            text="✕ End",
            width=80,
            height=30,
            corner_radius=8,
            fg_color="#FF4444",
            hover_color="#CC0000",
            font=ctk.CTkFont(size=12),
            command=self.end_interview
        ).place(relx=0.97, rely=0.5, anchor="e")

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            left_panel, height=8,
            fg_color="#D0D8F0",
            progress_color="#2B5CE6"
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(15, 0))
        self.progress_bar.set(0)

        # Question Card
        card = ctk.CTkFrame(
            left_panel,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E0E8FF"
        )
        card.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            card,
            text="QUESTION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#2B5CE6"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.question_label = ctk.CTkLabel(
            card,
            text="⏳ Loading your question...",
            font=ctk.CTkFont(family="Arial", size=15),
            text_color="#1A1A2E",
            wraplength=580,
            justify="left"
        )
        self.question_label.pack(anchor="w", padx=20, pady=(0, 20))

        # Answer Label
        ctk.CTkLabel(
            left_panel,
            text="Your Answer:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#1A1A2E"
        ).pack(anchor="w", padx=20)

        # Answer Box
        self.answer_box = PlaceholderTextbox(
            left_panel,
            placeholder="Type your answer here...",
            height=120,
            corner_radius=12,
            border_width=1,
            border_color="#D0D8FF",
            font=ctk.CTkFont(family="Arial", size=13),
            fg_color="white",
        )
        self.answer_box.pack(fill="x", padx=20, pady=(5, 10))

        # Buttons
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(pady=5)

        self.mic_btn = ctk.CTkButton(
            btn_frame,
            text="🎤  Mic",
            width=130,
            height=45,
            corner_radius=10,
            fg_color="white",
            text_color="#2B5CE6",
            hover_color="#E0E8FF",
            border_width=2,
            border_color="#2B5CE6",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.use_mic
        )
        self.mic_btn.grid(row=0, column=0, padx=10)

        self.next_btn = ctk.CTkButton(
            btn_frame,
            text="Next Question  →",
            width=190,
            height=45,
            corner_radius=10,
            fg_color="#2B5CE6",
            hover_color="#1A4ACC",
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.next_question
        )
        self.next_btn.grid(row=0, column=1, padx=10)

        # Status
        self.status_label = ctk.CTkLabel(
            left_panel,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        self.status_label.pack(pady=5)

    def load_next_question(self):
        # Start webcam on first question
        if self.current_question_num == 0 and not self.webcam_active:
            self.start_webcam()
        self.next_btn.configure(state="disabled")
        self.status_label.configure(text="⏳ Generating question...")
        self.question_label.configure(text="⏳ Fetching your question from AI...")

        def fetch():
            result = generate_question(self.domain, self.asked_questions)
            self.after(0, lambda: self.display_question(result))

        threading.Thread(target=fetch, daemon=True).start()

    def display_question(self, result):
        self.current_question_num += 1
        self.current_question = result["question"]
        self.asked_questions.append(self.current_question)

        self.question_label.configure(text=self.current_question)
        self.counter_label.configure(
            text=f"Question {self.current_question_num} / {QUESTIONS_PER_SESSION}"
        )
        self.progress_bar.set(self.current_question_num / QUESTIONS_PER_SESSION)

        if self.current_question_num >= QUESTIONS_PER_SESSION:
            self.next_btn.configure(text="Finish Interview ✓")

        self.next_btn.configure(state="normal")
        self.status_label.configure(
            text="✅ AI Generated" if result["success"] else "⚠️ Offline Question"
        )

        self.answer_box.reset()
        self.focus()

    def next_question(self):
        answer = self.answer_box.get_answer()

        self.answers.append({
            "question_num": self.current_question_num,
            "question": self.current_question,
            "answer": answer,
            "domain": self.domain
        })

        if self.current_question_num >= QUESTIONS_PER_SESSION:
            self.finish_interview()
        else:
            self.load_next_question()

    def use_mic(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start voice recording."""
        self.is_recording = True
        self.mic_btn.configure(
            text="⏹  Stop",
            fg_color="#FF4444",
            hover_color="#CC0000",
            text_color="white",
            border_width=0
        )
        self.status_label.configure(text="🎤 Recording... 0s (silence will auto-stop)")
        self.answer_box.reset()
        self.answer_box.configure(text_color="#1A1A2E")
        self.answer_box.delete("1.0", "end")
        self.answer_box.insert("1.0", "🎤 Listening...")
        self.next_btn.configure(state="disabled")

        self._recording_seconds = 0
        self._update_recording_timer()

        self.recorder.start_recording(self.on_recording_complete)

    def _update_recording_timer(self):
        if self.is_recording:
            self._recording_seconds += 1
            self.status_label.configure(
                text=f"🎤 Recording... {self._recording_seconds}s (silence will auto-stop)"
            )
            self.after(1000, self._update_recording_timer)

    def stop_recording(self):
        """Manually stop recording."""
        self.recorder.stop_recording()
        self.is_recording = False
        self.mic_btn.configure(
            text="🎤  Mic",
            fg_color="white",
            hover_color="#E0E8FF",
            text_color="#2B5CE6",
            border_width=2
        )
        self.status_label.configure(text="⏳ Transcribing your answer...")
        self.answer_box.delete("1.0", "end")
        self.answer_box.configure(text_color="#AAAAAA")
        self.answer_box.insert("1.0", "⏳ Transcribing your answer...")

    def on_recording_complete(self, text, error):
        """Called when recording and transcription is done."""
        self.after(0, lambda: self._update_after_recording(text, error))

    def _update_after_recording(self, text, error):
        """Update UI after recording completes."""
        self.is_recording = False

        # Reset mic button
        self.mic_btn.configure(
            text="🎤  Mic",
            fg_color="white",
            hover_color="#E0E8FF",
            text_color="#2B5CE6",
            border_width=2
        )
        self.next_btn.configure(state="normal")

        if text and not error:
            # Show transcribed text
            self.answer_box.delete("1.0", "end")
            self.answer_box.configure(text_color="#1A1A2E")
            self.answer_box.insert("1.0", text)
            self.status_label.configure(text="✅ Answer transcribed!")
        else:
            self.answer_box.reset()
            self.status_label.configure(
                text=f"❌ Transcription failed. Please type your answer."
            )

    def start_webcam(self):
        """Start face analyzer and webcam preview."""
        self.face_analyzer.start()
        self.webcam_active = True
        self.webcam_status.configure(text="✅ Camera active")
        self._update_webcam_preview()

    def stop_webcam(self):
        """Stop face analyzer and webcam."""
        self.webcam_active = False
        self.face_analyzer.stop()

    def _update_webcam_preview(self):
        """Update webcam preview every 33ms (~30fps display)."""
        if not self.webcam_active:
            return
        try:
            frame = self.face_analyzer.get_frame()
            if frame is not None:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Resize to fit panel
                frame_resized = cv2.resize(frame_rgb, (200, 150))

                # Convert to PIL Image
                img = Image.fromarray(frame_resized)
                ctk_img = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(200, 150)
                )
                self.webcam_label.configure(image=ctk_img)
                self.webcam_label.image = ctk_img

                # Update emotion
                emotion_log = self.face_analyzer.get_emotion_log()
                if emotion_log:
                    latest = emotion_log[-1]["emotion"]
                    emoji_map = {
                        "happy": "😊 Happy",
                        "sad": "😢 Sad",
                        "angry": "😠 Angry",
                        "fear": "😨 Nervous",
                        "surprise": "😲 Surprised",
                        "disgust": "😒 Disgust",
                        "neutral": "😐 Neutral",
                        "confused": "😕 Confused"
                    }
                    self.emotion_label.configure(
                        text=emoji_map.get(latest, "😐 Neutral")
                    )
        except Exception as e:
            pass

        self.after(33, self._update_webcam_preview)        

    def finish_interview(self):
        self.stop_webcam()
        report_data = {
            "domain": self.domain,
            "total_questions": QUESTIONS_PER_SESSION,
            "answers": self.answers,
            "emotion_log": self.face_analyzer.get_emotion_log(),
            "dominant_emotion": self.face_analyzer.get_dominant_emotion()
        }
        self.parent.show_report_screen(report_data)

    def end_interview(self):
        self.stop_webcam()
        self.parent.show_domain_screen()