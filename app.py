from multi_query_rag import implement_rag
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from helpers import format_docs
import tempfile


from dotenv import load_dotenv
load_dotenv()

import os
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


def load_docs(file):
    try:
        if file is not None:
            # temporarily store the file on the disk
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file.read())
                tmp_file_path = tmp_file.name

                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
                docs_formatted = format_docs(docs)

                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                
                st.success("File uploaded successfully.")
                return docs_formatted

    except FileNotFoundError:
        st.error(f"File not found.")
    except OSError as e:
        st.error(f"OS error occurred while handling the file: {e}")
    except PermissionError:
        st.error(f"Permission error: Cannot access the file.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


def split_docs(docs):
    #  split documents
    try:
        if docs is not None:

            splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=100,
                chunk_overlap=20,
                is_separator_regex=False,
            )
            return splitter.create_documents([docs])
        else:
            return None
    except:
        print("Splitting error encountered")
        return None


def process_file(file):
    loaded_docs = load_docs(file)
    processed_docs = split_docs(loaded_docs)
    return processed_docs


def app():

    st.title("AI Study Assistant")

    WELCOME_MESSAGE = "Welcome. I am your helpful AI Study Buddy! You can upload a file in the sidebar and then proceed to ask me any questions about the text. I will help you find answers to any queries you have."
    DOC_PROCESSED_MESSAGE = "I have read the document you uploaded. You can now ask me questions based on the text."


    # initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]


    # display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    # document upload widget
    is_doc_processed = False
    with st.sidebar:
        st .write("Please upload your file here.")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        try:
            if uploaded_file is not None:
                docs = process_file(uploaded_file)
                is_doc_processed = True
        except:
            st.error("Error in processing file. Please try again.")

    
    if is_doc_processed:
        if "doc_message" not in st.session_state:
            st.chat_message("assistant").write(DOC_PROCESSED_MESSAGE)
            st.session_state.messages.append({"role": "assistant", "content": DOC_PROCESSED_MESSAGE})
            st.session_state.doc_message = True
    

        if prompt := st.chat_input("How can I help you?"):
            st.session_state.messages.append({"role": "user", "content": prompt})

            # add the prompt to chat history
            with st.chat_message("user"):
                st.write(prompt)

            # invoke the AI model
            with st.chat_message("assistant"):
                generator = implement_rag(prompt, docs)
                st.write_stream(generator)

            # add the response to chat history
            response = "".join(generator)
            st.session_state.messages.append({"role": "assistant", "content": response })


if __name__ == "__main__":
    app()

