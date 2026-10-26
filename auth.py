"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Authentication, Password Security (PBKDF2-HMAC-SHA256), and Session Helpers.
"""

import hashlib
import os
import re
from typing import Optional, Tuple, Dict, Any
from database import get_db_connection

# Hash parameters
HASH_ALGORITHM = "sha256"
ITERATIONS = 200_000
SALT_BYTES = 16

def hash_password(password: str) -> Tuple[str, str]:
    """
    Hash a password securely using PBKDF2-HMAC-SHA256 with a unique random salt.
    Returns (hex_hash, hex_salt).
    """
    salt = os.urandom(SALT_BYTES)
    key = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode("utf-8"), salt, ITERATIONS)
    return key.hex(), salt.hex()

def verify_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    """
    Verify a candidate password against the stored PBKDF2 hash and salt.
    """
    try:
        salt = bytes.fromhex(stored_salt)
        key = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode("utf-8"), salt, ITERATIONS)
        return key.hex() == stored_hash
    except Exception:
        return False

def validate_college_email(email: str) -> bool:
    """Validate student email structure."""
    email = email.strip().lower()
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(regex, email))

def register_user(
    name: str,
    email: str,
    password: str,
    department: str,
    year_of_study: str,
    bio: str = "",
    learning_interests: str = "",
    is_admin: bool = False,
) -> Tuple[bool, str, Optional[int]]:
    """
    Register a new student account.
    Returns (success, message, user_id).
    """
    name = name.strip()
    email = email.strip().lower()

    if not name:
        return False, "Full Name is required.", None
    if not email:
        return False, "College Email is required.", None
    if not validate_college_email(email):
        return False, "Please provide a valid email address (e.g., student@sece.ac.in).", None
    if len(password) < 6:
        return False, "Password must be at least 6 characters long.", None
    if not department:
        return False, "Please select your department.", None
    if not year_of_study:
        return False, "Please select your year of study.", None

    pwd_hash, salt = hash_password(password)

    try:
        with get_db_connection() as conn:
            # Check existing email
            cur = conn.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cur.fetchone():
                return False, f"An account with email '{email}' already exists. Please log in.", None

            cur = conn.execute(
                """
                INSERT INTO users (name, email, password_hash, salt, department, year_of_study, bio, learning_interests, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (name, email, pwd_hash, salt, department, year_of_study, bio.strip(), learning_interests.strip(), 1 if is_admin else 0),
            )
            conn.commit()
            return True, "Registration successful! You can now log in.", cur.lastrowid
    except Exception as e:
        return False, f"Database error during registration: {str(e)}", None

def authenticate_user(email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Authenticate user with email and password.
    Returns (success, message, user_dict).
    """
    email = email.strip().lower()
    if not email or not password:
        return False, "Please enter both email and password.", None

    with get_db_connection() as conn:
        cur = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        if not row:
            return False, "Invalid email or password. Please check your credentials.", None

        if not verify_password(password, row["password_hash"], row["salt"]):
            return False, "Invalid email or password. Please check your credentials.", None

        user_data = dict(row)
        # Never keep hash & salt in active user session object
        user_data.pop("password_hash", None)
        user_data.pop("salt", None)
        return True, "Login successful!", user_data

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve user record by ID (sanitized of password hash)."""
    with get_db_connection() as conn:
        cur = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        user_data = dict(row)
        user_data.pop("password_hash", None)
        user_data.pop("salt", None)
        return user_data

def update_user_profile(
    user_id: int,
    name: str,
    department: str,
    year_of_study: str,
    bio: str,
    learning_interests: str,
) -> Tuple[bool, str]:
    """Update profile fields for an authenticated student."""
    name = name.strip()
    if not name:
        return False, "Name cannot be empty."

    try:
        with get_db_connection() as conn:
            conn.execute(
                """
                UPDATE users
                SET name = ?, department = ?, year_of_study = ?, bio = ?, learning_interests = ?
                WHERE id = ?
                """,
                (name, department, year_of_study, bio.strip(), learning_interests.strip(), user_id),
            )
            conn.commit()
            return True, "Profile updated successfully!"
    except Exception as e:
        return False, f"Failed to update profile: {str(e)}"
