import streamlit as st
from StreamlitChatLoopClasses import StreamlitChatLoop
import time

@st.cache(allow_output_mutation=True)
def load_chat_model():
    return StreamlitChatLoop()

# Initialize the chat loop
chat = load_chat_model()

# Streamlit interface
st.title("Chat with AI")


# Initialize session state for conversation if it doesn't exist
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Clear conversation button
if st.button('Clear Conversation'):
    st.session_state.conversation = []

# Display the conversation
for exchange in st.session_state.conversation:
    user_input, ai_response = exchange
    st.write(f"You: {user_input}")
    st.write(f"AI: {ai_response}")

# User input form
with st.form(key="input_form"):
    user_input = st.text_input("You:", key="input_form")
    submit_button = st.form_submit_button(label="Submit")

# When the user submits a question
if submit_button and user_input:
    # Process the question
    response = chat.ask_question(user_input)
    # Add the exchange to the conversation
    st.session_state.conversation.append((user_input, response))

    # Rerun the app to update the conversation display
    st.experimental_rerun()