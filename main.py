import customtkinter as ctk
from gui.main_window import MainWindow

def main():
    # Set appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Create and run app
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()