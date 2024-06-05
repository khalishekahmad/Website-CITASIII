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

    def login_admin():
        email = st.session_state.email
        password = st.session_state.password
        admin_email = "citasi2024@gmail.com"
        admin_password = "@WebsiteCitasi2024"
    
        if email == admin_email and password == admin_password:
            try:
                user = auth.get_user_by_email(email)
            except UserNotFoundError:
                # Create admin user if not found
                try:
                    user = auth.create_user(email=admin_email, password=admin_password)
                    db.collection('users').document(user.uid).set({
                        'email': admin_email,
                        'username': 'Admin',
                        'role': 'Admin',
                        'verified': True
                    })
                    st.success('Admin account created successfully. Please try logging in again.')
                    return
                except Exception as e:
                    st.error(f'Failed to create admin account: {e}')
                    return
            except Exception as e:
                st.error(f'Failed to fetch admin user: {e}')
                return
        
            # Check if the user is verified and has admin role
            user_ref = db.collection('users').document(user.uid).get()
            if user_ref.exists and user_ref.to_dict().get('role') == 'Admin':
                st.session_state.username = user_ref.to_dict().get('username')
                st.session_state.useremail = user.email
                st.session_state.signedout = True
                st.session_state.signout = True
                st.success('Admin Login Successfully')
                admin_page()
            else:
                st.warning('You are not authorized as Admin or account is not verified.')
        else:
            st.warning('Login Failed: Invalid Admin Credentials')

    def login_pegawai():
        email = st.session_state.email
        password = st.session_state.password
        try:
            user = auth.get_user_by_email(email)
            user_ref = db.collection('users').document(user.uid).get()
            if user_ref.exists and user_ref.to_dict().get('role') == 'Pegawai':
                st.session_state.username = user_ref.to_dict().get('username')
                st.session_state.useremail = user.email
                st.session_state.signedout = True
                st.session_state.signout = True
                st.success('Pegawai Login Successfully')
                pegawai_page()
            else:
                st.warning('You are not authorized as Pegawai or account is not verified.')
        except UserNotFoundError:
            st.warning('Login Failed: User not found')
        except Exception as e:
            st.warning(f'Login Failed: {e}')

    def signup_pegawai():
        email = st.session_state.email
        password = st.session_state.password
        username = st.session_state.username_input
        try:
            user = auth.create_user(email=email, password=password)
            db.collection('users').document(user.uid).set({
                'email': email,
                'username': username,
                'role': 'Pegawai',
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

    def admin_page():
        st.header('Admin Page')
        st.write(f'Welcome, {st.session_state.username}')
        users_ref = db.collection('users')
        pending_users = users_ref.where('verified', '==', False).stream()

        for user in pending_users:
            user_data = user.to_dict()
            st.write(f"Username: {user_data['username']}, Email: {user_data['email']}")
            if st.button(f'Verify {user_data["username"]}', key=user.id):
                users_ref.document(user.id).update({'verified': True})
                st.success(f'Pengguna {user_data["username"]} telah diverifikasi')

    def pegawai_page():
        st.header('Pegawai Page')
        st.write(f'Welcome, {st.session_state.username}')

    if not st.session_state['signedout']:
        choice = st.selectbox('Silakan pilih Admin atau Pegawai', ['Admin', 'Pegawai'])

        if choice == 'Admin':
            st.text_input('Email Address', key='email')
            st.text_input('Password', type='password', key='password')
            st.button('Login', on_click=login_admin)

        elif choice == 'Pegawai':
            action = st.selectbox('Login or Sign up', ['Login', 'Sign up'])
            if action == 'Login':
                st.text_input('Email Address', key='email')
                st.text_input('Password', type='password', key='password')
                st.button('Login', on_click=login_pegawai)
            elif action == 'Sign up':
                st.text_input('Email Address', key='email')
                st.text_input('Password', type='password', key='password')
                st.text_input('Enter Your Username', key='username_input')
                st.button('Create Account', on_click=signup_pegawai)

    if st.session_state.signout:
        st.text(f'Name: {st.session_state.username}')
        st.text(f'Email Id: {st.session_state.useremail}')
        st.button('Sign Out', on_click=signout)

def send_verification_email(email, username):
    admin_email = "citasi2024@gmail.com"
    msg = MIMEText(f"Please verify the new user:\n\nUsername: {username}\nEmail: {email}")
    msg['Subject'] = 'New User Verification Needed'
    msg['From'] = 'citasi2024@gmail.com'
    msg['To'] = admin_email

    # Using SMTP to send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        try:
            server.login('citasi2024@gmail.com', 'sricyajimfuzfgie')  # Use app password here
            server.sendmail('citasi2024@gmail.com', admin_email, msg.as_string())
            st.info('Verification email sent successfully.')
        except smtplib.SMTPAuthenticationError as e:
            st.error(f'SMTP Authentication Error: {e}')
        except Exception as e:
            st.error(f'Error sending email: {e}')

if __name__ == '__main__':
    app()
