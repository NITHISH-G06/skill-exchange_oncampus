"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Data Access Layer (CRUD and Query Operations for all application entities)
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from database import get_db_connection
from config import PLATFORM_COMMISSION_PERCENT, STATUS_PENDING, STATUS_ACCEPTED, STATUS_DECLINED, STATUS_COMPLETED

# ==========================================
# TUTOR LISTINGS
# ==========================================

def create_listing(
    tutor_id: int,
    subject: str,
    description: str,
    is_paid: bool,
    price: float,
    modes: List[str],
    availability: str,
) -> Tuple[bool, str, Optional[int]]:
    """Create a new tutoring listing for a student."""
    subject = subject.strip()
    description = description.strip()
    availability = availability.strip()

    if not subject:
        return False, "Subject or skill title is required.", None
    if not description:
        return False, "Description is required.", None
    if not modes:
        return False, "At least one learning mode (Online, On-Campus, Async) must be selected.", None
    if not availability:
        return False, "Availability schedule is required (e.g. 'Mon-Thu 4:30 PM - 6:30 PM').", None
    if is_paid and price <= 0:
        return False, "For paid tutoring, price must be greater than ₹0.", None

    modes_str = ",".join(modes)
    price_val = float(price) if is_paid else 0.0

    try:
        with get_db_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO listings (tutor_id, subject, description, is_paid, price, modes, availability, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (tutor_id, subject, description, 1 if is_paid else 0, price_val, modes_str, availability),
            )
            conn.commit()
            return True, "Listing created successfully!", cur.lastrowid
    except Exception as e:
        return False, f"Failed to create listing: {str(e)}", None

def update_listing(
    listing_id: int,
    tutor_id: int,
    subject: str,
    description: str,
    is_paid: bool,
    price: float,
    modes: List[str],
    availability: str,
    is_active: bool,
) -> Tuple[bool, str]:
    """Update an existing tutoring listing."""
    modes_str = ",".join(modes)
    price_val = float(price) if is_paid else 0.0

    try:
        with get_db_connection() as conn:
            # Check ownership
            cur = conn.execute("SELECT tutor_id FROM listings WHERE id = ?", (listing_id,))
            row = cur.fetchone()
            if not row or row["tutor_id"] != tutor_id:
                return False, "Unauthorized: You can only edit your own listings."

            conn.execute(
                """
                UPDATE listings
                SET subject = ?, description = ?, is_paid = ?, price = ?, modes = ?,
                    availability = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ? AND tutor_id = ?
                """,
                (subject.strip(), description.strip(), 1 if is_paid else 0, price_val,
                 modes_str, availability.strip(), 1 if is_active else 0, listing_id, tutor_id),
            )
            conn.commit()
            return True, "Listing updated successfully!"
    except Exception as e:
        return False, f"Failed to update listing: {str(e)}"

