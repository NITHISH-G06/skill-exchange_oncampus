"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Session Management (Learner Bookings, Tutor Requests, Google Meet Links & Reviews)
"""

import streamlit as st
from datetime import datetime
from db_ops import (
    get_requests_for_learner,
    get_requests_for_tutor,
    update_request_status,
    create_review,
    has_reviewed_session,
    get_request_by_id,
)
from services.calendar_service import schedule_online_meeting
from components.ui_helpers import get_current_user, render_status_badge
from config import STATUS_ACCEPTED, STATUS_DECLINED, STATUS_COMPLETED, STATUS_PENDING

def render_my_sessions_page() -> None:
    """Render Sessions Dashboard: Outgoing Learner Sessions and Incoming Tutor Requests."""
    user = get_current_user()
    if not user:
        st.warning("Please log in to manage your learning sessions.")
        return

    st.markdown("### 📅 My Learning & Tutoring Sessions")
    st.caption("Track scheduled meetings, join Google Meet rooms, coordinate on-campus spots, and review tutors.")

    tab_incoming, tab_outgoing = st.tabs([
        "📥 Incoming Requests (As a Tutor)",
        "📤 Outgoing Bookings (As a Learner)",
    ])

    # ==========================================
    # 1. INCOMING REQUESTS (AS TUTOR)
    # ==========================================
    with tab_incoming:
        tutor_requests = get_requests_for_tutor(user["id"])
        st.markdown(f"##### Requests from Students Seeking Your Help ({len(tutor_requests)})")

        if not tutor_requests:
            st.info("No incoming tutoring requests yet. When students book sessions from your listings, they will appear here.")
        else:
            for req in tutor_requests:
                with st.expander(
                    f"[{req['status'].upper()}] {req.get('subject') or 'Tutoring'} with {req['learner_name']} on {req['session_date']} at {req['session_time']}",
                    expanded=(req["status"] == STATUS_PENDING),
                ):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Student:** {req['learner_name']} ({req['learner_email']})")
                        st.markdown(f"**Department:** {req['learner_dept']} • Year: {req['learner_year']}")
                        st.markdown(f"**Mode:** `{req['mode']}`")
                        st.markdown(f"**Scheduled Date & Time:** 📅 {req['session_date']} at ⏰ {req['session_time']}")

                        if req["mode"] == "ON_CAMPUS":
                            st.markdown(f"**Meeting Spot (Sri Eshwar):** 📍 `{req['meeting_spot']}`")
                        elif req["mode"] == "ONLINE" and req.get("google_meet_link"):
                            is_demo = req.get("is_demo_link", False)
                            link = req["google_meet_link"]
                            if is_demo:
                                st.warning(f"⚠️ **Google Meet (Demo Mode):** [{link}]({link.replace('[DEMO MODE] ', '')})")
                            else:
                                st.success(f"🔗 **Google Meet Link:** [{link}]({link})")

                        if req.get("notes"):
                            st.info(f"**Student's Note/Doubt:** {req['notes']}")
                        if req.get("tutor_response_note"):
                            st.write(f"**Your Response:** {req['tutor_response_note']}")

                    with col2:
                        st.markdown(f"**Status:** {render_status_badge(req['status'])}", unsafe_allow_html=True)
                        st.markdown(f"**Session Fee:** `₹{req['price']:.2f}`" if req['price'] > 0 else "**Session Fee:** `Free`")
                        if req["price"] > 0:
                            st.caption(f"Platform commission: ₹{req['commission_amount']:.2f} (10%)")

                        st.write("---")

                        # Actions depending on status
                        if req["status"] == STATUS_PENDING:
                            tutor_resp = st.text_input("Note for student (optional)", key=f"tutor_note_{req['id']}")
                            
                            c_acc, c_dec = st.columns(2)
                            with c_acc:
                                if st.button("Accept Request", key=f"acc_{req['id']}", type="primary", use_container_width=True):
                                    # If Online, generate Meet link (or labeled demo fallback)
                                    meet_url = ""
                                    is_demo = False
                                    if req["mode"] == "ONLINE":
                                        meet_url, is_demo, _ = schedule_online_meeting(
                                            tutor_name=user["name"],
                                            tutor_email=user["email"],
                                            learner_name=req["learner_name"],
                                            learner_email=req["learner_email"],
                                            subject=req.get("subject", "Tutoring"),
                                            session_date=req["session_date"],
                                            session_time=req["session_time"],
                                        )

                                    succ, msg = update_request_status(
                                        request_id=req["id"],
                                        user_id=user["id"],
                                        new_status=STATUS_ACCEPTED,
                                        tutor_note=tutor_resp,
                                        meet_link=meet_url,
                                        is_demo_link=is_demo,
                                    )
                                    if succ:
                                        st.success("Session accepted!")
                                        st.rerun()
                                    else:
                                        st.error(msg)

                            with c_dec:
                                if st.button("Decline", key=f"dec_{req['id']}", use_container_width=True):
                                    succ, msg = update_request_status(
                                        request_id=req["id"],
                                        user_id=user["id"],
                                        new_status=STATUS_DECLINED,
                                        tutor_note=tutor_resp,
                                    )
                                    if succ:
                                        st.warning("Session declined.")
                                        st.rerun()
                                    else:
                                        st.error(msg)

                        elif req["status"] == STATUS_ACCEPTED:
                            if st.button("Mark Session Completed 🎓", key=f"complete_t_{req['id']}", type="primary"):
                                succ, msg = update_request_status(req["id"], user["id"], STATUS_COMPLETED)
                                if succ:
                                    st.success("Session marked as completed!")
                                    st.rerun()
                                else:
                                    st.error(msg)

    # ==========================================
    # 2. OUTGOING REQUESTS (AS LEARNER)
    # ==========================================
    with tab_outgoing:
        learner_requests = get_requests_for_learner(user["id"])
        st.markdown(f"##### Your Bookings with Peer Tutors ({len(learner_requests)})")

        if not learner_requests:
            st.info("You haven't requested any tutoring sessions yet. Go to 'Browse & Book Peer Tutors' to schedule one!")
        else:
            for req in learner_requests:
                with st.expander(
                    f"[{req['status'].upper()}] {req.get('subject') or 'Tutoring'} with {req['tutor_name']} on {req['session_date']} at {req['session_time']}",
                    expanded=(req["status"] == STATUS_ACCEPTED),
                ):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Tutor:** {req['tutor_name']} ({req['tutor_email']}) • {req['tutor_dept']}")
                        st.markdown(f"**Mode:** `{req['mode']}`")
                        st.markdown(f"**Date & Time:** 📅 {req['session_date']} at ⏰ {req['session_time']}")

                        if req["mode"] == "ON_CAMPUS":
                            st.markdown(f"**Campus Meeting Spot:** 📍 `{req['meeting_spot']}`")
                        elif req["mode"] == "ONLINE":
                            if req["status"] == STATUS_ACCEPTED and req.get("google_meet_link"):
                                link = req["google_meet_link"]
                                is_demo = req.get("is_demo_link", False)
                                if is_demo:
                                    raw_link = link.replace("[DEMO MODE] ", "")
                                    st.warning(f"⚠️ **Google Meet (Demo Mode):** [Click to Join Meeting]({raw_link})\n\n`{link}`")
                                else:
                                    st.success(f"🔗 **Google Meet Link:** [Click to Join Meeting]({link})")
                            elif req["status"] == STATUS_PENDING:
                                st.info("Google Meet link will be generated once tutor accepts your request.")

                        if req.get("tutor_response_note"):
                            st.write(f"**Tutor Note:** {req['tutor_response_note']}")

                    with col2:
                        st.markdown(f"**Status:** {render_status_badge(req['status'])}", unsafe_allow_html=True)
                        st.markdown(f"**Cost:** `₹{req['price']:.2f}`" if req['price'] > 0 else "**Cost:** `Free`")

                        # If Accepted, learner can also mark completed
                        if req["status"] == STATUS_ACCEPTED:
                            if st.button("Mark as Completed", key=f"complete_l_{req['id']}"):
                                succ, msg = update_request_status(req["id"], user["id"], STATUS_COMPLETED)
                                if succ:
                                    st.success("Session completed!")
                                    st.rerun()

                    # Review Section for Completed Sessions
                    if req["status"] == STATUS_COMPLETED:
                        st.write("---")
                        already_reviewed = has_reviewed_session(req["id"])
                        if already_reviewed:
                            st.success("✅ You have already submitted a review for this session. Thank you!")
                        else:
                            st.markdown("##### ⭐ Leave Feedback & Rating for Tutor")
                            with st.form(f"review_form_{req['id']}"):
                                rating_val = st.slider("Rating (1 = Poor, 5 = Excellent)", min_value=1, max_value=5, value=5)
                                rev_comment = st.text_area("Your Review", placeholder="How was the tutoring session? Was the explanation clear?")
                                submit_rev = st.form_submit_button("Submit Review", type="primary")

                                if submit_rev:
                                    succ, msg = create_review(
                                        request_id=req["id"],
                                        learner_id=user["id"],
                                        tutor_id=req["tutor_id"],
                                        rating=rating_val,
                                        review_text=rev_comment,
                                    )
                                    if succ:
                                        st.success(msg)
                                        st.rerun()
                                    else:
                                        st.error(msg)
