import os
import warnings
from langchain.document_loaders import UnstructuredPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models

warnings.filterwarnings("ignore")

# ✅ Set up Hugging Face API Token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")

"""class EmbeddingsManager:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
        self.collection_name = "vector_db"

    def create_embeddings(self, file_path: str):
        # ✅ Re-initialize QdrantClient inside function (avoids pickling issue)
        qdrant_client = QdrantClient(url="http://localhost:6333")

        # ✅ Ensure collection exists or delete existing one
        try:
            qdrant_client.get_collection(self.collection_name)
            qdrant_client.delete_collection(self.collection_name)  # Remove old data
        except Exception:
            pass  # Collection does not exist, so nothing to delete

        qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
        )

        file_extension = file_path.split(".")[-1]
        if file_extension == "pdf":
            loader = UnstructuredPDFLoader(file_path)
        elif file_extension == "csv":
            loader = CSVLoader(file_path)
        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)

        # ✅ Store embeddings in Qdrant
        Qdrant.from_documents(
            texts, self.embedding_model, collection_name=self.collection_name, client=qdrant_client
        )

        return "✅ Old data removed & new Vector DB Created!"""

class EmbeddingsManager:
    def __init__(
            self,
            model_name: str = "BAAI/bge-small-en",
            device: str = "cpu",
            encode_kwargs: dict = {"normalize_embeddings": True},
            qdrant_url: str = "http://localhost:6333",
            collection_name: str = "vector_db",
    ):
        """
        Initializes the EmbeddingsManager with the specified model and Qdrant settings.
        """
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )

    def create_embeddings(self, file_path: str):
        """
        Processes the PDF or CSV file, creates embeddings, and stores them in Qdrant.

        Args:
            file_path (str): The file path to the document (PDF or CSV).

        Returns:
            str: Success message upon completion.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")



        file_extension = file_path.split(".")[-1]
        if file_extension == "pdf":
            loader = UnstructuredPDFLoader(file_path)
        elif file_extension == "csv":
            loader = CSVLoader(file_path)
        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)

        # Create and store embeddings in Qdrant
        try:
            qdrant = Qdrant.from_documents(
                texts,
                self.embeddings,
                url=self.qdrant_url,
                force_recreate=True,
                prefer_grpc=False,
                collection_name=self.collection_name,
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Qdrant: {e}")

        return "✅ Vector DB Successfully Created and Stored in Qdrant!"
