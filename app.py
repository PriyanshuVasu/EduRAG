import streamlit as st
import uuid
from database import init_db, add_message_to_history, get_user_history
from rag_handler import rag_chain


st.set_page_config(page_title=" EduRAG Tutor", page_icon="🎓")
st.title("🎓 EduRAG Tutor")

init_db()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Display a login form if the user is not identified
if st.session_state.user_id is None:
    st.info("Welcome! Please enter a username to start or resume your session.")
    username = st.text_input("Username")
    if st.button("Start Chatting"):
        if username:
            st.session_state.user_id = username
            # Initialize a new session_id for this login
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
        else:
            st.warning("Please enter a username.")
else:
    st.info(f"Logged in as: **{st.session_state.user_id}**")

    # Load and display chat history for the identified user
    st.session_state.messages = get_user_history(st.session_state.user_id)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about your course material..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        add_message_to_history(st.session_state.user_id, st.session_state.session_id, "user", prompt)

        with st.spinner("Thinking..."):
            response = rag_chain.invoke({
                "question": prompt,
                "user_id": st.session_state.user_id
            })
            ai_response = response.content

        with st.chat_message("assistant"):
            st.markdown(ai_response)
        
        add_message_to_history(st.session_state.user_id, st.session_state.session_id, "assistant", ai_response)