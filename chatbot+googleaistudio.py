
import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(
    page_title="GLEARN AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 GLEARN AI Chatbot")
st.caption("Powered by Gemini API")

SYSTEM_PROMPT = """
You are a helpful AI assistant for GLEARN.
Explain Python, AI, Machine Learning and Generative AI
clearly for students. Use examples when helpful.
"""

MODEL = "gemini-3.8-flash"

# Read the API key from Streamlit secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me about Python or AI...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini uses "model" for assistant replies
    history = []
    for message in st.session_state.messages:
        history.append({
            "role": (
                "model"
                if message["role"] == "assistant"
                else "user"
            ),
            "parts": [{"text": message["content"]}]
        })

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # response = client.models.generate_content(
                #     model=MODEL,
                #     contents=history,
                #     config=types.GenerateContentConfig(
                #         system_instruction=SYSTEM_PROMPT
                #     )
                # )
                response = None

                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model=MODEL,
                            contents=history,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT
                            )
                        )
                        break

                    except Exception as error:
                        error_text = str(error)

                        if "503" in error_text and attempt < 2:
                            time.sleep(2 ** (attempt + 1))
                        else:
                            raise

                answer = response.text or "I couldn't generate a response."


                answer = response.text or "I couldn't generate a response."
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(
                    "The AI request failed. Check your API key, "
                    "model availability and API quota."
                )
                st.caption(str(error))
