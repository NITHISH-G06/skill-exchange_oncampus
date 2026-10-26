# END-SEMESTER ENGINEERING PROJECT REPORT

## PROJECT TITLE
# Campus Skill Exchange and Peer Learning Platform

### INSTITUTION
**SRI ESHWAR COLLEGE OF ENGINEERING**  
*Department of Computer Science & Engineering*  
Coimbatore, Tamil Nadu, India  
Academic Year: 2025–2026

---

## 1. ABSTRACT
In competitive engineering institutions, students often face hurdles in grasping advanced conceptual subjects, completing rigorous lab assignments, and preparing for campus placement assessments. Concurrently, high-performing students across departments seek avenues to reinforce their own mastery by teaching peers. Traditional study groups lack structured scheduling, accountability, and reach beyond close friend circles. 

The **Campus Skill Exchange and Peer Learning Platform** addresses this challenge by providing a centralized, secure web-based peer tutoring and knowledge exchange system designed specifically for the student body of **Sri Eshwar College of Engineering**. Built using Python, Streamlit, Plotly, and SQLite, the platform empowers each student to act simultaneously as a learner and a tutor under a unified account. It supports three distinct modes of engagement: **Online (Google Meet)**, **On-Campus (designated campus study pods)**, and **Asynchronous Q&A**. The platform also features an interactive analytics dashboard with real-time academic demand trends and demonstrates a self-sustaining institutional revenue model.

---

## 2. PROBLEM STATEMENT
1. **Academic Silos**: Knowledge is frequently siloed within specific batches or departments (e.g. CSE, AI&DS, ECE, EEE, MECH), limiting interdisciplinary cross-pollination.
2. **Scheduling Conflicts**: Engineering students have demanding laboratory schedules, project milestones, and club commitments, making ad-hoc peer coordination difficult.
3. **Lack of Incentives & Recognition**: High-achieving student tutors lack formal channels to build academic reputation, receive peer reviews, or earn micro-stipends for specialized coaching.
4. **Institutional Blindspots**: College academic councils lack data on which subjects students struggle with most outside official lecture hours.

---

## 3. PROJECT OBJECTIVES
- **Unified Profile System**: Implement a single student authentication and profile system where any registered student can both seek help and offer tutoring.
- **Flexible Learning Modes**:
  - Facilitate **Online 1-on-1 tutoring** with automated Google Meet video links.
  - Coordinate **On-Campus peer sessions** with verified physical meeting locations across the college campus.
  - Provide an **Asynchronous Q&A Board** for quick doubts and code debugging that do not require live scheduling.
- **Session Integrity & Accountability**: Enforce double-booking prevention, mutual session completion verification, and non-duplicative peer review mechanisms.
- **Institutional Visualizations**: Provide the academic council with real-time aggregated charts depicting skill demand, mode preferences, and tutoring activity without exposing private student records.
- **Sustainable Revenue Model**: Prototype a non-intrusive revenue model demonstrating financial sustainability through small optional micro-commissions while preserving free peer mentoring for all.

---

## 4. SYSTEM MODULES & ARCHITECTURE

```
+---------------------------------------------------------------------------------+
|                    Streamlit Responsive Interface & CSS Canvas                  |
|          (Branded Header, Interactive Connected Nodes, Role-Based Tabs)         |
+---------------------------------------------------------------------------------+
        |                        |                        |                |
        v                        v                        v                v
+---------------+        +---------------+        +---------------+  +------------+
| Auth & Profile|        |  Marketplace  |        |  Session Hub  |  |  Plotly    |
| (PBKDF2-SHA256|        |  & Scheduling |        |  & Reviews    |  |  Analytics |
|  sece.ac.in)  |        |  (3 Modes)    |        |  (Meet/Campus)|  |  Dashboard |
+---------------+        +---------------+        +---------------+  +------------+
        |                        |                        |                |
        +------------------------+------------------------+----------------+
                                 |
                                 v
        +-------------------------------------------------+
        |        Data Access Layer (db_ops.py)            |
        +-------------------------------------------------+
                                 |
                                 v
        +-------------------------------------------------+
        |         SQLite Relational Database Engine       |
        |  (users, listings, requests, questions,        |
        |   answers, reviews, commission_records)         |
        +-------------------------------------------------+
```

### Module 1: Student Identity & Profile Management
- Unified registration supporting college domain emails (`@sece.ac.in`).
- Passwords secured with **PBKDF2-HMAC-SHA256** and 16-byte random salts.
- Profiles maintain student department, year of study, biography, learning interests, and aggregate tutor ratings.

### Module 2: Tutor Marketplace & Listing Management
- Tutors publish course-specific listings detailing covered concepts, free/paid status, pricing, and availability schedules.
- Multi-parameter search filters listings by keyword, subject, mode, and cost.

