import streamlit as st

from streamlit_chat import message
from chatbot.chatbot import Chatbot
from helpers.constants import Constants


def main():
    set_markdown()

    st.title("Chat with USJ")

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ''

    # Initialize our chatbot (Make sure training text in data/scraped_text/)
    chatbot = Chatbot(model_name=Constants.ModelName.value, index_name=Constants.PineconeIndex.value, existing_index=True)

    # Text input to ask a question
    st.markdown("Ask anything about licenses, admission, international, help, financial support, insitutions and more:")
    st.text_input(label="text_input", key="widget", on_change=submit, label_visibility="collapsed")
    
    user_question = st.session_state["user_input"]

    if user_question:
        # Query answer from bot until success
        query_answer(chatbot, user_question)
    
    if st.session_state['generated']:

        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


def query_answer(chatbot, user_question):
    # Your code block goes here
    try:
        # Clear the cache to force re-execution of st.cache functions
        st.cache_data.clear()

        # Get the bot's response
        bot_response = chatbot.answer_question(user_question)["answer"]

        st.session_state.past.append(user_question)
        st.session_state.generated.append(bot_response)

    except Exception as e:
        # Retry the code block
        query_answer(chatbot, user_question)


def submit():
    st.session_state['user_input'] = st.session_state['widget']
    st.session_state['widget'] = ''


def set_markdown():
    # Custom CSS to set the background image and other styles
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #444; /* Set the background color to dark gray (#111) */
        }}
        .stTextInput input {{
            background-color: rgba(255, 255, 255, 0.8); /* Adjust the background color and opacity */
            color: black; /* Change the text color */
            border: 1px solid #cccccc; /* Add a border to the text input */
            border-radius: 8px; /* Round the corners of the text input */
            padding: 8px 12px; /* Adjust the padding as needed */
        }}
        .stMarkdown {{
            color: white; /* Set the color of the text above the input box to white */
        }}
        h1 {{
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()