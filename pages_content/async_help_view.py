"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Asynchronous Q&A Board (Open, Answered, Closed Doubts)
"""

import streamlit as st
from config import POPULAR_SKILLS
from db_ops import (
    get_async_questions,
    get_question_by_id,
    create_async_question,
    create_async_answer,
    get_answers_for_question,
    close_question,
)
from components.ui_helpers import get_current_user

def render_async_help_page() -> None:
    """Render asynchronous peer doubts and answer discussion board."""
    user = get_current_user()

    st.markdown("### 💬 Asynchronous Peer Q&A Board")
    st.caption("Post academic questions and coding doubts anytime. Tutors and fellow students can reply when free.")

    tab_questions, tab_ask = st.tabs(["📖 Browse College Questions", "❓ Ask a New Question"])

    with tab_ask:
        st.markdown("##### Post an Academic Question or Coding Query")
        if not user:
            st.warning("Please log in to post questions.")
        else:
            with st.form("ask_question_form"):
                subject = st.selectbox("Academic Subject *", POPULAR_SKILLS + ["General Engineering"])
                title = st.text_input("Question Title / Summary *", placeholder="e.g. Why does QuickSort degrade to O(N^2) time complexity?")
                details = st.text_area("Detailed Explanation / Doubt *", placeholder="Explain what concept is confusing or what you tried...")
                code = st.text_area("Code Snippet or Error Log (Optional)", placeholder="Paste relevant code or error output here...")

                submit_q = st.form_submit_button("Post Question to Community", type="primary", use_container_width=True)

                if submit_q:
                    succ, msg, qid = create_async_question(
                        learner_id=user["id"],
                        subject=subject,
                        title=title,
                        question_text=details,
                        code_snippet=code,
                    )
                    if succ:
                        st.success("🎉 " + msg)
                        st.rerun()
                    else:
                        st.error(msg)

    with tab_questions:
        # Filters
        c_status, c_subj = st.columns([1, 2])
        with c_status:
            status_filter = st.selectbox("Status Filter", ["All", "open", "answered", "closed"])
        with c_subj:
            subject_filter = st.selectbox("Subject Filter", ["All"] + POPULAR_SKILLS)

        questions = get_async_questions(status_filter=status_filter, subject_filter=subject_filter)

        if not questions:
            st.info("No questions found matching your filter criteria. Be the first to ask a question!")
        else:
            st.markdown(f"**Found {len(questions)} questions:**")
            
            for q in questions:
                status_color = {"open": "#16a34a", "answered": "#2563eb", "closed": "#64748b"}.get(q["status"], "#64748b")
                status_label = {"open": "🟢 OPEN", "answered": "🔵 ANSWERED", "closed": "⚪ RESOLVED"}.get(q["status"], q["status"].upper())

                with st.expander(f"[{status_label}] {q['title']} ({q['answer_count']} answers) — {q['subject']}"):
                    st.markdown(
                        f"""
                        <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 8px;">
                            Asked by <strong>{q['author_name']}</strong> ({q['author_dept']}) • 📅 {q['created_at']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.write(q["question_text"])

                    if q.get("code_snippet"):
                        st.code(q["code_snippet"], language="python")

                    # If author, option to close
                    if user and user["id"] == q["learner_id"] and q["status"] != "closed":
                        if st.button("Mark Question as Resolved / Closed", key=f"close_{q['id']}"):
                            close_question(q["id"], user["id"])
                            st.rerun()

                    st.markdown("---")
                    st.markdown("##### Answers & Peer Solutions")

                    answers = get_answers_for_question(q["id"])
                    if not answers:
                        st.caption("No peer answers yet. Be the first to help out!")
                    else:
                        for ans in answers:
                            st.markdown(
                                f"""
                                <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 10px 14px; border-radius: 4px; margin-bottom: 10px;">
                                    <div style="font-weight: 600; color: #1e3a8a; font-size: 0.9rem;">
                                        💡 {ans['tutor_name']} <span style="font-size: 0.8rem; font-weight: normal; color: #64748b;">({ans['tutor_dept']} • {ans['tutor_year']})</span>
                                    </div>
                                    <div style="margin-top: 6px; font-size: 0.92rem; color: #1e293b;">
                                        {ans['answer_text']}
                                    </div>
                                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">{ans['created_at']}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    # Form to submit an answer
                    if user:
                        if q["status"] == "closed":
                            st.caption("This question is closed for new answers.")
                        else:
                            with st.form(f"answer_form_{q['id']}"):
                                ans_text = st.text_area("Your Solution / Answer", key=f"ans_input_{q['id']}")
                                submit_ans = st.form_submit_button("Submit Answer", type="primary")

                                if submit_ans:
                                    succ, msg = create_async_answer(q["id"], user["id"], ans_text)
                                    if succ:
                                        st.success(msg)
                                        st.rerun()
                                    else:
                                        st.error(msg)
                    else:
                        st.caption("Please log in to answer this question.")
