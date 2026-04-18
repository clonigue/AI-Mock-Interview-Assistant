import customtkinter as ctk
import threading
import os
import subprocess
from core.scorer import score_session
from core.report_engine import generate_report

class ReportScreen(ctk.CTkFrame):
    def __init__(self, parent, report_data):
        super().__init__(parent, fg_color="#F0F4FF")
        self.parent = parent
        self.report_data = report_data
        self.report_path = None

        self.build_ui()
        self.after(100, self.start_scoring)

    def build_ui(self):
        # ── Header ──────────────────────────────
        header = ctk.CTkFrame(
            self, fg_color="#2B5CE6", corner_radius=0, height=70
        )
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="PrepAI  •  Interview Complete",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        ).place(x=20, rely=0.5, anchor="w")

        ctk.CTkLabel(
            header,
            text=f"Domain: {self.report_data['domain']}",
            font=ctk.CTkFont(size=13),
            text_color="#C8D8FF"
        ).place(relx=0.99, rely=0.5, anchor="e")

        # ── Status Card ──────────────────────────
        self.status_card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E0E8FF"
        )
        self.status_card.pack(fill="x", padx=40, pady=20)

        self.status_icon = ctk.CTkLabel(
            self.status_card,
            text="⏳",
            font=ctk.CTkFont(size=40)
        )
        self.status_icon.pack(pady=(20, 5))

        self.status_label = ctk.CTkLabel(
            self.status_card,
            text="Analyzing your performance...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1A1A2E"
        )
        self.status_label.pack(pady=5)

        self.status_sub = ctk.CTkLabel(
            self.status_card,
            text="Please wait while AI scores your answers",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.status_sub.pack(pady=(0, 20))

        # ── Progress Bar ─────────────────────────
        self.score_progress = ctk.CTkProgressBar(
            self,
            height=8,
            fg_color="#D0D8F0",
            progress_color="#2B5CE6"
        )
        self.score_progress.pack(fill="x", padx=40, pady=(0, 20))
        self.score_progress.set(0)

        # ── Results Frame (hidden until ready) ───
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#F0F4FF",
            corner_radius=0
        )

        # ── Bottom Buttons ───────────────────────
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(side="bottom", pady=15)

        self.download_btn = ctk.CTkButton(
            self.btn_frame,
            text="📄  Download Report",
            width=200,
            height=45,
            corner_radius=10,
            fg_color="#28A745",
            hover_color="#1E7E34",
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold"),
            state="disabled",
            command=self.open_report
        )
        self.download_btn.grid(row=0, column=0, padx=10)

        self.new_btn = ctk.CTkButton(
            self.btn_frame,
            text="🔄  New Interview",
            width=200,
            height=45,
            corner_radius=10,
            fg_color="#2B5CE6",
            hover_color="#1A4ACC",
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.new_interview
        )
        self.new_btn.grid(row=0, column=1, padx=10)

    def start_scoring(self):
        """Start scoring in background thread."""
        def score():
            answers = self.report_data.get("answers", [])
            domain = self.report_data.get("domain", "")
            total = len(answers)

            scored = []
            for i, item in enumerate(answers):
                from core.scorer import score_answer
                result = score_answer(
                    item["question"],
                    item["answer"],
                    domain
                )
                scored.append({
                    **item,
                    "score": result["score"],
                    "feedback": result["feedback"],
                    "ideal_answer": result["ideal_answer"]
                })
                progress = (i + 1) / total
                self.after(0, lambda p=progress, n=i+1, t=total:
                    self.update_scoring_progress(p, n, t))

            self.report_data["scored_answers"] = scored
            self.after(0, self.generate_pdf)

        threading.Thread(target=score, daemon=True).start()

    def update_scoring_progress(self, progress, current, total):
        """Update progress bar during scoring."""
        self.score_progress.set(progress)
        self.status_sub.configure(
            text=f"Scoring answer {current} of {total}..."
        )

    def generate_pdf(self):
        """Generate PDF report."""
        self.status_label.configure(text="Generating PDF report...")
        self.status_sub.configure(text="Almost done...")
        self.score_progress.set(0.95)

        def build_pdf():
            try:
                path = generate_report(self.report_data)
                self.after(0, lambda: self.show_results(path))
            except Exception as e:
                self.after(0, lambda: self.show_error(str(e)))

        threading.Thread(target=build_pdf, daemon=True).start()

    def show_results(self, path):
        """Show results after scoring and PDF generation."""
        self.report_path = path
        self.score_progress.set(1.0)

        scored = self.report_data.get("scored_answers", [])
        total = len(scored)
        avg = round(sum(a["score"] for a in scored) / total, 1) if total > 0 else 0
        dominant = self.report_data.get("dominant_emotion", "neutral")

        # Update status card
        if avg >= 8:
            icon, msg, color = "🎉", "Excellent Performance!", "#28A745"
        elif avg >= 6:
            icon, msg, color = "👍", "Good Performance!", "#2B5CE6"
        elif avg >= 4:
            icon, msg, color = "📈", "Average Performance", "#FFC107"
        else:
            icon, msg, color = "💪", "Keep Practicing!", "#DC3545"

        self.status_icon.configure(text=icon)
        self.status_label.configure(text=msg, text_color=color)
        self.status_sub.configure(
            text=f"Average Score: {avg}/10  •  Dominant Emotion: {dominant.title()}"
        )

        # Show results frame
        self.results_frame.pack(fill="both", expand=True, padx=40, pady=(0, 10))

        # Stats row
        stats_frame = ctk.CTkFrame(
            self.results_frame, fg_color="transparent"
        )
        stats_frame.pack(fill="x", pady=10)

        stats = [
            ("📊 Avg Score", f"{avg}/10"),
            ("✅ Questions", f"{total}"),
            ("😊 Emotion", dominant.title()),
            ("🏆 Rating", self.get_rating(avg))
        ]

        for i, (label, value) in enumerate(stats):
            card = ctk.CTkFrame(
                stats_frame,
                fg_color="white",
                corner_radius=10,
                border_width=1,
                border_color="#E0E8FF"
            )
            card.grid(row=0, column=i, padx=8, sticky="ew")
            stats_frame.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color="#888888"
            ).pack(pady=(10, 2))

            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#2B5CE6"
            ).pack(pady=(0, 10))

        # Per question scores
        ctk.CTkLabel(
            self.results_frame,
            text="Question Scores:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#1A1A2E"
        ).pack(anchor="w", pady=(10, 5))

        for item in scored:
            q_frame = ctk.CTkFrame(
                self.results_frame,
                fg_color="white",
                corner_radius=10,
                border_width=1,
                border_color="#E0E8FF"
            )
            q_frame.pack(fill="x", pady=4)

            top = ctk.CTkFrame(q_frame, fg_color="transparent")
            top.pack(fill="x", padx=15, pady=(10, 3))

            ctk.CTkLabel(
                top,
                text=f"Q{item['question_num']}: {item['question'][:70]}...",
                font=ctk.CTkFont(size=12),
                text_color="#1A1A2E"
            ).pack(side="left")

            score_color = (
                "#28A745" if item["score"] >= 8
                else "#FFC107" if item["score"] >= 5
                else "#DC3545"
            )
            ctk.CTkLabel(
                top,
                text=f"{item['score']}/10",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=score_color
            ).pack(side="right")

            ctk.CTkLabel(
                q_frame,
                text=f"💬 {item['feedback']}",
                font=ctk.CTkFont(size=11),
                text_color="#555555",
                wraplength=700,
                justify="left"
            ).pack(anchor="w", padx=15, pady=(0, 10))

        # Enable download button
        self.download_btn.configure(state="normal")

    def show_error(self, error):
        """Show error if something fails."""
        self.status_icon.configure(text="❌")
        self.status_label.configure(
            text="Something went wrong",
            text_color="#DC3545"
        )
        self.status_sub.configure(text=f"Error: {error}")

    def get_rating(self, score):
        if score >= 8: return "Excellent"
        elif score >= 6: return "Good"
        elif score >= 4: return "Average"
        else: return "Needs Work"

    def open_report(self):
        """Open PDF report."""
        if self.report_path and os.path.exists(self.report_path):
            os.startfile(self.report_path)

    def new_interview(self):
        """Go back to domain selection."""
        self.parent.show_domain_screen()