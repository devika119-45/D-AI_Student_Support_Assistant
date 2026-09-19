# 🎓 AI Student Support Assistant

An **AI-powered academic assistant** built to help students learn from study materials, ask questions, generate quizzes, and create study plans using **Generative AI, RAG, and Agentic AI**.

Built with **Python, Streamlit, LangChain, Google Gemini, and ChromaDB**.

---

## 🚀 Features

* 🤖 **AI Academic Assistant** — Ask questions and get AI-powered academic answers.
* 📚 **Study Materials** — Upload and analyze PDF study materials.
* 📄 **PDF Processing** — Extract and process content from academic PDFs.
* 🧠 **RAG-Based Question Answering** — Retrieve relevant information from uploaded documents.
* 📝 **AI Quiz Generator** — Generate quizzes from study materials.
* 📅 **Study Planner** — Organize subjects and study sessions.
* 📊 **Student Progress Support** — Support learning and exam preparation.

---

## 🛠️ Technologies Used

| Technology               | Purpose                         |
| ------------------------ | ------------------------------- |
| 🐍 Python                | Core programming language       |
| 🎨 Streamlit             | Web application interface       |
| 🔗 LangChain             | AI application framework        |
| ✨ Google Gemini          | Generative AI                   |
| 🗄️ ChromaDB             | Vector database                 |
| 📄 PyPDF                 | PDF text extraction             |
| 🧠 Sentence Transformers | Text embeddings                 |
| 🔐 python-dotenv         | Environment variable management |

---

## 🏗️ How It Works

```text
📄 Upload Study Material
          ↓
📖 Extract PDF Text
          ↓
✂️ Split Text into Chunks
          ↓
🧠 Generate Embeddings
          ↓
🗄️ Store in ChromaDB
          ↓
🔍 Retrieve Relevant Content
          ↓
✨ Google Gemini
          ↓
💬 Generate AI Response
```

---

## 📸 Application Screenshots

### 🤖 AI Academic Assistant

![AI Academic Assistant](assets/ai-assistant.png)

### 📚 Study Materials

![Study Materials](assets/study-materials.png)

### 📝 AI Quiz Generator

![AI Quiz](assets/quiz.png)

### 📅 Study Planner

![Study Planner](assets/study-planner.png)

### 📊 Student Progress

![Student Progress](assets/progress.png)

---

## 🎥 Project Demo

### ▶️ AI Student Support Assistant — Demo

[![Project Demo](assets/demo-thumbnail.png)](assets/demo.mp4)

> Click the thumbnail above to watch the project demo.

---

## 📂 Project Structure

```text
AI-Student-Support-Assistant/
│
├── agent/
│   └── Agent-related modules
│
├── tools/
│   └── AI and utility tools
│
├── utils/
│   └── Helper and session utilities
│
├── assets/
│   ├── ai-assistant.png
│   ├── study-materials.png
│   ├── quiz.png
│   ├── study-planner.png
│   ├── progress.png
│   ├── demo-thumbnail.png
│   └── demo.mp4
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Student-Support-Assistant.git
```

### 2. Open the Project

```bash
cd AI-Student-Support-Assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Configuration

Create a `.env` file in the project directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Replace the value with your actual Google Gemini API key.

⚠️ **Never upload your `.env` file or API key to GitHub.**

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🌐 Deployment

This application can be deployed using **Streamlit Community Cloud**.

### Deployment Steps

1. Push the project to GitHub.
2. Connect the GitHub repository to Streamlit Community Cloud.
3. Select `app.py` as the main application file.
4. Add your `GOOGLE_API_KEY` under Streamlit Secrets.
5. Deploy the application.

---

## 🎯 Project Objective

The main objective of this project is to create an intelligent academic assistant that combines **Generative AI, Retrieval-Augmented Generation, and Agentic AI** to provide students with an interactive platform for learning and exam preparation.

---

## 🔮 Future Enhancements

* 🎤 Voice-based AI Assistant
* 📖 Support for multiple document formats
* 📈 Advanced student analytics
* 🧑‍🏫 Personalized AI tutoring
* 🔔 Study reminders
* 📱 Mobile-friendly interface
* 🌐 Multi-language support
* 💾 Learning history and personalization

---

## 👩‍💻 Author

**Devika Kollu**

B.Tech — Artificial Intelligence and Machine Learning

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
