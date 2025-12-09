"""
Audit Logging and Intrusion Detection Module

Tracks all authentication attempts and detects suspicious patterns:
- Failed login attempts
- Multiple failures from same user
- Suspicious timing patterns
- Successful authentications
- Account lockouts
"""

import sqlite3
import datetime
import json
from collections import defaultdict
from typing import List, Dict, Tuple

AUDIT_DB = "audit_log.db"

# Intrusion detection thresholds
FAILED_ATTEMPTS_THRESHOLD = 5  # Max failed attempts before flagging
TIME_WINDOW_MINUTES = 15       # Time window to check for patterns
RAPID_ATTEMPTS_THRESHOLD = 10  # Attempts in short time = suspicious


def init_audit_db():
    """Initialize audit log database"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    # Audit log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            username TEXT NOT NULL,
            event_type TEXT NOT NULL,
            status TEXT NOT NULL,
            ip_address TEXT,
            details TEXT,
            risk_level TEXT DEFAULT 'LOW'
        )
    """)
    
    # Intrusion alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intrusion_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            username TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            resolved BOOLEAN DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()


def log_event(username: str, event_type: str, status: str, 
              ip_address: str = "127.0.0.1", details: dict = None):
    """
    Log an authentication event
    
    Args:
        username: Username attempting authentication
        event_type: LOGIN, TOTP, REGISTRATION, LOCKOUT
        status: SUCCESS, FAILURE, BLOCKED
        ip_address: IP address of client
        details: Additional event details
    """
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().isoformat()
    details_json = json.dumps(details) if details else None
    
    # Determine risk level
    risk_level = calculate_risk_level(username, event_type, status)
    
    cursor.execute("""
        INSERT INTO audit_log 
        (timestamp, username, event_type, status, ip_address, details, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, username, event_type, status, ip_address, details_json, risk_level))
    
    conn.commit()
    conn.close()
    
    # Check for intrusion patterns
    check_intrusion_patterns(username)


def calculate_risk_level(username: str, event_type: str, status: str) -> str:
    """Calculate risk level for an event"""
    if status == "FAILURE":
        # Check recent failures
        recent_failures = get_recent_failures(username, minutes=5)
        if len(recent_failures) >= 3:
            return "HIGH"
        elif len(recent_failures) >= 2:
            return "MEDIUM"
        return "LOW"
    
    if status == "BLOCKED":
        return "CRITICAL"
    
    if event_type == "REGISTRATION" and status == "SUCCESS":
        return "INFO"
    
    return "LOW"


def get_recent_failures(username: str, minutes: int = 15) -> List[Dict]:
    """Get recent failed attempts for a user"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    time_threshold = (datetime.datetime.now() - 
                     datetime.timedelta(minutes=minutes)).isoformat()
    
    cursor.execute("""
        SELECT timestamp, event_type, details 
        FROM audit_log
        WHERE username = ? 
        AND status = 'FAILURE'
        AND timestamp > ?
        ORDER BY timestamp DESC
    """, (username, time_threshold))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{"timestamp": r[0], "event_type": r[1], "details": r[2]} 
            for r in results]


def check_intrusion_patterns(username: str):
    """
    Detect intrusion patterns and create alerts
    
    Detects:
    1. Brute force attacks (multiple failed logins)
    2. Rapid-fire attempts (automated attacks)
    3. Account enumeration (testing multiple usernames)
    4. Time-based patterns (attacks at unusual hours)
    """
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    # Check for brute force
    recent_failures = get_recent_failures(username, TIME_WINDOW_MINUTES)
    
    if len(recent_failures) >= FAILED_ATTEMPTS_THRESHOLD:
        create_alert(
            username,
            "BRUTE_FORCE",
            "HIGH",
            f"Detected {len(recent_failures)} failed login attempts in {TIME_WINDOW_MINUTES} minutes"
        )
    
    # Check for rapid-fire attempts
    rapid_attempts = get_attempts_in_window(username, minutes=1)
    if len(rapid_attempts) >= RAPID_ATTEMPTS_THRESHOLD:
        create_alert(
            username,
            "RAPID_FIRE",
            "CRITICAL",
            f"Detected {len(rapid_attempts)} attempts in 1 minute - possible automated attack"
        )
    
    # Check for unusual timing
    current_hour = datetime.datetime.now().hour
    if current_hour < 6 or current_hour > 22:  # Between 10 PM and 6 AM
        if len(recent_failures) >= 2:
            create_alert(
                username,
                "UNUSUAL_TIMING",
                "MEDIUM",
                f"Multiple failed attempts detected at unusual hour ({current_hour}:00)"
            )
    
    conn.close()


