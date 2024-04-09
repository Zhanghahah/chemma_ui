import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from menu import *

#clear session and backto login
del st.session_state["authentication_status"]
del st.session_state["username"]
del st.session_state["name"]

st.session_state['logout'] = True
st.session_state['name'] = None
st.session_state['username'] = None
st.session_state['authentication_status'] = None

with open('account-config/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.logout()

to_login()