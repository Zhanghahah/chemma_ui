import streamlit as st
from menu import *

check_login()
set_sidebar()

st.subheader(f'func1',divider='rainbow')

st.text("main content")
print("1")

st.write("this is func1!!")
st.write("-------------------")
st.write(st.session_state)