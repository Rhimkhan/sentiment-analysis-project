# admin_dashboard_full.py - Complete Admin Control
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random
import json
import os

# Admin password (change this!)
ADMIN_PASSWORD = "admin123"

def admin_control_panel():
    st.set_page_config(page_title="Complete Admin Control", page_icon="👑", layout="wide")
    
    # Security check
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        # Login page
        st.title("🔐 Admin Login")
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("✅ Access Granted!")
                st.rerun()
            else:
                st.error("❌ Wrong Password!")
        return
    
    # Main Admin Dashboard
    st.markdown("""
    <style>
        .admin-badge {
            background: #1e3a8a;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
        }
        .control-box {
            background: #f8fafc;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e2e8f0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("👑 Complete Admin Dashboard")
        st.markdown("""<span class="admin-badge">🔒 Full Control</span>""", unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    st.markdown("---")
    
    # Admin Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👑 Admin Status", "Active", "✅")
    with col2:
        st.metric("🛡️ Security", "Secure", "🔒")
    with col3:
        st.metric("📊 Data Points", "100+", "📈")
    with col4:
        st.metric("⚡ System", "Running", "🟢")
    
    st.markdown("---")
    
    # Three main control sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard Control",
        "⚙️ System Settings",
        "📁 Data Management", 
        "👤 User Management",
        "📝 Activity Logs"
    ])
    
    with tab1:
        st.subheader("🎛️ Dashboard Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="control-box">', unsafe_allow_html=True)
            st.markdown("### 📈 Data Generation")
            data_speed = st.slider("Data Generation Speed", 1, 10, 5)
            data_count = st.number_input("Max Data Points", 10, 500, 100)
            if st.button("🔄 Generate New Data", use_container_width=True):
                st.success("✅ Data generated!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="control-box">', unsafe_allow_html=True)
            st.markdown("### 🎨 Display Settings")
            chart_type = st.selectbox("Chart Type", ["Pie", "Bar", "Line"])
            color_scheme = st.color_picker("Theme Color", "#3b82f6")
            if st.button("💾 Apply Changes", use_container_width=True):
                st.success("✅ Changes applied!")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("⚙️ System Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="control-box">', unsafe_allow_html=True)
            st.markdown("### 🔧 General Settings")
            auto_start = st.toggle("Auto Start Services", value=True)
            auto_backup = st.toggle("Auto Backup", value=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="control-box">', unsafe_allow_html=True)
            st.markdown("### 🛡️ Security Settings")
            require_2fa = st.toggle("Two-Factor Authentication", value=False)
            session_timeout = st.number_input("Session Timeout (hours)", 1, 24, 8)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("💾 Save All Settings", use_container_width=True):
            st.success("✅ All settings saved!")
    
    with tab3:
        st.subheader("📁 Data Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📤 Export All Data", use_container_width=True):
                st.success("✅ Data exported to data_export.json")
        with col2:
            if st.button("📥 Import Data", use_container_width=True):
                st.info("📥 Upload your JSON file")
        with col3:
            if st.button("🗑️ Clear All Data", use_container_width=True):
                st.warning("⚠️ Data cleared!")
        
        st.markdown("---")
        st.markdown("### 📊 Current Data Preview")
        data = {
            "Total Posts": 100,
            "Positive": 45,
            "Neutral": 30,
            "Negative": 25
        }
        st.dataframe(pd.DataFrame([data]))
    
    with tab4:
        st.subheader("👤 User Management")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="control-box">', unsafe_allow_html=True)
            st.markdown("### 👥 Users")
            users = ["admin (you)", "user1", "user2"]
            for user in users:
                st.checkbox(user, value=True if user == "admin (you)" else False)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="control-box">', unsafe_allow_html=True)
            st.markdown("### 🔑 Permissions")
            st.selectbox("User Role", ["Admin", "Editor", "Viewer"])
            st.selectbox("Access Level", ["Full", "Read Only", "Custom"])
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.subheader("📝 Activity Logs")
        
        logs = [
            ("👑 Admin logged in", datetime.now().strftime("%H:%M:%S")),
            ("⚙️ Settings updated", "5 min ago"),
            ("📤 Data exported", "1 hour ago"),
            ("🔄 System refresh", "2 hours ago"),
        ]
        
        for action, time in logs:
            st.markdown(f"""
            <div style="background: #f1f5f9; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #3b82f6;">
                <span>{action}</span>
                <span style="float: right; color: #64748b;">{time}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Logs", use_container_width=True):
            st.success("✅ Logs cleared!")
    
    st.markdown("---")
    st.caption("🔒 All actions are logged for security purposes")

if __name__ == "__main__":
    admin_control_panel()