import customtkinter as ctk

class ReportScreen(ctk.CTkFrame):
    def __init__(self, parent, report_data):
        super().__init__(parent, fg_color="#F0F4FF")
        self.parent = parent
        self.report_data = report_data
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="Report Screen — Coming in Phase 5",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1A1A2E"
        ).pack(expand=True)

        ctk.CTkButton(
            self,
            text="← Back to Domains",
            command=self.parent.show_domain_screen
        ).pack(pady=20)