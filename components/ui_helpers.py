"""
Sri Eshwar College of Engineering - Campus Skill Exchange
UI Helpers, Branding Banners, Badges, and Session State Management.
"""

import streamlit as st
from typing import Optional, Dict, Any
from config import COLLEGE_NAME, COLLEGE_TAGLINE

def init_session_state() -> None:
    """Initialize standard keys in Streamlit session_state."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Marketplace"
    if "selected_listing_id" not in st.session_state:
        st.session_state.selected_listing_id = None
    if "selected_question_id" not in st.session_state:
        st.session_state.selected_question_id = None

def get_current_user() -> Optional[Dict[str, Any]]:
    """Return currently authenticated student user record."""
    return st.session_state.get("user")

def is_logged_in() -> bool:
    """Check if a session is currently active."""
    return bool(st.session_state.get("authenticated") and st.session_state.get("user"))

def login_user(user_data: Dict[str, Any]) -> None:
    """Set active user session."""
    st.session_state.authenticated = True
    st.session_state.user = user_data

def logout_user() -> None:
    """Clear user session."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.selected_listing_id = None
    st.session_state.selected_question_id = None

def render_college_header(show_logo: bool = True) -> None:
    """Render prominent Sri Eshwar College of Engineering branding."""
    col1, col2 = st.columns([1, 8])
    with col1:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 12px; width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; color: white; font-size: 30px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                SE
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div style="margin-left: -10px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #2563eb; letter-spacing: 0.1em; text-transform: uppercase;">
                    College of Engineering & Technology
                </div>
                <div style="font-size: 1.55rem; font-weight: 800; color: #1e3a8a; line-height: 1.2;">
                    {COLLEGE_NAME}
                </div>
                <div style="font-size: 0.85rem; color: #64748b; font-weight: 500;">
                    {COLLEGE_TAGLINE}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.divider()

def render_star_rating(avg_rating: float, review_count: int) -> str:
    """Generate HTML snippet for star rating display."""
    if review_count == 0:
        return "<span style='color: #94a3b8; font-size: 0.85rem;'>⭐ New Peer Tutor</span>"
    stars = "★" * int(round(avg_rating)) + "☆" * (5 - int(round(avg_rating)))
    return f"<span style='color: #eab308; font-weight: 700;'>{stars} {avg_rating}</span> <span style='color: #64748b; font-size: 0.82rem;'>({review_count} reviews)</span>"

def render_status_badge(status: str) -> str:
    """Return styled HTML badge for session statuses."""
    status_lower = status.lower()
    styles = {
        "pending": ("#fef3c7", "#b45309", "⏳ Pending Tutor Acceptance"),
        "accepted": ("#dcfce7", "#15803d", "✅ Accepted & Scheduled"),
        "declined": ("#fee2e2", "#b91c1c", "❌ Declined"),
        "completed": ("#e0e7ff", "#4338ca", "🎓 Session Completed"),
    }
    bg, fg, label = styles.get(status_lower, ("#f1f5f9", "#475569", status.title()))
    return f"<span style='background-color: {bg}; color: {fg}; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.8rem; display: inline-block;'>{label}</span>"

def render_mode_badges(modes_str: str) -> str:
    """Return styled badge HTML for available learning modes."""
    badges = []
    modes = [m.strip() for m in modes_str.split(",") if m.strip()]
    for m in modes:
        if m == "ONLINE":
            badges.append("<span style='background: #dbeafe; color: #1e40af; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>💻 Online (Google Meet)</span>")
        elif m == "ON_CAMPUS":
            badges.append("<span style='background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>🏫 On-Campus</span>")
        elif m == "ASYNCHRONOUS":
            badges.append("<span style='background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>❓ Async Q&A</span>")
    return " ".join(badges)
