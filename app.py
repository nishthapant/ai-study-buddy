from multi_query_rag import implement_rag
import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from helpers import format_docs
import tempfile
import chromadb

from dotenv import load_dotenv
load_dotenv()

import os
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


# read and load uploaded file
def load_docs(file):
    try:
        if file is not None:
            # temporarily store the file on the disk
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_file_path = tmp_file.name

                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
                docs_formatted = format_docs(docs)

                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                
                return docs_formatted

    except FileNotFoundError:
        st.error(f"File not found.")
    except OSError as e:
        st.error(f"OS error occurred while handling the file: {e}")
    except PermissionError:
        st.error(f"Permission error: Cannot access the file.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


# split documents for embedding
def split_docs(docs):
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
    except Exception as e:
        st.error(f"SPLITTING - Error in splitting file: {e}")


# load and split data in uploaded file
def process_file(file):
    try:
        loaded_docs = load_docs(file)
        processed_docs = split_docs(loaded_docs)
        return processed_docs

    except Exception as e:
        st.error(f"PROCESSING - Error in processing file: {e}")
        return None


# populate vector store of docs
def populate_vectorstore(docs):
    if docs is None:
        st.error("No valid text extracted from the document. Please try another file.")
        return
    try:
        # if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
        
        # if "processed_file" not in st.session_state:
        st.session_state.processed_file = False

        # delete the vector store
        chroma_db_path = "./chroma_db"

        client = chromadb.PersistentClient(path=chroma_db_path)

        # List all collections
        collection_names = client.list_collections()

        if collection_names:
            for name in collection_names:
                print(f"Deleting collection: {name}")
                client.delete_collection(name)


        # Optional: Now create a new collection to reset the state
        client.get_or_create_collection(name="default_collection")
        print("✅ Created a fresh default collection.")
        
        if not os.path.exists(chroma_db_path):
            raise Exception(f"ChromaDB directory {chroma_db_path} was not created successfully.")
        
        # create a new vector store:
        print("Initializing ChromaDBs")
        st.session_state.vectorstore = Chroma.from_documents(
            documents=docs, 
            embedding=OpenAIEmbeddings(), 
            persist_directory=chroma_db_path
        )
        st.success("New document read successfully.")

    except Exception as e:
        st.error(f"POPULATING VECTOR STORE - Error in populating vectorstore: {e}")


def app():

    st.title("AI Study Assistant")

    WELCOME_MESSAGE = "Welcome. I am your helpful AI Study Buddy! You can upload a file in the sidebar and then proceed to ask me any questions about the text. I will help you find answers to any queries you have."
    DOC_PROCESSED_MESSAGE = "I have read the document you uploaded. You can now ask me questions based on the text."


    # initialize
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    if "uploaded_filename" not in st.session_state:
        st.session_state.uploaded_filename = None
    if "doc_message" not in st.session_state:
            st.session_state.doc_message = False
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None


    # display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    # document upload widget
    with st.sidebar:
        st .write("Please upload a single PDF file.")

        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], accept_multiple_files=False)

        if "uploaded_filename" not in st.session_state:
            st.session_state.uploaded_filename = None
        
        if uploaded_file is None:
            st.session_state.uploaded_filename = None
            st.session_state.processed_file = False
            st.session_state.vectorstore = None
            st.warning("No file uploaded. Please upload a new document.")

        elif uploaded_file.name != st.session_state.uploaded_filename:
            try:
                st.session_state.uploaded_filename = uploaded_file.name

                # process the new file
                docs = process_file(uploaded_file)
                if docs:
                    # reset vector store when a new file is uploaded.
                    populate_vectorstore(docs)
                    st.session_state.processed_file = True

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    if st.session_state.vectorstore is not None and st.session_state.processed_file:
        if not st.session_state.doc_message:
            st.chat_message("assistant").write(DOC_PROCESSED_MESSAGE)
            st.session_state.messages.append({"role": "assistant", "content": DOC_PROCESSED_MESSAGE})
            st.session_state.doc_message = True
    
        prompt = st.chat_input("How can I help you?")

        if prompt:
            # add the prompt to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # display the user's prompt
            with st.chat_message("user"):
                st.write(prompt)

            if "vectorstore" in st.session_state and st.session_state.vectorstore is not None:
                with st.chat_message("assistant"):
                    generator = implement_rag(prompt, st.session_state.vectorstore)
                    st.write_stream(generator)

                    # add the response to chat history
                    if generator:
                        response = "".join(generator)
                    else:
                        response = "Sorry, I could not retrieve a response."
                    st.session_state.messages.append({"role": "assistant", "content": response })

if __name__ == "__main__":
    app()

