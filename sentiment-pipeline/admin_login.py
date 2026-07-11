import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta

# Admin credentials (CHANGE THESE!)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Session management
SESSION_FILE = "admin_session.json"

def check_admin(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def create_session():
    session_data = {
        "username": ADMIN_USERNAME,
        "login_time": datetime.now().isoformat(),
        "expires": (datetime.now() + timedelta(hours=24)).isoformat()
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f)
    return session_data

def check_session():
    if not os.path.exists(SESSION_FILE):
        return False
    try:
        with open(SESSION_FILE, "r") as f:
            session = json.load(f)
        expire_time = datetime.fromisoformat(session["expires"])
        if datetime.now() > expire_time:
            os.remove(SESSION_FILE)
            return False
        return True
    except:
        return False

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def login_page():
    st.set_page_config(page_title="Admin Login", page_icon="🔐", layout="centered")
    
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .login-title {
            text-align: center;
            color: #1e3a8a;
            margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="login-title">🔐 Admin Login</h1>', unsafe_allow_html=True)
    
    username = st.text_input("👤 Username", placeholder="Enter username")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔓 Login", use_container_width=True):
            if check_admin(username, password):
                create_session()
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("🔒 Admin access only")

def admin_dashboard():
    st.set_page_config(page_title="Admin Dashboard", page_icon="👑", layout="wide")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 👑 Admin Panel")
        st.markdown("---")
        st.markdown(f"**👤 Logged in as:** {ADMIN_USERNAME}")
        st.markdown(f"**🕐 Login time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown("---")
        st.markdown("### 📊 Navigation")
        st.markdown("• 🏠 Dashboard")
        st.markdown("• 📈 Analytics")
        st.markdown("• ⚙️ Settings")
        st.markdown("• 👥 Users")
        st.markdown("• 📝 Logs")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            clear_session()
            st.rerun()
    
    # Main content
    st.title("👑 Admin Dashboard")
    st.markdown(f"Welcome back, **{ADMIN_USERNAME}!** You have full control.")
    st.markdown("---")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👤 Admin Users", "1", "✅")
    with col2:
        st.metric("🟢 System Health", "100%", "✅")
    with col3:
        st.metric("⚠️ Alerts", "0", "✅")
    with col4:
        st.metric("🛡️ Security", "Active", "🔒")
    
    st.markdown("---")
    
    # Controls
    st.subheader("🎛️ Admin Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Dashboard Controls")
        dashboard_mode = st.selectbox(
            "Dashboard Mode",
            ["Live Data", "Demo Mode", "Maintenance"]
        )
        st.info(f"Current mode: {dashboard_mode}")
        if st.button("🔄 Refresh Data"):
            st.success("✅ Data refreshed!")
    
    with col2:
        st.markdown("### ⚙️ System Settings")
        auto_update = st.checkbox("🔄 Auto Update", value=True)
        if st.button("💾 Save Settings"):
            st.success("✅ Settings saved!")
    
    st.markdown("---")
    
    # Data Management
    st.subheader("📁 Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Export Data"):
            st.success("✅ Data exported!")
    
    with col2:
        if st.button("📥 Import Data"):
            st.info("📥 Import feature ready")
    
    with col3:
        if st.button("🗑️ Clear Cache"):
            st.warning("⚠️ Cache cleared!")
    
    st.markdown("---")
    
    # Activity Log
    st.subheader("📝 Recent Activity")
    
    activities = [
        ("👑 Admin logged in", "Just now"),
        ("⚙️ Settings updated", "5 minutes ago"),
        ("📤 Data exported", "1 hour ago"),
    ]
    
    for activity, time in activities:
        st.write(f"• {activity} - {time}")

def main():
    if check_session():
        admin_dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()