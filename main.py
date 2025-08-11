from pipeline.pipeline import generate_mcqs, extract_text_from_pdf, chunk_text
from database.firebase import upload_question
from config.settings import SECTIONS, DIFFICULTIES

if __name__ == "__main__":
    # Example: load a PDF
    text = extract_text_from_pdf("resources/books/book1.pdf")

    # Chunk the text
    chunks = chunk_text(text)

    # Pick section for this run
    section = "math"
    num_questions = 3  # change as needed

    # Generate questions for each difficulty
    for difficulty in DIFFICULTIES:
        for chunk in chunks:
            questions = generate_mcqs(chunk, difficulty, section, num_questions=num_questions)
            for q in questions:
                upload_question(q)
    print("Pipeline completed.")
