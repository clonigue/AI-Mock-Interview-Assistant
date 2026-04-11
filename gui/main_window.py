import customtkinter as ctk
from gui.domain_screen import DomainScreen

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("PrepAI — AI Mock Interview Assistant")
        self.geometry("900x600")
        self.resizable(False, False)

        # Center window on screen
        self.center_window()

        # Current screen tracker
        self.current_screen = None

        # Show domain selection screen first
        self.show_domain_screen()

    def center_window(self):
        self.update_idletasks()
        width = 900
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_domain_screen(self):
        # Clear current screen
        if self.current_screen:
            self.current_screen.destroy()

        # Show domain screen
        self.current_screen = DomainScreen(self)
        self.current_screen.pack(fill="both", expand=True)

    def show_interview_screen(self, domain):
        # Clear current screen
        if self.current_screen:
            self.current_screen.destroy()

        # Import here to avoid circular imports
        from gui.interview_screen import InterviewScreen

        # Show interview screen
        self.current_screen = InterviewScreen(self, domain)
        self.current_screen.pack(fill="both", expand=True)

    def show_report_screen(self, report_data):
        # Clear current screen
        if self.current_screen:
            self.current_screen.destroy()

        # Import here to avoid circular imports
        from gui.report_screen import ReportScreen

        # Show report screen
        self.current_screen = ReportScreen(self, report_data)
        self.current_screen.pack(fill="both", expand=True)