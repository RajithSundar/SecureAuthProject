"""
User Database Module
Handles user registration, authentication, and TOTP secret management using SQLite.
"""

import sqlite3
import hashlib
import pyotp
import os
import audit_log  # Audit logging integration

DB_FILENAME = "users.db"


def init_db():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            totp_secret TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def generate_totp_secret():
    """Generate a random Base32 TOTP secret for Google Authenticator"""
    return pyotp.random_base32()


def register_user(username, password):
    """
    Register a new user with username and password.
    Returns (success: bool, message: str, totp_secret: str or None)
    """
    if not username or not password:
        return False, "Username and password cannot be empty", None
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters", None
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters", None
    
    # Check if user already exists
    if user_exists(username):
        return False, "Username already exists", None
    
    # Hash password and generate TOTP secret
    pwd_hash = hash_password(password)
    totp_secret = generate_totp_secret()
    
    # Store in database
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, totp_secret) VALUES (?, ?, ?)",
            (username, pwd_hash, totp_secret)
        )
        conn.commit()
        conn.close()
        
        # Audit log: Successful registration
        audit_log.log_event(
            username=username,
            event_type="REGISTRATION",
            status="SUCCESS",
            details={"secret_generated": True}
        )
        
        return True, "Registration successful", totp_secret
    except Exception as e:
        # Audit log: Failed registration
        audit_log.log_event(
            username=username,
            event_type="REGISTRATION",
            status="FAILURE",
            details={"error": str(e)}
        )
        return False, f"Database error: {str(e)}", None


def validate_credentials(username, password):
    """
    Validate username and password.
    Returns True if credentials are valid, False otherwise.
    """
    if not username or not password:
        audit_log.log_event(
            username=username or "EMPTY",
            event_type="LOGIN",
            status="FAILURE",
            details={"reason": "empty_credentials"}
        )
        return False
    
    pwd_hash = hash_password(password)
    
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == pwd_hash:
            # Audit log: Successful login (password stage)
            audit_log.log_event(
                username=username,
                event_type="LOGIN",
                status="SUCCESS",
                details={"stage": "password_verified"}
            )
            return True
        else:
            # Audit log: Failed login
            audit_log.log_event(
                username=username,
                event_type="LOGIN",
                status="FAILURE",
                details={"reason": "invalid_credentials"}
            )
            return False
    except Exception as e:
        audit_log.log_event(
            username=username,
            event_type="LOGIN",
            status="FAILURE",
            details={"reason": "database_error", "error": str(e)}
        )
        return False


def get_user_secret(username):
    """
    Retrieve the TOTP secret for a given username.
    Returns the secret string or None if user not found.
    """
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT totp_secret FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None
    except Exception:
        return None


def user_exists(username):
    """Check if a username already exists in the database"""
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?",
            (username,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Exception:
        return False


def verify_totp(username, totp_code):
    """
    Verify a TOTP code for a given user.
    Returns True if valid, False otherwise.
    """
    secret = get_user_secret(username)
    if not secret:
        audit_log.log_event(
            username=username,
            event_type="TOTP",
            status="FAILURE",
            details={"reason": "no_secret_found"}
        )
        return False
    
    try:
        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(totp_code, valid_window=1)
        
        if is_valid:
            # Audit log: Successful TOTP verification
            audit_log.log_event(
                username=username,
                event_type="TOTP",
                status="SUCCESS",
                details={"mfa_completed": True}
            )
        else:
            # Audit log: Failed TOTP verification
            audit_log.log_event(
                username=username,
                event_type="TOTP",
                status="FAILURE",
                details={"reason": "invalid_totp_code"}
            )
        
        return is_valid
    except Exception as e:
        audit_log.log_event(
            username=username,
            event_type="TOTP",
            status="FAILURE",
            details={"reason": "verification_error", "error": str(e)}
        )
        return False


# Initialize database on module import
if not os.path.exists(DB_FILENAME):
    init_db()
