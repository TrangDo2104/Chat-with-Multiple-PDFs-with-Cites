import streamlit as st
from auth import login_user, register_user
from pdf_utils import get_pdf_text, get_text_chunks
from chat_utils import get_vectorstore, get_retrieval_qa, handle_userinput, handle_direct_query
from ui_utils import apply_custom_styles, display_chat_history
from db import create_users_table
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings

def main():
    """Main function to run the Streamlit application.

    Initializes the application by loading environment variables, setting up the page configuration,
    applying custom CSS styles, and ensuring the necessary database tables exist. It then manages
    user authentication, presenting login and registration options if the user is not authenticated.
    Once authenticated, it sets up the application's state for handling conversations and direct queries,
    enabling users to upload PDFs and query their contents through a conversational interface.
    """
    load_dotenv() # Load environment variables from .env file
    st.set_page_config(page_title="Conversational Interface for PDFs") # Configure page settings
    apply_custom_styles()  # Apply custom CSS styles

    create_users_table()  # Ensure the users table exists

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "is_premium" not in st.session_state:
        st.session_state["is_premium"] = False

    if not st.session_state["authenticated"]:
        login_user()  # Show login form
        register_user()  # Show registration form below the login form
    else:
        # Your existing app logic here, users see this after logging in
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "user_input" not in st.session_state:
            st.session_state.user_input = ''

        st.header("📚 Explore Your Library: Start a Conversation with Your PDFs")

        with st.sidebar:
            st.subheader("Your documents")
            pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True, on_change=handle_userinput)
            if st.button("Process"):
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.retrieval_qa = get_retrieval_qa(vectorstore, embeddings=OpenAIEmbeddings)

        display_chat_history()

        # Direct query input and processing
        st.text_input("🔍 Dive into Discovery: What Secrets Do Your Documents Hold? Ask Away!", key="direct_query", on_change=handle_direct_query)

if __name__ == '__main__':
    main()