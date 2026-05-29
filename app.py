import streamlit as st
from groq import Groq

st.set_page_config(page_title="My AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 My AI Chatbot")
st.caption("Powered by Groq · Bring Your Own API Key")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Your Groq API Key", type="password", placeholder="gsk_...", help="Get your key at console.groq.com")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("Get your API key at [console.groq.com](https://console.groq.com)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    if not api_key:
        st.warning("⚠️ Please enter your Groq API key in the sidebar first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    max_tokens=1024,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                if "invalid_api_key" in str(e).lower() or "401" in str(e):
                    st.error("❌ Invalid API key. Please check and try again.")
                elif "rate_limit" in str(e).lower():
                    st.error("⏳ Rate limit hit. Wait a moment and retry.")
                else:
                    st.error(f"Something went wrong: {e}")
