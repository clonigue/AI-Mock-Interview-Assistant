from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

# Configure Groq client
client = Groq(api_key=GROQ_API_KEY)

# Domain-specific prompt templates
DOMAIN_PROMPTS = {
    "Python": """You are a technical interviewer conducting a Python programming interview.
Generate a single interview question for a beginner to intermediate level candidate.
The question should test practical Python knowledge.
Topics can include: data types, functions, OOP, lists, dictionaries, loops, 
error handling, file handling, or basic algorithms.
Return ONLY the question, nothing else. No numbering, no explanation.""",

    "DBMS & SQL": """You are a technical interviewer conducting a DBMS and SQL interview.
Generate a single interview question for a beginner to intermediate level candidate.
Topics can include: SQL queries, joins, normalization, indexes, transactions,
keys, relationships, or basic database concepts.
Return ONLY the question, nothing else. No numbering, no explanation.""",

    "Operating Systems": """You are a technical interviewer conducting an Operating Systems interview.
Generate a single interview question for a beginner to intermediate level candidate.
Topics can include: processes, threads, memory management, deadlocks,
scheduling algorithms, file systems, or synchronization.
Return ONLY the question, nothing else. No numbering, no explanation.""",

    "JavaScript": """You are a technical interviewer conducting a JavaScript interview.
Generate a single interview question for a beginner to intermediate level candidate.
Topics can include: variables, functions, closures, promises, async/await,
DOM manipulation, event handling, or ES6+ features.
Return ONLY the question, nothing else. No numbering, no explanation.""",

    "HTML & CSS": """You are a technical interviewer conducting an HTML and CSS interview.
Generate a single interview question for a beginner to intermediate level candidate.
Topics can include: semantic HTML, CSS selectors, box model, flexbox, grid,
responsive design, media queries, CSS animations, or HTML forms.
Return ONLY the question, nothing else. No numbering, no explanation.""",

    "HR Interview": """You are an HR interviewer conducting a personality and behavioral interview.
Generate a single interview question to assess the candidate's soft skills.
Topics can include: self introduction, confidence, leadership, teamwork,
strengths, weaknesses, career goals, conflict resolution, or situational judgment.
The question should be conversational and open-ended.
Return ONLY the question, nothing else. No numbering, no explanation.""",

    "⚡ Demo Mode": """You are a friendly host doing a casual introduction interview.
Generate a single simple personal question to get to know the person better.
Topics: name, hometown, hobbies, favorite food, favorite movie, interests,
favorite subject, dream job, favorite sport, or fun facts about themselves.
Keep it very short, casual and friendly.
Return ONLY the question, nothing else. No numbering, no explanation."""
}

def generate_question(domain, asked_questions=[]):
    """
    Generate a single SHORT and SIMPLE interview question for a beginner level candidate.
    The question must be one sentence only, clear and concise.
    Avoids repeating questions already asked in this session.
    """
    try:
        # Build prompt
        base_prompt = DOMAIN_PROMPTS.get(domain, DOMAIN_PROMPTS["Python"])

        # Add already asked questions to avoid repeats
        if asked_questions:
            avoid = "\n".join(f"- {q}" for q in asked_questions)
            base_prompt += f"\n\nDo NOT repeat any of these questions:\n{avoid}"

        # Call Groq API
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional interviewer. Return ONLY the question, nothing else."
                },
                {
                    "role": "user",
                    "content": base_prompt
                }
            ],
            temperature=0.8,
            max_tokens=150
        )

        question = response.choices[0].message.content.strip()
        return {"success": True, "question": question}

    except Exception as e:
        print(f"Groq API Error: {e}")
        fallback = get_fallback_question(domain, asked_questions)
        return {"success": False, "question": fallback}


# Offline fallback question bank
FALLBACK_QUESTIONS = {
    "Python": [
        "What is the difference between a list and a tuple in Python?",
        "Explain how dictionary works in Python.",
        "What are Python decorators and how do you use them?",
        "What is the difference between deep copy and shallow copy?",
        "Explain the concept of list comprehension with an example.",
        "What is the Global Interpreter Lock (GIL) in Python?",
        "How does exception handling work in Python?",
    ],
    "DBMS & SQL": [
        "What is the difference between PRIMARY KEY and UNIQUE KEY?",
        "Explain the different types of JOINs in SQL.",
        "What is normalization? Explain 1NF, 2NF, and 3NF.",
        "What is the difference between DELETE, TRUNCATE, and DROP?",
        "Explain ACID properties in database transactions.",
        "What is an index in a database and why is it used?",
        "What is the difference between WHERE and HAVING clause?",
    ],
    "Operating Systems": [
        "What is the difference between a process and a thread?",
        "Explain deadlock and the four conditions for it to occur.",
        "What is virtual memory and how does it work?",
        "Explain the different CPU scheduling algorithms.",
        "What is the difference between paging and segmentation?",
        "What are semaphores and how are they used?",
        "Explain the concept of context switching.",
    ],
    "JavaScript": [
        "What is the difference between let, var, and const?",
        "Explain closures in JavaScript with an example.",
        "What is the difference between == and === in JavaScript?",
        "Explain how promises work in JavaScript.",
        "What is event bubbling and event capturing?",
        "What is the difference between null and undefined?",
        "Explain async/await and how it simplifies promises.",
    ],
    "HTML & CSS": [
        "What is the difference between inline, block, and inline-block elements?",
        "Explain the CSS box model.",
        "What is the difference between class and id selectors?",
        "Explain Flexbox and when you would use it.",
        "What are semantic HTML elements and why are they important?",
        "What is responsive design and how do you achieve it?",
        "Explain the difference between absolute, relative, fixed, and sticky positioning.",
    ],
    "HR Interview": [
        "Tell me about yourself and your background.",
        "What are your greatest strengths and weaknesses?",
        "Where do you see yourself in the next 5 years?",
        "Describe a situation where you showed leadership.",
        "How do you handle pressure and tight deadlines?",
        "Tell me about a time you resolved a conflict in a team.",
        "Why should we hire you over other candidates?",
    ],
    "⚡ Demo Mode": [
        "What is your name and where are you from?",
        "What are your hobbies and interests?",
        "What is your favorite subject in school or college?",
        "What is your dream job and why?",
        "What do you like to do in your free time?",
        "What is your favorite movie or TV show?",
        "What sport or game do you enjoy the most?",
    ],
}

def get_fallback_question(domain, asked_questions=[]):
    """Returns a fallback question when API is unavailable."""
    questions = FALLBACK_QUESTIONS.get(domain, FALLBACK_QUESTIONS["Python"])

    # Filter out already asked questions
    available = [q for q in questions if q not in asked_questions]

    if available:
        import random
        return random.choice(available)
    else:
        return "What are your strengths and weaknesses as a developer?"