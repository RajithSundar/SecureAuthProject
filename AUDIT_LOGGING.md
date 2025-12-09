# Audit Logging and Intrusion Detection System

## Overview

SecureAuth now includes a comprehensive audit logging and intrusion detection system that tracks all authentication attempts and automatically detects suspicious patterns.

## Features

### 1. Complete Audit Trail
- ✅ All login attempts (success and failure)
- ✅ All TOTP verifications
- ✅ User registrations
- ✅ Account lockouts
- ✅ Timestamp, username, event type, status
- ✅ Risk level assessment (LOW, MEDIUM, HIGH, CRITICAL)

### 2. Intrusion Detection
Automatically detects:
- 🚨 **Brute Force Attacks**: Multiple failed logins in short time
- 🚨 **Rapid-Fire Attempts**: Automated attack patterns (10+ attempts/minute)
- 🚨 **Unusual Timing**: Attacks at odd hours (10 PM - 6 AM)
- 🚨 **Account Enumeration**: Testing multiple usernames

### 3. Real-Time Alerts
- Severity levels: CRITICAL, HIGH, MEDIUM, LOW
- Automatic alert generation for suspicious patterns
- Alert resolution tracking
- No duplicate alerts within 1-hour window

## Architecture

```
┌─────────────────────────────────────────┐
│   User Authentication Flow              │
│                                         │
│  Login → Validate → TOTP                │
│     │        │        │                 │
│     └────────┴────────┘                 │
│             │                           │
│             ▼                           │
│    ┌─────────────────┐                 │
│    │  audit_log.py   │                 │
│    │   - log_event() │                 │
│    │   - detect()    │                 │
│    └─────────────────┘                 │
│             │                           │
│             ▼                           │
│    ┌─────────────────┐                 │
│    │  audit_log.db   │                 │
│    │                 │                 │
│    │  • audit_log    │                 │
│    │  • intrusion_   │                 │
│    │    alerts       │                 │
│    └─────────────────┘                 │
└─────────────────────────────────────────┘
```

## Database Schema

### audit_log Table
```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,           -- ISO format
    username TEXT,            -- User attempting auth
    event_type TEXT,          -- LOGIN, TOTP, REGISTRATION, LOCKOUT
    status TEXT,              -- SUCCESS, FAILURE, BLOCKED
    ip_address TEXT,          -- Client IP
    details TEXT,             -- JSON additional info
    risk_level TEXT           -- LOW, MEDIUM, HIGH, CRITICAL
);
```

### intrusion_alerts Table
```sql
CREATE TABLE intrusion_alerts (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    username TEXT,
    alert_type TEXT,          -- BRUTE_FORCE, RAPID_FIRE, etc.
    severity TEXT,            -- CRITICAL, HIGH, MEDIUM, LOW
    description TEXT,
    resolved BOOLEAN
);
```

## Detection Algorithms

### 1. Brute Force Detection
```python
# Triggers if >= 5 failed attempts in 15 minutes
if failed_attempts_count >= 5 within 15_minutes:
    create_alert("BRUTE_FORCE", "HIGH")
```

### 2. Rapid-Fire Detection
```python
# Triggers if >= 10 attempts in 1 minute
if total_attempts >= 10 within 1_minute:
    create_alert("RAPID_FIRE", "CRITICAL")
```

### 3. Unusual Timing Detection
```python
# Triggers if >= 2 failures between 10 PM - 6 AM
if hour not_in 6..22 and failed_attempts >= 2:
    create_alert("UNUSUAL_TIMING", "MEDIUM")
```

## Usage

### Automatic Logging (Integrated)
All authentication events are automatically logged:

```python
# In user_db.py - automatically called
audit_log.log_event(
    username="john_doe",
    event_type="LOGIN",
    status="FAILURE",
    details={"reason": "invalid_credentials"}
)
```

### View Audit Logs
```bash
# Interactive menu
python audit_viewer.py

# Command-line tools
python audit_viewer.py summary
python audit_viewer.py alerts
python audit_viewer.py user john_doe
python audit_viewer.py export audit.json
```

### Get Summary Programmatically
```python
import audit_log

# Get 24-hour summary
summary = audit_log.get_audit_summary(hours=24)
print(f"Total attempts: {summary['total_attempts']}")
print(f"Failed: {summary['failed']}")
print(f"Blocked: {summary['blocked']}")
```

