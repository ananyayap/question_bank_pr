import uuid
from typing import List, Optional

class Question:
    def __init__(self, question_text: str, options: dict, correct: str, difficulty: str, section: str, tags: List[str], image_url: Optional[str] = None):
        self.question_id = str(uuid.uuid4())  # unique id
        self.question_text = question_text
        self.options = options  # {"A": "...", "B": "...", ...}
        self.correct = correct  # "A" / "B" / ...
        self.difficulty = difficulty  # "easy" / "medium" / "hard"
        self.section = section  # "maths" / "reading" / "writing"
        self.tags = tags
        self.image_url = image_url 

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "question_text": self.question_text,
            "options": self.options,
            "correct": self.correct,
            "difficulty": self.difficulty,
            "section": self.section,
            "tags": self.tags,
            "image_url": self.image_url
        }

    @staticmethod
    def from_dict(data: dict):
        return Question(
            question_text=data["question_text"],
            options=data["options"],
            correct=data["correct"],
            difficulty=data["difficulty"],
            section=data["section"],
            tags=data["tags"],
            image_url=data.get("image_url")  # Optional field
        )
