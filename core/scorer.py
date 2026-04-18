from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

def score_answer(question, answer, domain):
    """
    Score a single answer using Groq AI.
    Returns score (1-10) and feedback.
    """
    if not answer or answer.strip() == "":
        return {
            "score": 0,
            "feedback": "No answer provided.",
            "ideal_answer": "N/A"
        }

    prompt = f"""You are an expert interviewer evaluating a candidate's answer.

Domain: {domain}
Question: {question}
Candidate's Answer: {answer}

Evaluate the answer and respond in this EXACT format:
SCORE: [number from 1-10]
FEEDBACK: [2-3 sentences of constructive feedback]
IDEAL: [1-2 sentences describing an ideal answer]

Be fair, constructive and encouraging."""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical interviewer. Always respond in the exact format requested."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=300
        )

        text = response.choices[0].message.content.strip()
        return parse_score_response(text)

    except Exception as e:
        print(f"Scoring error: {e}")
        return {
            "score": 5,
            "feedback": "Unable to score this answer automatically.",
            "ideal_answer": "N/A"
        }


def parse_score_response(text):
    """Parse the score response from Groq."""
    result = {
        "score": 5,
        "feedback": "Good attempt.",
        "ideal_answer": "N/A"
    }

    try:
        lines = text.strip().split('\n')
        for line in lines:
            if line.startswith("SCORE:"):
                score_str = line.replace("SCORE:", "").strip()
                result["score"] = int(''.join(filter(str.isdigit, score_str[:2])))
            elif line.startswith("FEEDBACK:"):
                result["feedback"] = line.replace("FEEDBACK:", "").strip()
            elif line.startswith("IDEAL:"):
                result["ideal_answer"] = line.replace("IDEAL:", "").strip()
    except:
        pass

    # Clamp score between 0 and 10
    result["score"] = max(0, min(10, result["score"]))
    return result


def score_session(answers, domain):
    """
    Score all answers in a session.
    Returns list of scored answers.
    """
    scored = []
    for item in answers:
        print(f"Scoring question {item['question_num']}...")
        score_result = score_answer(
            item["question"],
            item["answer"],
            domain
        )
        scored.append({
            **item,
            "score": score_result["score"],
            "feedback": score_result["feedback"],
            "ideal_answer": score_result["ideal_answer"]
        })
    return scored