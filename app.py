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
            st.success("File uploaded successfully.")

            # temporarily store the file on the disk
            with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp_file:
                tmp_file.write(file.read())
                tmp_file_path = tmp_file.name

            # load documents
            try:
                loader = PyPDFLoader(file)
                docs = loader.load()
                docs_formatted = format_docs(docs)
                return docs_formatted
            except:
                print("Loading error encountered")
                return None
    
    except FileNotFoundError:
        st.error(f"File not found: {tmp_file_path}")
    except OSError as e:
        st.error(f"OS error occurred while handling the file: {e}")
    except PermissionError:
        st.error(f"Permission error: Cannot access the file at {tmp_file_path}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    finally:
        # delete temp file if has not been deleted
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
            st.write("Temporary file has been deleted.")



def split_docs(docs):
    #  split documents
    if docs is not None:
        try:
            splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=100,
                chunk_overlap=20,
                is_separator_regex=False,
            )

            return splitter.create_documents([docs])
        except:
            print("Splitting error encountered")
            return None
    else:
            st.write("Documents incorrectly loaded. Cannot proceed. Please try again.")


def process_docs_data(file):
    loaded_docs = load_docs(file)
    processed_docs = split_docs(loaded_docs)
    return processed_docs


def app():
    # ask user to upload doc
    file = input("Bot: Upload your document here.\n")

    # load and split documents
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    docs = process_docs_data(uploaded_file)

    # take query
    # TO DO!
    question = input("Bot: Enter your query below.\nYou: ")

    # invoke rag app
    response = implement_rag(question, docs)
    print(response)


if __name__ == "__main__":
    app()

