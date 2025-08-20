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
    Generates MCQs using a more sophisticated prompt to achieve true SAT-level difficulty.
    """
    # NEW: More detailed, action-oriented difficulty definitions
    difficulty_definitions = {
        "easy": "An 'easy' SAT question is straightforward and requires minimal interpretation. The answer is usually found directly in the provided text or image. It should test a core concept without complex steps. The incorrect options should be clearly wrong.",
        
        "medium": "A 'medium' SAT question requires multiple steps of reasoning or calculation. The user might need to synthesize information from different parts of the text or image. The incorrect options (distractors) should be plausible and target common student errors.",
        
        "hard": "A 'hard' SAT question is complex and requires deep analytical or inferential skills. The question may be phrased in a convoluted way, and the answer might be the 'best' choice among several plausible options. The distractors must be very tempting and specifically designed to mislead students who have a superficial understanding of the topic."
    }

    # NEW: A more professional and demanding system prompt
    system_prompt = (
        f"You are a psychometrician and expert SAT {section} test developer. Your sole focus is creating high-quality, realistic test questions that precisely mirror the cognitive complexity and style of the official College Board SAT exam.\n"
        "Your questions must be novel and challenging. Critically analyze the provided syllabus and difficulty definition to inform your creation.\n"
        "Above all, create plausible, tricky distractors for the incorrect answers. An excellent 'hard' question is defined by its clever and tempting incorrect options.\n"
        "Return your response exclusively in the specified JSON format."
    )
    
    user_prompt_text = f"""
    ### Difficulty Level & Definition to Embody
    '{difficulty}': {difficulty_definitions[difficulty]}

    ---
    ### Detailed SAT Syllabus (Core Topics)
    {json.dumps(DETAILED_SYLLABUS.get(section, {}), indent=2)}

    ---
    ### Reference Asset (for thematic inspiration)
    {chunk}

    ---
    ### Your Task
    Generate exactly {num_questions} questions that perfectly match the '{difficulty}' definition. For 'hard' questions, focus on creating subtle and challenging answer choices.
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
        temperature=0.5, # Increase temperature for more creativity and less repetitive questions
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