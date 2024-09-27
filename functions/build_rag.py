from uuid import uuid4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS

from functions.generate_random_string import generate_random_string
from functions.get_embeddings import get_embeddings
from functions.load_config import load_config
from globals import Globals

def build_rag(transcript):
    """
    Construye RAG del texto y guarda en variables globales en memoria.
    Solo podemos procesar un solo video a la vez
    """
    config = load_config()
    globals = Globals()

    # split it into chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["ragChunkSize"], chunk_overlap=0
    )
    splitted_text = text_splitter.split_text(transcript)
    embeddings = get_embeddings()

    # Config if create tags or not, build metadatas with [] if not
    uuids = [str(uuid4()) for _ in range(len(splitted_text))]

    metadatas = []  # Initialize an empty list for metadata
    for chunk, uuid in zip(splitted_text, uuids):
        metadata = {"id": uuid}
        metadatas.append(metadata)

    globals.chat_id = generate_random_string(10)

    # Prepara los retriever para Hybrid-Search
    # Metadata tiene que ser del mismo largo que los chunks
    bm25_retriever_metadatas = [
        {"source": "BM25Retriever", **meta} for meta in metadatas
    ]  # Combine with existing metadata
    globals.bm25_retriever = BM25Retriever.from_texts(
        texts=splitted_text, metadatas=bm25_retriever_metadatas, ids=uuids
    )
    globals.bm25_retriever.k = config["ragSearchK"]

    faiss_metadatas = [{"source": "FAISS", **meta} for meta in metadatas]
    globals.faiss_vectorstore = FAISS.from_texts(
        texts=splitted_text, embedding=embeddings, metadatas=faiss_metadatas, ids=uuids
    )

