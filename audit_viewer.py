"""
Audit Log Viewer and Analyzer

Command-line tool to view and analyze audit logs and intrusion alerts.
"""

import audit_log
import sys
from datetime import datetime


def print_header(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_colored(text, color="white"):
    """Print colored text (basic colors)"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[0m"
    }
    end = "\033[0m"
    print(f"{colors.get(color, colors['white'])}{text}{end}")


def show_summary():
    """Display audit summary"""
    print_header("AUDIT SUMMARY (Last 24 Hours)")
    
    summary = audit_log.get_audit_summary(hours=24)
    
    print(f"\n📊 Total Authentication Attempts: {summary['total_attempts']}")
    print(f"   ✅ Successful: {summary['successful']}")
    print(f"   ❌ Failed: {summary['failed']}")
    print(f"   🚫 Blocked: {summary['blocked']}")
    
    if summary['top_failed_users']:
        print("\n👥 Top Users with Failed Attempts:")
        for username, count in summary['top_failed_users']:
            if count >= 5:
                print_colored(f"   ⚠️  {username}: {count} failures", "red")
            elif count >= 3:
                print_colored(f"   ⚠️  {username}: {count} failures", "yellow")
            else:
                print(f"      {username}: {count} failures")
    
    if summary['active_alerts']:
        print("\n🚨 Active Security Alerts:")
        for severity, count in summary['active_alerts'].items():
            color = {"CRITICAL": "red", "HIGH": "red", 
                    "MEDIUM": "yellow", "LOW": "blue"}.get(severity, "white")
            print_colored(f"   {severity}: {count} alert(s)", color)


def show_alerts():
    """Display active intrusion alerts"""
    print_header("ACTIVE INTRUSION ALERTS")
    
    alerts = audit_log.get_active_alerts()
    
    if not alerts:
        print_colored("\n✅ No active alerts - system is secure!", "green")
        return
    
    print(f"\n🚨 {len(alerts)} Active Alert(s):\n")
    
    for alert in alerts:
        severity_color = {
            "CRITICAL": "red",
            "HIGH": "red",
            "MEDIUM": "yellow",
            "LOW": "blue"
        }.get(alert['severity'], "white")
        
        print_colored(f"[{alert['severity']}] {alert['alert_type']}", severity_color)
        print(f"   User: {alert['username']}")
        print(f"   Time: {alert['timestamp']}")
        print(f"   Description: {alert['description']}")
        print(f"   Alert ID: {alert['id']}")
        print()


def show_user_activity(username):
    """Display activity for a specific user"""
    print_header(f"USER ACTIVITY: {username}")
    
    activities = audit_log.get_user_activity(username, limit=20)
    
    if not activities:
        print(f"\nNo activity found for user: {username}")
        return
    
    print(f"\n📋 Last {len(activities)} events:\n")
    
    for activity in activities:
        # Color code by status
        if activity['status'] == 'SUCCESS':
            status_symbol = "✅"
            color = "green"
        elif activity['status'] == 'FAILURE':
            status_symbol = "❌"
            color = "red"
        else:
            status_symbol = "⚠️"
            color = "yellow"
        
        time_str = activity['timestamp'].split('T')[1][:8]  # Just HH:MM:SS
        
        print_colored(
            f"{status_symbol} {time_str} - {activity['event_type']}: {activity['status']} "
            f"[{activity['risk_level']}]",
            color if activity['status'] == 'FAILURE' else "white"
        )


def export_logs():
    """Export audit logs to JSON"""
    print_header("EXPORT AUDIT LOGS")
    
    filename = input("\nEnter filename (default: audit_export.json): ").strip()
    if not filename:
        filename = "audit_export.json"
    
    result = audit_log.export_audit_log(filename)
    print_colored(f"\n✅ Audit logs exported to: {result}", "green")


def resolve_alert_interactive():
    """Interactively resolve alerts"""
    print_header("RESOLVE ALERTS")
    
    alerts = audit_log.get_active_alerts()
    
    if not alerts:
        print_colored("\n✅ No active alerts to resolve!", "green")
        return
    
    print("\nActive Alerts:")
    for i, alert in enumerate(alerts, 1):
        print(f"\n{i}. [{alert['severity']}] {alert['username']} - {alert['alert_type']}")
        print(f"   {alert['description']}")
        print(f"   Alert ID: {alert['id']}")
    
    try:
        choice = input("\nEnter alert number to resolve (or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            return
        
        idx = int(choice) - 1
        if 0 <= idx < len(alerts):
            alert_id = alerts[idx]['id']
            audit_log.resolve_alert(alert_id)
            print_colored(f"\n✅ Alert {alert_id} marked as resolved!", "green")
        else:
            print_colored("\n❌ Invalid choice!", "red")
    except ValueError:
        print_colored("\n❌ Invalid input!", "red")


def main_menu():
    """Main interactive menu"""
    while True:
        print_header("SECUREAUTH AUDIT LOG VIEWER")
        print("\n1. View Audit Summary")
        print("2. View Active Alerts")
        print("3. View User Activity")
        print("4. Export Audit Logs")
        print("5. Resolve Alerts")
        print("6. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            show_summary()
        elif choice == '2':
            show_alerts()
        elif choice == '3':
            username = input("Enter username: ").strip()
            show_user_activity(username)
        elif choice == '4':
            export_logs()
        elif choice == '5':
            resolve_alert_interactive()
        elif choice == '6':
            print("\nExiting...")
            break
        else:
            print_colored("\n❌ Invalid option!", "red")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Check if command-line arguments provided
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "summary":
            show_summary()
        elif command == "alerts":
            show_alerts()
        elif command == "user" and len(sys.argv) > 2:
            show_user_activity(sys.argv[2])
        elif command == "export":
            filename = sys.argv[2] if len(sys.argv) > 2 else "audit_export.json"
            audit_log.export_audit_log(filename)
            print(f"Exported to: {filename}")
        else:
            print("Usage:")
            print("  python audit_viewer.py summary")
            print("  python audit_viewer.py alerts")
            print("  python audit_viewer.py user <username>")
            print("  python audit_viewer.py export [filename]")
    else:
        # Interactive mode
        main_menu()
