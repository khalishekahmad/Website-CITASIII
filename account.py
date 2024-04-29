import streamlit as st
import firebase_admin

from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate('citasi-ae1a8ca595ae.json')
firebase_admin.initialize_app(cred)


def app():
    st.write('Account')

    st.title('Welcome to :blue[Citasi]')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    
    choice = ''

    def f():
        try:
            user = auth.get_user_by_email(email)
            #print(user.id)
            st.write('Login Successfully')

            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True

        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Signup',['Login','Sign up'])


    if choice =='Login':
        email = st.text_input('Email Addres')
        password = st.text_input('password', type='password')

        st.button ('Login', on_click=f)

    else:
        email = st.text_input('Email Addres')
        password = st.text_input('password', type='password')
        username = st.text_input('Enter Your Username')

        if st.button ('Create Account'):
            user = auth.create_user(email = email, password = password, uid = username)

            st.success('Account Create Successfully')
            st.balloons()

    if st.session_state.signout:
        st.text('Name : '+st.session_state.username)
        st.text('Email Id : '+st.session_state.useremail)
        st.button('Sign Out', on_click=t)

if __name__ == '_main_':
    app()