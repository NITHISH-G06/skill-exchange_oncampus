"""
Sri Eshwar College of Engineering - Campus Skill Exchange & Peer Learning Platform
Main Application Entrance & Page Router
"""

import streamlit as st
from database import init_db
from components.ui_helpers import (
    init_session_state,
    get_current_user,
    is_logged_in,
    logout_user,
    render_college_header,
)
from components.background import render_interactive_background
from pages_content.login_register import render_login_register_page
from pages_content.profile_view import render_profile_page
from pages_content.listings_view import render_listings_page
from pages_content.my_sessions_view import render_my_sessions_page
from pages_content.async_help_view import render_async_help_page
from pages_content.admin_dashboard_view import render_admin_dashboard_page
from config import COLLEGE_NAME

# Configure Streamlit Page
st.set_page_config(
    page_title=f"{COLLEGE_NAME} - Peer Learning",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    # 1. Initialize Database Schema and Session
    init_db()
    init_session_state()

    # 2. Render subtle interactive connected nodes background
    render_interactive_background()

    # 3. Check Authentication State
    authenticated = is_logged_in()
    current_user = get_current_user()

    # 4. Sidebar Navigation & Branding
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px 0 16px 0;">
                <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 12px; width: 50px; height: 50px; margin: 0 auto 8px auto; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white;">
                    SE
                </div>
                <div style="font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.08em;">
                    Campus Skill Exchange
                </div>
                <div style="font-size: 1rem; font-weight: 800; color: #ffffff; line-height: 1.2;">
                    {COLLEGE_NAME}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        if authenticated and current_user:
            st.markdown(
                f"""
                <div style="background: #1e293b; border-radius: 8px; padding: 12px; margin-bottom: 16px;">
                    <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Logged In As</div>
                    <div style="font-weight: 700; color: #38bdf8; font-size: 1.05rem;">{current_user['name']}</div>
                    <div style="font-size: 0.8rem; color: #cbd5e1;">{current_user.get('department', '').split('(')[-1].replace(')', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            nav_choice = st.radio(
                "Navigation",
                [
                    "🔍 Browse & Book Tutors",
                    "📅 My Sessions & Reviews",
                    "💬 Peer Q&A Board",
                    "🧑‍🎓 My Profile & Tutoring",
                    "📊 College Analytics Dashboard",
                ],
                label_visibility="collapsed",
            )

            st.divider()
            if st.button("🚪 Sign Out", use_container_width=True, type="secondary"):
                logout_user()
                st.rerun()

        else:
            st.markdown("##### 🏛️ Sri Eshwar Portal")
            st.caption("Sign in to book peer sessions, ask questions, or review college analytics.")
            
            nav_choice = st.radio(
                "Portal View",
                ["🔐 Sign In / Register", "📊 Public College Analytics"],
                label_visibility="collapsed",
            )

        st.markdown(
            """
            <div style="margin-top: 50px; font-size: 0.72rem; color: #64748b; text-align: center;">
                Sri Eshwar College of Engineering<br/>
                Engineering Project • 2026
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 5. Page Routing
    if not authenticated:
        if nav_choice == "📊 Public College Analytics":
            render_college_header()
            render_admin_dashboard_page()
        else:
            render_login_register_page()
    else:
        render_college_header()
        
        if nav_choice == "🔍 Browse & Book Tutors":
            render_listings_page()
        elif nav_choice == "📅 My Sessions & Reviews":
            render_my_sessions_page()
        elif nav_choice == "💬 Peer Q&A Board":
            render_async_help_page()
        elif nav_choice == "🧑‍🎓 My Profile & Tutoring":
            render_profile_page()
        elif nav_choice == "📊 College Analytics Dashboard":
            render_admin_dashboard_page()

if __name__ == "__main__":
    main()
