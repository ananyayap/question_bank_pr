import uuid
from google.cloud import firestore
# We don't need to import the Question class here anymore as we will work with dictionaries

db = firestore.Client()

def upload_question(question_data: dict) -> str:
    """
    Uploads a question to Firestore under the structured SAT path for each of its tags.
    Returns the generated question ID.
    """
    # Generate a unique ID for the question
    question_id = str(uuid.uuid4())
    question_data["question_id"] = question_id

    section = question_data["section"]
    difficulty = question_data["difficulty"]
    tags = question_data.get("tags", [])

    if not tags: # If no tags were assigned, give it a default
        tags.append("untagged")

    # Create an entry for each tag
    for tag in tags:
        # Sanitize tag to be a valid Firestore path element
        safe_tag = tag.replace("/", "_")
        path = f"SAT/{section}/{difficulty}/{safe_tag}/questions"
        db.collection(path).document(question_id).set(question_data)

    print(f"Uploaded question {question_id} to SAT collection under {len(tags)} tags.")
    return question_id

def create_quiz_entry(question_id: str, question_data: dict):
    """
    Creates a separate entry for the question in the 'quiz_questions' collection.
    """
    db.collection("quiz_questions").document(question_id).set(question_data)
    print(f"Created entry for {question_id} in quiz_questions collection.")


def get_questions(section, difficulty, tag):
    # Sanitize tag for lookup
    safe_tag = tag.replace("/", "_")
    path = f"SAT/{section}/{difficulty}/{safe_tag}/questions"
    docs = db.collection(path).stream()
    return [doc.to_dict() for doc in docs]