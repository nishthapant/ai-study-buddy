from dotenv import load_dotenv
load_dotenv()

import os
os.environ['LANGSMITH_ENDPOINT'] = os.getenv('LANGSMITH_ENDPOINT')
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_PROJECT'] = os.getenv('LANGSMITH_PROJECT')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.load import loads, dumps
from langchain.schema import Document


# format generated queries
def get_queries(queries):
    return queries.split('\n')


# Convert list of documents to a single string
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


# use serialization/deserialization to get a unique union
def get_unique_union(retrieved_docs):
    # serialize the docs
    serialized_docs = []
    for doc_list in retrieved_docs:
        for doc in doc_list:
            serialized_docs.append(dumps(doc))

    # convert the list to a set to remove non distinct documents
    unique_serialized_docs = list(set(serialized_docs))

    # deserialize the documents
    unique_union = []
    for doc in unique_serialized_docs:
        unique_union.append(loads(doc))

    return unique_union


