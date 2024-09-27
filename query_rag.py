import json
from globals import Globals
from functions.load_config import load_config
from functions.get_hybrid_retriever import get_hybrid_retriever
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from functions.send_message import send_message

globals = Globals()


async def query_rag(query):
    config = load_config()
    retriever = get_hybrid_retriever()
    rag_llm = None

    try:
        if "claude" in config["ragModel"]:
            rag_llm = ChatAnthropic(model=config["ragModel"], max_tokens=2048)
        if "gpt" in config["ragModel"]:
            rag_llm = ChatOpenAI(model=config["ragModel"])
    except Exception as e:
        print("Error al configurar los modelos, quiza falta una API_KEY")
        print(e)
        return

    # Basado en https://python.langchain.com/v0.2/docs/how_to/qa_chat_history_how_to/#prompt
    contextualize_q_system_prompt = "Tu tarea es exclusivamente reformular la siguiente pregunta para que sea entendida sin contexto adicional. Bajo ninguna circunstancia debes proporcionar una respuesta o explicación. Si la pregunta ya es clara y no necesita reformulación, devuélvela tal como está. Solo realiza la reformulación, sin añadir contenido extra."

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        rag_llm, retriever, contextualize_q_prompt
    )

    system_prompt = (
        "Responde a la pregunta basándote únicamente en el siguiente contexto y extrae una respuesta significativa."
        "Por favor, escribe en oraciones completas con la ortografía y puntuación correctas. Si tiene sentido, usa listas."
        "Si el contexto no contiene la respuesta, simplemente responde que no puedes encontrar una respuesta."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # Esto es algo que viene en langchain: https://python.langchain.com/v0.2/docs/tutorials/rag/#built-in-chains
    # pero funciona bien, no tenemos que crear a mano una chain (creo)
    question_answer_chain = create_stuff_documents_chain(rag_llm, prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    response = conversational_rag_chain.invoke(
        {"input": query},
        config={"configurable": {"session_id": globals.chat_id}},
    )

    context_array = []
    for doc in response["context"]:
        # Create a dictionary for each document
        doc_dict = {
            "source": doc.metadata['source'],
            "content": doc.page_content
        }
        
        # Append the dictionary to the array
        context_array.append(doc_dict)

    await send_message(
        {
            "action": "ragAnswer",
            "answer": response["answer"],
            "context": context_array 
        }
    )
    return


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in globals.store:
        globals.store[session_id] = ChatMessageHistory()
    return globals.store[session_id]
