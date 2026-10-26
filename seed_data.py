"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Sample Data Seeder

Seeds the SQLite database with realistic fictional data reflecting peer tutoring
across multiple academic engineering departments at Sri Eshwar College of Engineering.
"""

from datetime import datetime, timedelta
import random
from database import init_db, get_db_connection
from auth import register_user
from db_ops import (
    create_listing,
    create_session_request,
    update_request_status,
    create_async_question,
    create_async_answer,
    create_review,
    close_question,
)
from config import CAMPUS_MEETING_SPOTS, STATUS_ACCEPTED, STATUS_COMPLETED, STATUS_PENDING, STATUS_DECLINED

def seed_sample_data(reset_existing: bool = False) -> None:
    """Populate database with sample college data."""
    init_db()

    with get_db_connection() as conn:
        cur = conn.execute("SELECT COUNT(id) as count FROM users")
        user_count = cur.fetchone()["count"]
        if user_count > 0 and not reset_existing:
            print("Database already contains data. Skipping seeding (or pass reset_existing=True).")
            return

        if reset_existing:
            conn.execute("DELETE FROM commission_records")
            conn.execute("DELETE FROM reviews")
            conn.execute("DELETE FROM async_answers")
            conn.execute("DELETE FROM async_questions")
            conn.execute("DELETE FROM session_requests")
            conn.execute("DELETE FROM listings")
            conn.execute("DELETE FROM users")
            conn.commit()

    print("Seeding Sri Eshwar College student profiles...")

    # 1. Create Users
    # Admin
    register_user(
        name="Dean of Academics (Admin)",
        email="admin@sece.ac.in",
        password="admin123",
        department="Computer Science & Engineering (CSE)",
        year_of_study="Faculty / Admin",
        bio="Academic coordinator overseeing peer tutoring initiatives and skill exchange.",
        learning_interests="Curriculum Analytics, Student Mentorship, Engineering Pedagogy",
        is_admin=True,
    )

    sample_students = [
        {
            "name": "Kavya Sundaram",
            "email": "kavya.cse@sece.ac.in",
            "password": "student123",
            "department": "Computer Science & Engineering (CSE)",
            "year_of_study": "3rd Year (Junior)",
            "bio": "Competitive programmer (LeetCode 1800+), passionate about teaching Data Structures, C++, and Python.",
            "learning_interests": "Cloud Computing, Distributed Systems, System Design",
        },
        {
            "name": "Arun Kumar M",
            "email": "arun.aids@sece.ac.in",
            "password": "student123",
            "department": "Artificial Intelligence & Data Science (AI & DS)",
            "year_of_study": "4th Year (Senior)",
            "bio": "Deep Learning enthusiast. Winner of Smart India Hackathon. Love demystifying neural nets and math.",
            "learning_interests": "Large Language Models, MLOps, Computer Vision",
        },
        {
            "name": "Priyanka Ravi",
            "email": "priyanka.ece@sece.ac.in",
            "password": "student123",
            "department": "Electronics & Communication Engineering (ECE)",
            "year_of_study": "3rd Year (Junior)",
            "bio": "Embedded systems nerd working with ESP32 and ARM Cortex. Can help with digital logic and microcontrollers.",
            "learning_interests": "IoT Protocols, PCB Design, Robotics",
        },
        {
            "name": "Dinesh Chandran",
            "email": "dinesh.it@sece.ac.in",
            "password": "student123",
            "department": "Information Technology (IT)",
            "year_of_study": "2nd Year (Sophomore)",
            "bio": "Full-stack developer building with React, Node.js, and SQL. Happy to help freshers build their first web app.",
            "learning_interests": "Next.js, TailwindCSS, Docker, DevOps",
        },
        {
            "name": "Sneha Venkatesh",
            "email": "sneha.mech@sece.ac.in",
            "password": "student123",
            "department": "Mechanical Engineering (MECH)",
            "year_of_study": "4th Year (Senior)",
            "bio": "SolidWorks and AutoCAD specialist. Interested in EV design and finite element analysis.",
            "learning_interests": "MATLAB, CFD Simulation, Python for Engineers",
        },
        {
            "name": "Rahul Ramanathan",
            "email": "rahul.eee@sece.ac.in",
            "password": "student123",
            "department": "Electrical & Electronics Engineering (EEE)",
            "year_of_study": "2nd Year (Sophomore)",
            "bio": "Enthusiastic about power electronics and circuit simulation. Currently preparing for gate and placements.",
            "learning_interests": "Embedded C, Control Systems, Power Systems",
        },
    ]

    user_ids = {}
    for st in sample_students:
        success, msg, uid = register_user(
            name=st["name"],
            email=st["email"],
            password=st["password"],
            department=st["department"],
            year_of_study=st["year_of_study"],
            bio=st["bio"],
            learning_interests=st["learning_interests"],
        )
        if success:
            user_ids[st["email"]] = uid

    print(f"Registered {len(user_ids)} student profiles.")

    # 2. Create Tutor Listings
    listings_data = [
        {
            "email": "kavya.cse@sece.ac.in",
            "subject": "Data Structures & Algorithms",
            "description": "Master Trees, Graphs, Dynamic Programming and complexity analysis for technical interview rounds.",
            "is_paid": False,
            "price": 0.0,
            "modes": ["ONLINE", "ON_CAMPUS", "ASYNCHRONOUS"],
            "availability": "Mon, Wed, Fri: 4:30 PM - 6:30 PM",
        },
        {
            "email": "kavya.cse@sece.ac.in",
            "subject": "Python Programming",
            "description": "From basics to OOP and standard libraries. Hands-on coding exercises and lab exam prep.",
            "is_paid": True,
            "price": 150.0,
            "modes": ["ONLINE", "ON_CAMPUS"],
            "availability": "Tue, Thu: 5:00 PM - 7:00 PM; Sat: 10:00 AM - 12:00 PM",
        },
        {
            "email": "arun.aids@sece.ac.in",
            "subject": "Machine Learning & AI",
            "description": "Supervised/unsupervised algorithms, scikit-learn, PyTorch fundamentals, and practical math intuition.",
            "is_paid": True,
            "price": 200.0,
            "modes": ["ONLINE", "ON_CAMPUS", "ASYNCHRONOUS"],
            "availability": "Wed, Sat: 3:00 PM - 6:00 PM",
        },
        {
            "email": "priyanka.ece@sece.ac.in",
            "subject": "Microcontrollers & Embedded C",
            "description": "ESP32, Arduino, timer interrupts, ADC, and I2C/SPI sensor interfacing with live hardware debugging.",
            "is_paid": False,
            "price": 0.0,
            "modes": ["ON_CAMPUS", "ASYNCHRONOUS"],
            "availability": "Mon, Thu: 4:00 PM - 6:00 PM",
        },
        {
            "email": "dinesh.it@sece.ac.in",
            "subject": "Web Development (HTML/CSS/JS/React)",
            "description": "Frontend fundamentals, building responsive web apps, DOM manipulation, and React state basics.",
            "is_paid": True,
            "price": 100.0,
            "modes": ["ONLINE", "ON_CAMPUS"],
            "availability": "Daily: 5:30 PM - 7:30 PM",
        },
        {
            "email": "sneha.mech@sece.ac.in",
            "subject": "Engineering Mathematics & Statistics",
            "description": "Linear algebra, differential equations, Fourier transforms, and probability simplified.",
            "is_paid": False,
            "price": 0.0,
            "modes": ["ONLINE", "ON_CAMPUS", "ASYNCHRONOUS"],
            "availability": "Sat, Sun: 10:00 AM - 1:00 PM",
        },
    ]

    listing_ids = []
    for l in listings_data:
        t_id = user_ids.get(l["email"])
        if t_id:
            s, m, lid = create_listing(
                tutor_id=t_id,
                subject=l["subject"],
                description=l["description"],
                is_paid=l["is_paid"],
                price=l["price"],
                modes=l["modes"],
                availability=l["availability"],
            )
            if s and lid:
                listing_ids.append((lid, t_id, l))

    print(f"Created {len(listing_ids)} tutor listings.")

    # 3. Create Session Requests across dates
    today = datetime.now().date()
    kavya_id = user_ids["kavya.cse@sece.ac.in"]
    arun_id = user_ids["arun.aids@sece.ac.in"]
    dinesh_id = user_ids["dinesh.it@sece.ac.in"]
    rahul_id = user_ids["rahul.eee@sece.ac.in"]
    priyanka_id = user_ids["priyanka.ece@sece.ac.in"]

    # Session 1: Completed Online session (Rahul with Kavya for Python)
    date1 = (today - timedelta(days=5)).strftime("%Y-%m-%d")
    s, m, req1 = create_session_request(
        listing_id=listing_ids[1][0],
        learner_id=rahul_id,
        tutor_id=kavya_id,
        mode="ONLINE",
        session_date=date1,
        session_time="17:00",
        notes="Need help preparing for Python lab assessment on dictionaries and list comprehensions.",
        price=150.0,
    )
    if s and req1:
        # Tutor accepted
        update_request_status(
            req1, kavya_id, STATUS_ACCEPTED,
            tutor_note="Accepted! Bring your practice questions.",
            meet_link="[DEMO MODE] https://meet.google.com/sec-dsa-kvy",
            is_demo_link=True,
        )
        # Marked completed
        update_request_status(req1, kavya_id, STATUS_COMPLETED)
        # Rahul leaves a review
        create_review(req1, rahul_id, kavya_id, 5, "Kavya is an amazing tutor! Cleared all my recursion doubts patiently.")

    # Session 2: Completed On-Campus session (Dinesh with Arun for ML)
    date2 = (today - timedelta(days=3)).strftime("%Y-%m-%d")
    s, m, req2 = create_session_request(
        listing_id=listing_ids[2][0],
        learner_id=dinesh_id,
        tutor_id=arun_id,
        mode="ON_CAMPUS",
        session_date=date2,
        session_time="15:30",
        meeting_spot="Central Library - 2nd Floor Discussion Zone",
        notes="Discussing gradient descent convergence issues in my project.",
        price=200.0,
    )
    if s and req2:
        update_request_status(req2, arun_id, STATUS_ACCEPTED, tutor_note="See you at table 4 near the whiteboard.")
        update_request_status(req2, dinesh_id, STATUS_COMPLETED)
        create_review(req2, dinesh_id, arun_id, 5, "Incredible insights into backprop and loss curves. Highly recommend!")

    # Session 3: Completed On-Campus session (Rahul with Priyanka for Embedded C)
    date3 = (today - timedelta(days=2)).strftime("%Y-%m-%d")
    s, m, req3 = create_session_request(
        listing_id=listing_ids[3][0],
        learner_id=rahul_id,
        tutor_id=priyanka_id,
        mode="ON_CAMPUS",
        session_date=date3,
        session_time="16:00",
        meeting_spot="ECE Block - Embedded Systems Lab Discussion Area",
        notes="Setting up GPIO interrupts on ESP32 development board.",
        price=0.0,
    )
    if s and req3:
        update_request_status(req3, priyanka_id, STATUS_ACCEPTED, tutor_note="Bring your ESP32 board and USB cable.")
        update_request_status(req3, rahul_id, STATUS_COMPLETED)
        create_review(req3, rahul_id, priyanka_id, 4, "Hands-on and very practical. Resolved our hardware glitch in 30 mins.")

    # Session 4: Accepted upcoming Online session (Dinesh with Kavya for DSA)
    date4 = (today + timedelta(days=2)).strftime("%Y-%m-%d")
    s, m, req4 = create_session_request(
        listing_id=listing_ids[0][0],
        learner_id=dinesh_id,
        tutor_id=kavya_id,
        mode="ONLINE",
        session_date=date4,
        session_time="17:00",
        notes="Trie implementation and graph BFS traversals.",
        price=0.0,
    )
    if s and req4:
        update_request_status(
            req4, kavya_id, STATUS_ACCEPTED,
            tutor_note="Accepted! We will code live on Google Meet.",
            meet_link="[DEMO MODE] https://meet.google.com/sec-alg-dsa",
            is_demo_link=True,
        )

    # Session 5: Pending Request (Rahul with Dinesh for Web Dev)
    date5 = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    create_session_request(
        listing_id=listing_ids[4][0],
        learner_id=rahul_id,
        tutor_id=dinesh_id,
        mode="ON_CAMPUS",
        session_date=date5,
        session_time="17:30",
        meeting_spot="SECE Innovation & Incubation Center - Brainstorm Pod",
        notes="Connecting Streamlit UI to a REST API.",
        price=100.0,
    )

    # 4. Asynchronous Questions and Answers
    s, m, q1 = create_async_question(
        learner_id=rahul_id,
        subject="Python Programming",
        title="Why does mutable default argument behave unexpectedly in Python functions?",
        question_text="I defined `def append_item(val, my_list=[]): my_list.append(val); return my_list`. When I call it multiple times, the list accumulates items across calls! Why does this happen and what is the idiomatic fix?",
        code_snippet="def add_item(val, container=[]):\n    container.append(val)\n    return container\n\nprint(add_item(1)) # [1]\nprint(add_item(2)) # [1, 2] -- expected [2]!",
    )
    if s and q1:
        create_async_answer(
            question_id=q1,
            tutor_id=kavya_id,
            answer_text="In Python, default arguments are evaluated only once at the time of function definition, not on each invocation! To fix this, use `None` as the default sentinel value:\n\n```python\ndef add_item(val, container=None):\n    if container is None:\n        container = []\n    container.append(val)\n    return container\n```",
        )

    s, m, q2 = create_async_question(
        learner_id=dinesh_id,
        subject="Machine Learning & AI",
        title="Difference between L1 (Lasso) and L2 (Ridge) Regularization in simple terms?",
        question_text="Can someone explain the geometrical intuition of why L1 regularization produces sparse weights (forces some coefficients to exact zero) while L2 only shrinks them?",
    )
    if s and q2:
        create_async_answer(
            question_id=q2,
            tutor_id=arun_id,
            answer_text="Geometrically, L1 has sharp diamond-shaped constraint boundaries whose corners intersect coordinate axes directly, driving coefficients to zero. L2 has circular/hyperspherical constraints where the minimum loss contour usually touches smooth arcs instead of axes.",
        )

    s, m, q3 = create_async_question(
        learner_id=priyanka_id,
        subject="Data Structures & Algorithms",
        title="Best approach to detect a cycle in a Directed Graph vs Undirected Graph?",
        question_text="For undirected graphs we can use simple BFS/DFS with a parent pointer or Disjoint Set Union (DSU). Why doesn't simple parent checking work for directed graphs, and what is the standard algorithm?",
    )

    print("Sample data populated successfully with realistic Sri Eshwar academic scenarios!")

if __name__ == "__main__":
    seed_sample_data(reset_existing=True)
