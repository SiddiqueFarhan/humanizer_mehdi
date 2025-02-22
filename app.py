from openai import OpenAI
import streamlit as st
import os

# Replace with secure handling for API keys
model = "ft:gpt-3.5-turbo-0125:mywordsai::B3UebHU4"
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Hardcoded credentials (store securely in production)
user = "josh"
password = "fomo"

# Login system
def login():
    st.title("Login")
    username_ = st.text_input("Username")
    password_ = st.text_input("Password", type="password")
    if st.button("Login"):
        if username_ == user and password_ == password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid username or password")

# Humanization function
def humanize_text(AI_text, model):
    response = client.chat.completions.create(
        model=model,
        temperature=0.85,
        messages=[
            {
                "role": "system",
                "content": """Transform the given AI-generated text into a human-written version that feels warm, spontaneous, and full of personality. Follow these rules:
                - **Keep the Original Meaning:** Do not change the message or add new opinions.
                - **Same Length:** The output must closely match the input length.
                - **Humanize the Style:** Vary sentence lengths, use natural pauses and informal constructions, and choose a richer, more diverse vocabulary.
                - **Creative Punctuation:** Use punctuation (dashes, ellipses, exclamation marks) to convey emotion and rhythm.
                - **No Extra Content:** Only transform what is provided without adding new ideas.
                """
            },
            {
                "role": "user",
                "content": f"{AI_text}"
            }
        ]
    )
    return response.choices[0].message.content.strip()

# Main app
def main():
    st.title("AI Text Humanizer")

    AI_text = st.text_area("Enter the AI text", height=200)

    if st.button("Submit"):
        if AI_text.strip():
            human_text = humanize_text(AI_text, model)
            st.write("### Humanized Text:")
            st.write(human_text)
        else:
            st.warning("Please enter some text.")

# Authentication check
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    main()
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
