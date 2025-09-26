import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import is_admin, get_current_user
from api import api

def show_admin_page():
    """Display admin management page"""
    if not is_admin():
        st.error("❌ Access Denied: Admin privileges required")
        return
    
    st.title("👥 Admin Panel")
    st.markdown("---")
    
    # Admin Stats
    st.subheader("📊 System Overview")
    
    tasks = api.get_tasks()  # Admin sees all tasks
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total Tasks", len(tasks))
    
    with col2:
        # Count unique users from tasks
        unique_users = len(set(task['owner_id'] for task in tasks))
        st.metric("👥 Active Users", unique_users)
    
    with col3:
        completed_tasks = len([t for t in tasks if t.get('status') == 'completed'])
        st.metric("✅ Completed Tasks", completed_tasks)
    
    with col4:
        pending_tasks = len([t for t in tasks if t.get('status') == 'pending'])
        st.metric("⏳ Pending Tasks", pending_tasks)
    
    st.markdown("---")
    
    # User Management
    st.subheader("👤 User Management")
    
    # Create New User
    with st.expander("➕ Create New User"):
        with st.form("create_user_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_username = st.text_input("Username")
            
            with col2:
                new_password = st.text_input("Password", type="password")
            
            with col3:
                new_role = st.selectbox("Role", ["user", "admin"])
            
            create_user_button = st.form_submit_button("Create User", use_container_width=True)
            
            if create_user_button:
                if new_username and new_password:
                    with st.spinner("Creating user..."):
                        result = api.register_user(new_username, new_password, new_role)
                        if "error" not in result:
                            st.success(f"✅ User created: {result['username']} ({result['role']})")
                        else:
                            st.error(f"❌ Failed to create user: {result['error']}")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    # Task Management Overview
    st.subheader("📝 All Tasks Overview")
    
    if tasks:
        # Group tasks by user
        tasks_by_user = {}
        for task in tasks:
            user_id = task['owner_id']
            if user_id not in tasks_by_user:
                tasks_by_user[user_id] = []
            tasks_by_user[user_id].append(task)
        
        # Display tasks by user
        for user_id, user_tasks in tasks_by_user.items():
            with st.expander(f"👤 User ID {user_id} - {len(user_tasks)} tasks"):
                for task in user_tasks:
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        status_emoji = "✅" if task['status'] == 'completed' else "⏳" if task['status'] == 'pending' else "🔄"
                        st.write(f"{status_emoji} {task['title']}")
                    
                    with col2:
                        priority_colors = {"low": "🟢", "medium": "🟡", "high": "🔥"}
                        st.write(f"{priority_colors.get(task['priority'], '⚪')} {task['priority']}")
                    
                    with col3:
                        st.write(task['status'])
                    
                    with col4:
                        if st.button("🗑️", key=f"admin_delete_{task['id']}", help="Delete as admin"):
                            result = api.delete_task(task['id'])
                            if "error" not in result:
                                st.success("✅ Task deleted!")
                                st.rerun()
                            else:
                                st.error(f"❌ Delete failed: {result['error']}")
    else:
        st.info("No tasks in the system yet.")
    
    # System Information
    st.markdown("---")
    st.subheader("⚙️ System Information")
    
    current_user = get_current_user()
    st.info(f"""
    **Current Admin:** {current_user['username']}
    **Admin ID:** {current_user['id']}
    **API Base URL:** http://127.0.0.1:8000
    **Total System Tasks:** {len(tasks)}
    """)