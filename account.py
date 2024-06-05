import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_admin._auth_utils import EmailAlreadyExistsError, UserNotFoundError
import smtplib
from email.mime.text import MIMEText

import admin

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('citasi-ae1a8ca595ae.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def app():
    st.title('Welcome to :blue[Citasi]')
    st.write('Account')

    # Initialize session state variables
    if 'admin_username' not in st.session_state:
        st.session_state.admin_username = ''
    if 'admin_useremail' not in st.session_state:
        st.session_state.admin_useremail = ''
    if 'pegawai_username' not in st.session_state:
        st.session_state.pegawai_username = ''
    if 'pegawai_useremail' not in st.session_state:
        st.session_state.pegawai_useremail = ''
    if 'admin_signedout' not in st.session_state:
        st.session_state.admin_signedout = False
    if 'admin_signout' not in st.session_state:
        st.session_state.admin_signout = False
    if 'pegawai_signedout' not in st.session_state:
        st.session_state.pegawai_signedout = False
    if 'pegawai_signout' not in st.session_state:
        st.session_state.pegawai_signout = False

    choice = st.selectbox('Silakan pilih Admin atau Pegawai', ['Admin', 'Pegawai'])

    if choice == 'Admin':
        if not st.session_state.admin_signedout:
            st.text_input('Email Address', key='admin_email')
            st.text_input('Password', type='password', key='admin_password')
            
            email = st.session_state.admin_email
            password = st.session_state.admin_password
            admin_email = "citasi2024@gmail.com"
            admin_password = "@WebsiteCitasi2024"
        
            if st.button('Login'):
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
                        st.session_state.admin_username = user_ref.to_dict().get('username')
                        st.session_state.admin_useremail = user.email
                        st.session_state.admin_signedout = True
                        st.session_state.admin_signout = True
                        st.success('Admin Login Successfully')
                        
                    else:
                        st.warning('You are not authorized as Admin or account is not verified.')
                else:
                    st.warning('Login Failed: Invalid Admin Credentials')

        if st.session_state.admin_signedout:
            st.text(f'Name: {st.session_state.admin_username}')
            st.text(f'Email Id: {st.session_state.admin_useremail}')
            st.button('Sign Out', on_click=admin_signout)
            admin.app()

    elif choice == 'Pegawai':
        def login():
            email = st.session_state.pegawai_email
            password = st.session_state.pegawai_password
            try:
                user = auth.get_user_by_email(email)
                # Check if the user is verified
                user_ref = db.collection('users').document(user.uid).get()
                if user_ref.exists and user_ref.to_dict().get('verified'):
                    st.session_state.pegawai_username = user_ref.to_dict().get('username')
                    st.session_state.pegawai_useremail = user.email
                    st.session_state.pegawai_signedout = True
                    st.session_state.pegawai_signout = True
                    st.success('Login Berhasil')
                else:
                    st.warning('Akun Anda belum diverifikasi.')
            except auth.UserNotFoundError:
                st.warning('Login Gagal: Pengguna tidak ditemukan')
            except Exception as e:
                st.warning(f'Login Gagal: {e}')

        def signup():
            email = st.session_state.pegawai_email
            password = st.session_state.pegawai_password
            username = st.session_state.pegawai_username_input
            try:
                user = auth.create_user(email=email, password=password)
                # Add user to Firestore with a 'verified' flag
                db.collection('users').document(user.uid).set({
                    'email': email,
                    'username': username,
                    'verified': False
                })
                send_verification_email(email, username)
                st.success('Akun berhasil dibuat. Silakan tunggu verifikasi dari admin.')
            except EmailAlreadyExistsError:
                st.warning('Pembuatan akun gagal: Email sudah terdaftar')
            except Exception as e:
                st.warning(f'Pembuatan akun gagal: {e}')

        def signout():
            st.session_state.pegawai_signout = False
            st.session_state.pegawai_signedout = False
            st.session_state.pegawai_username = ''
            st.session_state.pegawai_useremail = ''
            st.info('Berhasil keluar')

        if not st.session_state.pegawai_signedout:
            choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

            if choice == 'Login':
                st.text_input('Email Address', key='pegawai_email')
                st.text_input('Password', type='password', key='pegawai_password')
                st.button('Login', on_click=login)

            elif choice == 'Sign up':
                st.text_input('Email Address', key='pegawai_email')
                st.text_input('Password', type='password', key='pegawai_password')
                st.text_input('Enter Your Username', key='pegawai_username_input')
                st.button('Create Account', on_click=signup)

        if st.session_state.pegawai_signedout:
            st.text(f'Name: {st.session_state.pegawai_username}')
            st.text(f'Email Id: {st.session_state.pegawai_useremail}')
            st.button('Sign Out', on_click=signout)

def admin_signout():
    st.session_state.admin_signout = False
    st.session_state.admin_signedout = False
    st.session_state.admin_username = ''
    st.session_state.admin_useremail = ''
    st.info('Berhasil keluar')

def send_verification_email(email, username):
    admin_email = "youradminemail@gmail.com"
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
            st.info('Email verifikasi berhasil dikirim.')
        except smtplib.SMTPAuthenticationError as e:
            st.error(f'Error Autentikasi SMTP: {e}')
        except Exception as e:
            st.error(f'Error mengirim email: {e}')

if __name__ == '__main__':
    app()
st.caption('Copyright © Citasi 2024')