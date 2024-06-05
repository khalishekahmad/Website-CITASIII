import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('citasi-ae1a8ca595ae.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def app():
    st.title('Admin - Verifikasi Pengguna')
    users_ref = db.collection('users')
    pending_users = users_ref.where('verified', '==', False).stream()

    for user in pending_users:
        user_data = user.to_dict()
        st.write(f"Username: {user_data['username']}, Email: {user_data['email']}")
        if st.button(f'Verify {user_data["username"]}', key=user.id):
            users_ref.document(user.id).update({'verified': True})
            st.success(f'Pengguna {user_data["username"]} telah diverifikasi')