def toggle_listing_status(listing_id: int, tutor_id: int, new_status: bool) -> Tuple[bool, str]:
    """Activate or deactivate a listing."""
    try:
        with get_db_connection() as conn:
            cur = conn.execute("SELECT tutor_id FROM listings WHERE id = ?", (listing_id,))
            row = cur.fetchone()
            if not row or row["tutor_id"] != tutor_id:
                return False, "Unauthorized."
            conn.execute(
                "UPDATE listings SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (1 if new_status else 0, listing_id),
            )
            conn.commit()
            status_text = "activated" if new_status else "deactivated"
            return True, f"Listing {status_text} successfully."
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_listing_by_id(listing_id: int) -> Optional[Dict[str, Any]]:
    """Fetch listing details along with tutor information and rating."""
    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT l.*, u.name as tutor_name, u.email as tutor_email,
                   u.department as tutor_dept, u.year_of_study as tutor_year,
                   u.bio as tutor_bio
            FROM listings l
            JOIN users u ON l.tutor_id = u.id
            WHERE l.id = ?
            """,
            (listing_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        data = dict(row)
        rating_summary = get_tutor_rating_summary(data["tutor_id"])
        data.update(rating_summary)
        return data

def get_tutor_listings(tutor_id: int, include_inactive: bool = True) -> List[Dict[str, Any]]:
    """Retrieve listings belonging to a specific student tutor."""
    with get_db_connection() as conn:
        if include_inactive:
            cur = conn.execute(
                "SELECT * FROM listings WHERE tutor_id = ? ORDER BY created_at DESC",
                (tutor_id,),
            )
        else:
            cur = conn.execute(
                "SELECT * FROM listings WHERE tutor_id = ? AND is_active = 1 ORDER BY created_at DESC",
                (tutor_id,),
            )
        return [dict(r) for r in cur.fetchall()]

def search_listings(
    subject_query: str = "",
    mode_filter: str = "All",
    price_filter: str = "All",
    exclude_user_id: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Search and filter active tutoring listings.
    Allows filtering by subject text, mode (Online, On-Campus, Async), and free/paid.
    """
    query = """
        SELECT l.*, u.name as tutor_name, u.email as tutor_email,
               u.department as tutor_dept, u.year_of_study as tutor_year,
               u.bio as tutor_bio
        FROM listings l
        JOIN users u ON l.tutor_id = u.id
        WHERE l.is_active = 1
    """
    params: List[Any] = []

    if exclude_user_id:
        query += " AND l.tutor_id != ?"
        params.append(exclude_user_id)

    if subject_query.strip():
        query += " AND (l.subject LIKE ? OR l.description LIKE ? OR u.name LIKE ?)"
        term = f"%{subject_query.strip()}%"
        params.extend([term, term, term])

    if mode_filter and mode_filter != "All":
        query += " AND l.modes LIKE ?"
        params.append(f"%{mode_filter}%")

    if price_filter == "Free Only":
        query += " AND l.is_paid = 0"
    elif price_filter == "Paid Only":
        query += " AND l.is_paid = 1"

    query += " ORDER BY l.created_at DESC"

    with get_db_connection() as conn:
        cur = conn.execute(query, params)
        results = []
        for row in cur.fetchall():
            item = dict(row)
            stats = get_tutor_rating_summary(item["tutor_id"])
            item.update(stats)
            results.append(item)
        return results

# ==========================================
# SESSION REQUESTS & SCHEDULING
# ==========================================

def check_booking_conflict(tutor_id: int, learner_id: int, session_date: str, session_time: str) -> Tuple[bool, str]:
    """
    Prevent double-booking: Checks if tutor or learner already has an accepted session at the same date and time.
    """
    with get_db_connection() as conn:
        # Check tutor conflict
        cur = conn.execute(
            """
            SELECT id FROM session_requests
            WHERE tutor_id = ? AND session_date = ? AND session_time = ? AND status = ?
            """,
            (tutor_id, session_date, session_time, STATUS_ACCEPTED),
        )
        if cur.fetchone():
            return True, "The tutor already has an accepted session scheduled at this date and time."

        # Check learner conflict
        cur = conn.execute(
            """
            SELECT id FROM session_requests
            WHERE learner_id = ? AND session_date = ? AND session_time = ? AND status = ?
            """,
            (learner_id, session_date, session_time, STATUS_ACCEPTED),
        )
        if cur.fetchone():
            return True, "You already have another accepted session scheduled at this date and time."

    return False, ""

def create_session_request(
    listing_id: int,
    learner_id: int,
    tutor_id: int,
    mode: str,
    session_date: str,
    session_time: str,
    meeting_spot: str = "",
    notes: str = "",
    price: float = 0.0,
) -> Tuple[bool, str, Optional[int]]:
    """Submit a peer learning session request."""
    if learner_id == tutor_id:
        return False, "You cannot book a tutoring session with yourself.", None

    if not session_date or not session_time:
        return False, "Both session date and time are required.", None

    if mode == "ON_CAMPUS" and not meeting_spot.strip():
        return False, "For On-Campus sessions, you must specify a campus meeting spot.", None

    # Check potential conflicts
    conflict, conflict_msg = check_booking_conflict(tutor_id, learner_id, session_date, session_time)
    if conflict:
        return False, conflict_msg, None

    commission_val = round(price * (PLATFORM_COMMISSION_PERCENT / 100.0), 2) if price > 0 else 0.0

    try:
        with get_db_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO session_requests (
                    listing_id, learner_id, tutor_id, mode, session_date, session_time,
                    meeting_spot, notes, status, price, commission_amount
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    listing_id, learner_id, tutor_id, mode, session_date, session_time,
                    meeting_spot.strip(), notes.strip(), STATUS_PENDING, price, commission_val
                ),
            )
            conn.commit()
            return True, "Session request sent to tutor successfully!", cur.lastrowid
    except Exception as e:
        return False, f"Failed to submit request: {str(e)}", None

