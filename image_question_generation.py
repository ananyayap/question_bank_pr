import os
import fitz  # PyMuPDF
from google.cloud import storage
from pipeline.pipeline import generate_mcqs
from database.firebase import upload_question
from config.settings import SECTIONS, DIFFICULTIES

# --- CONFIGURE YOUR GOOGLE CLOUD STORAGE ---

GCS_BUCKET_NAME = "pratinidhi-ai-project.firebasestorage.app" 


def upload_image_to_gcs(file_path: str, destination_blob_name: str) -> str:
    """Uploads a file to the GCS bucket and returns its public URL."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(file_path)
        blob.make_public()
        
        print(f"INFO: Uploaded {file_path} to gs://{GCS_BUCKET_NAME}/{destination_blob_name}")
        return blob.public_url
    except Exception as e:
        print(f"ERROR: Could not upload {file_path}. Is your bucket name correct? Error: {e}")
        return None

def extract_and_process_images(pdf_path: str, output_dir="extracted_images"):
    """
    Extracts images from a PDF, uploads them to GCS, and generates questions for each.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = fitz.open(pdf_path)
    print(f"INFO: Starting processing for {pdf_path}...")

    for page_num, page in enumerate(doc, 1):
        image_list = page.get_images(full=True)
        if not image_list:
            continue

        print(f"\n--- Processing Page {page_num} ---")
        page_text_context = page.get_text("text")

        for img_index, img in enumerate(image_list, 1):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                local_filename = f"page{page_num}_img{img_index}.{image_ext}"
                local_filepath = os.path.join(output_dir, local_filename)
                with open(local_filepath, "wb") as img_file:
                    img_file.write(image_bytes)

                public_url = upload_image_to_gcs(local_filepath, local_filename)
                if not public_url:
                    continue 

                print(f"INFO: Generating questions for image: {public_url}")
                for section in SECTIONS:
                    for difficulty in DIFFICULTIES:
                        print(f"  -> Generating: {section}, {difficulty}")
                        
                        questions = generate_mcqs(
                            chunk=page_text_context,
                            difficulty=difficulty,
                            section=section,
                            num_questions=1,
                            image_url=public_url
                        )
                        
                        for q_data in questions:
                            upload_question(q_data)

            except Exception as e:
                print(f"ERROR: Failed during processing of image {img_index} on page {page_num}: {e}")

    doc.close()
    print("\n--- Pipeline Completed ---")

if __name__ == "__main__":
    extract_and_process_images("resources/books/ppreading.pdf")