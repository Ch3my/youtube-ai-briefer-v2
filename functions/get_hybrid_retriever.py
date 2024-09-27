from globals import Globals
from functions.load_config import load_config
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers import EnsembleRetriever

def get_hybrid_retriever():
    config = load_config()
    globals = Globals()

    # score_threshold 1 = more relavant documents
    faiss_retriever = globals.faiss_vectorstore.as_retriever(
        search_type=config["ragSearchType"],
        search_kwargs={"k": config["ragSearchK"]},
    )
    ensemble_retriever = EnsembleRetriever(
        retrievers=[globals.bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
    )
    compressor = FlashrankRerank(top_n=config["ragSearchK"])
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=ensemble_retriever
    )
    return compression_retriever