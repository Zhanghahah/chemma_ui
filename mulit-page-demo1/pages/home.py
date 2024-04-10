import streamlit as st
from menu import *
import random
import time
from openai import OpenAI

check_login()
set_sidebar()

st.subheader(f'Chat With Chemma',divider='rainbow')

# st.text("main content")

def disable_input():
    st.session_state["disabled"] = True

def enable_input():
    st.session_state["disabled"] = False

def response_generator(prompt):
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )

    client = OpenAI(base_url="http://202.120.39.36:8800/v1", api_key="not used actually")
    # input test case:
    print("++++++++++++++++++++++++++++++++++++")
    print(prompt)
    response = client.completions.create(
        model="11-07-output_step1_llama2_7b",
        max_tokens=200,
        temperature=1.5,
        stop=["<|endoftext|>"],
        prompt=f"Human:{prompt} Assistant:"
               )

    #print(response['choices'][0]['text'])
    print("++++++++++++++++++++++++++++++++++++")
    print(response[1][1]['text'])


    #处理逻辑。。。。。。。。


    for word in response:
        time.sleep(0.05)
        yield word
    # time.sleep(5)
    # return response



def chat_ui():

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if 'disabled' not in st.session_state:
        st.session_state['disabled'] = False
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    prompt = st.chat_input("Input your question", key='user_input', disabled=st.session_state['disabled'] or not st.session_state["authentication_status"], on_submit=disable_input)
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.spinner('thinking'):
            with st.chat_message("assistant"):
                response = st.write_stream(response_generator(prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        enable_input()
        st.rerun()
chat_ui()
print("1")