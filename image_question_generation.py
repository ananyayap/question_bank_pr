import os
from google.cloud import storage
from pipeline.pipeline import generate_mcqs
from database.firebase import upload_question
from config.settings import SECTIONS, DIFFICULTIES

# --- CONFIGURE YOUR GOOGLE CLOUD STORAGE ---
# Make sure this is your correct GCS bucket name
GCS_BUCKET_NAME = "pratinidhi-ai-project.appspot.com" 
# -----------------------------------------

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

def generate_questions_for_single_image(local_image_path: str, num_versions_per_category: int):
    """
    Generates multiple question versions for a single local image.
    """
    if not os.path.exists(local_image_path):
        print(f"ERROR: Image file not found at: {local_image_path}")
        return

    print(f"--- Starting processing for image: {local_image_path} ---")
    
    # Use the image's own filename as its name in the cloud
    image_filename = os.path.basename(local_image_path)
    
    # 1. Upload the single image to GCS to get its URL
    public_url = upload_image_to_gcs(local_image_path, image_filename)
    if not public_url:
        print("ERROR: Halting process due to image upload failure.")
        return

    # 2. Generate questions for this image across all sections and difficulties
    print(f"\nINFO: Generating {num_versions_per_category} question(s) per category for image: {public_url}")
    
    # We provide a generic text context for the AI
    generic_context = "Generate a question based on the provided image and the SAT syllabus."
    
    for section in SECTIONS:
        for difficulty in DIFFICULTIES:
            print(f"  -> Generating: {section}, {difficulty}")
            
            # Call the generator to create the desired number of questions
            questions = generate_mcqs(
                chunk=generic_context,
                difficulty=difficulty,
                section=section,
                num_questions=num_versions_per_category, # Use the parameter here
                image_url=public_url
            )
            
            # 3. Upload the newly generated questions to Firestore
            for q_data in questions:
                upload_question(q_data)

    print("\n--- Pipeline Completed ---")

if __name__ == "__main__":
    # --- YOUR INPUT GOES HERE ---
    
    # 1. Tell the script where to find your local image file.
    #    (e.g., "C:\\Users\\Ananya\\Downloads\\my_graph_image.png")
    image_to_process = "images_to_process/my_graph_image.png" 
    
    # 2. Tell the script how many questions you want for EACH category.
    #    (e.g., 3 easy math, 3 medium math, 3 hard math, 3 easy reading, etc.)
    number_of_questions_to_create = 2
    
    # --------------------------
    
    generate_questions_for_single_image(image_to_process, number_of_questions_to_create)