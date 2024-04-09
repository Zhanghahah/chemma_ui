import streamlit as st
import streamlit_authenticator as stauth

import random
import time
from typing import Optional
import yaml
from yaml.loader import SafeLoader

class FixedAuthenticate(stauth.Authenticate): 
    def _implement_logout(self):
        # Clears cookie and session state variables associated with the logged in user.
        try:
            self.cookie_manager.delete(self.cookie_name)
        except Exception as e: 
            print(e)
        self.credentials['usernames'][st.session_state['username']]['logged_in'] = False
        st.session_state['logout'] = True
        st.session_state['name'] = None
        st.session_state['username'] = None
        st.session_state['authentication_status'] = None
        st.session_state.messages = []


    def logout(self, button_name: str='Logout', location: str='main', key: Optional[str]=None):
        """
        Creates a logout button.

        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar or unrendered.
        key: str
            A unique key to be used in multipage applications.
        """
        if location not in ['main', 'sidebar','unrendered']:
            raise ValueError("Location must be one of 'main' or 'sidebar' or 'unrendered'")
        if location == 'main':
            if st.button(button_name, key):
                self._implement_logout()
        elif location == 'sidebar':
            logout_form = st.sidebar.form('Logout')
            logout_form.subheader(f'Welcome *{st.session_state["name"]}*')
            if logout_form.form_submit_button(button_name):
            # if st.sidebar.button(button_name, key):
                self._implement_logout()
        elif location == 'unrendered':
            if st.session_state['authentication_status']:
                self._implement_logout()


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response:
        time.sleep(0.05)
        yield word
    # time.sleep(5)
    # return response


def read_yaml(cfg_path):
    with open(cfg_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def write_yaml(cfg_path, config):
    with open(cfg_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def disable_input():
    st.session_state["disabled"] = True

def enable_input():
    st.session_state["disabled"] = False

def chat_ui():

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
                response = st.write_stream(response_generator())
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        enable_input()
        st.rerun()


def web_ui():
    cfg_path = './config.yaml'
    config = read_yaml(cfg_path)
    authenticator = FixedAuthenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        # config['preauthorized']
    )
    authenticator.login(location='sidebar')

    # st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Chat With Chemma')
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if 'disabled' not in st.session_state:
        st.session_state['disabled'] = False

    if st.session_state["authentication_status"]:
        # st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
        authenticator.logout(location='sidebar')
    elif st.session_state["authentication_status"] is False:
        st.sidebar.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.sidebar.warning('Please enter your username and password')

    chat_ui()
    # write_yaml(cfg_path, config)


if __name__ == '__main__':
    web_ui()