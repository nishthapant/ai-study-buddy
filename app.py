from multi_query_rag import implement_rag
from helpers import process_docs_data

def app():
    # take path of doc to use
    file = input("Bot: Enter the path of the document you wish to use.\nYou: ")

    # load and split documents
    docs = process_docs_data(file)

    #  take query
    question = input("Bot: Enter your query below.\nYou: ")

    #  invoke rag app
    response = implement_rag(question, docs)
    print(response)


if __name__ == "__main__":
    app()

