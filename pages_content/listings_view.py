"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Tutor Listings Marketplace & Booking Portal
"""

from datetime import datetime, date
import streamlit as st
from config import CAMPUS_MEETING_SPOTS, POPULAR_SKILLS, MODE_ONLINE, MODE_ON_CAMPUS, MODE_ASYNC
from db_ops import (
    search_listings,
    get_tutor_listings,
    create_listing,
    update_listing,
    toggle_listing_status,
    create_session_request,
)
from components.ui_helpers import get_current_user, render_star_rating, render_mode_badges

def render_listings_page() -> None:
    """Render Marketplace and Listing Management tabs."""
    user = get_current_user()

    tab_browse, tab_manage = st.tabs(["🔍 Browse & Book Peer Tutors", "📚 Offer Tutoring / My Listings"])

    with tab_browse:
        st.markdown("### Find a Peer Tutor at Sri Eshwar")
        st.caption("Search across academic subjects, filter by learning mode or price, and schedule peer learning sessions.")

        # Filter bar
        col_s, col_m, col_p = st.columns([2, 1, 1])
        with col_s:
            search_query = st.text_input("Search subject, keyword, or tutor name", placeholder="e.g. Data Structures, Python, ECE, ML")
        with col_m:
            mode_filter = st.selectbox("Mode", ["All", "ONLINE", "ON_CAMPUS", "ASYNCHRONOUS"])
        with col_p:
            price_filter = st.selectbox("Pricing", ["All", "Free Only", "Paid Only"])

        # Fetch matching listings (exclude user's own from browse if logged in)
        listings = search_listings(
            subject_query=search_query,
            mode_filter=mode_filter,
            price_filter=price_filter,
            exclude_user_id=user["id"] if user else None,
        )

        if not listings:
            st.info("No tutoring listings found matching your search criteria. Try adjusting the filters or be the first to offer tutoring!")
        else:
            st.markdown(f"**Showing {len(listings)} available tutor listings:**")
            
            for item in listings:
                with st.container():
                    st.markdown(
                        f"""
                        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px 22px; margin-bottom: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                                <div>
                                    <h4 style="margin: 0; color: #1e3a8a; font-size: 1.25rem;">{item['subject']}</h4>
                                    <div style="margin-top: 4px; font-size: 0.88rem; color: #475569;">
                                        Tutor: <strong>{item['tutor_name']}</strong> ({item['tutor_dept']} • {item['tutor_year']})
                                    </div>
                                    <div style="margin-top: 4px;">
                                        {render_star_rating(item['avg_rating'], item['review_count'])}
                                    </div>
                                </div>
                                <div style="text-align: right;">
                                    {"<span class='badge-free'>FREE MENTORSHIP</span>" if not item['is_paid'] else f"<span class='badge-paid'>₹{item['price']:.2f} / session</span>"}
                                </div>
                            </div>
                            <div style="margin-top: 10px; color: #334155; font-size: 0.92rem; line-height: 1.45;">
                                {item['description']}
                            </div>
                            <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; border-top: 1px solid #f1f5f9; padding-top: 10px;">
                                <div>
                                    <span style="font-size: 0.8rem; color: #64748b; font-weight: 600;">Modes: </span>
                                    {render_mode_badges(item['modes'])}
                                </div>
                                <div style="font-size: 0.8rem; color: #64748b;">
                                    ⏰ <strong>Availability:</strong> {item['availability']}
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Action buttons
                    b_col1, b_col2 = st.columns([4, 1])
                    with b_col2:
                        book_clicked = st.button("Request Session", key=f"book_btn_{item['id']}", use_container_width=True, type="primary")
                        if book_clicked:
                            st.session_state.booking_listing = item

            # Interactive Booking Dialog when a listing is selected
            if "booking_listing" in st.session_state and st.session_state.booking_listing:
                selected_item = st.session_state.booking_listing
                st.divider()
                st.markdown(f"#### 📅 Schedule Session: {selected_item['subject']} with {selected_item['tutor_name']}")
                
                with st.form(f"request_session_form_{selected_item['id']}"):
                    # Filter allowed modes for this listing
                    allowed_modes = [m.strip() for m in selected_item['modes'].split(",") if m.strip() and m.strip() in [MODE_ONLINE, MODE_ON_CAMPUS]]
                    if not allowed_modes:
                        allowed_modes = [MODE_ONLINE, MODE_ON_CAMPUS]

                    b_mode = st.radio("Choose Session Mode *", allowed_modes, horizontal=True)

                    c_d, c_t = st.columns(2)
                    with c_d:
                        sess_date = st.date_input("Date *", min_value=date.today())
                    with c_t:
                        sess_time = st.time_input("Session Start Time *")

                    meeting_spot = ""
                    if b_mode == MODE_ON_CAMPUS:
                        meeting_spot = st.selectbox("Campus Meeting Spot (Sri Eshwar) *", CAMPUS_MEETING_SPOTS)
                        st.caption("📍 Note: Both campus location and time are mandatory for On-Campus sessions.")
                    else:
                        st.info("💻 Online Session: When the tutor accepts, a Google Meet link will be generated automatically and attached to your session request.")

                    req_notes = st.text_area("Learning Objectives / Specific Doubts", placeholder="E.g., I'd like help with Graph Traversal (DFS/BFS) and preparing for lab test.")

                    price_display = f"₹{selected_item['price']:.2f}" if selected_item['is_paid'] else "Free (Peer Support)"
                    st.markdown(f"**Session Cost:** `{price_display}`")

                    col_sub, col_can = st.columns(2)
                    with col_sub:
                        submit_req = st.form_submit_button("Submit Session Request", type="primary", use_container_width=True)
                    with col_can:
                        cancel_req = st.form_submit_button("Cancel", use_container_width=True)

                    if submit_req:
                        if not user:
                            st.error("Please log in first to submit a session request.")
                        else:
                            success, msg, req_id = create_session_request(
                                listing_id=selected_item["id"],
                                learner_id=user["id"],
                                tutor_id=selected_item["tutor_id"],
                                mode=b_mode,
                                session_date=sess_date.strftime("%Y-%m-%d"),
                                session_time=sess_time.strftime("%H:%M"),
                                meeting_spot=meeting_spot,
                                notes=req_notes,
                                price=selected_item["price"] if selected_item["is_paid"] else 0.0,
                            )
                            if success:
                                st.success("🎉 " + msg)
                                st.session_state.booking_listing = None
                                st.info("Check 'My Sessions' tab to track your tutor's response.")
                            else:
                                st.error(msg)

                    if cancel_req:
                        st.session_state.booking_listing = None
                        st.rerun()

    with tab_manage:
        st.markdown("### Manage Your Tutoring Offerings")
        st.caption("Share your knowledge with fellow Sri Eshwar students. Create listings for subjects you are confident in.")

        if not user:
            st.warning("Please log in to offer tutoring.")
            return

        with st.expander("➕ Create a New Tutoring Listing", expanded=False):
            with st.form("create_listing_form"):
                subject_choice = st.selectbox("Select Subject / Skill", POPULAR_SKILLS + ["Custom Skill..."])
                custom_subject = ""
                if subject_choice == "Custom Skill...":
                    custom_subject = st.text_input("Enter Custom Subject / Skill Name *")
                
                final_subject = custom_subject if subject_choice == "Custom Skill..." else subject_choice

                desc = st.text_area("Description *", placeholder="What topics will you cover? (e.g. Trees, Sorting, Exam preparation)")

                c_p1, c_p2 = st.columns(2)
                with c_p1:
                    is_paid = st.checkbox("Charge a fee (Paid Tutoring)?", value=False)
                with c_p2:
                    price_val = st.number_input("Session Fee (₹)", min_value=0.0, max_value=2000.0, value=100.0, step=25.0) if is_paid else 0.0

                st.markdown("**Available Learning Modes ***")
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    mode_online_chk = st.checkbox("💻 Online (Google Meet)", value=True)
                with col_m2:
                    mode_oncampus_chk = st.checkbox("🏫 On-Campus (Sri Eshwar)", value=True)
                with col_m3:
                    mode_async_chk = st.checkbox("❓ Asynchronous Q&A", value=True)

                avail = st.text_input("Your Availability Schedule *", placeholder="e.g. Mon, Wed: 4:30 PM - 6:30 PM; Sat: 10:00 AM - 1:00 PM")

                create_btn = st.form_submit_button("Publish Tutoring Listing", type="primary", use_container_width=True)

                if create_btn:
                    selected_modes = []
                    if mode_online_chk: selected_modes.append("ONLINE")
                    if mode_oncampus_chk: selected_modes.append("ON_CAMPUS")
                    if mode_async_chk: selected_modes.append("ASYNCHRONOUS")

                    success, msg, lid = create_listing(
                        tutor_id=user["id"],
                        subject=final_subject,
                        description=desc,
                        is_paid=is_paid,
                        price=price_val,
                        modes=selected_modes,
                        availability=avail,
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        # List existing listings for this tutor
        my_listings = get_tutor_listings(user["id"], include_inactive=True)
        st.markdown(f"##### Your Active & Archived Listings ({len(my_listings)})")

        if not my_listings:
            st.info("You haven't posted any tutoring listings yet. Use the form above to post your first skill!")
        else:
            for my_l in my_listings:
                status_color = "#15803d" if my_l["is_active"] else "#64748b"
                status_text = "ACTIVE" if my_l["is_active"] else "DEACTIVATED"

                with st.expander(f"{my_l['subject']} — [{status_text}]"):
                    st.write(f"**Description:** {my_l['description']}")
                    st.write(f"**Pricing:** {'Free Peer Mentoring' if not my_l['is_paid'] else f'₹{my_l['price']:.2f}'}")
                    st.write(f"**Modes:** {my_l['modes']}")
                    st.write(f"**Availability:** {my_l['availability']}")

                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        if my_l["is_active"]:
                            if st.button("Deactivate Listing", key=f"deact_{my_l['id']}"):
                                toggle_listing_status(my_l["id"], user["id"], False)
                                st.rerun()
                        else:
                            if st.button("Reactivate Listing", key=f"react_{my_l['id']}"):
                                toggle_listing_status(my_l["id"], user["id"], True)
                                st.rerun()
