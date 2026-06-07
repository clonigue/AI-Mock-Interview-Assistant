<div align="center">

# PrepAI — AI Mock Interview Assistant

**by [Clonigue](https://github.com/clonigue)**

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-1F6AA5?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-F55036?style=for-the-badge&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active_Development-orange?style=for-the-badge)
![ICRTSET](https://img.shields.io/badge/Published-ICRTSET_2026-green?style=for-the-badge)

*Practice technical interviews with AI-generated questions, real-time voice recognition, and facial expression analysis.*

</div>

---

## What is PrepAI?

PrepAI is a desktop application that simulates a real technical interview environment. It listens to your spoken answers, watches your facial expressions, evaluates your responses using an LLM, and generates a detailed PDF report at the end — all running locally on your machine.

---

## Features

- **AI-generated questions** — domain-specific questions generated fresh every session via Groq API
- **Voice recognition** — answers captured via Whisper STT, no typing required
- **Facial expression analysis** — DeepFace + FER monitor confidence and engagement in real time
- **PDF performance report** — detailed session report with scores, feedback, and improvement tips generated via ReportLab
- **Session history** — track your progress across multiple practice sessions

---

## Domains Supported

| Domain | Topics Covered |
|--------|---------------|
| Python | OOP, data structures, standard library, best practices |
| DBMS & SQL | Normalization, queries, transactions, indexing |
| Operating Systems | Processes, memory management, scheduling, deadlocks |
| JavaScript | ES6+, async/await, DOM, closures, event loop |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| GUI | CustomTkinter |
| Voice Recognition | Whisper (via Groq API) |
| Question Generation & Scoring | LLaMA 3 via Groq API |
| Facial Analysis | DeepFace + FER |
| PDF Reports | ReportLab |
| Packaging | PyInstaller |

---

## Getting Started

### Prerequisites
- Python 3.11
- A [Groq API key](https://console.groq.com) (free tier available)
- Webcam (for facial analysis)
- Microphone

### Installation

```bash
# Clone the repo
git clone https://github.com/clonigue/AI-Mock-Interview-Assistant.git
cd AI-Mock-Interview-Assistant

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
# Create a .env file and add:
# GROQ_API_KEY=your_key_here

# Run the app
python main.py
```

---

## Research

This project was accepted and presented at **ICRTSET-2026** (International Conference on Recent Trends in Science, Engineering and Technology).

---

## Related Project

> **[AI Interview Coach](https://github.com/clonigue/AI-Interview-Coach)** — cloud-deployed version of this concept built with n8n + LLaMA 3, accessible via browser with voice and text input.

---

## Status

🚧 Under active development — new domains and features being added.

---

## Author

**Suraj Kohare** · [github.com/clonigue](https://github.com/clonigue)

*At least 0.01% improvement everyday.*
