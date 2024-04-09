import streamlit as st
from menu import *

print("in login func2")
check_login_args(st.session_state)
check_login()
set_sidebar()

st.subheader(f'func2',divider='rainbow')
st.text("main content")
print("1")

st.write("this is func2!!")
st.write("-------------------")
st.write(st.session_state)