from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from duckduckgo_search import DDGS
from pypdf import PdfReader

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from rag.chain import retrieve_context

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL")

print("URL:", URL)
print("PROJECT_ID:", PROJECT_ID)
print("API Key Loaded:", bool(API_KEY))

# ==========================
# Flask App
# ==========================

app = Flask(__name__)
app.secret_key = "campuspilot_secret_key"


bcrypt = Bcrypt(app)

uploaded_text = ""
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return ""

        web_text = ""

        for result in results:
            web_text += f"Title: {result['title']}\n"
            web_text += f"Body: {result['body']}\n\n"

        return web_text

    except Exception:
        return ""

# ==========================
# IBM Credentials
# ==========================

credentials = Credentials(
    url=URL,
    api_key=API_KEY
)

# ==========================
# IBM Granite Model
# ==========================

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=PROJECT_ID
)

# ==========================
# Signup
# ==========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name, email, hashed_password)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Email already exists."

        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


# ==========================
# Login
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id,name,password FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            if bcrypt.check_password_hash(user[2], password):

                session["user_id"] = user[0]
                session["user_name"] = user[1]

                return redirect(url_for("home"))

        return "Invalid Email or Password"

    return render_template("login.html")


# ==========================
# Logout
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))
# ==========================
# Home Page
# ==========================

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        username=session["user_name"]
    )
# ==========================
# Chat API (RAG)
# ==========================

        # Retrieve relevant information from FAISS
    context = retrieve_context(user_message)

        # Search latest information from the web
    web_context = search_web(user_message)

        # Merge both contexts
    if web_context:
            context += "\n\nLatest Web Information:\n" + web_context

      prompt = f"""
You are CampusPilot AI.

Use the admission documents first.
If the answer is not available there, use the latest web information.

Context:
{context}

Student Question:
{user_message}

Instructions:
- Prefer admission document information.
- If needed, use the latest web information.
- Answer clearly in bullet points whenever possible.

Answer:
"""

  else:

     prompt = f"""
You are CampusPilot AI.

No relevant admission information was found.

Student Question:
{user_message}

Reply:
This information is not available in the provided admission documents.
"""

        response = model.generate_text(
            prompt=prompt,
            params={
                "max_new_tokens": 300,
                "temperature": 0.3,
                "top_p": 0.9
            }
        )
        if "user_id" in session:

            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO chats(user_id, question, answer)
                VALUES (?, ?, ?)
            """, (
                session["user_id"],
                user_message,
                response
            ))

            conn.commit()
            conn.close()

        return jsonify({
            "response": response
        })
    except Exception as e:

    return jsonify({
            "response": str(e)
        })
    # ==========================
# Upload API
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

        # Create uploads folder
        os.makedirs("uploads", exist_ok=True)

        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        uploaded_text = ""

        # Read PDF
        if file.filename.lower().endswith(".pdf"):

            reader = PdfReader(filepath)

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    uploaded_text += text + "\n"

        # Read TXT
        elif file.filename.lower().endswith(".txt"):

            with open(filepath, "r", encoding="utf-8") as f:
                uploaded_text = f.read()

        else:

            return jsonify({
                "message": "Only PDF and TXT files are supported."
            })

        # Generate AI Summary
        summary = "No text found in the uploaded document."

        if uploaded_text.strip():

            summary_prompt = f"""
You are CampusPilot AI.

Summarize the following admission document in exactly 5 detailed bullet points.

Document:
{uploaded_text[:6000]}
"""

            summary = model.generate_text(
                prompt=summary_prompt,
                params={
                    "max_new_tokens": 500,
                    "temperature": 0.2,
                    "top_p": 0.9
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
@app.route("/history")
@app.route("/recommend", methods=["GET", "POST"])
def recommend():

    if request.method == "GET":
        return render_template("recommendation.html")

    percentage = request.form.get("percentage")
    stream = request.form.get("stream")
    course = request.form.get("course")
    state = request.form.get("state")

    question = f"""
Suggest suitable colleges for a student with:

Class 12 Percentage: {percentage}
Stream: {stream}
Preferred Course: {course}
Preferred State: {state}
"""

    context = retrieve_context(question)

    prompt = f"""
You are CampusPilot AI.

Use ONLY the context below.

Context:
{context}

Student Profile:
{question}

Instructions:

- Recommend colleges only from the context.
- Mention:
  • College Name
  • Eligibility
  • Course
  • Fees (if available)
  • Admission Process
  • Deadlines (if available)

If nothing is found, say:
"No suitable colleges were found in the admission database."

Answer in bullet points.
"""

    response = model.generate_text(
        prompt=prompt,
        params={
            "max_new_tokens": 400,
            "temperature": 0.3,
            "top_p": 0.9
        }
    )

    return render_template(
        "recommendation.html",
        result=response
    )
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question, answer
        FROM chats
        WHERE user_id = ?
        ORDER BY id DESC
    """, (session["user_id"],))

    chats = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        chats=chats
    )
if __name__ == "__main__":
    app.run(debug=True)