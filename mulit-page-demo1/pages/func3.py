import streamlit as st
from menu import *

print("in login func3")
check_login_args(st.session_state)
check_login()
set_sidebar()

st.subheader(f'func2',divider='rainbow')
#creates three columns where the second one is two times the width of the first one, and the third one is three times that width
col1, col2, col3 = st.columns(spec=[1, 2, 1])


col1.header("A cat")
col1.image("https://static.streamlit.io/examples/cat.jpg")

col2.header("A dog")
col2.image("https://static.streamlit.io/examples/dog.jpg")

col3.header("An owl")
col3.image("https://static.streamlit.io/examples/owl.jpg")