# admin_login.py
import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
import time

# Admin credentials (change these!)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # Change this!

# Session management
SESSION_FILE = "admin_session.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
    
    # Custom CSS
    st.markdown("""
    <style>
        .admin-header {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 5px solid #3b82f6;
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #1e3a8a;
        }
        .stat-label {
            color: #666;
            font-size: 14px;
        }
        .control-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        .admin-sidebar {
            background: #1e293b;
            color: white;
            padding: 20px;
            border-radius: 10px;
            height: 100%;
        }
        .admin-sidebar a {
            color: #94a3b8;
            text-decoration: none;
            display: block;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }
        .admin-sidebar a:hover {
            background: #334155;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="admin-sidebar">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    st.markdown(f"""
    <div class="admin-header">
        <h1>👑 Admin Dashboard</h1>
        <p>Welcome back, {ADMIN_USERNAME}! You have full control.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">1</div>
            <div class="stat-label">👤 Admin Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card" style="border-left-color: #22c55e;">
            <div class="stat-value">100%</div>
            <div class="stat-label">🟢 System Health</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card" style="border-left-color: #f59e0b;">
            <div class="stat-value">0</div>
            <div class="stat-label">⚠️ Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card" style="border-left-color: #8b5cf6;">
            <div class="stat-value">✓</div>
            <div class="stat-label">🛡️ Security</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Control Panels
    st.subheader("🎛️ Admin Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="control-card">
            <h4>📊 Dashboard Controls</h4>
            <p>Manage what users see</p>
        </div>
        """, unsafe_allow_html=True)
        
        dashboard_mode = st.selectbox(
            "Dashboard Mode",
            ["Live Data", "Demo Mode", "Maintenance"]
        )
        st.info(f"Current mode: {dashboard_mode}")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.success("✅ Data refreshed!")
    
    with col2:
        st.markdown("""
        <div class="control-card">
            <h4>⚙️ System Settings</h4>
            <p>Configure your system</p>
        </div>
        """, unsafe_allow_html=True)
        
        auto_update = st.toggle("🔄 Auto Update", value=True)
        dark_mode = st.toggle("🌙 Dark Mode", value=False)
        
        if st.button("💾 Save Settings", use_container_width=True):
            st.success("✅ Settings saved!")
    
    st.markdown("---")
    
    # Data Management
    st.subheader("📁 Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Export Data", use_container_width=True):
            st.success("✅ Data exported!")
    
    with col2:
        if st.button("📥 Import Data", use_container_width=True):
            st.info("📥 Import feature ready")
    
    with col3:
        if st.button("🗑️ Clear Cache", use_container_width=True):
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
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 10px; border-radius: 5px; margin: 5px 0;">
            <span>{activity}</span>
            <span style="float: right; color: #666; font-size: 12px;">{time}</span>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Check if already logged in
    if check_session():
        admin_dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()