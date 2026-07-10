from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model

# Load environment variables
load_dotenv()

# IBM Credentials
API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL")

print("URL:", URL)
print("PROJECT_ID:", PROJECT_ID)
print("API key loaded:", bool(API_KEY))

app = Flask(__name__)

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

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    prompt = f"""
You are CampusPilot AI, an AI assistant for students.

Your job is to help students with:
- College admissions
- Scholarships
- Required documents
- Entrance exams
- Counselling
- Eligibility
- Admission deadlines

Rules:
1. Answer ONLY education and college admission related questions.
2. If the question is unrelated, reply:
   "I can only help with college admissions and scholarships."
3. Give complete, clear and accurate answers.
4. Use bullet points whenever useful.
5. Never stop in the middle of a sentence.
6. Finish your answer completely.

Student Question:
{user_message}

Complete Answer:
"""

    try:
        response = model.generate_text(prompt=prompt)

        return jsonify({
            "response": response
        })

    except Exception as e:
        return jsonify({
            "response": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)