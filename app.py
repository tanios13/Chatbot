import streamlit as st
import requests

from streamlit_chat import message
from chatbot.chatbot import Chatbot
from helpers.constants import Constants

def main():
    st.title("Chat with USJ")

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    # Initialize our chatbot (Make sure training text in data/scraped_text/)
    chatbot = Chatbot(model_name=Constants.ModelName.value, index_name=Constants.PineconeIndex.value, existing_index=True)

    # Text input to ask a question
    user_question = st.text_input("Ask a question about admission, international, help, financial support, insitutions and more:")
        
    if st.button("Submit") and user_question:
    # Query answer from bot until success
        query_answer(chatbot, user_question)
    
    if st.session_state['generated']:

        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


def query_answer(chatbot, user_question):
    # Your code block goes here
    try:
        # Get the bot's response
        bot_response = chatbot.answer_question(user_question)["answer"]

        st.session_state.past.append(user_question)
        st.session_state.generated.append(bot_response)

    except Exception as e:
        # Clear the cache to force re-execution of st.cache functions
        st.cache_resource.clear()

        # Retry the code block
        query_answer(chatbot, user_question)


if __name__ == "__main__":
    main()