import uuid
from google.cloud import firestore

db = firestore.Client()

def upload_question(question_data: dict) -> str:
    """
    Uploads a question ID to the SAT index collection and the full data
    to the quiz_questions collection.
    """
    question_id = str(uuid.uuid4())
    section = question_data["section"]
    difficulty = question_data["difficulty"]
    tags = question_data.get("tags", [])

    if not tags:
        tags.append("untagged")

    index_data = {"question_id": question_id}

    for tag in tags:
        safe_tag = tag.replace("/", "_").replace(" ", "-")
        path = f"SAT/{section}/{difficulty}/{safe_tag}/questions"
        db.collection(path).document(question_id).set(index_data)

    print(f"Indexed question {question_id} in SAT collection under {len(tags)} tags.")

    final_question_data = {
        "question_id": question_id,
        "question_text": question_data["question_text"],
        "options": question_data["options"],
        "correct": question_data["correct"],
        "difficulty": difficulty,
        "section": section,
        "tags": tags,
        "image_url": question_data.get("image_url", None) # Safely get image_url
    }
    
    create_quiz_entry(question_id, final_question_data)
    return question_id

def create_quiz_entry(question_id: str, question_data: dict):
    """
    Saves the complete question data to the main quiz_questions collection.
    """
    db.collection("quiz_questions").document(question_id).set(question_data)
    print(f"Saved full data for {question_id} in quiz_questions collection.")