def get_requests_for_learner(learner_id: int) -> List[Dict[str, Any]]:
    """Retrieve all requests sent by a learner."""
    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT sr.*, l.subject, u.name as tutor_name, u.email as tutor_email,
                   u.department as tutor_dept
            FROM session_requests sr
            JOIN users u ON sr.tutor_id = u.id
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE sr.learner_id = ?
            ORDER BY sr.created_at DESC
            """,
            (learner_id,),
        )
        return [dict(r) for r in cur.fetchall()]

def get_requests_for_tutor(tutor_id: int) -> List[Dict[str, Any]]:
    """Retrieve all incoming requests received by a tutor."""
    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT sr.*, l.subject, u.name as learner_name, u.email as learner_email,
                   u.department as learner_dept, u.year_of_study as learner_year
            FROM session_requests sr
            JOIN users u ON sr.learner_id = u.id
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE sr.tutor_id = ?
            ORDER BY sr.created_at DESC
            """,
            (tutor_id,),
        )
        return [dict(r) for r in cur.fetchall()]

def get_request_by_id(request_id: int) -> Optional[Dict[str, Any]]:
    """Fetch complete details of a single session request."""
    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT sr.*, l.subject,
                   t.name as tutor_name, t.email as tutor_email,
                   lr.name as learner_name, lr.email as learner_email
            FROM session_requests sr
            JOIN users t ON sr.tutor_id = t.id
            JOIN users lr ON sr.learner_id = lr.id
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE sr.id = ?
            """,
            (request_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

def update_request_status(
    request_id: int,
    user_id: int,
    new_status: str,
    tutor_note: str = "",
    meet_link: str = "",
    is_demo_link: bool = False,
) -> Tuple[bool, str]:
    """
    Update the status of a request (accept, decline, complete).
    Enforces authorization: Only tutor can accept/decline; either can mark completed.
    """
    req = get_request_by_id(request_id)
    if not req:
        return False, "Request not found."

    # Authorization checks
    if new_status in [STATUS_ACCEPTED, STATUS_DECLINED]:
        if req["tutor_id"] != user_id:
            return False, "Only the requested tutor can accept or decline this request."
    elif new_status == STATUS_COMPLETED:
        if user_id not in [req["tutor_id"], req["learner_id"]]:
            return False, "Only the tutor or learner can mark this session as completed."

    try:
        with get_db_connection() as conn:
            if new_status == STATUS_ACCEPTED and req["mode"] == "ONLINE" and meet_link:
                conn.execute(
                    """
                    UPDATE session_requests
                    SET status = ?, tutor_response_note = ?, google_meet_link = ?,
                        is_demo_link = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (new_status, tutor_note.strip(), meet_link.strip(), 1 if is_demo_link else 0, request_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE session_requests
                    SET status = ?, tutor_response_note = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (new_status, tutor_note.strip(), request_id),
                )

            # If completed and paid, record commission transaction
            if new_status == STATUS_COMPLETED and req["price"] > 0:
                record_commission(
                    conn,
                    request_id=req["id"],
                    tutor_id=req["tutor_id"],
                    total_amount=req["price"],
                    commission_rate=PLATFORM_COMMISSION_PERCENT,
                )

            conn.commit()
            return True, f"Session request marked as {new_status}."
    except Exception as e:
        return False, f"Error updating request: {str(e)}"

# ==========================================
# ASYNCHRONOUS HELP (Q&A BOARD)
# ==========================================

