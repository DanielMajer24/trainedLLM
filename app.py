import os
import streamlit as st
import fsstreamlit

@st.cache_resource
def load_models():
    chat = fsstreamlit.StreamlitChatLoop(os.getenv('MODEL_PATH', '/Users/ryanhurst/.cache/huggingface/hub/models--lmsys--fastchat-t5-3b-v1.0/snapshots/0b1da230a891854102d749b93f7ddf1f18a81024/'))
    chat.load_models()
    return chat

chat = load_models()

output = st.text('')

def clear_conversation():
    chat.clear_conversation()

st.button('Clear Conversation', on_click=clear_conversation)


with st.form(key='input-form', clear_on_submit=True):
    user_input = st.text_area("You:", key='input', height=100)
    submit_button = st.form_submit_button(label='Send')
    
if not submit_button:
    st.stop()

chat.take_user_input(user_input)
messages = [f'{role}: {"" if message is None else message}' for role, message in chat.conv.messages]
message_string = "\n\n".join(messages)
for text in chat.loop():
    message = message_string + text
    message = message.replace('\n', '\n\n')
    output.write(message)