import streamlit as st

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

def apply_custom_styles():
    """Applies custom CSS styles to the Streamlit application.

    This function injects CSS styles for customizing the appearance of the application's UI,
    including chat messages and other components.
    """
    ss = '''
    <style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; align-items: center;
    }
    .chat-message.user {
        background-color: #2b313e; justify-content: right; flex-direction: row-reverse;
    }
    .chat-message.bot {
        background-color: #475063; justify-content: left;
    }
    .chat-message .avatar img {
      width: 78px; height: 78px; border-radius: 50%; object-fit: cover;
    }
    .chat-message .message {
      padding: 0 1.5rem; color: #fff; font-size: 1rem;
    }
    </style>
    '''
    st.markdown(ss, unsafe_allow_html=True)


def display_chat_history():
    """Displays the chat history in the Streamlit application.

    Parameters:
    - chat_history (list): A list of chat messages to be displayed.

    Each message in the chat history is displayed according to its sender,
    with different styling for user and bot messages.
    """
    for message in st.session_state.chat_history:
        if message["sender"] == "user":
            st.markdown(user_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
        else:  # Bot messages
            # Display bot's response
            if "source_documents" in message:  # Check if there are source documents in the message
                # Display the bot's answer
                st.markdown(bot_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
                
                # Display a header for source documents if available
                if message["source_documents"]:
                    # Use an expander to hide the detailed reference texts
                    with st.expander("Click here to view the reference texts"):
                        st.markdown("**Top relevant reference texts from your uploaded documents:**")
                        for doc in message["source_documents"]:
                            # Extract the page content and metadata from each document
                            source_text = doc.page_content
                            
                            # Prepare the display string with source and page information
                            source_display = f"**Reference text**:\n\n{source_text}..."
                            
                            # Display the source document snippet
                            st.markdown(source_display, unsafe_allow_html=True)
            else:
                # If there are no source documents, just display the bot's message
                st.markdown(bot_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)