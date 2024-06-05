import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('citasi-ae1a8ca595ae.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def admin_app():
    st.title('Admin - User Verification')
    users_ref = db.collection('users')
    pending_users = users_ref.where('verified', '==', False).stream()

    for user in pending_users:
        user_data = user.to_dict()
        st.write(f"Username: {user_data['username']}, Email: {user_data['email']}")
        
        button_key = f'verify_{user.id}'
        if st.button(f'Verify {user_data["username"]}', key=button_key):
            users_ref.document(user.id).update({'verified': True})
            st.success(f'User {user_data["username"]} has been verified')
            st.experimental_rerun()

if __name__ == '__main__':
    admin_app()
