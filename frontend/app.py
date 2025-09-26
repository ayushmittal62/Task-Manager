import streamlit as st
from auth import initialize_session_state, is_authenticated, logout_user, is_admin, get_current_user
from api import api

# Page configuration
st.set_page_config(
    page_title="Task Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e6e9ef;
    }
</style>
""", unsafe_allow_html=True)

def show_login_page():
    """Display login page"""
    st.title("🔐 Task Manager Login")
    st.markdown("---")
    
    # Login Form
    with st.form("login_form"):
        st.subheader("Sign In")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        login_button = st.form_submit_button("Login", use_container_width=True)
        
        if login_button:
            if username and password:
                with st.spinner("Authenticating..."):
                    from auth import login_user
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
                        st.success(f"✅ Account created successfully! Username: {result['username']} (ID: {result.get('id', 'N/A')})")
                        st.info("👆 Now login with your new credentials above")
                        st.rerun()  # Refresh the page to clear form
                    else:
                        st.error(f"❌ Registration failed: {result['error']}")
                        st.write("Debug info:", result)  # Temporary debug info
            else:
                st.warning("⚠️ Please fill in all fields")

def show_dashboard():
    """Display main dashboard"""
    user = get_current_user()
    
    # Header
    st.title(f"📋 Task Manager Dashboard")
    st.markdown(f"**Welcome back, {user['username']}!** ({user['role'].title()})")
    st.markdown("---")
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    
    # Get tasks for stats
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
                        st.success(f"✅ Task created: {result['title']} (ID: {result.get('id', 'N/A')}) - Priority: {result.get('priority', 'N/A')}")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to create task: {result['error']}")
                        st.write("Debug info:", result)  # Temporary debug info
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
    
    # Display tasks
    for task in tasks:
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
                # Delete button
                if st.button("🗑️", key=f"delete_{task['id']}", help="Delete task"):
                    with st.spinner("Deleting..."):
                        result = api.delete_task(task['id'])
                        if "error" not in result:
                            st.success("✅ Task deleted!")
                            st.rerun()
                        else:
                            st.error(f"❌ Delete failed: {result['error']}")
            
            st.markdown("---")

def show_admin_page():
    """Display admin management page"""
    if not is_admin():
        st.error("❌ Access Denied: Admin privileges required")
        return
    
    st.title("👥 Admin Panel")
    st.markdown("---")
    
    # Create New User
    st.subheader("➕ Create New User")
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
                        st.success(f"✅ User created: {result['username']} (ID: {result.get('id', 'N/A')}) - Role: {result.get('role', 'N/A')}")
                        st.rerun()  # Refresh to clear form and update data
                    else:
                        st.error(f"❌ Failed to create user: {result['error']}")
                        st.write("Debug info:", result)  # Temporary debug info
            else:
                st.warning("⚠️ Please fill in all fields")
    
    # System stats
    tasks = api.get_tasks()
    st.subheader("📊 System Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📋 Total Tasks", len(tasks))
    
    with col2:
        completed_tasks = len([t for t in tasks if t.get('status') == 'completed'])
        st.metric("✅ Completed Tasks", completed_tasks)
    
    with col3:
        pending_tasks = len([t for t in tasks if t.get('status') == 'pending'])
        st.metric("⏳ Pending Tasks", pending_tasks)
    
    st.markdown("---")
    
    # User Management Section
    st.subheader("👥 User Management")
    
    # Get all users
    users = api.get_all_users()
    
    if "error" not in users:
        if users:
            st.write(f"**Total Users:** {len(users)}")
            st.markdown("---")
            
            # Display users in a table-like format
            for user in users:
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"👤 **{user['username']}**")
                
                with col2:
                    role_emoji = "👑" if user['role'] == 'admin' else "👤"
                    st.write(f"{role_emoji} {user['role'].title()}")
                
                with col3:
                    st.write(f"ID: {user['id']}")
                
                with col4:
                    # Don't allow deleting yourself
                    current_user = get_current_user()
                    if user['id'] != current_user['id']:
                        if st.button("🗑️ Delete", key=f"delete_user_{user['id']}", help=f"Delete user {user['username']}"):
                            with st.spinner(f"Deleting user {user['username']}..."):
                                result = api.delete_user(user['id'])
                                if "error" not in result:
                                    st.success(f"✅ User {user['username']} deleted!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed to delete user: {result['error']}")
                    else:
                        st.write("🔒 *You*")
                
                st.markdown("---")
        else:
            st.info("No users found")
    else:
        st.error(f"❌ Failed to load users: {users['error']}")

def main():
    """Main application logic"""
    
    # Check authentication
    if not is_authenticated():
        show_login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📋 Task Manager")
        st.markdown("---")
        
        # User info
        user = get_current_user()
        st.success(f"👤 Welcome, **{user['username']}**")
        st.write(f"Role: {user['role'].title()}")
        
        st.markdown("---")
        
        # Navigation
        st.subheader("🧭 Navigation")
        
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        
        if st.button("📝 Tasks", use_container_width=True):
            st.session_state.page = "tasks"
            st.rerun()
        
        if is_admin():
            if st.button("👥 Admin Panel", use_container_width=True):
                st.session_state.page = "admin"
                st.rerun()
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()
        
        st.markdown("---")
        
        # App info
        st.subheader("ℹ️ App Info")
        st.write("**Version:** 1.0.0")
        st.write("**Backend:** FastAPI + JWT")
        st.write("**Frontend:** Streamlit")
        
        if is_admin():
            st.success("🔑 Admin Mode")
        
        # API Status
        st.write("**API Status:** 🟢 Connected")
    
    # Main content area
    # Initialize page if not set
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    
    # Route to appropriate page
    if st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "tasks":
        show_tasks_page()
    elif st.session_state.page == "admin":
        show_admin_page()
    else:
        show_dashboard()  # Default fallback

if __name__ == "__main__":
    main()