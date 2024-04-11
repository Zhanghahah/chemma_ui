import sys
sys.path.append("../")
import streamlit as st
from menu import *
import random
import time
from openai import OpenAI

check_login()
set_sidebar()

with st.expander("Instruction handbook"):

    tab0, tab1, tab2, tab3 = st.tabs(["Instruction handbook", "Condition generation", "Retrosynthesis", "Forward prediction"])
    with tab0:
        st.markdown("""Chemma is capable of human-AI interactions for primary tasks in chemistry, including retrosynthesis, reaction performance prediction (yield prediction &
        selectivity prediction), condition generation, and reaction exploration & optimization. Here, we give examples of prompts for each task. Please follow the
        prompts format, and replace contents marked by colors with the SMILES of your molecules. For example, if you are conducting a condition generation task, you
        need to prepare the SMILES of reactants, products, and other conditions. The more information about this reaction you give, the more useful answers Chemma
        will generate.""")

        st.image("static/ui-reaction.png")

    with tab1:
        st.markdown("""Considering a chemical reaction, SMILES is sequenced-based string used to encode the molecular structure. A chemical reaction includes reactants,
        conditions and products. Thus, reactants for this reaction are  :blue[*FC(F)(F)c1ccc(Cl)cc1.Cc1ccc(N)cc1*], SMILES for products of reactions are
          :blue[*Cc1ccc(Nc2ccc(C(F)(F)F)cc2)cc1*], then the reaction can be described as  :blue[*FC(F)(F)c1ccc(Cl)cc1.Cc1ccc(N)cc1>>Cc1ccc(Nc2ccc(C(F)(F)F)cc2)cc1*], base for this
        reaction is :blue[*CCN=P(N=P(N(C)C)(N(C)C)N(C)C)(N(C)C)N(C)C*], product yield for this reaction is 10.65, Could you oer any recommendations for catalysts or
        ligands that could have been used in this specic chemical reaction?""")

    with tab2:
        st.markdown("""Considering a chemical reaction, SMILES is sequenced-based string used to encode the molecular structure. A chemical reaction includes reactants,
        conditions and products. SMILES for products of reactions are :blue[*Cc1ccc(Nc2ccc(C(F)(F)F)cc2)cc1*], Can you provide which reactants would lead to this resulting
        product?""")

    with tab3:
        st.markdown("""Considering a chemical reaction, SMILES is sequenced-based string used to encode the molecular structure. A chemical reaction includes reactants,
        conditions and products. Thus, reactants for this reaction are :blue[*FC(F)(F)c1ccc(Br)cc1.Cc1ccc(N)cc1*], What could be a potential product based on the interaction
        of these reactants?""")



                

    
    

st.subheader(f'Chat With Chemma',divider='rainbow')

# st.text("main content")

def disable_input():
    st.session_state["disabled"] = True

def enable_input():
    st.session_state["disabled"] = False

def response_generator(prompt):
    final_answer = ""
    dummy_response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    if prompt in ['hi', 'hello', 'hello']:
        final_answer = dummy_response
    else:

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