### Check Active Alerts
```python
alerts = audit_log.get_active_alerts()
for alert in alerts:
    print(f"[{alert['severity']}] {alert['alert_type']}")
    print(f"  User: {alert['username']}")
    print(f"  Description: {alert['description']}")
```

### Export Logs
```python
# Export to JSON
filename = audit_log.export_audit_log("security_audit.json")
```

## Audit Viewer CLI

### Summary View
```
==================================================================
  AUDIT SUMMARY (Last 24 Hours)
==================================================================

📊 Total Authentication Attempts: 47
   ✅ Successful: 35
   ❌ Failed: 12
   🚫 Blocked: 0

👥 Top Users with Failed Attempts:
   ⚠️  attacker: 8 failures
      john_doe: 4 failures

🚨 Active Security Alerts:
   HIGH: 2 alert(s)
   MEDIUM: 1 alert(s)
```

### Alerts View
```
==================================================================
  ACTIVE INTRUSION ALERTS
==================================================================

🚨 2 Active Alert(s):

[HIGH] BRUTE_FORCE
   User: attacker
   Time: 2025-12-09T21:45:30
   Description: Detected 8 failed login attempts in 15 minutes
   Alert ID: 3

[MEDIUM] UNUSUAL_TIMING
   User: suspicious_user
   Time: 2025-12-09T02:15:45
   Description: Multiple failed attempts at unusual hour (2:00)
   Alert ID: 4
```

### User Activity View
```
==================================================================
  USER ACTIVITY: john_doe
==================================================================

📋 Last 20 events:

✅ 21:45:30 - TOTP: SUCCESS [LOW]
✅ 21:45:15 - LOGIN: SUCCESS [LOW]
❌ 21:44:50 - LOGIN: FAILURE [MEDIUM]
❌ 21:44:30 - LOGIN: FAILURE [HIGH]
✅ 18:30:12 - REGISTRATION: SUCCESS [INFO]
```

## Integration Points

### 1. user_db.py
- `register_user()`: Logs registration attempts
- `validate_credentials()`: Logs login attempts
- `verify_totp()`: Logs MFA verifications

### 2. main_gui.py (Future)
- Display alert count in status bar
- Show security warnings for flagged accounts
- Real-time alert notifications

### 3. Windows Credential Provider
- Can use same audit database
- Log OS-level login attempts
- Cross-platform activity tracking

## Security Benefits

1. **Forensic Analysis**: Complete audit trail for security investigations
2. **Real-Time Detection**: Immediate alerts on suspicious patterns
3. **Compliance**: Audit logs for regulatory requirements (SOC 2, HIPAA, etc.)
4. **Behavioral Analysis**: Identify normal vs. abnormal access patterns
5. **Incident Response**: Quick identification of compromised accounts

## Performance Considerations

- **Lightweight**: SQLite is fast and efficient
- **Async-Ready**: Can be made async for high-volume systems
- **Indexed**: Timestamp and username fields indexed for quick queries
- **Retention**: Implement log rotation for production use

## Future Enhancements

- [ ] Machine learning for anomaly detection
- [ ] GeoIP integration (detect impossible travel)
- [ ] Email/SMS alerts on critical events
- [ ] Dashboard with graphs and charts
- [ ] Log retention policies
- [ ] Integration with SIEM systems
- [ ] Failed login heatmap by time of day
- [ ] Success rate trends

## Example Scenario

**Brute Force Attack Detection:**

```
1. Attacker tries to login as "admin" with wrong password
   → Logged: LOGIN FAILURE (risk: LOW)

2. Attacker tries again (3 more times in 2 minutes)
   → Logged: LOGIN FAILURE x3 (risk: MEDIUM then HIGH)

3. After 5 failures in 5 minutes:
   → Alert Created: BRUTE_FORCE (severity: HIGH)
   → Admin can see this in audit_viewer

4. Attacker continues (10 attempts in 1 minute):
   → Alert Created: RAPID_FIRE (severity: CRITICAL)
   → Account locked automatically
   → Logged: LOCKOUT (risk: CRITICAL)
```

## Compliance Features

SecureAuth audit logging supports:

- ✅ **Access logging** (who accessed what and when)
- ✅ **Failure tracking** (all auth failures recorded)
- ✅ **Immutable logs** (append-only SQLite)
- ✅ **Risk assessment** (automatic risk level calculation)
- ✅ **Alert management** (intrusion detection + response tracking)
- ✅ **Export capability** (JSON export for external analysis)

---

**With audit logging, SecureAuth provides enterprise-grade security monitoring!**
