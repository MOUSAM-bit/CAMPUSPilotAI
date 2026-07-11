from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

import os
import sqlite3

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from pypdf import PdfReader
import fitz
import pytesseract
from PIL import Image
from duckduckgo_search import DDGS

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from rag.chain import retrieve_context

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL")

print("IBM URL:", URL)
print("IBM Project:", PROJECT_ID)

# ==========================
# Flask App
# ==========================

app = Flask(__name__)

app.secret_key = "campuspilot_secret_key"

bcrypt = Bcrypt(app)

uploaded_text = ""

# ==========================
# IBM Granite
# ==========================

credentials = Credentials(
    url=URL,
    api_key=API_KEY
)

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=PROJECT_ID
)

# ==========================
# Web Search
# ==========================

def search_web(query):

    try:

        with DDGS() as ddgs:

            results = list(ddgs.text(query, max_results=3))

        if not results:
            return ""

        text = ""

        for item in results:

            text += f"Title: {item['title']}\n"
            text += f"Body: {item['body']}\n\n"

        return text

    except Exception as e:

        print("Web Search Error:", e)
        return ""


# ==========================
# Home
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
# Signup
# ==========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users(name,email,password)
                VALUES(?,?,?)
                """,
                (name, email, hashed)
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
            """
            SELECT id,name,password
            FROM users
            WHERE email=?
            """,
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and bcrypt.check_password_hash(
            user[2],
            password
        ):

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
# Chat API
# ==========================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:

            return jsonify({
                "response": "Please enter a question."
            })

        # Retrieve context from FAISS
        context = retrieve_context(user_message)
               # Search latest information from web
        web_context = search_web(user_message)

        print("WEB CONTEXT:")
        print(web_context)

        # Merge both
        if web_context:
            context += "\n\nLatest Web Information:\n" + web_context

        print("FINAL CONTEXT:")
        print(context)
        prompt = f"""
You are CampusPilot AI, an intelligent college admission assistant.

You have two knowledge sources:

1. Admission documents (highest priority)
2. Latest web information (fallback)

Context:
{context}

Student Question:
{user_message}

Instructions:

- First check whether the admission documents answer the question.
- If the answer exists in the documents, answer using them.
- If the documents do not contain the answer, use the latest web information.
- Never reply only with "This information is not available in the provided admission documents."
- If web information is available, answer using it.
- Clearly mention whether the answer came from:
  • Admission Documents
  • Latest Web Information

Format your answer in clear bullet points whenever possible.

Answer:
"""

        response = model.generate_text(
            prompt=prompt,
            params={
                "max_new_tokens": 400,
                "temperature": 0.3,
                "top_p": 0.9
            }
        )

        # Save Chat History
        if "user_id" in session:

            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO chats(user_id, question, answer)
                VALUES(?,?,?)
                """,
                (
                    session["user_id"],
                    user_message,
                    response
                )
            )

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

        if not file:
            return jsonify({
                "message": "No file selected."
            })

        os.makedirs("uploads", exist_ok=True)

        filepath = os.path.join(
            "uploads",
            file.filename
        )

        file.save(filepath)

        uploaded_text = ""

        # ================= PDF =================
        if file.filename.lower().endswith(".pdf"):

            reader = PdfReader(filepath)

            # Try normal text extraction
            for page in reader.pages:

                text = page.extract_text()

                if text:
                    uploaded_text += text + "\n"

            # If scanned PDF, use OCR
            if not uploaded_text.strip():

                doc = fitz.open(filepath)

                for page_num in range(len(doc)):

                    page = doc.load_page(page_num)

                    pix = page.get_pixmap(dpi=300)

                    image_path = os.path.join(
                        "uploads",
                        f"page_{page_num}.png"
                    )

                    pix.save(image_path)

                    image = Image.open(image_path)

                    text = pytesseract.image_to_string(image)

                    uploaded_text += text + "\n"

                doc.close()

        # ================= TXT =================
        elif file.filename.lower().endswith(".txt"):

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as f:

                uploaded_text = f.read()

        else:

            return jsonify({
                "message": "Only PDF and TXT files are supported."
            })
        summary = "No text found."

        if uploaded_text.strip():

            prompt = f"""
Summarize the following admission document into 5 detailed bullet points.

Document:

{uploaded_text[:6000]}
"""

            summary = model.generate_text(
                prompt=prompt,
                params={
                    "max_new_tokens": 500,
                    "temperature": 0.2
                }
            )

        return jsonify({
            "message": "Upload Successful",
            "summary": summary
        })

    except Exception as e:

        return jsonify({
            "message": str(e)
        })

# ==========================
# Chat History
# ==========================

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT question,answer
        FROM chats
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    )

    chats = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        chats=chats
    )


# ==========================
# Recommendation
# ==========================

@app.route("/recommend", methods=["GET", "POST"])
def recommend():

    if request.method == "GET":

        return render_template(
            "recommendation.html"
        )

    percentage = request.form["percentage"]
    stream = request.form["stream"]
    course = request.form["course"]
    state = request.form["state"]

    question = f"""

Percentage : {percentage}

Stream : {stream}

Course : {course}

State : {state}

Recommend suitable colleges.

"""

    context = retrieve_context(question)

    prompt = f"""
You are CampusPilot AI.

Recommend colleges using
the admission documents.

Context:

{context}

Student Profile:

{question}

Mention:

- College
- Course
- Eligibility
- Fees
- Admission Process
- Deadlines

If unavailable,
say no suitable college found.
"""

    result = model.generate_text(
        prompt=prompt,
        params={
            "max_new_tokens": 400,
            "temperature": 0.3
        }
    )

    return render_template(
        "recommendation.html",
        result=result
    )
    # ==========================
# Run
# ==========================

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
    