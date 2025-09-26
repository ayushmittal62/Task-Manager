import streamlit as st
from api import api

def initialize_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "jwt_token" not in st.session_state:
        st.session_state.jwt_token = None
    if "current_user" not in st.session_state:
        st.session_state.current_user = None

def login_user(username: str, password: str) -> bool:
    result = api.login(username, password)
    
    if "error" not in result:
        st.session_state.jwt_token = result["access_token"]
        st.session_state.authenticated = True
        
        user_info = api.get_current_user()
        if "error" not in user_info:
            st.session_state.current_user = user_info
            return True
    
    return False

def logout_user():
    st.session_state.authenticated = False
    st.session_state.jwt_token = None
    st.session_state.current_user = None

def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)

def is_admin() -> bool:
    if not is_authenticated():
        return False
    user = st.session_state.get("current_user", {})
    return user.get("role") == "admin"

def get_current_user():
    return st.session_state.get("current_user", {})