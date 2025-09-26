import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import get_current_user, is_admin
from api import api

def show_tasks_page():
    """Display tasks management page"""
    st.title("📝 Task Management")
    st.markdown("---")
    
    # Create New Task Section
    st.subheader("➕ Create New Task")
    with st.form("create_task_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            task_title = st.text_input("Task Title", placeholder="Enter task description...")
        
        with col2:
            task_priority = st.selectbox("Priority", ["low", "medium", "high"])
        
        create_button = st.form_submit_button("Create Task", use_container_width=True)
        
        if create_button:
            if task_title:
                with st.spinner("Creating task..."):
                    result = api.create_task(task_title, task_priority)
                    if "error" not in result:
                        st.success(f"✅ Task created: {result['title']}")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to create task: {result['error']}")
            else:
                st.warning("⚠️ Please enter a task title")
    
    st.markdown("---")
    
    # Tasks List
    st.subheader("📋 Your Tasks")
    
    # Get all tasks
    tasks = api.get_tasks()
    
    if not tasks:
        st.info("No tasks found. Create your first task above!")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", ["all", "pending", "in_progress", "completed"])
    
    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["all", "low", "medium", "high"])
    
    with col3:
        sort_by = st.selectbox("Sort by", ["id", "title", "priority", "status"])
    
    # Apply filters
    filtered_tasks = tasks
    if status_filter != "all":
        filtered_tasks = [t for t in filtered_tasks if t.get('status') == status_filter]
    if priority_filter != "all":
        filtered_tasks = [t for t in filtered_tasks if t.get('priority') == priority_filter]
    
    # Sort tasks
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x.get(sort_by, ''))
    
    st.write(f"Showing {len(filtered_tasks)} of {len(tasks)} tasks")
    
    # Display tasks
    for i, task in enumerate(filtered_tasks):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            # Task info
            with col1:
                status_emoji = "✅" if task['status'] == 'completed' else "⏳" if task['status'] == 'pending' else "🔄"
                st.write(f"{status_emoji} **{task['title']}** (ID: {task['id']})")
            
            with col2:
                priority_colors = {"low": "🟢", "medium": "🟡", "high": "🔥"}
                st.write(f"{priority_colors.get(task['priority'], '⚪')} {task['priority'].title()}")
            
            with col3:
                st.write(task['status'].replace('_', ' ').title())
            
            # Action buttons
            with col4:
                # Update status
                new_status = st.selectbox(
                    "Status",
                    ["pending", "in_progress", "completed"],
                    index=["pending", "in_progress", "completed"].index(task['status']),
                    key=f"status_{task['id']}"
                )
                
                if new_status != task['status']:
                    if st.button("Update", key=f"update_{task['id']}"):
                        with st.spinner("Updating..."):
                            result = api.update_task(task['id'], status=new_status)
                            if "error" not in result:
                                st.success("✅ Task updated!")
                                st.rerun()
                            else:
                                st.error(f"❌ Update failed: {result['error']}")
            
            with col5:
                # Delete button (admin or task owner)
                user = get_current_user()
                can_delete = is_admin() or task['owner_id'] == user['id']
                
                if can_delete:
                    if st.button("🗑️", key=f"delete_{task['id']}", help="Delete task"):
                        with st.spinner("Deleting..."):
                            result = api.delete_task(task['id'])
                            if "error" not in result:
                                st.success("✅ Task deleted!")
                                st.rerun()
                            else:
                                st.error(f"❌ Delete failed: {result['error']}")
                else:
                    st.button("🗑️", disabled=True, key=f"delete_disabled_{task['id']}", help="Cannot delete this task")
            
            st.markdown("---")