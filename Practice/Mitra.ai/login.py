import streamlit as st
from database import validate_user


def login():

    st.title("Mitra AI Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = validate_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid username or password")


def logout():

    st.session_state.clear()