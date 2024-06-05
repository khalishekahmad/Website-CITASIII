import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_admin._auth_utils import EmailAlreadyExistsError, UserNotFoundError
import smtplib
from email.mime.text import MIMEText

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('citasi-ae1a8ca595ae.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def app():
    st.title('Welcome to :blue[Citasi]')
    st.write('Account')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    def login():
        email = st.session_state.email
        password = st.session_state.password
        try:
            user = auth.get_user_by_email(email)
            # Check if the user is verified
            user_ref = db.collection('users').document(user.uid).get()
            if user_ref.exists and user_ref.to_dict().get('verified'):
                st.session_state.username = user_ref.to_dict().get('username')
                st.session_state.useremail = user.email
                st.session_state.signedout = True
                st.session_state.signout = True
                st.success('Login Successfully')
            else:
                st.warning('Your account is not verified yet.')
        except UserNotFoundError:
            st.warning('Login Failed: User not found')
        except Exception as e:
            st.warning(f'Login Failed: {e}')

    def signup():
        email = st.session_state.email
        password = st.session_state.password
        username = st.session_state.username_input
        try:
            user = auth.create_user(email=email, password=password)
            # Add user to Firestore with a 'verified' flag
            db.collection('users').document(user.uid).set({
                'email': email,
                'username': username,
                'verified': False
            })
            send_verification_email(email, username)
            st.success('Account Created Successfully. Please wait for admin verification.')
        except EmailAlreadyExistsError:
            st.warning('Account creation failed: Email already exists')
        except Exception as e:
            st.warning(f'Account creation failed: {e}')

    def signout():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.useremail = ''
        st.info('Signed out successfully')

    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

        if choice == 'Login':
            st.text_input('Email Address', key='email')
            st.text_input('Password', type='password', key='password')
            st.button('Login', on_click=login)

        elif choice == 'Sign up':
            st.text_input('Email Address', key='email')
            st.text_input('Password', type='password', key='password')
            st.text_input('Enter Your Username', key='username_input')
            st.button('Create Account', on_click=signup)

    if st.session_state.signout:
        st.text(f'Name: {st.session_state.username}')
        st.text(f'Email Id: {st.session_state.useremail}')
        st.button('Sign Out', on_click=signout)

def send_verification_email(email, username):
    admin_email = "citasi2024@gmail.com"
    msg = MIMEText(f"Please verify the new user:\n\nUsername: {username}\nEmail: {email}")
    msg['Subject'] = 'New User Verification Needed'
    msg['From'] = 'noreply@example.com'
    msg['To'] = admin_email

    # Using SMTP to send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('citasi2024@gmail.com', '@WebsiteCitasi')  # Use app password here
        server.sendmail('noreply@example.com', admin_email, msg.as_string())

if __name__ == '__main__':
    app()
