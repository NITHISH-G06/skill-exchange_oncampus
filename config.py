"""
Sri Eshwar College of Engineering - Campus Skill Exchange & Peer Learning Platform
Configuration and Application Constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load optional .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# College Branding
COLLEGE_NAME = os.getenv("COLLEGE_NAME", "SRI ESHWAR COLLEGE OF ENGINEERING")
COLLEGE_TAGLINE = "Empowering Students Through Collaborative Peer Tutoring & Skill Exchange"
COLLEGE_DOMAIN = os.getenv("COLLEGE_DOMAIN", "sece.ac.in")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "campus_skill_exchange.db"))

# Platform Revenue Model
PLATFORM_COMMISSION_PERCENT = float(os.getenv("PLATFORM_COMMISSION_PERCENT", "10.0"))

# Academic Departments at Sri Eshwar
DEPARTMENTS = [
    "Computer Science & Engineering (CSE)",
    "Artificial Intelligence & Data Science (AI & DS)",
    "Information Technology (IT)",
    "Electronics & Communication Engineering (ECE)",
    "Electrical & Electronics Engineering (EEE)",
    "Mechanical Engineering (MECH)",
    "Civil Engineering",
    "Biomedical Engineering",
    "Science & Humanities",
]

YEARS_OF_STUDY = [
    "1st Year (Fresher)",
    "2nd Year (Sophomore)",
    "3rd Year (Junior)",
    "4th Year (Senior)",
    "Post Graduate (M.E. / M.Tech / MBA)",
]

# Standardized Campus Learning Spots for Sri Eshwar
CAMPUS_MEETING_SPOTS = [
    "Central Library - 2nd Floor Discussion Zone",
    "Central Library - Digital Resource Center",
    "SECE Innovation & Incubation Center - Brainstorm Pod",
    "CSE Department - Open Collaborative Study Lounge",
    "IT Department - Project Lab Discussion Corner",
    "ECE Block - Embedded Systems Lab Discussion Area",
    "Student Activity Center (SAC) - Learning Kiosk",
    "Campus Cafeteria - Open Air Study Gazebo",
    "Main Auditorium Foyer - Study Tables",
]

# Popular Subject / Skill Categories
POPULAR_SKILLS = [
    "Python Programming",
    "Data Structures & Algorithms",
    "Database Management Systems (SQL)",
    "Machine Learning & AI",
    "Web Development (HTML/CSS/JS/React)",
    "Digital Signal Processing",
    "Microcontrollers & Embedded C",
    "Object-Oriented Programming (Java/C++)",
    "Computer Networks",
    "Engineering Mathematics & Statistics",
    "Cloud Computing & DevOps",
    "UI/UX Design & Figma",
    "Aptitude & Placement Interview Prep",
]

# Learning Modes
MODE_ONLINE = "ONLINE"
MODE_ON_CAMPUS = "ON_CAMPUS"
MODE_ASYNC = "ASYNCHRONOUS"

LEARNING_MODES = [MODE_ONLINE, MODE_ON_CAMPUS, MODE_ASYNC]

# Request Statuses
STATUS_PENDING = "pending"
STATUS_ACCEPTED = "accepted"
STATUS_DECLINED = "declined"
STATUS_COMPLETED = "completed"

# Google Calendar Credentials / Demo Mode Check
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
IS_GOOGLE_CONFIGURED = bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET and "your-google" not in GOOGLE_CLIENT_ID)