### Module 3: Multi-Mode Session Scheduling
- **Online Mode**: Creates Google Meet video links upon tutor acceptance (with clearly labeled `[DEMO MODE]` fallback when credentials are not configured).
- **On-Campus Mode**: Enforces selection of designated campus spots (Central Library, Innovation Hub, Department Labs) and validated time slots.
- **Conflict Avoidance**: Validates both tutor and learner schedules to prevent double-booking.

### Module 4: Asynchronous Q&A Board
- Students submit queries with formatted code snippets.
- Tutors and peers submit answers asynchronously.
- Status transitions through `open`, `answered`, and `closed`.

### Module 5: Quality Assurance & Review System
- Post-session rating (1–5 stars) and textual feedback.
- Strict constraint prevents multiple reviews for the same completed session.
- Real-time recalculation of tutor average scores.

### Module 6: Institutional Analytics & Revenue Model
- High-level aggregations displaying popular subjects, mode distribution, engagement over time, and tutor performance.
- Prototype revenue engine calculating platform commissions.

---

## 5. TOOLS & TECHNOLOGIES USED

| Category | Technology | Rationale |
| :--- | :--- | :--- |
| **Programming Language** | Python 3.14 / 3.10+ | Fast prototyping, clean syntax, rich ecosystem. |
| **Web Framework** | Streamlit 1.30+ | Rapid interactive UI development with Python-native state. |
| **Data Analysis** | Pandas | High-performance tabular transformation and query grouping. |
| **Data Visualizations** | Plotly (Express & Graph Objects) | Dynamic, interactive charts with tooltips and responsive layouts. |
| **Database** | SQLite 3 | Embedded, lightweight, zero-configuration ACID relational storage. |
| **Security** | Python Standard `hashlib` | PBKDF2-HMAC-SHA256 encryption compliant with NIST standards. |
| **Video Integration** | Google Calendar / Meet API | Standard enterprise video conferencing with safe labeled demo fallback. |

---

## 6. DATA VISUALIZATIONS & ANALYTICS

The college administrative dashboard incorporates six Plotly charts:
1. **Tutoring Demand by Subject / Skill**: Horizontal bar chart identifying high-demand topics (e.g. *Data Structures*, *Python*, *Machine Learning*).
2. **Learning Modes Breakdown**: Donut chart displaying student preference across Online (Google Meet), On-Campus, and Asynchronous Q&A.
3. **Session Volume Over Time**: Dual-axis line chart tracking total submitted requests vs completed sessions.
4. **Q&A Health & Resolution**: Bar chart measuring open vs answered vs resolved questions.
5. **Top Peer Tutors Leaderboard**: Bar chart ranking tutors by completed sessions conducted with star ratings.
6. **Free vs Paid Tutoring Distribution**: Ratio comparison ensuring free peer tutoring remains available to all students.

---

## 7. PROPOSED REVENUE MODEL

### Concept
While peer mentorship at Sri Eshwar College of Engineering remains fundamentally free and accessible, senior students offering specialized, intensive bootcamps or placement coaching may charge an optional modest fee (e.g. ₹100–₹250 per session).

### Mechanism
- The platform retains an automated **10% platform commission** on paid sessions upon completion.
- The prototype tracks these transactions under `commission_records` and computes platform commission without processing real payments.
- An interactive simulator allows administrators to evaluate revenue projections under variable adoption rates (e.g., 80 paid sessions/month at ₹150 average fee yields ₹1,200/month or ₹14,400/year to support student club activities).

---

## 8. LIMITATIONS OF THE PROTOTYPE
1. **Payment Gateway**: Current implementation simulates financial commissions; payment processing (e.g., Razorpay/UPI) is not connected.
2. **Real-Time WebSockets**: Streamlit relies on reactive reruns rather than instantaneous bi-directional socket messaging.
3. **Automated Calendar Reminders**: Requires full Google Workspace tenant approval for campus-wide automated Calendar invitations without demo fallback.

---

## 9. FUTURE ENHANCEMENTS
- **UPI / Razorpay Integration**: Seamless micro-transactions directly credited to student bank accounts.
- **AI Peer Matching Assistant**: Embed an LLM to recommend peer tutors based on student syllabus weak areas and timetable availability.
- **Campus Geo-Fencing**: Mobile check-in verification when students meet at campus spots using QR codes.
- **Verified Skill Badges**: Academic council verification of student grades (e.g. 'O' Grade in DSA) automatically displayed on tutor profile cards.

---

## 10. CONCLUSION
The **Campus Skill Exchange and Peer Learning Platform** demonstrates a complete, secure, and practical software engineering solution tailored to **Sri Eshwar College of Engineering**. By combining flexible learning modes, institutional branding, cryptographic data protection, and insightful administrative visualizations, the project provides an impactful template for collaborative peer learning in higher engineering education.
