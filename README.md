# 🎓 CampusPilot AI

**An AI-Powered College Admission Assistant using IBM Granite & Retrieval-Augmented Generation (RAG)**

CampusPilot AI is an intelligent admission assistant that helps students quickly find accurate and up-to-date information about college admissions. It combines official admission documents with real-time web information to provide trustworthy, personalized, and conversational guidance.

---

## 🚀 Problem Statement

Students often spend hours searching through university websites, admission brochures, and FAQs to understand eligibility, fees, admission procedures, deadlines, and course details. Since this information is scattered across multiple sources and frequently updated, students often face confusion or rely on outdated information.

CampusPilot AI simplifies this process by providing a single platform where students can ask questions in natural language and receive accurate, personalized, and up-to-date admission guidance.

---

## 💡 Proposed Solution

CampusPilot AI acts as a virtual admission counselor by combining official admission documents with the latest web information.

The system:
- Retrieves information from admission brochures using **Retrieval-Augmented Generation (RAG)**.
- Searches trusted web sources if the information is unavailable in the uploaded documents.
- Generates natural, context-aware responses using **IBM Granite Foundation Models**.
- Recommends suitable colleges based on student preferences.
- Summarizes lengthy admission brochures into easy-to-understand points.

---

# ✨ Features

- 📄 Upload Admission Brochures (PDF/TXT)
- 🔍 RAG-based Document Retrieval
- 🌐 Real-Time Web Search Integration
- 🤖 IBM Granite AI-powered Responses
- 📑 Automatic Document Summarization
- 🎯 Personalized College Recommendations
- 🔐 User Authentication (Signup/Login)
- 📚 Chat History
- 📝 OCR Support for Scanned PDFs

---

# 🏗️ Architecture

```
Student
   │
   ▼
Flask Web Application
   │
   ├── Admission Documents (RAG)
   │        │
   │        ▼
   │    FAISS Vector Database
   │
   ├── DuckDuckGo Web Search
   │
   ▼
Context Generation
   │
   ▼
IBM Granite Foundation Model
   │
   ▼
Personalized AI Response
```

---

# 🛠️ Technologies Used

| Technology | Version |
|------------|---------|
| Python | 3.13 |
| Flask | Latest |
| IBM watsonx.ai | Granite Foundation Models |
| IBM Granite Model | granite-4-h-small |
| FAISS | Latest |
| Sentence Transformers | Latest |
| SQLite | Built-in |
| PyPDF | Latest |
| PyMuPDF (fitz) | Latest |
| Tesseract OCR | Latest |
| Pillow | Latest |
| DuckDuckGo Search | Latest |
| HTML | HTML5 |
| CSS | CSS3 |
| JavaScript | ES6 |

---

# 🤖 IBM Granite Model Used

**IBM Granite 4 H Small**

Used for:
- Natural Language Understanding
- Admission Query Answering
- Personalized Guidance
- Document Summarization
- Conversational AI

---

# 🧠 Role of Agentic AI

CampusPilot AI acts as an intelligent admission assistant rather than a simple chatbot.

It:
- Understands student queries.
- Retrieves information from official admission documents.
- Searches trusted web sources when required.
- Reasons over multiple knowledge sources.
- Generates personalized admission guidance.

---

# 🌟 Novelty & Uniqueness

- Retrieval-Augmented Generation (RAG) for accurate responses.
- IBM Granite-powered conversational AI.
- OCR support for scanned admission brochures.
- FAISS semantic document retrieval.
- Real-time web search for latest admission updates.
- Personalized college recommendations.
- Automatic document summarization.
- Secure user authentication and chat history.
- Combines multiple AI technologies into one admission platform.

---

# 📂 Project Structure

```
CampusPilotAI/
│
├── app.py
├── rag/
│   ├── chain.py
│   └── retriever.py
├── templates/
├── static/
├── uploads/
├── users.db
├── requirements.txt
├── README.md
└── .env
```

---

# ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/MOUSAM-bit/CAMPUSPilotAI.git
```

```bash
cd CAMPUSPilotAI
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create .env File

```env
IBM_API_KEY=YOUR_API_KEY
IBM_PROJECT_ID=YOUR_PROJECT_ID
IBM_URL=https://us-south.ml.cloud.ibm.com
```

### Run

```bash
python app.py
```

Visit

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

Add screenshots of:

- Login Page
- Home Page
- Chat Interface
- Upload Document
- College Recommendation
- Chat History

---

# 🚀 Future Scope

- Support more universities across India.
- Multilingual support.
- Mobile application.
- Admission deadline reminders.
- Enhanced recommendation engine.
- Integration with official university portals.

---

# 👨‍💻 Team

**Project Name:** CampusPilot AI

**Developer:** Mousam Kumari

---

# 📄 License

This project is developed for educational Purpose

---

# 🔗 Links

**GitHub Repository**

https://github.com/MOUSAM-bit/CAMPUSPilotAI

**Live Demo**
https://campuspilotai-production.up.railway.app/login


---

⭐ If you found this project useful, consider giving it a star on GitHub!
