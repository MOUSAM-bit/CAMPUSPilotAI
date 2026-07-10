from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from pypdf import PdfReader

# Load environment variables
load_dotenv()

# IBM Credentials
API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL")

print("URL:", URL)
print("PROJECT_ID:", PROJECT_ID)
print("API Key Loaded:", bool(API_KEY))

app = Flask(__name__)
uploaded_text =""

# IBM Credentials
credentials = Credentials(
    url=URL,
    api_key=API_KEY
)

# IBM Granite Model
model = Model(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=PROJECT_ID,
    params={
        "max_new_tokens": 300,
        "min_new_tokens": 50,
        "temperature": 0.2,
        "top_p": 0.9
    }
)

# ==========================
# Home Page
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Chat API
# ==========================
@app.route("/chat", methods=["POST"])
def chat():

    global uploaded_text

    try:
        user_message = request.json.get("message")

        if uploaded_text.strip():

            prompt = f"""
You are CampusPilot AI.

The student has uploaded the following document.

Document:
{uploaded_text}

Student Question:
{user_message}

Instructions:
- Answer ONLY using the uploaded document whenever possible.
- If the answer is not present in the document, clearly say:
  "This information is not available in the uploaded document."
- Give clear answers using bullet points where appropriate.
"""

        else:

            prompt = f"""
You are CampusPilot AI.

You help students with:

- College Admissions
- Scholarships
- Eligibility
- Entrance Exams
- Required Documents
- Counselling
- Career Guidance

Rules:
1. Answer ONLY education-related questions.
2. If the question is unrelated, reply:
"I can only help with education and college admissions."
3. Give complete answers.
4. Use bullet points whenever appropriate.
5. Never stop in the middle of a sentence.

Student Question:
{user_message}

Answer:
"""

        response = model.generate_text(prompt=prompt)

        return jsonify({
            "response": response
        })

    except Exception as e:

        return jsonify({
            "response": f"Error: {str(e)}"
        })


# ==========================
# Upload File API
# ==========================
@app.route("/upload", methods=["POST"])
def upload():

    global uploaded_text

    try:

        file = request.files.get("file")

        if file is None:
            return jsonify({
                "message": "No file selected."
            })

        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        uploaded_text = ""

        # PDF File
        if file.filename.lower().endswith(".pdf"):

            reader = PdfReader(filepath)

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    uploaded_text += text + "\n"

        # TXT File
        elif file.filename.lower().endswith(".txt"):

            with open(filepath, "r", encoding="utf-8") as f:
                uploaded_text = f.read()

          else:

            uploaded_text = ""

        # ==========================
        # Generate AI Summary
        # ==========================

        summary = ""

        if uploaded_text.strip():

            summary_prompt = f"""
Summarize the following admission document in 5 clear bullet points.

Document:
{uploaded_text}
"""

            summary = model.generate_text(
                prompt=summary_prompt,
                params={
                    "max_new_tokens": 200,
                    "temperature": 0.2
                }
            )

        return jsonify({
            "message": f"{file.filename} uploaded successfully!",
            "summary": summary
        })   

    except Exception as e:

        return jsonify({
            "message": str(e)
        })

# ==========================
# Run Flask
# ==========================
if __name__ == "__main__":
    app.run(debug=True)