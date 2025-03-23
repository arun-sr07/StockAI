import streamlit as st
import pandas as pd
import time
import base64
import os
from vectors import EmbeddingsManager
from chatbot import ChatbotManager

# Function to display PDFs
def displayPDF(file):
    base64_pdf = base64.b64encode(file.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to display CSV files
def displayCSV(file):
    df = pd.read_csv(file)
    st.dataframe(df)  # Show CSV content in table format

# Initialize session state
if 'chatbot_manager' not in st.session_state:
    st.session_state['chatbot_manager'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Sidebar

st.sidebar.markdown("### 📚 StockChat AI")
menu = ["🏠 Home", "🤖 Chatbot"]
choice = st.sidebar.selectbox("Navigate", menu)

# Home Page
if choice == "🏠 Home":
    st.title("📄 StockChat AI")
    st.markdown("Supports both **PDF and CSV** files! 🚀")

# Chatbot Page
elif choice == "🤖 Chatbot":
    st.title("🤖 Chatbot Interface")
    #col1, col2 = st.columns(2)


    col1, col2, col3 = st.columns(3)

    # Column 1: File Uploader
    with col1:
        st.header("📂 Upload Document")
        uploaded_file = st.file_uploader("Upload a PDF or CSV", type=["pdf", "csv"])

        if uploaded_file is not None:
            st.success(f"📄 File '{uploaded_file.name}' Uploaded Successfully!")

            file_type = uploaded_file.type
            st.session_state['file_type'] = file_type

            if file_type == "application/pdf":
                st.markdown("### 📖 PDF Preview")
                displayPDF(uploaded_file)
                temp_path = "temp.pdf"
            elif file_type == "text/csv":
                st.markdown("### 📊 CSV Preview")
                displayCSV(uploaded_file)
                temp_path = "temp.csv"

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state['temp_file_path'] = temp_path

    # Column 2: Create Embeddings
    with col2:
        st.header(" Create Embeddings")
        create_embeddings = st.checkbox("✅ Generate Embeddings")

        if create_embeddings:
            if st.session_state['temp_file_path'] is None:
                st.warning("⚠️ Please upload a document first.")
            else:
                try:
                    embeddings_manager = EmbeddingsManager()

                    with st.spinner("🔄 Creating Embeddings..."):
                        result = embeddings_manager.create_embeddings(st.session_state['temp_file_path'])
                        time.sleep(1)
                    st.success(result)

                    # Initialize ChatbotManager
                    if st.session_state['chatbot_manager'] is None:
                        st.session_state['chatbot_manager'] = ChatbotManager()

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Column 3: Chatbot Interface
    with col3:
        st.header("💬 Chat with Document")

        if st.session_state['chatbot_manager'] is None:
            st.info("🤖 Upload a file and generate embeddings to chat.")
        else:
            for msg in st.session_state['messages']:
                st.chat_message(msg['role']).markdown(msg['content'])

            if user_input := st.chat_input("Type your message..."):
                st.chat_message("user").markdown(user_input)
                st.session_state['messages'].append({"role": "user", "content": user_input})

                with st.spinner("🤖 Responding..."):
                    try:
                        answer = st.session_state['chatbot_manager'].get_response(user_input)
                        time.sleep(1)
                    except Exception as e:
                        answer = f"⚠️ Error: {e}"

                st.chat_message("assistant").markdown(answer)
                st.session_state['messages'].append({"role": "assistant", "content": answer})
