"""
CLI Demo - Manual Testing Runner for Alerts & Notifications
"""

from datetime import datetime, timedelta
from .service import AlertsService
from .constants import Language


def run_demo():
    print("=" * 80)
    print("🌾 KISSAN MITRA - ALERTS SYSTEM MODULE DEMO 🌾")
    print("=" * 80)

    # Initialize Service
    service = AlertsService()
    
    # Farmer ID to test
    farmer_id = "FARMER001"
    
    print(f"\n[SYSTEM] Scanning for new alerts for: {farmer_id}...")
    
    # 1. Run Scan (Simulate last check was yesterday)
    last_check = datetime.now() - timedelta(days=1)
    output = service.run_alert_scan(farmer_id, last_check)
    
    # 2. Results
    print(f"\n✨ DASHBOARD HEADER: {output.header}")
    print(f"🌍 LANGUAGE: {output.language.value.upper()}")
    print(f"🔥 HIGHEST URGENCY: {output.urgencyLevel.upper()}")
    
    print("\n" + "-" * 40)
    print("🔊 VOICE OUTPUT (SPEECH TEXT):")
    print(output.speechText)
    print("-" * 40)
    
    print("\n🔔 ALERT CARDS (RANKED BY PRIORITY):")
    for idx, alert in enumerate(output.alerts, 1):
        print(f"\n{idx}. [{alert.urgency.upper()}] {alert.title}")
        print(f"   TYPE: {alert.alertType.value}")
        print(f"   MSG: {alert.message}")
        print(f"   SCHEDULED: {alert.scheduledAt.strftime('%H:%M %p')}")
        
    print("\n📊 SUMMARY COUNTS:")
    for level, count in output.summaryCounts.items():
        print(f"   - {level.capitalize()}: {count}")

    # 3. Mark as Read demonstration
    if output.alerts:
        alert_id = output.alerts[0].alertId
        print(f"\n[ACTION] Marking alert ID {alert_id[:8]}... as READ")
        service.mark_alert_as_read(alert_id)
        
        # Verify
        stored_alerts = service.alert_repo.list_alerts(farmer_id)
        read_count = len([a for a in stored_alerts if a.status.value == "read"])
        print(f"[SUCCESS] Alerts marked as read: {read_count}")

    print("\n" + "=" * 80)
    print("✅ BACKEND ALERTS MODULE - TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    run_demo()
