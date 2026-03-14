import streamlit as st
from login import login, logout
from uploads import upload_page as upload_documents
from chatbot import ask_question


# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# LOGIN PAGE
if not st.session_state.logged_in:
    login()
    st.stop()


# SIDEBAR
st.sidebar.title("Mitra AI")

page = st.sidebar.radio(
    "Navigation",
    ["Chatbot", "Upload Documents", "Logout"]
)


# CHATBOT PAGE
if page == "Chatbot":

    st.title("Chatbot")

    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input("Ask a question about the uploaded documents")

    if prompt:

        # Show user message
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Get chatbot response
        response = ask_question(prompt)

        # Show bot response
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })


# UPLOAD PAGE
elif page == "Upload Documents":

    st.title("Upload Documents")

    upload_documents()


# LOGOUT
elif page == "Logout":

    logout()
    st.rerun()