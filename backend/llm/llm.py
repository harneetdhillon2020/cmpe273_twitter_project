from langchain_chroma import Chroma
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import Document
import os
from pymongo import MongoClient
from fastapi import FastAPI

from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings
from dataclasses import dataclass
import uvicorn

app = FastAPI()

MONGO_CONNECTION_STR = os.environ['MONGO_CONNECTION_STR']

llm = ChatCohere(model="command-r-plus")

@dataclass
class Question:
    question: str

def retrieve_tweets():
    ret = []

    try:
        client = MongoClient(MONGO_CONNECTION_STR)
        db = client.twitter_db
        collection = db.tweets
        
        tweets = collection.find()

        for tweet in tweets:
            print(tweet.get('text'))
            ret.append(Document(page_content=tweet.get('text')))

    except Exception as e:
        print(f"Error retrieving data from MongoDB: {e}")

    return ret

@app.post("/ask")
def get_resp(question: Question):
    documents = retrieve_tweets()

    VECTORSTORE = Chroma.from_documents(documents=documents, embedding=CohereEmbeddings(model="embed-english-v3.0"))

    retriever = VECTORSTORE.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question.question)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)