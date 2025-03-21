from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_skills(text):
    doc = nlp(text)
    skills = set()
    for ent in doc.ents:
        if ent.label_ == "ORG" or ent.label_ == "PRODUCT":
            skills.add(ent.text)
    return list(skills)

def extract_experience(text):
    doc = nlp(text)
    experience = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            experience.append(ent.text)
    return experience

def score_resume(text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text, job_description])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0] * 100  

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files or "jobDescription" not in request.files:
        return jsonify({"error": "Resume or Job Description file missing"}), 400

    resume_file = request.files["resume"]
    job_file = request.files["jobDescription"]

    if resume_file.filename == "" or job_file.filename == "":
        return jsonify({"error": "One or more files not selected"}), 400

    # Save files temporarily
    resume_path = os.path.join("uploads", resume_file.filename)
    job_path = os.path.join("uploads", job_file.filename)

    resume_file.save(resume_path)
    job_file.save(job_path)

    # Extract text
    resume_text = extract_text_from_pdf(resume_path)
    job_description = extract_text_from_txt(job_path)

    # Process data
    skills = extract_skills(resume_text)
    experience = extract_experience(resume_text)
    score = score_resume(resume_text, job_description)

    # Clean up
    os.remove(resume_path)
    os.remove(job_path)

    return jsonify({
        "feedback": {
            "skills": skills,
            "experience": experience,
            "score": round(score, 2),
        }
    })

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(port=5000)

















# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import PyPDF2
# import os
# import spacy
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# app = Flask(__name__)
# CORS(app)

# # Load spaCy model for NLP
# nlp = spacy.load("en_core_web_sm")

# def extract_text_from_pdf(file_path):
#     with open(file_path, "rb") as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#     return text

# def extract_skills(text):
#     # Use spaCy to extract skills (customize based on your needs)
#     doc = nlp(text)
#     skills = set()
#     for ent in doc.ents:
#         if ent.label_ == "ORG" or ent.label_ == "PRODUCT":  # Example: Extract organizations/products as skills
#             skills.add(ent.text)
#     return list(skills)

# def extract_experience(text):
#     # Use spaCy to extract experience (customize based on your needs)
#     doc = nlp(text)
#     experience = []
#     for ent in doc.ents:
#         if ent.label_ == "DATE":  # Example: Extract dates
#             experience.append(ent.text)
#     return experience

# def score_resume(text, job_description):
#     # Use TF-IDF and cosine similarity to score the resume
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform([text, job_description])
#     similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
#     return similarity[0][0] * 100  # Convert to percentage

# @app.route("/analyze", methods=["POST"])
# def analyze():
#     if "resume" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["resume"]
#     job_description = request.form.get("jobDescription", "")  # Get job description from form data

#     if file.filename == "":
#         return jsonify({"error": "No file selected"}), 400

#     file_path = os.path.join("uploads", file.filename)
#     file.save(file_path)

#     text = extract_text_from_pdf(file_path)
#     skills = extract_skills(text)
#     experience = extract_experience(text)
#     score = score_resume(text, job_description)

#     os.remove(file_path)  # Delete the uploaded file
#     return jsonify({
#         "feedback": {
#             "skills": skills,
#             "experience": experience,
#             "score": round(score, 2),
#         }
#     })

# if __name__ == "__main__":
#     os.makedirs("uploads", exist_ok=True)
#     app.run(port=5000)










# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import PyPDF2
# import os

# app = Flask(__name__)
# CORS(app)

# def extract_text_from_pdf(file_path):
#     with open(file_path, "rb") as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#     return text

# def analyze_resume(text):
#     # Example: Count keywords
#     keywords = ["Python", "React", "JavaScript", "AI"]
#     score = sum(text.count(keyword) for keyword in keywords)
#     return f"Your resume contains {score} relevant keywords."

# @app.route("/analyze", methods=["POST"])
# def analyze():
#     if "resume" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["resume"]
#     if file.filename == "":
#         return jsonify({"error": "No file selected"}), 400

#     file_path = os.path.join("uploads", file.filename)
#     file.save(file_path)

#     text = extract_text_from_pdf(file_path)
#     result = analyze_resume(text)

#     os.remove(file_path)  # Delete the uploaded file
#     return jsonify({"feedback": result})

# if __name__ == "__main__":
#     os.makedirs("uploads", exist_ok=True)
#     app.run(port=5000)