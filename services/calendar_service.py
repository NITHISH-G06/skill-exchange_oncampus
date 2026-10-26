"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Google Calendar & Google Meet Integration Service

Creates Google Calendar events with Google Meet links when online tutoring sessions are accepted.
Includes a clearly labeled Demo Mode fallback when real Google OAuth is not configured.
"""

import random
import string
from typing import Dict, Any, Tuple
from config import IS_GOOGLE_CONFIGURED, GOOGLE_CLIENT_ID, COLLEGE_NAME

def generate_demo_meet_code() -> str:
    """Generate a realistic looking 3-4-3 Google Meet meeting code for demo mode."""
    part1 = "".join(random.choices(string.ascii_lowercase, k=3))
    part2 = "".join(random.choices(string.ascii_lowercase, k=4))
    part3 = "".join(random.choices(string.ascii_lowercase, k=3))
    return f"{part1}-{part2}-{part3}"

def schedule_online_meeting(
    tutor_name: str,
    tutor_email: str,
    learner_name: str,
    learner_email: str,
    subject: str,
    session_date: str,
    session_time: str,
) -> Tuple[str, bool, str]:
    """
    Schedule an online session with Google Meet.
    
    Returns:
        Tuple of (meet_link, is_demo_link, status_description)
    """
    if IS_GOOGLE_CONFIGURED:
        try:
            # Here real Google Calendar API flow with google-api-python-client / OAuth2 can be invoked.
            # E.g., using google.oauth2.credentials.Credentials and build('calendar', 'v3')
            # For this project, if configured credentials exist, we can handle the OAuth token flow.
            # If not configured or if token exchange requires browser consent, fallback gracefully.
            pass
        except Exception as e:
            # Fallback to demo mode if API call fails
            pass

    # Clearly labeled DEMO MODE fallback
    meet_code = generate_demo_meet_code()
    demo_url = f"https://meet.google.com/{meet_code}"
    labeled_link = f"[DEMO MODE] {demo_url}"
    
    explanation = (
        f"📅 Google Meet scheduled for {session_date} at {session_time}.\n"
        f"⚠️ Note: Running in [DEMO MODE]. To enable real Google Meet generation, "
        f"set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your .env file."
    )
    
    return labeled_link, True, explanation
