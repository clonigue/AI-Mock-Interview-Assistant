import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Info
APP_NAME = "PrepAI"
APP_VERSION = "1.0.0"
AUTHOR = "Clonigue"

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

# Interview Settings
QUESTIONS_PER_SESSION = 7
DIFFICULTY = "medium"

# Domains
DOMAINS = [
    "Python",
    "DBMS & SQL",
    "Operating Systems",
    "HTML & CSS",
    "JavaScript",
    "HR Interview"
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