def create_async_question(
    learner_id: int,
    subject: str,
    title: str,
    question_text: str,
    code_snippet: str = "",
) -> Tuple[bool, str, Optional[int]]:
    """Post an asynchronous question."""
    title = title.strip()
    question_text = question_text.strip()
    if not subject:
        return False, "Subject is required.", None
    if not title:
        return False, "Question title is required.", None
    if not question_text:
        return False, "Question details cannot be empty.", None

    try:
        with get_db_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO async_questions (learner_id, subject, title, question_text, code_snippet, status)
                VALUES (?, ?, ?, ?, ?, 'open')
                """,
                (learner_id, subject, title, question_text, code_snippet.strip()),
            )
            conn.commit()
            return True, "Question posted to the peer learning community!", cur.lastrowid
    except Exception as e:
        return False, f"Failed to post question: {str(e)}", None

def get_async_questions(status_filter: str = "All", subject_filter: str = "All") -> List[Dict[str, Any]]:
    """Retrieve async questions with author details and answer count."""
    query = """
        SELECT q.*, u.name as author_name, u.department as author_dept,
               COUNT(a.id) as answer_count
        FROM async_questions q
        JOIN users u ON q.learner_id = u.id
        LEFT JOIN async_answers a ON q.id = a.question_id
        WHERE 1=1
    """
    params: List[Any] = []

    if status_filter != "All":
        query += " AND q.status = ?"
        params.append(status_filter.lower())

    if subject_filter != "All":
        query += " AND q.subject = ?"
        params.append(subject_filter)

    query += " GROUP BY q.id ORDER BY q.created_at DESC"

    with get_db_connection() as conn:
        cur = conn.execute(query, params)
        return [dict(r) for r in cur.fetchall()]

def get_question_by_id(question_id: int) -> Optional[Dict[str, Any]]:
    """Fetch question by ID with learner info."""
    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT q.*, u.name as author_name, u.email as author_email, u.department as author_dept
            FROM async_questions q
            JOIN users u ON q.learner_id = u.id
            WHERE q.id = ?
            """,
            (question_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

def create_async_answer(question_id: int, tutor_id: int, answer_text: str) -> Tuple[bool, str]:
    """Add a tutor or peer answer to a question."""
    answer_text = answer_text.strip()
    if not answer_text:
        return False, "Answer cannot be empty."

    try:
        with get_db_connection() as conn:
            conn.execute(
                """
                INSERT INTO async_answers (question_id, tutor_id, answer_text)
                VALUES (?, ?, ?)
                """,
                (question_id, tutor_id, answer_text),
            )
            # Update question status to 'answered' if it was 'open'
            conn.execute(
                "UPDATE async_questions SET status = 'answered', updated_at = CURRENT_TIMESTAMP WHERE id = ? AND status = 'open'",
                (question_id,),
            )
            conn.commit()
            return True, "Your answer has been submitted!"
    except Exception as e:
        return False, f"Failed to submit answer: {str(e)}"

def get_answers_for_question(question_id: int) -> List[Dict[str, Any]]:
    """Fetch all peer answers for a given question."""
    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT a.*, u.name as tutor_name, u.department as tutor_dept, u.year_of_study as tutor_year
            FROM async_answers a
            JOIN users u ON a.tutor_id = u.id
            WHERE a.question_id = ?
            ORDER BY a.created_at ASC
            """,
            (question_id,),
        )
        return [dict(r) for r in cur.fetchall()]

def close_question(question_id: int, user_id: int) -> Tuple[bool, str]:
    """Close a question once resolved."""
    q = get_question_by_id(question_id)
    if not q:
        return False, "Question not found."
    if q["learner_id"] != user_id:
        return False, "Only the author of the question can close it."

    try:
        with get_db_connection() as conn:
            conn.execute(
                "UPDATE async_questions SET status = 'closed', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (question_id,),
            )
            conn.commit()
            return True, "Question marked as closed."
    except Exception as e:
        return False, f"Error: {str(e)}"

# ==========================================
# REVIEWS & RATINGS
# ==========================================

def has_reviewed_session(request_id: int) -> bool:
    """Check if a completed session already has a review (prevents duplicates)."""
    with get_db_connection() as conn:
        cur = conn.execute("SELECT id FROM reviews WHERE request_id = ?", (request_id,))
        return cur.fetchone() is not None

def create_review(
    request_id: int,
    learner_id: int,
    tutor_id: int,
    rating: int,
    review_text: str = "",
) -> Tuple[bool, str]:
    """Submit a rating and review for a completed session."""
    if rating < 1 or rating > 5:
        return False, "Rating must be between 1 and 5 stars."

    # Validate session status
    req = get_request_by_id(request_id)
    if not req:
        return False, "Session request not found."
    if req["status"] != STATUS_COMPLETED:
        return False, "You can only review a completed session."
    if req["learner_id"] != learner_id:
        return False, "Only the student learner who attended the session can submit a review."

    if has_reviewed_session(request_id):
        return False, "You have already reviewed this session. Duplicate reviews are not permitted."

    try:
        with get_db_connection() as conn:
            conn.execute(
                """
                INSERT INTO reviews (request_id, learner_id, tutor_id, rating, review_text)
                VALUES (?, ?, ?, ?, ?)
                """,
                (request_id, learner_id, tutor_id, rating, review_text.strip()),
            )
            conn.commit()
            return True, "Thank you! Your review has been recorded."
    except Exception as e:
        return False, f"Failed to save review: {str(e)}"

def get_tutor_rating_summary(tutor_id: int) -> Dict[str, Any]:
    """Calculate aggregate average rating and total review count for a tutor."""
    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT AVG(rating) as avg_rating, COUNT(id) as review_count
            FROM reviews
            WHERE tutor_id = ?
            """,
            (tutor_id,),
        )
        row = cur.fetchone()
        avg = round(float(row["avg_rating"]), 1) if row and row["avg_rating"] is not None else 0.0
        count = int(row["review_count"]) if row and row["review_count"] is not None else 0
        return {"avg_rating": avg, "review_count": count}

