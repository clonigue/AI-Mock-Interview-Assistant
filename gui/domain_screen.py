import customtkinter as ctk
from config import DOMAINS, APP_NAME, AUTHOR

class DomainScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F0F4FF")
        self.parent = parent
        self.selected_domain = None
        self.domain_buttons = {}

        self.build_ui()

    def build_ui(self):
        # ── Header ──────────────────────────────
        header = ctk.CTkFrame(self, fg_color="#2B5CE6", corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="PrepAI",
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 0))

        ctk.CTkLabel(
            header,
            text="AI Mock Interview Assistant  •  by Clonigue",
            font=ctk.CTkFont(family="Arial", size=13),
            text_color="#C8D8FF"
        ).pack(pady=(0, 20))

        # ── Subtitle ────────────────────────────
        ctk.CTkLabel(
            self,
            text="Select Your Interview Domain",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="#1A1A2E"
        ).pack(pady=(40, 5))

        ctk.CTkLabel(
            self,
            text="Choose a topic to begin your practice session",
            font=ctk.CTkFont(family="Arial", size=13),
            text_color="#666666"
        ).pack(pady=(0, 30))

        # ── Domain Buttons Grid ──────────────────
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=10)

        domain_icons = {
            "Python": "🐍",
            "DBMS & SQL": "🗄️",
            "Operating Systems": "💻",
            "JavaScript": "⚡"
        }

        row, col = 0, 0
        for domain in DOMAINS:
            icon = domain_icons.get(domain, "📚")
            btn = ctk.CTkButton(
                grid_frame,
                text=f"{icon}  {domain}",
                font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
                width=200,
                height=80,
                corner_radius=12,
                fg_color="white",
                text_color="#1A1A2E",
                hover_color="#E8EFFF",
                border_width=2,
                border_color="#D0D8F0",
                command=lambda d=domain: self.select_domain(d)
            )
            btn.grid(row=row, column=col, padx=15, pady=15)
            self.domain_buttons[domain] = btn

            col += 1
            if col == 2:
                col = 0
                row += 1

        # ── Start Button ─────────────────────────
        self.start_btn = ctk.CTkButton(
            self,
            text="Start Interview  →",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            width=250,
            height=55,
            corner_radius=12,
            fg_color="#CCCCCC",
            hover_color="#CCCCCC",
            text_color="white",
            state="disabled",
            command=self.start_interview
        )
        self.start_btn.pack(pady=30)

        # ── Footer ───────────────────────────────
        ctk.CTkLabel(
            self,
            text="PrepAI v1.0  •  by Clonigue",
            font=ctk.CTkFont(family="Arial", size=11),
            text_color="#AAAAAA"
        ).pack(side="bottom", pady=10)

    def select_domain(self, domain):
        # Reset all buttons
        for d, btn in self.domain_buttons.items():
            btn.configure(
                fg_color="white",
                text_color="#1A1A2E",
                border_color="#D0D8F0"
            )

        # Highlight selected
        self.domain_buttons[domain].configure(
            fg_color="#2B5CE6",
            text_color="white",
            border_color="#2B5CE6"
        )

        # Save selection
        self.selected_domain = domain

        # Enable start button
        self.start_btn.configure(
            fg_color="#2B5CE6",
            hover_color="#1A4ACC",
            state="normal"
        )

    def start_interview(self):
        if self.selected_domain:
            self.parent.show_interview_screen(self.selected_domain)