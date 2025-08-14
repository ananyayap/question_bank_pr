import json
import openai
from config.settings import DETAILED_SYLLABUS, SECTION_TAGS

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
    user_prompt = f"QUESTION:\n{question_text}\n\nAVAILABLE TAGS:\n{json.dumps(tags_list, indent=2)}"

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
        result = json.loads(resp.choices[0].message.content)
        return result.get("tags", ["untagged"])
    except Exception as e:
        print(f"ERROR during tagging: {e}")
        return ["tagging_error"]

def generate_mcqs(chunk, difficulty, section, num_questions=2, image_url=None):
    """
    Generates MCQs using a sophisticated prompt. Now supports images.
    """
    difficulty_definitions = {
        "easy": "An 'easy' question should be straightforward, with clear information. It requires minimal interpretation or multi-step reasoning but should still be a valid SAT-style question, not a simple trivia fact.",
        "medium": "A 'medium' question requires some interpretation, analysis, or multiple steps to solve. The answer may not be immediately obvious.",
        "hard": "A 'hard' question is complex, requiring deep analysis or synthesis of multiple concepts. The answer choices may be deliberately tricky."
    }
    system_prompt = (
        f"You are an expert SAT {section} question creator, specializing in creating high-quality, realistic test questions.\n"
        "Your task is to generate questions based based on the detailed syllabus and reference text provided by the user.\n.\n"
        "Adhere strictly to the provided difficulty definition.\n"
        "Return your response exclusively in the specified JSON format."
    )
    user_prompt_text = f"""
### Difficulty Definition
{difficulty_definitions[difficulty]}
---
### Detailed SAT Syllabus (for reference)
{json.dumps(DETAILED_SYLLABUS.get(section, {}), indent=2)}
---
### Reference Text (for thematic inspiration)
{chunk}
---
### Instructions
Generate exactly {num_questions} questions that match the '{difficulty}' difficulty definition.
If an image is provided, ensure the question is directly related to the image.
"""
    
    user_content = [{"type": "text", "text": user_prompt_text}]

    if image_url:
        print(f"INFO: Generating question with image: {image_url}")
        user_content.append({
            "type": "image_url",
            "image_url": {"url": image_url}
        })

    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.4,
        response_format={"type": "json_object"}
    )

    try:
        content = json.loads(resp.choices[0].message.content)
        mcqs = content.get("questions", content)
        for q in mcqs:
            q["difficulty"] = difficulty
            q["section"] = section
            if image_url:
                q["image_url"] = image_url
            q["tags"] = tag_question_by_concept(q["question_text"], section)
        return mcqs
    except Exception as e:
        print(f"Error parsing MCQs from model output: {e}")
        return []