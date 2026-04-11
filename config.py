import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Info
APP_NAME = "PrepAI"
APP_VERSION = "1.0.0"
AUTHOR = "Clonigue"

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

# Interview Settings
QUESTIONS_PER_SESSION = 7
DIFFICULTY = "medium"

# Domains
DOMAINS = [
    "Python",
    "DBMS & SQL",
    "Operating Systems",
    "JavaScript"
]

# Theme
THEME = "light"
COLOR_PRIMARY = "#2B5CE6"
COLOR_SECONDARY = "#F0F4FF"
COLOR_TEXT = "#1A1A2E"
COLOR_SUCCESS = "#28A745"
COLOR_WARNING = "#FFC107"
COLOR_DANGER = "#DC3545"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
MODELS_DIR = os.path.join(BASE_DIR, "models")