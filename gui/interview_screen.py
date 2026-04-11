import customtkinter as ctk

class InterviewScreen(ctk.CTkFrame):
    def __init__(self, parent, domain):
        super().__init__(parent, fg_color="#F0F4FF")
        self.parent = parent
        self.domain = domain
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text=f"Interview Screen — {self.domain}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1A1A2E"
        ).pack(expand=True)

        ctk.CTkButton(
            self,
            text="← Back to Domains",
            command=self.parent.show_domain_screen
        ).pack(pady=20)