import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"
API_KEY = "my-secret-key"

st.set_page_config(page_title="AI Assistant", layout="wide")

st.title("🤖 Agentic AI Assistant")

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

# -----------------------------
# Display Chat History
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input("Ask something...")

if user_input:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -----------------------------
    # Call API
    # -----------------------------

    headers = {
        "x-api-key": API_KEY
    }

    payload = {
        "message": user_input,
        "session_id": st.session_state.session_id
    }

    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        full_response = ""

        try:
            with requests.post(API_URL, json=payload, headers=headers, stream=True) as r:

                if r.status_code == 200:

                    for chunk in r.iter_content(chunk_size=20):

                        if chunk:
                            text = chunk.decode("utf-8")
                            full_response += text
                            response_placeholder.markdown(full_response)

                else:
                    full_response = "⚠️ API Error"

        except Exception:
            full_response = "⚠️ Connection error"

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })

        