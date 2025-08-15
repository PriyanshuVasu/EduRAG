# EduRAG Tutor
*A Personal Study Companion that Remembers Your Conversations*

EduRAG Tutor is a smart chatbot I built to act as a personal study helper. It uses a powerful technique called Retrieval-Augmented Generation (RAG) to answer questions based on specific documents, like course notes or textbooks. This means it gives accurate, factual answers instead of making things up.

The best part is its long-term memory. If you log in with the same username, it remembers your past conversations, allowing you to pick up right where you left off.



---
## What It Can Do

* **Answers from Your Documents**: The bot's knowledge is limited to the documents you provide, so its answers are always relevant and fact-based.
* **Remembers You**: By using a simple username, the chatbot saves your chat history and remembers you across different sessions.
* **Handles Follow-up Questions**: It understands the context of the conversation, so you don't have to repeat yourself.
* **Works for Any Subject**: You can load it with any PDF or webpage to create a specialized tutor for any course.

---
## Tech Stack

* **Backend**: Python
* **UI**: Streamlit
* **AI Framework**: LangChain
* **Language Model**: Google Gemini 
* **Vector Storage**: ChromaDB 
* **Memory**: SQLite 

---
## How It Works

The system is built around a simple idea: retrieve, then generate.

1.  **Ingestion**: First, it runs a script (`ingest.py`) that reads documents, breaks them into small chunks, and creates a searchable library in ChromaDB.
2.  **Conversation**: When you chat with the bot, it performs two key steps:
    * It looks at your recent chat history to understand any follow-up questions.
    * It searches its library for the most relevant document chunks related to your question.
3.  **Generation**: Finally, it sends your question, the chat history, and the relevant document chunks to the Gemini model, which generates a smart, context-aware answer.



---
## Getting Started

Here’s how to get the project running on your own machine.

### 1. Prerequisites
* Python 3.10+
* A Google Gemini API Key

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/EduRAG-Tutor.git](https://github.com/your-username/EduRAG-Tutor.git)
cd EduRAG-Tutor
```

### 3. Set Up a Virtual Environment
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Add Your API Key
Create a file named `.env` in the main folder and add your Google API key like this:
```
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

### 6. Create Your Knowledge Base
Put your own PDFs or other documents in the `data` folder and run the ingestion script once:
```bash
python ingest.py
```
This will create the `chroma_db` folder containing your custom knowledge base.

---
## How to Use the App

1.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

2.  **Enter a Username**: This is how the app will save and load your chat history.

3.  **Start Studying**: Ask questions about the topics in your documents. The tutor will use its knowledge base to help you out!