def get_tutor_reviews(tutor_id: int) -> List[Dict[str, Any]]:
    """Fetch individual reviews received by a tutor."""
    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT r.*, u.name as learner_name, u.department as learner_dept,
                   sr.session_date, l.subject
            FROM reviews r
            JOIN users u ON r.learner_id = u.id
            JOIN session_requests sr ON r.request_id = sr.id
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE r.tutor_id = ?
            ORDER BY r.created_at DESC
            """,
            (tutor_id,),
        )
        return [dict(r) for r in cur.fetchall()]

# ==========================================
# COMMISSION TRANSACTIONS & REVENUE
# ==========================================

def record_commission(conn: sqlite3.Connection, request_id: int, tutor_id: int, total_amount: float, commission_rate: float) -> None:
    """Internal helper to log commission transaction upon session completion."""
    # Check if already logged
    cur = conn.execute("SELECT id FROM commission_records WHERE request_id = ?", (request_id,))
    if cur.fetchone():
        return

    commission = round(total_amount * (commission_rate / 100.0), 2)
    tutor_earnings = round(total_amount - commission, 2)

    conn.execute(
        """
        INSERT INTO commission_records (request_id, tutor_id, total_amount, commission_rate, commission_amount, tutor_earnings)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (request_id, tutor_id, total_amount, commission_rate, commission, tutor_earnings),
    )

# ==========================================
# ADMIN & COLLEGE ANALYTICS QUERIES
# ==========================================

