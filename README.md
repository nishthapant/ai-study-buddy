# **AI Study Buddy**

## Project Description
This is an intelligent chatbot that allows users to upload a **PDF document** and ask questions about its content. This can be useful for studying, research, or summarizing key points from documents, emails, textbooks, etc.

The chatbot optimizes response retrieval using the **Multi-Query RAG strategy**, ensuring more relevant and accurate answers.  


This is an AI-powered study assistant that helps users extract insights from uploaded PDF documents using Retrieval-Augmented Generation (RAG). The assistant enables users to upload educational materials, research papers, or notes and then interact with a chatbot to ask context-aware questions about the content.

## Key features:
- **Document Understanding** – Users can upload PDFs, which are processed and converted into structured embeddings for easy retrieval.
- **Efficient Information Retrieval** – The system uses Multi-Query RAG Optimization for better response retrieval.
- **Conversational AI** – A chatbot interface built with Streamlit allows seamless Q&A interactions with the document’s content.
- **Dynamic Vector Store Management** – Implements real-time vector store updates, ensuring context-specific answers without old data interference.


## Tech Stack
- Backend: Python, LangChain
- Vectorstore: ChromaDB
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

3. Create environment variables
	- Open your project folder.
	- Create a new file and name it .env (without any extension).
	- Add the following key-value pairs inside the file like this:
        ```
        LANGSMITH_ENDPOINT="<your-langsmith-endpoint>"
        LANGSMITH_API_KEY="<your-langsmith-api-key>"
        OPENAI_API_KEY="<your-openai-api-key>"
        LANGSMITH_PROJECT="<project-name>"
        ```
        For a more detailed explanation visit [this page](https://docs.smith.langchain.com/observability).
    - Add ".env" to your ```
    .gitignore ``` file.
    
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
The chatbot will run on ```
localhost:8501 ```

### How to use?
1. When the browser window opens, you are asked to upload a pdf file.
2. Once you have uploaded a file, you can use the text input field at the bottom to ask questions to the chatbot about the content of the file uploaded.

## Use Cases:
This AI Study Assistant bridges the gap between unstructured documents and actionable insights, making it an essential tool for education, corporate learning, research, and productivity. Its scalable, adaptable architecture makes it a valuable project for AI, NLP, and software engineering roles.

Here are some key use cases:

### **Education and Learning**
- **Personalized Study Assistant**: Students can upload textbooks, research papers, or notes and ask questions to quickly understand complex concepts.
- **Exam Preparation**: Helps students summarize and review study materials efficiently, reducing time spent searching for information.
- **Tutoring Support**: Acts as an AI tutor for learners who need explanations or insights from specific learning materials.

### **Corporate and Workplace Learning**
- **Employee Training & Onboarding**: Employees can upload company handbooks or training materials and get instant answers to work-related queries.
- **Compliance & Policy Assistance**: Businesses can use it to help employees navigate company policies, HR guidelines, or legal compliance documents.

### **Legal Research**
- **Legal Document Analysis**: Lawyers and legal researchers can quickly extract relevant information from contracts, case laws, and regulatory documents.
- **Academic Research**: Researchers can upload scientific papers or reports and use the assistant to summarize findings and identify key points.

### **Business and Productivity**
- **Meeting & Report Summarization**: Professionals can upload long business reports or meeting transcripts and extract key takeaways instantly.
- **Customer Support Knowledge Base**: Companies can integrate the assistant with FAQs or support documentation to help customers and employees get relevant information quickly.

### **Developer and AI Applications**
- **AI Chatbot for Document-Based Queries**: Can be adapted as a chatbot in enterprise solutions where employees or users need to retrieve information from large document repositories.
- **RAG-Powered Search for Websites** : The system can be used as an intelligent document retrieval tool for company portals or knowledge bases.


## Potential Improvements & Future Enhancements
1. ### **Multi-format Support**
    Extend support beyond PDFs to Word documents (.docx), PowerPoint (.pptx), plain text files, media like websites and images of scanned documents, etc.

2. ### **Scalability & Deployment**
    **Cloud Integration**
    Deploy the app on AWS, GCP, or Azure for better sc lability and performance.

3. ### **UI/UX & User Engagement**
    **Voice Input & Text-to-Speech**
    Allow users to speak their questions and hear AI-generated responses
    **Mobile-Friendly Design**
    Optimize the Streamlit UI for mobile users, making it more accessible.

4. ### **Multi-Agent Collaboration**
    **Auto-Generated Flashcards & Notes**
    Create AI-generated flashcards from uploaded documents to help with study sessions.


## Acknowledgements
1. [Streamlit]()
2. [ChromaDB]()
3. [ChatOpenAI](https://python.langchain.com/docs/integrations/chat/openai/)
4. [Langchain](https://python.langchain.com/docs/tutorials/llm_chain/)
5. [Langsmith](https://docs.smith.langchain.com/)
5. [Multi Query - Query Transformation](https://community.fullstackretrieval.com/query-transformation/multi-query)
