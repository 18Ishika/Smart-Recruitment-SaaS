import os
import re
import pdfplumber
from docx import Document
from sentence_transformers import SentenceTransformer
import numpy as np
from django.conf import settings
def get_resume_path(job_id):
    # If running inside Django
    try:
        base_media = settings.MEDIA_ROOT
    except:
        # Fallback for standalone testing
        base_media = os.path.join(os.getcwd(), 'media')
    
    return os.path.join(base_media, 'resumes', f'job_{job_id}')
# Initialize the model once (globally) to save memory/time
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text(file_path):
    """Extracts text from PDF or DOCX files."""
    try:
        if file_path.lower().endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                text = '\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])
            return text
        elif file_path.lower().endswith(('.doc', '.docx')):
            doc = Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return ""
    return ""

def get_similarity_score(resume_text, jd_vector):
    """Calculates cosine similarity between a resume and the JD vector."""
    if not resume_text.strip():
        return 0.0
    
    resume_vector = model.encode(resume_text)
    
    # Using numpy for much faster cosine similarity calculation
    dot_product = np.dot(resume_vector, jd_vector)
    norm_resume = np.linalg.norm(resume_vector)
    norm_jd = np.linalg.norm(jd_vector)
    
    if norm_resume == 0 or norm_jd == 0:
        return 0.0
    return float(dot_product / (norm_resume * norm_jd))

def rank_resumes(job_description, resumes_folder):
    """
    Processes all resumes in a folder and ranks them against the JD.
    """
    # Pre-calculate JD vector so we only do it once
    jd_vector = model.encode(job_description)
    
    results = []
    
    # Supported extensions
    valid_extensions = ('.pdf', '.docx', '.doc')
    
    for filename in os.listdir(resumes_folder):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(resumes_folder, filename)
            print(f"Processing: {filename}...")
            
            text = extract_text(file_path)
            score = get_similarity_score(text, jd_vector)
            
            results.append({
                "filename": filename,
                "score": round(score * 100, 2), # Convert to percentage
                "text_preview": text[:200]      # Store snippet for LLM stage
            })
    
    # Sort by score descending
    ranked_results = sorted(results, key=lambda x: x['score'], reverse=True)
    return ranked_results

def process_and_score_resume(resume, job_description):
    """
    Processes a single Resume model instance:
    - extracts text
    - computes similarity score
    - saves parsed_text & score to DB
    """
    jd_vector = model.encode(job_description)

    file_path = resume.resume_file.path
    text = extract_text(file_path)
    score = get_similarity_score(text, jd_vector) * 100

    resume.parsed_text = text
    resume.score = round(score, 2)
    resume.save()

    return {
        "resume_id": resume.id,
        "filename": os.path.basename(file_path),
        "score": resume.score
    }

"""
# --- Example Usage ---
if __name__ == "__main__":
    job_desc = '''
    We are looking for a Python Developer with 2 years of experience. 
    Required skills: Machine Learning, NLP, PyTorch, and FastAPI. 
    Experience with AWS and Docker is a plus.
    '''
    
    # Path to the folder containing your resumes
    folder_path = get_resume_path(job_id="1")
    # Ensure folder exists
    if os.path.exists(folder_path):


        rankings = rank_resumes(job_desc, folder_path)
        
        print("\n--- Final Rankings ---")
        for i, res in enumerate(rankings):
            print(f"{i+1}. {res['filename']} - Score: {res['score']}%")
    else:
        print(f"Folder '{folder_path}' not found. Please create it and add resumes.")
"""