def get_analytics_metrics(subject_filter: str = "All", date_from: Optional[str] = None, date_to: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch comprehensive aggregated statistics for the Sri Eshwar College Admin Dashboard.
    Ensures student privacy: only aggregated totals and distributions are returned.
    """
    with get_db_connection() as conn:
        # Base query filters
        where_clauses = ["1=1"]
        params: List[Any] = []

        if subject_filter != "All":
            where_clauses.append("l.subject = ?")
            params.append(subject_filter)
        if date_from:
            where_clauses.append("sr.session_date >= ?")
            params.append(date_from)
        if date_to:
            where_clauses.append("sr.session_date <= ?")
            params.append(date_to)

        where_str = " AND ".join(where_clauses)

        # 1. Requests by Subject
        cur = conn.execute(
            f"""
            SELECT COALESCE(l.subject, 'General Mentoring') as subject, COUNT(sr.id) as request_count
            FROM session_requests sr
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE {where_str}
            GROUP BY subject
            ORDER BY request_count DESC
            """,
            params,
        )
        requests_by_subject = [dict(r) for r in cur.fetchall()]

        # 2. Mode distribution (Online vs On-Campus vs Async)
        cur = conn.execute(
            f"""
            SELECT sr.mode, COUNT(sr.id) as count
            FROM session_requests sr
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE {where_str}
            GROUP BY sr.mode
            """,
            params,
        )
        mode_counts = {r["mode"]: r["count"] for r in cur.fetchall()}
        
        # Count async questions in the same context
        cur = conn.execute("SELECT COUNT(id) as count FROM async_questions")
        async_count = cur.fetchone()["count"]

        # 3. Status breakdown (pending, accepted, declined, completed)
        cur = conn.execute(
            f"""
            SELECT sr.status, COUNT(sr.id) as count
            FROM session_requests sr
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE {where_str}
            GROUP BY sr.status
            """,
            params,
        )
        status_counts = {r["status"]: r["count"] for r in cur.fetchall()}

        # 4. Sessions over time (grouped by date)
        cur = conn.execute(
            f"""
            SELECT sr.session_date,
                   COUNT(sr.id) as total_requests,
                   SUM(CASE WHEN sr.status = '{STATUS_COMPLETED}' THEN 1 ELSE 0 END) as completed_sessions
            FROM session_requests sr
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE {where_str}
            GROUP BY sr.session_date
            ORDER BY sr.session_date ASC
            """,
            params,
        )
        time_series = [dict(r) for r in cur.fetchall()]

        # 5. Async questions: Open vs Answered vs Closed
        cur = conn.execute(
            """
            SELECT status, COUNT(id) as count
            FROM async_questions
            GROUP BY status
            """
        )
        qa_counts = {r["status"]: r["count"] for r in cur.fetchall()}

        # 6. Free vs Paid listing counts
        cur = conn.execute(
            """
            SELECT is_paid, COUNT(id) as count
            FROM listings
            WHERE is_active = 1
            GROUP BY is_paid
            """
        )
        free_paid_counts = {("Paid" if r["is_paid"] else "Free"): r["count"] for r in cur.fetchall()}

        # 7. Estimated Commission and Financials
        cur = conn.execute(
            f"""
            SELECT
                COUNT(sr.id) as total_paid_sessions,
                COALESCE(SUM(sr.price), 0.0) as total_paid_volume,
                COALESCE(SUM(sr.commission_amount), 0.0) as estimated_commission
            FROM session_requests sr
            LEFT JOIN listings l ON sr.listing_id = l.id
            WHERE sr.status = '{STATUS_COMPLETED}' AND sr.price > 0 AND {where_str}
            """,
            params,
        )
        finance_row = cur.fetchone()

        # 8. Tutor participation and ratings distribution
        cur = conn.execute(
            """
            SELECT u.name as tutor_name, u.department,
                   COUNT(DISTINCT sr.id) as sessions_conducted,
                   AVG(r.rating) as avg_rating,
                   COUNT(DISTINCT r.id) as review_count
            FROM users u
            JOIN session_requests sr ON u.id = sr.tutor_id AND sr.status = 'completed'
            LEFT JOIN reviews r ON u.id = r.tutor_id
            GROUP BY u.id
            HAVING sessions_conducted > 0
            ORDER BY avg_rating DESC, sessions_conducted DESC
            LIMIT 10
            """
        )
        tutor_ratings = [
            {
                "tutor_name": r["tutor_name"],
                "department": r["department"],
                "sessions_conducted": r["sessions_conducted"],
                "avg_rating": round(r["avg_rating"], 1) if r["avg_rating"] else 5.0,
                "review_count": r["review_count"],
            }
            for r in cur.fetchall()
        ]

        # Total counts
        cur = conn.execute("SELECT COUNT(id) as count FROM users")
        total_users = cur.fetchone()["count"]

        cur = conn.execute("SELECT COUNT(id) as count FROM listings WHERE is_active = 1")
        total_active_listings = cur.fetchone()["count"]

        cur = conn.execute("SELECT COUNT(id) as count FROM session_requests")
        total_all_requests = cur.fetchone()["count"]

        return {
            "total_users": total_users,
            "total_active_listings": total_active_listings,
            "total_all_requests": total_all_requests,
            "requests_by_subject": requests_by_subject,
            "mode_counts": mode_counts,
            "async_count": async_count,
            "status_counts": status_counts,
            "time_series": time_series,
            "qa_counts": qa_counts,
            "free_paid_counts": free_paid_counts,
            "financials": dict(finance_row) if finance_row else {},
            "top_tutors": tutor_ratings,
        }
