# **AI Study Buddy**

## Project Description
This is an intelligent chatbot that allows users to upload a **PDF document** and ask questions about its content. This can be useful for studying, research, or summarizing key points from documents, emails, textbooks, etc.

The chatbot optimizes response retrieval using the **Multi-Query RAG strategy**, ensuring more relevant and accurate answers.  


## Features  
✔ **Upload a PDF** and chat with it in real-time. 
✔ **Multi-Query RAG Optimization** for better response retrieval.  
✔ **Fast and Interactive UI** built with **Streamlit**.  
✔ **Accurate responses** powered by **LangChain** and **ChromaDB**.  


## Tech Stack
- Backend: Python, LangChain
- Vectorstore: Chromadb
- Frontend: Streamlit
- AI Model: OpenAI


## Getting Started
Follow the steps below to install dependencies and run the chatbot.

### Prerequisites
Make sure you have the following installed on your system:
- Python 3.x
- Pip (Python package manager)
- Git (optional, for version control)

### Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/nishthapant/adv-rag-bot
   cd adv-rag-bot
   ```

2. Create and activate a virtual environment
    Create venv
   ```bash
    python3 -m venv venv
    ```

    Activate venv

    ```bash
    source venv/bin/activate
    ```

3. Install dependencies:
   Run the following command to install all necessary dependencies:  
   ```bash
   python3 install.py
   ```

### Run the chatbot
After installing dependencies, start the chatbot by running:
    ```bash
    streamlit run app.py
    ```
The chatbot will run on ```bash 
localhost:8501```

### How to use?
1. When the browser window opens, you are asked to upload a pdf file.
2. Once you have uploaded a file, you can use the text input field at the bottom to ask questions to the chatbot about the content of the file uploaded.
3. Some use cases for this AI Study Buddy:
    -  you can upload a research paper, and ask the chatbot to summarize it, give you a list of three main ideas covered in the paper, etc.
    - You can upload your textbook or paper and ask this chatbot to guide you as you you do your homework.
    - More use cases TBD.
