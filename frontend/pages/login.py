import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import api
from auth import login_user, is_authenticated

def show_login_page():
    if is_authenticated():
        st.rerun()

    st.title("Task Manager Login")
    st.markdown("---")

    with st.form("login_form"):
        st.subheader("Sign In")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        login_button = st.form_submit_button("Login", use_container_width=True)
        
        if login_button:
            if username and password:
                with st.spinner("Authenticating..."):
                    if login_user(username, password):
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
            else:
                st.warning("⚠️ Please enter both username and password")
    
    st.markdown("---")
    
    # Registration Section
    st.subheader("New User? Register Here")
    with st.form("register_form"):
        new_username = st.text_input("New Username", placeholder="Choose a username")
        new_password = st.text_input("New Password", type="password", placeholder="Choose a password")
        role = st.selectbox("Role", ["user", "admin"])
        register_button = st.form_submit_button("Register", use_container_width=True)
        
        if register_button:
            if new_username and new_password:
                with st.spinner("Creating account..."):
                    result = api.register_user(new_username, new_password, role)
                    if "error" not in result:
                        st.success(f"✅ Account created successfully! Username: {result['username']}")
                        st.info("👆 Now login with your new credentials above")
                    else:
                        st.error(f"❌ Registration failed: {result['error']}")
            else:
                st.warning("⚠️ Please fill in all fields")
    
    # Demo credentials info
    with st.expander("📋 Demo Credentials"):
        st.info("""
        **Try these demo credentials:**
        - Username: `admin1` / Password: `pass123` (Admin)
        - Username: `user1` / Password: `pass123` (User)
        
        Or register a new account above!
        """)