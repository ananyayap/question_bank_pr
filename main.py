import fitz  
from pipeline.pipeline import generate_mcqs
from database.firebase import upload_question, create_quiz_entry
from config.settings import SECTIONS, DIFFICULTIES

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a given PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def chunk_text(text: str, chunk_size: int = 2000) -> list[str]:
    """Splits text into smaller chunks of a specified size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

if __name__ == "__main__":
    # 1. Extract text from your resource file
    # Make sure you have a 'resources/books' directory with 'book1.pdf' inside
    print("Extracting text from PDF...")
    text = extract_text_from_pdf("resources/Notes/A.pdf")

    # 2. Chunk the text
    chunks = chunk_text(text)
    print(f"Split text into {len(chunks)} chunks.")

    # 3. Pick section for this run
    section = "math"  # You can change this to "reading" or "writing"
    num_questions = 1 # Number of questions to generate per chunk

    # 4. Generate questions for each difficulty and upload
    for difficulty in DIFFICULTIES:
        print(f"--- Generating {difficulty} questions for section: {section} ---")
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            questions = generate_mcqs(chunk, difficulty, section, num_questions=num_questions)
            for q_data in questions:
                # Firestore has trouble with the Question class object, so we pass the dictionary directly
                question_id = upload_question(q_data) # This saves to the main SAT path
                if question_id:
                    create_quiz_entry(question_id, q_data) # This creates the separate quiz entry
            print(f"Generated and uploaded {len(questions)} questions for chunk {i+1}.")

    print("\nPipeline completed successfully!")