def get_attempts_in_window(username: str, minutes: int = 1) -> List[Dict]:
    """Get all attempts (success + failure) in time window"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    time_threshold = (datetime.datetime.now() - 
                     datetime.timedelta(minutes=minutes)).isoformat()
    
    cursor.execute("""
        SELECT timestamp, event_type, status
        FROM audit_log
        WHERE username = ?
        AND timestamp > ?
        ORDER BY timestamp DESC
    """, (username, time_threshold))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{"timestamp": r[0], "event_type": r[1], "status": r[2]} 
            for r in results]


def create_alert(username: str, alert_type: str, severity: str, description: str):
    """Create an intrusion detection alert"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().isoformat()
    
    # Check if similar alert already exists (avoid duplicates)
    cursor.execute("""
        SELECT COUNT(*) FROM intrusion_alerts
        WHERE username = ?
        AND alert_type = ?
        AND resolved = 0
        AND timestamp > ?
    """, (username, alert_type, 
          (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()))
    
    if cursor.fetchone()[0] == 0:  # No recent unresolved alert
        cursor.execute("""
            INSERT INTO intrusion_alerts
            (timestamp, username, alert_type, severity, description)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, username, alert_type, severity, description))
        
        conn.commit()
    
    conn.close()


def get_active_alerts() -> List[Dict]:
    """Get all unresolved intrusion alerts"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, username, alert_type, severity, description
        FROM intrusion_alerts
        WHERE resolved = 0
        ORDER BY timestamp DESC
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    return [{
        "id": r[0],
        "timestamp": r[1],
        "username": r[2],
        "alert_type": r[3],
        "severity": r[4],
        "description": r[5]
    } for r in results]


def resolve_alert(alert_id: int):
    """Mark an alert as resolved"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE intrusion_alerts
        SET resolved = 1
        WHERE id = ?
    """, (alert_id,))
    
    conn.commit()
    conn.close()


def get_audit_summary(hours: int = 24) -> Dict:
    """Get audit summary statistics"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    time_threshold = (datetime.datetime.now() - 
                     datetime.timedelta(hours=hours)).isoformat()
    
    # Total attempts
    cursor.execute("""
        SELECT COUNT(*) FROM audit_log
        WHERE timestamp > ?
    """, (time_threshold,))
    total_attempts = cursor.fetchone()[0]
    
    # Success vs failure
    cursor.execute("""
        SELECT status, COUNT(*) FROM audit_log
        WHERE timestamp > ?
        GROUP BY status
    """, (time_threshold,))
    status_counts = dict(cursor.fetchall())
    
    # Top users with failures
    cursor.execute("""
        SELECT username, COUNT(*) as failures
        FROM audit_log
        WHERE timestamp > ?
        AND status = 'FAILURE'
        GROUP BY username
        ORDER BY failures DESC
        LIMIT 5
    """, (time_threshold,))
    top_failed_users = cursor.fetchall()
    
    # Active alerts
    cursor.execute("""
        SELECT severity, COUNT(*)
        FROM intrusion_alerts
        WHERE resolved = 0
        GROUP BY severity
    """)
    alert_counts = dict(cursor.fetchall())
    
    conn.close()
    
    return {
        "total_attempts": total_attempts,
        "successful": status_counts.get("SUCCESS", 0),
        "failed": status_counts.get("FAILURE", 0),
        "blocked": status_counts.get("BLOCKED", 0),
        "top_failed_users": top_failed_users,
        "active_alerts": alert_counts,
        "time_window_hours": hours
    }


def get_user_activity(username: str, limit: int = 50) -> List[Dict]:
    """Get activity history for a specific user"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp, event_type, status, risk_level, details
        FROM audit_log
        WHERE username = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (username, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{
        "timestamp": r[0],
        "event_type": r[1],
        "status": r[2],
        "risk_level": r[3],
        "details": json.loads(r[4]) if r[4] else None
    } for r in results]


def export_audit_log(filename: str = "audit_export.json"):
    """Export audit log to JSON file"""
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp, username, event_type, status, ip_address, details, risk_level
        FROM audit_log
        ORDER BY timestamp DESC
    """)
    
    logs = [{
        "timestamp": r[0],
        "username": r[1],
        "event_type": r[2],
        "status": r[3],
        "ip_address": r[4],
        "details": json.loads(r[5]) if r[5] else None,
        "risk_level": r[6]
    } for r in cursor.fetchall()]
    
    conn.close()
    
    with open(filename, 'w') as f:
        json.dump({
            "export_date": datetime.datetime.now().isoformat(),
            "total_entries": len(logs),
            "logs": logs
        }, f, indent=2)
    
    return filename


# Initialize database on import
init_audit_db()
