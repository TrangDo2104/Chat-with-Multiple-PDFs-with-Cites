import streamlit as st
from db import add_user, verify_user

def login_user():
    """Handle the login process."""
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        authenticated, is_premium = verify_user(username, password)
        if authenticated:
            st.session_state["authenticated"] = True
            st.session_state["is_premium"] = is_premium
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid username or password")

def register_user():
    """Display a user registration form and handle new user registration."""
    st.sidebar.subheader("Register")
    new_username = st.sidebar.text_input("Choose a username", key="new_username")
    new_password = st.sidebar.text_input("Choose a password", type="password", key="new_password")
    confirm_password = st.sidebar.text_input("Confirm password", type="password", key="confirm_password")
    if st.sidebar.button("Register"):
        if new_password == confirm_password:
            result = add_user(new_username, new_password)
            if result:
                st.sidebar.success("You have successfully registered. You can now log in.")
            else:
                st.sidebar.error("Username already exists or registration failed.")
        else:
            st.sidebar.error("Passwords do not match.")