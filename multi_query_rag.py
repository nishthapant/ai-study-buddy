from dotenv import load_dotenv
load_dotenv()

import os
os.environ['LANGSMITH_TRACING_V2'] = 'true'
os.environ['LANGSMITH_ENDPOINT'] = os.getenv('LANGSMITH_ENDPOINT')
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_PROJECT'] = os.getenv('LANGSMITH_PROJECT')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter
import templates
from helpers import get_queries, get_unique_union, format_docs_to_str


def implement_rag(question, docs):
    # embedding and indexing
    vectorstore = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    # prompt and model setup
    template = templates.MULTI_QUERY_PROMPT
    prompt_versions = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0.7)

    # multi query chain
    generate_multi_queries = (
        prompt_versions
        | llm
        | StrOutputParser()
        | get_queries
    )

    # define the RAG chain that leverages multi query strategy
    # returns a final list of documents to use as context
    context_chain = (
        generate_multi_queries
        | retriever.map()
        | get_unique_union
    )

    #  RAG chain to generate multiple queries and
    #  unique union of corresponding relevant docs
    context = context_chain.invoke({"question": question})
    final_context = format_docs_to_str(context)
    final_prompt = ChatPromptTemplate.from_template(templates.BASIC_RAG_TEMPLATE)

    # RAG chain to generate the result from the context generated using the prev chain
    final_rag_chain = (
        {"question":itemgetter("question"), "context": itemgetter("context")}
        | final_prompt
        | llm
        | StrOutputParser()
    )

    response = final_rag_chain.invoke({"question":question, "context":final_context})
    return response