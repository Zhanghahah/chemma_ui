import streamlit as st

def dashboard():
    print("===========dashboard============")
    st.switch_page("pages/home.py")

def to_login():
    print("===========to_login============")
    st.switch_page("app.py")

def set_sidebar():
    print("===========set_sidebar============")
    #TODO角色和功能控制
    st.sidebar.image("static/IMG_8209.PNG")
    st.sidebar.caption(f'Welcome :blue[*{st.session_state["name"]}*]!')
    # st.sidebar.header("_Category1_")
    st.sidebar.page_link("pages/home.py", label="dashboard",icon="🏠")
    # st.sidebar.page_link("pages/func1.py", label="func1",icon="1️⃣")
    # st.sidebar.header("_Category2_")
    # st.sidebar.page_link("pages/func2.py", label="func2",icon="2️⃣")
    # st.sidebar.page_link("pages/func3.py", label="中文字体123",icon="3️⃣")
    st.sidebar.divider()
    st.sidebar.page_link("pages/logout.py", label="退出登录",icon="⏏️")
    


def to_menu():
    print("===========to_menu============")
    if 'authentication_status'  not in st.session_state:
        print("--to_login--")
        to_login()     

    if st.session_state["authentication_status"]:
        print("--dashboard--")
        dashboard()
        
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        print("2")
    elif st.session_state["authentication_status"] is None:
        print("3")

def check_login():
    print("===========check_login============")
    print(st.session_state)
    if 'authentication_status'  not in st.session_state:
        print("--to_login--")
        to_login() 

def check_login_args(st_in):
    print("===========check_login_args============")
    print(st_in)
    


