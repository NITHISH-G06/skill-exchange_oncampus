"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Student Profile & Unified Learner/Tutor Management
"""

import streamlit as st
from config import COLLEGE_NAME, DEPARTMENTS, YEARS_OF_STUDY
from auth import update_user_profile, get_user_by_id
from db_ops import get_tutor_rating_summary, get_tutor_reviews, get_tutor_listings
from components.ui_helpers import get_current_user, render_star_rating

def render_profile_page() -> None:
    """Render profile view and edit options for the logged-in student."""
    user = get_current_user()
    if not user:
        st.warning("Please log in to view your profile.")
        return

    # Refresh user data from database
    refreshed_user = get_user_by_id(user["id"])
    if refreshed_user:
        user = refreshed_user
        st.session_state.user = refreshed_user

    # Prominent College Branding on Profile Screen
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); color: white; padding: 22px 28px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 4px 10px rgba(30, 58, 138, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <div style="text-transform: uppercase; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.12em; color: #93c5fd;">
                        Official Student Identity
                    </div>
                    <h2 style="margin: 4px 0 6px 0; color: #ffffff; font-size: 1.85rem; font-weight: 800;">
                        {COLLEGE_NAME}
                    </h2>
                    <div style="font-size: 0.9rem; color: #e2e8f0;">
                        Campus Peer Learning & Skill Exchange Network
                    </div>
                </div>
                <div style="text-align: right; background: rgba(255,255,255,0.15); padding: 8px 16px; border-radius: 8px; backdrop-filter: blur(4px);">
                    <div style="font-size: 0.75rem; text-transform: uppercase; color: #bfdbfe; font-weight: 600;">Account Status</div>
                    <div style="font-weight: 700; font-size: 1rem; color: #ffffff;">Unified Learner & Peer Tutor</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tutor_stats = get_tutor_rating_summary(user["id"])
    tutor_listings = get_tutor_listings(user["id"])
    reviews = get_tutor_reviews(user["id"])

    # Student KPI / Highlights
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.metric("Tutor Average Rating", f"⭐ {tutor_stats['avg_rating']}/5.0" if tutor_stats['review_count'] > 0 else "N/A")
    with stat_col2:
        st.metric("Peer Reviews Received", tutor_stats["review_count"])
    with stat_col3:
        st.metric("Active Tutoring Listings", sum(1 for l in tutor_listings if l["is_active"]))
    with stat_col4:
        st.metric("Department", user.get("department", "").split("(")[-1].replace(")", "") if "(" in user.get("department", "") else "SECE")

    st.markdown("<br/>", unsafe_allow_html=True)

    tab_overview, tab_edit, tab_reviews = st.tabs(["👤 Profile Card", "✏️ Edit Academic Profile", "⭐ Peer Reviews Received"])

    with tab_overview:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(
                f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                    <div style="width: 80px; height: 80px; border-radius: 50%; background: #3b82f6; color: white; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 800; margin: 0 auto 12px auto;">
                        {user['name'][:1].upper()}
                    </div>
                    <h3 style="margin-bottom: 2px; color: #0f172a;">{user['name']}</h3>
                    <div style="color: #2563eb; font-weight: 600; font-size: 0.9rem; margin-bottom: 8px;">{user['email']}</div>
                    <div style="background: #f1f5f9; padding: 4px 12px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; color: #475569; display: inline-block;">
                        {user['year_of_study']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                    <h4 style="color: #1e3a8a; margin-top: 0;">Academic Details</h4>
                    <p><strong>Department:</strong> {user['department']}</p>
                    <p><strong>Year of Study:</strong> {user['year_of_study']}</p>
                    <p><strong>Learning Interests & Skills Seeking:</strong><br/>
                       <span style="color: #475569;">{user.get('learning_interests') or 'None specified yet'}</span>
                    </p>
                    <p><strong>About Me / Bio:</strong><br/>
                       <span style="color: #475569;">{user.get('bio') or 'No biography provided yet. Click the Edit tab to add your bio!'}</span>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_edit:
        st.markdown("##### Update Profile Information")
        with st.form("edit_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Full Name *", value=user["name"])
                dept_index = DEPARTMENTS.index(user["department"]) if user["department"] in DEPARTMENTS else 0
                new_dept = st.selectbox("Department *", DEPARTMENTS, index=dept_index)
            with col2:
                year_index = YEARS_OF_STUDY.index(user["year_of_study"]) if user["year_of_study"] in YEARS_OF_STUDY else 0
                new_year = st.selectbox("Year of Study *", YEARS_OF_STUDY, index=year_index)
                new_interests = st.text_input("Learning Interests", value=user.get("learning_interests", ""))

            new_bio = st.text_area("Short Bio", value=user.get("bio", ""))
            
            save_btn = st.form_submit_button("Save Profile Changes", type="primary")
            if save_btn:
                success, msg = update_user_profile(
                    user_id=user["id"],
                    name=new_name,
                    department=new_dept,
                    year_of_study=new_year,
                    bio=new_bio,
                    learning_interests=new_interests,
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with tab_reviews:
        st.markdown(f"##### Student Feedback for {user['name']}")
        if not reviews:
            st.info("No reviews received yet. Once you complete tutoring sessions with peers, their feedback will appear here.")
        else:
            for rev in reviews:
                st.markdown(
                    f"""
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong>{rev['learner_name']}</strong> ({rev['learner_dept']})
                            <span>{"⭐" * rev['rating']}</span>
                        </div>
                        <div style="color: #64748b; font-size: 0.8rem; margin-top: 2px;">
                            Session on {rev.get('subject', 'Tutoring')} • Date: {rev['session_date']}
                        </div>
                        <div style="margin-top: 8px; color: #334155; font-style: italic;">
                            "{rev.get('review_text') or 'No comment provided.'}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
