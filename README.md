# 🎓 CampusPilot AI

**An AI-Powered College Admission Assistant using IBM Granite & Retrieval-Augmented Generation (RAG)**

CampusPilot AI is an intelligent admission assistant that helps students quickly find accurate and up-to-date information about college admissions. It combines official admission documents with real-time web information to provide trustworthy, personalized, and conversational guidance.

---

## 🚀 Problem Statement

Students often struggle to access accurate and up-to-date college admission information because it is scattered across university websites, admission brochures, and official notices. This makes it difficult to quickly find details about eligibility, fees, application procedures, and important deadlines, leading to confusion and poor admission decisions

## 💡 Proposed Solution

CampusPilot AI is an intelligent college admission assistant that simplifies the entire admission journey for students. Instead of searching through multiple websites and lengthy admission brochures, students can simply ask their questions in natural language.
The system uses Retrieval-Augmented Generation (RAG) with IBM Granite to retrieve accurate information from official admission documents. If the required information is not available in the uploaded documents, it automatically searches trusted web sources to provide the latest admission updates.

CampusPilot AI also helps students identify colleges that match their percentage, preferred course, stream, and state. In addition, it can summarize admission brochures, answer queries related to eligibility, fees, application procedures, and deadlines, and even extract text from scanned PDF documents using OCR technology.
By bringing official documents, real-time web information, and AI-powered guidance together on a single platform, CampusPilot AI reduces the time and effort students spend searching for information, minimizes confusion, and enables them to make confident and well-informed admission decisions.



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

Key Responsibilities of Agentic AI
Understands student questions in natural language. 
Searches official admission documents for reliable information. 
Retrieves the latest admission updates from trusted web sources when needed. 
Recommends colleges based on the student's profile and preferences. 
Summarizes lengthy admission brochures into easy-to-read points. 
Provides personalized, accurate, and conversational guidance throughout the admission process. 

# 🌟 Novelty & Uniqueness
Retrieval-Augmented Generation (RAG): Retrieves information directly from official admission documents, ensuring accurate and context-based responses instead of relying only on AI-generated knowledge. IBM Granite Foundation Model: Uses IBM Granite on watsonx.ai to understand student queries, reason over retrieved information, summarize documents, and generate natural, human-like responses. OCR-Enabled Document Intelligence: Extracts text from both searchable and scanned admission brochures using Tesseract OCR, making image-based PDFs searchable. Hybrid 

 Knowledge Retrieval: Combines official admission documents with real-time web search to provide both reliable institutional information and the latest admission updates. FAISS Vector Search: Enables fast semantic search across uploaded admission documents for quick and relevant information retrieval. Personalized College Recommendations: Suggests colleges based on students' marks, stream, preferred course, and location instead of providing generic recommendations.

 Admission Brochure Summarization: Converts lengthy admission PDFs into concise, easy-to-understand summaries, saving students time.
Natural Language Interaction: Students can ask questions in simple everyday language without needing technical keywords. 

Secure User Experience: Includes authentication and chat history, allowing students to securely access their previous conversations. 

All-in-One Admission Platform: Integrates document processing, OCR, RAG, AI reasoning, web search, and personalized recommendations into a single intelligent admission assistant

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
