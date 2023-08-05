## To delete all older migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

## To create migrations for models [run the following from root directory]
> python manage.py makemigrations api


# Generate translations
> for web app
python manage.py makemessages -l en -i "web/*" -e html,py,js,txt
python manage.py compilemessages

> for both apps
python manage.py makemessages -l en -i "web/*" -i "api/*" -e html,py,js,txt
python manage.py compilemessages



## Langchain References
https://github.com/easonlai/azure_openai_langchain_sample/blob/main/chat_with_pdf.ipynb


## Also here
https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/qdrant/QA_with_Langchain_Qdrant_and_OpenAI.ipynb


---
Make Chain [using conversation retrieval chain]
---
```py
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
# Import Azure OpenAI
from langchain.llms import AzureOpenAI
from langchain.vectorstores.base import VectorStore

from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import SystemMessagePromptTemplate
from langchain.memory import VectorStoreRetrieverMemory

load_dotenv()
import os

def make_chain(vector_store: VectorStore, mode: str, initial_prompt: str) -> ConversationalRetrievalChain:
    # https://github.com/easonlai/azure_openai_langchain_sample/blob/main/chat_with_pdf.ipynb
    llm = AzureOpenAI(
        openai_api_key=os.environ['OPENAI_API_KEY'], 
        deployment_name=os.environ['OPENAI_DEPLOYMENT_NAME'], 
        model_name=os.environ['OPENAI_COMPLETION_MODEL']
    )

    memory = VectorStoreRetrieverMemory(retriever=vector_store.as_retriever(), memory_key="chat_history", return_docs=False, return_messages=True)

    qachat = ConversationalRetrievalChain.from_llm(llm, retriever=vector_store.as_retriever(), memory=memory, return_source_documents=True, get_chat_history=lambda h : h)

    # MEMORY 👇
    chat_history = []

    ## Question 1
    query = "Hi there, how are you?"
    result = qachat({"question": query, "chat_history": chat_history})
    print(result['answer'])
    
    
    return qachat


```

---
Better Question answering
https://python.langchain.com/docs/use_cases/question_answering/how_to/chat_vector_db


---
Using Retreival QA Chain


https://python.langchain.com/docs/use_cases/question_answering/how_to/chat_vector_db


Another chain
---
def make_chain(vector_store: VectorStore, mode, initial_prompt: str) -> ConversationalRetrievalChain:
    # https://github.com/easonlai/azure_openai_langchain_sample/blob/main/chat_with_pdf.ipynb
    llm = AzureOpenAI(
        openai_api_key=os.environ['OPENAI_API_KEY'], 
        deployment_name=os.environ['OPENAI_DEPLOYMENT_NAME'], 
        model_name=os.environ['OPENAI_COMPLETION_MODEL'],
        max_tokens=1000,
        n=1,
        temperature=0,
    )

    # use it if you want to maintain the state in the backend.
    # memory = VectorStoreRetrieverMemory(retriever=vector_store.as_retriever(), memory_key="chat_history", return_docs=False, return_messages=True)

    prompts = get_prompt_by_mode(mode=mode, initial_prompt=initial_prompt)
    
    condense_question_prompt = prompts.get(UserAgent.CONDENSE_PROMPT)
    qa_prompt = """You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
If the question is not related to the context, politely respond that you are teached to only answer questions that are related to the context.
If you don't know the answer, just say you don't know. DO NOT try to make up an answer. Keep answers as concise as possible

{context}

Question: {question}
Answer in markdown format:"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=qa_prompt,
    )

    condense_question_prompt = PromptTemplate(template = condense_question_prompt, input_variables=["question", "chat_history"])

    question_generator = LLMChain(llm=llm, prompt=condense_question_prompt)
    doc_chain = load_qa_chain(llm, chain_type="stuff")

    chain = ConversationalRetrievalChain(
        retriever=vector_store.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
    )


    return chain


---
Conversational retriever chain with qa_prompts
https://github.com/langchain-ai/langchain/issues/5542



---
To run celery app: 
There are fork issues with mac m1, a complete thread can be found here
> https://github.com/rails/rails/issues/38560

To start: 
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES && export DISABLE_SPRING=true && celery -A dj_backend_server worker --loglevel=info



---
https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/document-qa/question_answering_large_documents_langchain.ipynb



---

Up Next
--
Integrating mysql instead of sqlite, and provide configuration in env files or some other config file