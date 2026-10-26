"""
Sri Eshwar College of Engineering - Campus Skill Exchange
College Administration Analytics Dashboard & Revenue Visualizations
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from config import POPULAR_SKILLS, COLLEGE_NAME, PLATFORM_COMMISSION_PERCENT
from db_ops import get_analytics_metrics
from seed_data import seed_sample_data

# Dual-mode data analysis support: use pandas if system policy permits, else native aggregation
try:
    import pandas as pd
    HAS_PANDAS = True
except (ImportError, Exception):
    pd = None
    HAS_PANDAS = False

def render_admin_dashboard_page() -> None:
    """Render comprehensive interactive college analytics with Plotly charts."""
    st.markdown("### 📊 College Academic & Peer Tutoring Analytics")
    st.caption(f"Aggregated learning trends, engagement metrics, and revenue model simulation for {COLLEGE_NAME}.")

    # Sample Data Loader / Seeder Action Bar
    with st.expander("⚙️ Dataset Management & Sample Data Controls", expanded=False):
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            st.info("💡 You can reset or reload realistic Sri Eshwar academic sample data for project demonstration at any time.")
        with col_s2:
            if st.button("Reload Sample Dataset", type="secondary", use_container_width=True):
                seed_sample_data(reset_existing=True)
                st.success("Sample data reloaded!")
                st.rerun()

    # Dashboard Filters
    st.markdown("##### 🔍 Analytics Filters")
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        subject_filter = st.selectbox("Filter by Subject", ["All"] + POPULAR_SKILLS, key="admin_subj_filter")
    with col_f2:
        start_date = st.date_input("From Date", value=None, key="admin_start_date")
    with col_f3:
        end_date = st.date_input("To Date", value=None, key="admin_end_date")

    from_str = start_date.strftime("%Y-%m-%d") if start_date else None
    to_str = end_date.strftime("%Y-%m-%d") if end_date else None

    # Fetch aggregated data
    metrics = get_analytics_metrics(
        subject_filter=subject_filter,
        date_from=from_str,
        date_to=to_str,
    )

    if metrics["total_all_requests"] == 0 and metrics["total_users"] == 0:
        st.warning("⚠️ The database is currently empty. Click 'Reload Sample Dataset' above to populate sample records.")
        return

    # Top KPI Metrics Row
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Total Students", metrics["total_users"])
    with kpi2:
        st.metric("Active Listings", metrics["total_active_listings"])
    with kpi3:
        st.metric("Session Requests", metrics["total_all_requests"])
    with kpi4:
        st.metric("Completed Sessions", metrics["status_counts"].get("completed", 0))
    with kpi5:
        est_commission = metrics["financials"].get("estimated_commission", 0.0)
        st.metric("Est. Commission (10%)", f"₹{est_commission:.2f}")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Visualization Row 1: Requests by Subject & Learning Modes Distribution
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("##### 📚 Tutoring Demand by Subject / Skill")
        subj_data = metrics["requests_by_subject"]
        if subj_data:
            x_vals = [r["request_count"] for r in subj_data]
            y_vals = [r["subject"] for r in subj_data]
            
            fig_subj = go.Figure(
                go.Bar(
                    x=x_vals,
                    y=y_vals,
                    orientation="h",
                    marker=dict(
                        color=x_vals,
                        colorscale="Blues",
                        showscale=False,
                    ),
                )
            )
            fig_subj.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
                xaxis_title="Number of Requests",
                yaxis_title="Subject / Skill",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig_subj, use_container_width=True)
        else:
            st.info("No request records available for current filter.")

    with col_chart2:
        st.markdown("##### 🌐 Usage by Learning Mode (Online vs On-Campus vs Async)")
        modes_dict = dict(metrics["mode_counts"])
        modes_dict["ASYNCHRONOUS (Q&A)"] = metrics["async_count"]

        if any(modes_dict.values()):
            labels = list(modes_dict.keys())
            values = list(modes_dict.values())
            
            colors = {
                "ONLINE": "#2563eb",
                "ON_CAMPUS": "#10b981",
                "ASYNCHRONOUS (Q&A)": "#f59e0b",
            }
            marker_colors = [colors.get(k, "#64748b") for k in labels]

            fig_modes = go.Figure(
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.45,
                    marker=dict(colors=marker_colors),
                )
            )
            fig_modes.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            )
            st.plotly_chart(fig_modes, use_container_width=True)
        else:
            st.info("No mode distribution data available.")

    # Visualization Row 2: Sessions Over Time & Asynchronous Questions Health
    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.markdown("##### 📈 Requests & Completed Sessions Over Time")
        time_data = metrics["time_series"]
        if time_data:
            dates = [r["session_date"] for r in time_data]
            req_counts = [r["total_requests"] for r in time_data]
            comp_counts = [r["completed_sessions"] for r in time_data]

            fig_time = go.Figure()
            fig_time.add_trace(
                go.Scatter(
                    x=dates,
                    y=req_counts,
                    mode="lines+markers",
                    name="Total Requests",
                    line=dict(color="#3b82f6", width=3),
                )
            )
            fig_time.add_trace(
                go.Scatter(
                    x=dates,
                    y=comp_counts,
                    mode="lines+markers",
                    name="Completed Sessions",
                    line=dict(color="#10b981", width=3, dash="dot"),
                )
            )
            fig_time.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
                xaxis_title="Session Date",
                yaxis_title="Count",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("No time series data for the selected range.")

    with col_chart4:
        st.markdown("##### 💬 Peer Q&A Health (Open vs Answered vs Closed)")
        qa_data = metrics["qa_counts"]
        if qa_data:
            status_labels = list(qa_data.keys())
            status_vals = list(qa_data.values())
            status_colors = [{"open": "#16a34a", "answered": "#2563eb", "closed": "#64748b"}.get(s, "#94a3b8") for s in status_labels]

            fig_qa = go.Figure(
                go.Bar(
                    x=status_labels,
                    y=status_vals,
                    marker=dict(color=status_colors),
                )
            )
            fig_qa.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
                xaxis_title="Question Status",
                yaxis_title="Total Questions",
            )
            st.plotly_chart(fig_qa, use_container_width=True)
        else:
            st.info("No Q&A data available.")

    # Visualization Row 3: Top Peer Tutors & Free vs Paid Offerings
    col_chart5, col_chart6 = st.columns(2)

    with col_chart5:
        st.markdown("##### 🏆 Top Peer Tutors by Completed Sessions & Rating")
        tutors = metrics["top_tutors"]
        if tutors:
            tut_names = [r["tutor_name"] for r in tutors]
            tut_sessions = [r["sessions_conducted"] for r in tutors]
            tut_ratings = [r["avg_rating"] for r in tutors]

            fig_tut = go.Figure(
                go.Bar(
                    x=tut_names,
                    y=tut_sessions,
                    text=[f"⭐ {r}" for r in tut_ratings],
                    textposition="outside",
                    marker=dict(
                        color=tut_ratings,
                        colorscale="Viridis",
                        showscale=False,
                    ),
                )
            )
            fig_tut.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
                xaxis_title="Peer Tutor",
                yaxis_title="Completed Sessions Conducted",
            )
            st.plotly_chart(fig_tut, use_container_width=True)
        else:
            st.info("Tutor participation data will appear after completed sessions.")

    with col_chart6:
        st.markdown("##### 🏷️ Free Mentorship vs Paid Tutoring Listings")
        free_paid = metrics["free_paid_counts"]
        if free_paid:
            fp_labels = list(free_paid.keys())
            fp_vals = list(free_paid.values())
            fp_colors = ["#10b981" if l == "Free" else "#8b5cf6" for l in fp_labels]

            fig_fp = go.Figure(
                go.Pie(
                    labels=fp_labels,
                    values=fp_vals,
                    marker=dict(colors=fp_colors),
                    hole=0.4,
                )
            )
            fig_fp.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            )
            st.plotly_chart(fig_fp, use_container_width=True)
        else:
            st.info("No listing distribution data.")

    # Platform Revenue Model Demonstration & Interactive Simulator
    st.markdown("---")
    st.markdown("### 💰 Platform Revenue Model Demonstration")
    st.caption("Demonstrating financial sustainability through optional micro-commissions on paid peer tutoring.")

    rev_col1, rev_col2 = st.columns([1, 1])

    with rev_col1:
        st.markdown(
            f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px;">
                <h4 style="margin-top: 0; color: #1e3a8a;">Proposed College Revenue Model</h4>
                <p style="font-size: 0.92rem; color: #475569;">
                    The platform maintains <strong>100% free peer mentoring</strong> for students seeking standard peer help.
                    For advanced or intensive tutoring where senior students charge an optional small fee (e.g. ₹100 - ₹200),
                    the platform applies an automated <strong>{PLATFORM_COMMISSION_PERCENT}% platform commission</strong>.
                </p>
                <div style="background: #f8fafc; border-radius: 8px; padding: 12px; margin-top: 10px;">
                    <div><strong>Actual Prototype Financials:</strong></div>
                    <ul style="margin: 6px 0 0 0; padding-left: 20px; font-size: 0.9rem; color: #334155;">
                        <li>Completed Paid Sessions: <strong>{metrics['financials'].get('total_paid_sessions', 0)}</strong></li>
                        <li>Total Paid Volume: <strong>₹{metrics['financials'].get('total_paid_volume', 0.0):.2f}</strong></li>
                        <li>Platform Commission Earned: <strong>₹{metrics['financials'].get('estimated_commission', 0.0):.2f}</strong></li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with rev_col2:
        st.markdown(
            """
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px;">
                <h4 style="margin-top: 0; color: #1e3a8a;">Interactive Revenue Simulator</h4>
                <p style="font-size: 0.88rem; color: #64748b;">
                    Simulate college-wide adoption with projected student participation.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        sim_students = st.slider("Active Paid Sessions / Month", min_value=10, max_value=500, value=80, step=10)
        sim_avg_fee = st.slider("Average Session Fee (₹)", min_value=50, max_value=400, value=150, step=25)
        sim_commission_rate = st.slider("Commission Rate (%)", min_value=5.0, max_value=20.0, value=PLATFORM_COMMISSION_PERCENT, step=1.0)

        monthly_volume = sim_students * sim_avg_fee
        monthly_commission = monthly_volume * (sim_commission_rate / 100.0)
        annual_commission = monthly_commission * 12

        st.success(
            f"📈 **Projected Monthly Commission:** `₹{monthly_commission:,.2f}` | "
            f"**Projected Annual Revenue:** `₹{annual_commission:,.2f}`"
        )
