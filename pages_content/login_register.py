"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Unified Student Registration and Login Portal
"""

import streamlit as st
from config import COLLEGE_NAME, DEPARTMENTS, YEARS_OF_STUDY
from auth import authenticate_user, register_user
from components.ui_helpers import login_user

def render_login_register_page() -> None:
    """Render unified login and registration interface."""
    # College Hero Section
    st.markdown(
        f"""
        <div style="text-align: center; padding: 24px 10px 10px 10px;">
            <div style="display: inline-block; background: #e0e7ff; color: #3730a3; padding: 6px 18px; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px;">
                Official Peer Learning Network
            </div>
            <h1 style="color: #1e3a8a; font-size: 2.3rem; font-weight: 800; margin-bottom: 6px; letter-spacing: -0.02em;">
                {COLLEGE_NAME}
            </h1>
            <p style="color: #475569; font-size: 1.05rem; max-width: 650px; margin: 0 auto 24px auto;">
                Connect with peers, master challenging engineering coursework, schedule 1-on-1 tutoring, and share knowledge across departments.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_login, tab_register, tab_demo = st.tabs(["🔐 Sign In to Campus Portal", "📝 New Student Registration", "⚡ Quick Demo Access"])

    with tab_login:
        st.markdown("##### Enter your college credentials")
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("College Email Address", placeholder="e.g., student.cse@sece.ac.in")
            password = st.text_input("Password", type="password", placeholder="Enter your account password")
            submitted = st.form_submit_button("Sign In to Platform", use_container_width=True, type="primary")

            if submitted:
                success, msg, user_data = authenticate_user(email, password)
                if success and user_data:
                    login_user(user_data)
                    st.success(f"Welcome back, {user_data['name']}!")
                    st.rerun()
                else:
                    st.error(msg)

    with tab_register:
        st.markdown("##### Create a Unified Student Account (Learner & Peer Tutor)")
        st.caption("One account lets you search for tutors, schedule sessions, and also offer tutoring in your strong subjects.")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *", placeholder="e.g. Anandha Kumar")
                email = st.text_input("College Email *", placeholder="e.g. anand.cse@sece.ac.in")
                password = st.text_input("Create Password *", type="password", help="Minimum 6 characters")
            with col2:
                dept = st.selectbox("Department *", DEPARTMENTS)
                year = st.selectbox("Year of Study *", YEARS_OF_STUDY)
                interests = st.text_input("Learning Interests / Skills Seeking", placeholder="e.g. Python, DSA, IoT, AI")

            bio = st.text_area("Short Bio", placeholder="Tell fellow students about your academic background or subjects you can help with...")

            reg_submit = st.form_submit_button("Complete Registration", use_container_width=True, type="primary")
            if reg_submit:
                success, msg, uid = register_user(
                    name=name,
                    email=email,
                    password=password,
                    department=dept,
                    year_of_study=year,
                    bio=bio,
                    learning_interests=interests,
                )
                if success:
                    st.success(msg)
                    st.info("You can now switch to the 'Sign In' tab to log in.")
                else:
                    st.error(msg)

    with tab_demo:
        st.markdown("##### Fast Demo Profiles for Project Evaluation")
        st.caption("Click any persona below to immediately log in and explore features with realistic pre-populated data:")
        
        demo_cols = st.columns(3)
        with demo_cols[0]:
            st.markdown(
                """
                <div style="background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                    <strong>Kavya Sundaram</strong><br/>
                    <small style="color: #64748b;">CSE • 3rd Year<br/>Active Tutor (DSA, Python)</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Log In as Kavya (Tutor)", key="demo_kavya", use_container_width=True):
                success, msg, u = authenticate_user("kavya.cse@sece.ac.in", "student123")
                if success and u:
                    login_user(u)
                    st.rerun()

        with demo_cols[1]:
            st.markdown(
                """
                <div style="background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                    <strong>Rahul Ramanathan</strong><br/>
                    <small style="color: #64748b;">EEE • 2nd Year<br/>Active Learner</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Log In as Rahul (Learner)", key="demo_rahul", use_container_width=True):
                success, msg, u = authenticate_user("rahul.eee@sece.ac.in", "student123")
                if success and u:
                    login_user(u)
                    st.rerun()

        with demo_cols[2]:
            st.markdown(
                """
                <div style="background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                    <strong>Dean of Academics</strong><br/>
                    <small style="color: #64748b;">Admin & Faculty<br/>College Analytics Access</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Log In as College Admin", key="demo_admin", use_container_width=True):
                success, msg, u = authenticate_user("admin@sece.ac.in", "admin123")
                if success and u:
                    login_user(u)
                    st.rerun()
