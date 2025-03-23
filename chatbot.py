from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import Qdrant
from langchain_ollama import ChatOllama
from qdrant_client import QdrantClient
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub

class ChatbotManager:
    def __init__(self):
        self.embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en", model_kwargs={"device": "cpu"})

        # Using Falcon-7B as LLM
        self.llm = HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct", model_kwargs={"temperature": 0.1})

        # ✅ Initialize Qdrant Client
        self.client = QdrantClient(url="http://localhost:6333")
        self.collection_name = "vector_db"

        # ✅ Load the stored vectors from Qdrant
        self.db = Qdrant(client=self.client, embeddings=self.embeddings, collection_name=self.collection_name)



        self.prompt = PromptTemplate(
            template="You are an AI assistant answering questions based on the latest uploaded document only.\n"
                   
                     "Document Context:\n{context}\n\n"
                     "User Question:\n{question}\n\n"
                     "Helpful and precise answer:",
            input_variables=["context", "question", "answer"]
        )

        """self.prompt = FewShotPromptTemplate(
             examples=examples,
            example_prompt=example_prompt,
            suffix="Use only the following document to answer:\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:",
            input_variables=["context", "question"]
        )"""

        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})
        self.qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.retriever,
                                              return_source_documents=False, chain_type_kwargs={"prompt": self.prompt})

    def get_response(self, query: str) -> str:
        try:
            return self.qa.run(query)
        except Exception as e:
            return f"⚠️ Error: {e}"
