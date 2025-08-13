import json
import openai
from config.settings import SECTION_TAGS, DETAILED_SYLLABUS # Import the tags and detailed syllabus


def tag_question_by_concept(question_text: str, section: str) -> list:
    """
    Uses the LLM to assign relevant tags to a question based on the section's syllabus.
    This version correctly parses the JSON object returned by the AI.
    """
    tags_list = SECTION_TAGS.get(section, [])
    if not tags_list:
        return ["untagged"]

    system_prompt = (
        "You are an expert curriculum developer. Based on the provided question, "
        "select the most relevant tags from the given list. "
        "Return a JSON object with a single key 'tags' containing an array of the selected tag strings."
    )

    user_prompt = f"""
    QUESTION:
    {question_text}

    AVAILABLE TAGS:
    {json.dumps(tags_list, indent=2)}
    """

    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        
        # We parse the JSON and then correctly extract the list from the "tags" key.
        result = json.loads(resp.choices[0].message.content)
        return result.get("tags", ["untagged"]) # Use .get() for safety

    except Exception as e:
        print(f"ERROR during tagging: {e}")
        return ["tagging_error"]


def generate_mcqs(chunk, difficulty, section, num_questions=2):
    """
    Generates exactly `num_questions` MCQs from a text chunk.
    """
     # 1. GET THE DETAILED SYLLABUS
    syllabus_dict = DETAILED_SYLLABUS.get(section, {})
    formatted_syllabus = "\n".join([f"- {topic}: {desc}" for topic, desc in syllabus_dict.items()])

    

    
        
    system_prompt = (
        f"You are an expert SAT {section} question creator.\n"
        "Your task is to generate high-quality SAT-style multiple choice questions based on the detailed syllabus and reference text provided by the user.\n"
        "You must match the requested difficulty and return your response exclusively in the JSON format shown below.\n"
        "Ensure that the questions are clear, concise, and relevant to the SAT curriculum.\n"
        "Each question should have 4 options labeled A, B, C, D, with one correct answer.\n"
        "The questions should be challenging but fair, reflecting the SAT's standards.\n"
        "The options should be plausible distractors, not obviously incorrect.\n"
        """
        [
        {
            "question_text": "...",
            "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
            "correct": "A"
        }
        ]
        """
    )

    user_prompt = f"""

    ### DETAILED SAT SYLLABUS

    {formatted_syllabus}

    ---
    ### REFERENCE TEXT (for thematic inspiration)

    {chunk}
        ---

    Difficulty: {difficulty}
    Number of Questions: {num_questions}
    """

    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2, # A little creativity might be good
        response_format={"type": "json_object"} # Use json_object for better reliability
    )

    try:
        # Note: The model might return a dictionary with a key like "questions"
        # that contains the list. Adjust parsing as needed.
        content = json.loads(resp.choices[0].message.content)
        mcqs = content.get("questions", content) # Adapt to the model's output format

        for q in mcqs:
            q["difficulty"] = difficulty
            q["section"] = section
            # Call the new tagging function
            q["tags"] = tag_question_by_concept(q["question_text"], section)
        return mcqs
    except Exception as e:
        print(f"Error parsing MCQs from model output: {e}")
        print("Model Response:", resp.choices[0].message.content)
        return []