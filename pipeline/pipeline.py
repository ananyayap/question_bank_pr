import json
import openai
from config.settings import tag_question_by_concept


def generate_mcqs(chunk, difficulty, section, num_questions=2):
    """
    Generates exactly `num_questions` MCQs from a text chunk.
    """
    system_prompt = (
        f"You are an expert SAT {section} question creator.\n"
        "Given the provided text, generate exactly the requested number of high-quality "
        "SAT-style multiple choice questions.\n"
        "Each question should:\n"
        "- Have four options labeled A, B, C, D.\n"
        "- Have one correct answer labeled as 'A', 'B', 'C', or 'D'.\n"
        "- Be based only on the provided text.\n"
        "- Match the given difficulty.\n"
        "Return ONLY a JSON array of objects in this format:\n"
        "[\n"
        "  {\n"
        '    "question": "...",\n'
        '    "A": "...",\n'
        '    "B": "...",\n'
        '    "C": "...",\n'
        '    "D": "...",\n'
        '    "correct": "A"\n'
        "  }\n"
        "]"
    )

    user_prompt = f"""
    TEXT:
    {chunk}

    Difficulty: {difficulty}
    Number of Questions: {num_questions}
    """

    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        response_format={"type": "json"}
    )

    try:
        mcqs = json.loads(resp.choices[0].message.content)
        for q in mcqs:
            q["difficulty"] = difficulty
            q["section"] = section
            q["tags"] = tag_question_by_concept(q["question"], q.get("correct"))
        return mcqs
    except Exception as e:
        print("Error parsing MCQs:", e)
        return []
