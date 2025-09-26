import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import get_current_user, is_admin
from api import api

def show_dashboard():
    user = get_current_user()

    st.title(f"📋 Task Manager Dashboard")
    st.markdown(f"**Welcome back, {user['username']}!** ({user['role'].title()})")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    tasks = api.get_tasks()
    
    with col1:
        st.metric("📊 Total Tasks", len(tasks))
    
    with col2:
        pending_tasks = len([t for t in tasks if t.get('status') == 'pending'])
        st.metric("⏳ Pending", pending_tasks)
    
    with col3:
        completed_tasks = len([t for t in tasks if t.get('status') == 'completed'])
        st.metric("✅ Completed", completed_tasks)
    
    with col4:
        high_priority = len([t for t in tasks if t.get('priority') == 'high'])
        st.metric("🔥 High Priority", high_priority)   

    st.markdown("---")
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Task", use_container_width=True):
            st.session_state.page = "tasks"
            st.rerun()
    
    with col2:
        if st.button("📝 View All Tasks", use_container_width=True):
            st.session_state.page = "tasks"
            st.rerun()
    
    with col3:
        if is_admin():
            if st.button("👥 Manage Users", use_container_width=True):
                st.session_state.page = "admin"
                st.rerun()
        else:
            st.button("👥 Admin Only", disabled=True, use_container_width=True)
    
    st.markdown("---")
    
    # Recent Tasks
    st.subheader("📋 Recent Tasks")
    if tasks:
        # Display last 5 tasks
        recent_tasks = tasks[-5:]
        for task in reversed(recent_tasks):
            status_emoji = "✅" if task['status'] == 'completed' else "⏳" if task['status'] == 'pending' else "🔄"
            priority_emoji = "🔥" if task['priority'] == 'high' else "🟡" if task['priority'] == 'medium' else "🟢"
            
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{status_emoji} {task['title']}")
                with col2:
                    st.write(f"{priority_emoji} {task['priority'].title()}")
                with col3:
                    st.write(f"Status: {task['status'].title()}")
                st.markdown("---")
    else:
        st.info("No tasks found. Create your first task!")
    
    # User Info
    with st.sidebar:
        st.header("👤 User Info")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Role:** {user['role'].title()}")
        st.write(f"**User ID:** {user['id']}")
        
        if is_admin():
            st.success("🔑 Admin Privileges")
        else:
            st.info("👤 Standard User")