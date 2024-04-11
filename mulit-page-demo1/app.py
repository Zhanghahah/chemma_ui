import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from menu import *
import email_utils

st.set_page_config(
    page_title="Chemma",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


with open('account-config/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

col1, col2, col3 = st.columns(3)

with col2:
    st.image("static/chemma_logo-2.png")
    authenticator.login()

    register_form = st.sidebar.form("Register")
    subheader = register_form.subheader('Register')
    email = register_form.text_input('Notes: submit your email to request access to Chemma')
    if register_form.form_submit_button('Submit'):
        print(email)
        if not authenticator.validator.validate_email(email):
            st.sidebar.warning('Email is not valid')
        else:
            if email_utils.send_email(['452516515@qq.com'], 'chemc', 'cdad'):
                st.sidebar.warning('Successfully submit')
            else:
                st.sidebar.warning('Failed to send email')

    st.text("沪交ICP备20230107")

to_menu()

#验证session是否被清理
print(st.session_state)
     
