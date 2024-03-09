import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from apps.config import OPENAI_API_KEY

def get_vectorstore(text_chunks):
    """Creates a vector store from text chunks using embeddings.

    Parameters:
    - text_chunks (list): A list of text chunks to be embedded.

    Returns:
    - FAISS VectorStore: A vector store containing the embeddings of the text chunks.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_retrieval_qa(vectorstore, embeddings):
    """Sets up a retrieval-based QA system using the provided vector store.

    Parameters:
    - vectorstore (FAISS VectorStore): The vector store to be used for retrieval.

    Returns:
    - RetrievalQA: A retrieval-based QA system configured to use the specified vector store.
    """
    retriever = vectorstore.as_retriever()
    qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name='gpt-3.5-turbo'), chain_type="stuff", retriever=retriever, return_source_documents=True)
        
    return qa

def handle_userinput():
    """Processes user input from the Streamlit application's UI.

    This function retrieves the user's input from Streamlit's session state and checks if it is not empty.
    If there is input and a conversation object exists in the session state, it sends the user's question
    to the conversation handler. It then appends both the user's question and the bot's response to the chat
    history stored in the session state. Finally, it resets the user input field to prepare for the next query.

    The function assumes that the last message in 'chat_history' after calling the conversation handler
    contains the bot's response, which it then appends to the chat history.
    """
    user_question = st.session_state.user_input  # Retrieve user input from session state
    if user_question:  # Check if the input is not empty
        if "conversation" in st.session_state:
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history.append({"content": user_question, "sender": "user"})
            bot_response = response['chat_history'][-1].content
            st.session_state.chat_history.append({"content": bot_response, "sender": "bot"})
            st.session_state.user_input = ''  # Reset the input box after processing

def handle_direct_query():
    """Processes a direct query input from the Streamlit application's UI.

    This function is specifically designed for handling direct queries from the user.
    It retrieves the direct query from Streamlit's session state and checks if it is not empty.
    If there is a direct question and a RetrievalQA object exists in the session state, it sends
    the direct question to the RetrievalQA handler.

    After processing, it appends the user's direct question and the bot's response, including
    any source documents related to the response, to the chat history in the session state.
    The input box is then reset for the next query.

    This enables handling of queries that require specific information retrieval from
    the uploaded documents, showcasing the bot's ability to provide targeted responses.
    """
    direct_question = st.session_state.direct_query  # Retrieve direct query input from session state
    if direct_question:  # Check if the input is not empty
        # Use RetrievalQA for direct querying
        if "retrieval_qa" in st.session_state:
            # Call the RetrievalQA object with the user's query
            response = st.session_state.retrieval_qa({"query": direct_question})
            # Append the user's query to chat history
            st.session_state.chat_history.append({"content": direct_question, "sender": "user"})
            
            # Extract the 'result' and 'source_documents' from the response
            bot_response = response.get('result', 'No answer available')
            source_documents = response.get('source_documents', [])
            
            # Append the bot's response to chat history
            st.session_state.chat_history.append({"content": bot_response, "sender": "bot", "source_documents": source_documents})
            st.session_state.direct_query = ''  # Reset the input box after processing
