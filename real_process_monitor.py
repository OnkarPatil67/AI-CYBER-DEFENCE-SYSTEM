import psutil
import time
import json
from datetime import datetime

# SUSPICIOUS KEYWORDS

suspicious_keywords = [
    "nmap",
    "hydra",
    "wireshark",
    "metasploit",
    "aircrack",
    "john",
    "sqlmap"
]

# SAVE ALERT FUNCTION

def save_alert(alert_data):

    try:

        with open("alerts.json", "r") as file:
            alerts = json.load(file)

    except:
        alerts = []

    alerts.insert(0, alert_data)

    # keep only latest 20 alerts
    alerts = alerts[:20]

    with open("alerts.json", "w") as file:
        json.dump(alerts, file, indent=4)

# START MONITOR

print("\n======================================")
print(" REAL-TIME HOST PROCESS MONITOR ")
print("======================================\n")

while True:

    print("\nScanning Running Processes...\n")

    suspicious_found = False

    for process in psutil.process_iter(
        ['pid', 'name', 'cpu_percent']
    ):

        try:

            pid = process.info['pid']
            name = process.info['name']

            cpu = process.info['cpu_percent']

            if cpu is None:
                cpu = 0

            print(f"PID: {pid}")
            print(f"Process: {name}")
            print(f"CPU Usage: {cpu}%")
            print("--------------------------")

            # SUSPICIOUS TOOL DETECTION
            
            for keyword in suspicious_keywords:

                if keyword.lower() in str(name).lower():

                    suspicious_found = True

                    print("🚨 ALERT: Suspicious Tool Detected")

                    alert = {
                        "title": "Suspicious Tool Detected",
                        "description": f"{name} process detected",
                        "level": "CRITICAL",
                        "time": str(datetime.now())
                    }

                    save_alert(alert)

            # HIGH CPU DETECTION
            
            if cpu > 80:

                suspicious_found = True

                print("⚠ HIGH CPU PROCESS DETECTED")

                alert = {
                    "title": "High CPU Process Detected",
                    "description": f"{name} using {cpu}% CPU",
                    "level": "HIGH",
                    "time": str(datetime.now())
                }

                save_alert(alert)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            pass

    if not suspicious_found:

        print("\n✅ System Behavior Appears Normal")

    print("\nWaiting for next scan...\n")

    time.sleep(10)