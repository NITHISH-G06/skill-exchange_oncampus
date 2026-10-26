# Campus Skill Exchange and Peer Learning Platform
### SRI ESHWAR COLLEGE OF ENGINEERING
**End-Semester Engineering Project**

---

## 📌 Project Overview
The **Campus Skill Exchange and Peer Learning Platform** is a centralized, student-driven academic collaboration hub tailored for **Sri Eshwar College of Engineering**. It bridges the gap between students seeking help with demanding engineering coursework and peer tutors who excel in specific technical domains. 

The platform accommodates students with busy schedules through flexible learning modes, provides actionable data visualizations for the college academic council, and demonstrates a sustainable platform revenue model.

---

## 🚀 Key Features

### 1. Unified Student Identity & Security
- **Single Account for Both Roles**: Every student can seamlessly act as both a **Learner** and a **Peer Tutor** from the same account without separate portals.
- **Sri Eshwar College Branding**: Institutional identity prominently displayed on both login and profile screens.
- **Enterprise-Grade Password Security**: Passwords are cryptographically hashed using **PBKDF2-HMAC-SHA256** (200,000 rounds + random salt). Plaintext passwords are never stored.
- **Profile Fields**: Full name, college email (`@sece.ac.in`), department, year of study, biography, and learning interests.

### 2. Tutor Marketplace & Listings
- **Offer Tutoring**: Students publish skills/subjects they want to teach with descriptions and availability schedules.
- **Flexible Pricing**: Support for both **100% Free Peer Mentorship** and optional small-fee paid tutoring.
- **Search & Filter**: Filter listings by subject/skill, learning mode, pricing (Free/Paid), and availability.
- **Social Proof**: Displays tutor rating stars and review count on every listing card.

### 3. Three Flexible Learning Modes
1. **Online (Google Meet)**:
   - Learner selects preferred date and time.
   - Starts as `pending`.
   - Upon tutor acceptance, generates a Google Calendar event with a **Google Meet link**.
   - If Google OAuth is not configured, automatically operates in a **clearly labeled [DEMO MODE]** (`[DEMO MODE] https://meet.google.com/xyz-abcd-efg`). Never masquerades as an unverified real link.
2. **On-Campus**:
   - Learner selects date, time, and a designated Sri Eshwar campus meeting spot (e.g. *Central Library 2nd Floor Discussion Zone*, *SECE Innovation Hub Pod*, *ECE Embedded Systems Lab Discussion Area*).
   - Enforces location and time validation before booking.
3. **Asynchronous Help (Q&A)**:
   - Students post doubts with code snippets anytime.
   - Peer tutors respond asynchronously.
   - Status tracking across `open`, `answered`, and `closed`.

### 4. Review & Rating System
- Learners can rate (1 to 5 stars) and write a review after a session is marked `completed`.
- Strict duplicate review prevention for the same session.
- Real-time updates to tutor aggregate scores.

### 5. College Administration Dashboard & Visualizations
Interactive **Plotly** data visualizations for college administrators and faculty:
- **Tutoring Demand by Subject / Skill** (Horizontal bar chart)
- **Learning Modes Distribution** (Online vs On-Campus vs Async Donut chart)
- **Session Volume Over Time** (Requests vs Completed Sessions trend line)
- **Q&A Health & Resolution Rate** (Open vs Answered vs Closed)
- **Tutor Leaderboard** (Top tutors ranked by sessions and ratings)
- **Free vs Paid Tutoring Breakdown**
- **Date & Subject Filters**
- **Privacy First**: Zero exposure of private student identifiers.

### 6. Proposed Revenue Model Demonstration
- Demonstrates institutional self-sustainability through an automated **10% platform commission** on paid tutoring sessions.
- Core peer learning remains **100% free**.
- Includes an **Interactive Revenue Simulator** allowing administrators to project monthly and annual returns based on campus adoption.

---

