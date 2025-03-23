# 📄 StockAI



Stock market analysis requires both fundamental insights (company reports, financial statements) and technical data (historical prices, trends). Manually analyzing these datasets is complex and time-consuming. This project leverages LLM and RAG techniques to build an intelligent chatbot that assists investors by retrieving relevant stock information and generating insightful responses in real-time.

## 🛠️ Features

- **📂 Upload Documents**: Easily upload and preview your PDF documents within the app.
- **🧠 Create Embeddings**: Generate embeddings for your documents to enable efficient search and retrieval.
- **🤖 Chatbot Interface**: Interact with your documents using a smart chatbot that leverages the created embeddings.
- **🌟 User-Friendly Interface**: Enjoy a sleek and intuitive UI with emojis and responsive design for enhanced user experience.

## 🖥️ Tech Stack

The Document Buddy App leverages a combination of cutting-edge technologies to deliver a seamless and efficient user experience. Here's a breakdown of the technologies and tools used:

- **[LangChain](https://langchain.readthedocs.io/)**: Utilized as the orchestration framework to manage the flow between different components, including embeddings creation, vector storage, and chatbot interactions.
  
- **[Unstructured](https://github.com/Unstructured-IO/unstructured)**: Employed for robust PDF processing, enabling the extraction and preprocessing of text from uploaded PDF documents.
  
- **[BGE Embeddings from HuggingFace](https://huggingface.co/BAAI/bge-small-en)**: Used to generate high-quality embeddings for the processed documents, facilitating effective semantic search and retrieval.
  
- **[Qdrant](https://qdrant.tech/)**: A vector database running locally via Docker, responsible for storing and managing the generated embeddings for fast and scalable retrieval.
  
  
- **[Streamlit](https://streamlit.io/)**: The core framework for building the interactive web application, offering an intuitive interface for users to upload documents, create embeddings, and interact with the chatbot.

## 📁 Directory Structure

document_buddy_app/
```
│── logo.png
├── new.py
├── vectors.py
├── chatbot.py
├── requirements.txt
```


CONCLUSION 
Key Takeaways

✅ Automated Stock Analysis – The chatbot processes fundamental (PDFs) and technical (CSV) data for real-time insights.

✅ AI-Powered Decision Making – Uses LLM and RAG to analyze and predict stock trends effectively.

✅ Multi-Query Support – Handles multiple user questions simultaneously for better interaction.

✅ Seamless Integration – Built with LangChain, Streamlit, and Qdrant for efficient data retrieval.

✅ User-Friendly Interface – Allows easy PDF & CSV uploads and provides quick stock insights.

✅ Reduces Manual Effort – Automates stock research, saving time for investors and analysts.

✅ Enhanced Accuracy – Combines historical stock data + financial reports for well-rounded predictions.

