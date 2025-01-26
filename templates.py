MULTI_QUERY_PROMPT = """You are an AI assistant. Your objective is to create four distinct 
variations of the provided user question in order to retrieve relevant documents from a vector database.
Your aim is to help the user overcome some of the limitations of similarity search algorithms by generating
4 different perspectives of the given user question. Present these alternative questions separated by a newline. 
Original question: {question} """

BASIC_RAG_TEMPLATE = """You are a helpful AI assitant. Answer the following question based on this context only:
{context}
Question: {question}
Answer:
"""