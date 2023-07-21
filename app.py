import streamlit as st
import random
import time

from chatbot.chatbot import Chatbot
from helpers.constants import Constants


def main():
    st.title("Chat with USJ")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Initialize our chatbot (Make sure training text in data/scraped_text/)
    chatbot = Chatbot(model_name=Constants.ModelName.value, index_name=Constants.PineconeIndex.value, existing_index=True)

    # Accept user input 
    if prompt := st.chat_input("Ask me anything about USJ"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = chatbot.answer_question(prompt)["answer"]
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(assistant_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


def query_answer(chatbot, prompt, attempts):
    # Clear the cache to force re-execution of st.cache functions
    st.cache_data.clear()    

    # Put a limit of query attempts
    attempts += 1
    if attempts > 5:
        return "Could not find an answer. Please try to reload the page or clear the cache."
    
    try:
        # Get the bot's response
        return chatbot.answer_question(prompt)["answer"]
    
    except Exception as e:
        # Retry the code block
        query_answer(chatbot, prompt, attempts)

if __name__ == "__main__":
    main()