## 🛠️ Technology Stack
- **Language**: Python 3.10+ (tested on Python 3.14)
- **Web Interface**: [Streamlit](https://streamlit.io/)
- **Visualizations**: [Plotly](https://plotly.com/)
- **Data Analysis**: [Pandas](https://pandas.pydata.org/)
- **Database**: [SQLite](https://sqlite.org/) (zero-configuration, ACID compliant)
- **Styling**: Minimal CSS, responsive card design, subtle interactive connected-nodes canvas background.

---

## 📂 Project Structure

```
anti gravity/
├── app.py                      # Main entry point & routing engine
├── config.py                   # Sri Eshwar branding, departments, spots & constants
├── database.py                 # SQLite database initialization & connection management
├── auth.py                     # PBKDF2 password hashing & authentication logic
├── db_ops.py                   # Data access layer (CRUD for listings, bookings, Q&A, reviews, analytics)
├── seed_data.py                # Fictional sample data generator for Sri Eshwar College
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
├── README.md                   # Project documentation
├── PROJECT_REPORT.md           # Formal engineering project report
├── services/
│   └── calendar_service.py     # Google Meet / Calendar service with labeled Demo fallback
├── components/
│   ├── background.py           # Subtle interactive connected-nodes canvas background
│   └── ui_helpers.py           # Banners, badges, and session helpers
└── pages_content/
    ├── login_register.py       # Unified registration & login with Quick Demo personas
    ├── profile_view.py         # Branded student identity & profile editor
    ├── listings_view.py        # Tutor marketplace, search/filter & session booking modal
    ├── my_sessions_view.py     # Request acceptance, Meet links & session reviews
    ├── async_help_view.py      # College Q&A board & answers
    └── admin_dashboard_view.py # College Plotly analytics & revenue simulator
```

---

## ⚡ Installation & Setup Instructions

### Prerequisites
- Python 3.10 or newer installed.
- Git (optional).

### Step 1: Clone or Navigate to the Workspace
```bash
cd "anti gravity"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
# OR
python -m pip install -r requirements.txt
```

### Step 3: Configure Environment (Optional)
Copy the `.env.example` template:
```bash
cp .env.example .env
```
> *Note: If Google credentials are not set, the platform will automatically run in clearly labeled **[DEMO MODE]** for Google Meet links.*

### Step 4: Populate Sample College Data
Run the included seeder to populate realistic Sri Eshwar academic data:
```bash
python seed_data.py
```

### Step 5: Run the Application
```bash
python -m streamlit run app.py
```
Open your browser and navigate to: **`http://localhost:8501`**

---

## 👥 Demo Accounts for Evaluation

You can use the **⚡ Quick Demo Access** tab on the login screen for 1-click access, or log in manually with these credentials:

| Role | Name | Email | Password | Department |
| :--- | :--- | :--- | :--- | :--- |
| **Peer Tutor** | Kavya Sundaram | `kavya.cse@sece.ac.in` | `student123` | CSE (3rd Year) |
| **Learner** | Rahul Ramanathan | `rahul.eee@sece.ac.in` | `student123` | EEE (2nd Year) |
| **Peer Tutor** | Arun Kumar M | `arun.aids@sece.ac.in` | `student123` | AI & DS (4th Year) |
| **Peer Tutor** | Priyanka Ravi | `priyanka.ece@sece.ac.in` | `student123` | ECE (3rd Year) |
| **College Admin** | Dean of Academics | `admin@sece.ac.in` | `admin123` | CSE / Admin |

---

## 🔒 Security & Privacy Practices
- **Password Hashes**: Standard PBKDF2 with 200,000 SHA256 iterations and unique 16-byte cryptographically secure salts.
- **Authorization Enforcement**: Strict checks verify that only the assigned tutor can accept/decline a booking, and only the attending learner can submit a review.
- **Aggregated Analytics**: Dashboard charts aggregate counts and trends without exposing student names, personal emails, or private messages.
#   s k i l l - e x c h a n g e - o n c a m p u s  
 