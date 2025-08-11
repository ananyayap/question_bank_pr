from google.cloud import firestore
from Question import Question

db = firestore.Client()

def upload_question(question: Question):
    for tag in question.tags:
        path = f"SAT/{question.section}/{question.difficulty}/{tag}/questions"
        db.collection(path).document(question.question_id).set(question.to_dict())

def get_questions(section, difficulty, tag):
    path = f"SAT/{section}/{difficulty}/{tag}/questions"
    docs = db.collection(path).stream()
    return [doc.to_dict() for doc in docs]
