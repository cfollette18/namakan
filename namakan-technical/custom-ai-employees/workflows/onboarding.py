#!/usr/bin/env python3
"""
AI Employee Onboarding — Custom AI Employees Pipeline
Four-phase onboarding: Shadow → Assist → Partial → Full Autonomy
Usage: python3 onboarding.py --employee "acme-cs-agent" --phase shadow
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta

PHASES = {
    "shadow": {
        "name": "Shadow Mode",
        "description": "AI observes human, takes no action. Learns workflows.",
        "duration_days": 7,
        "color": "\033[94m",  # Blue
        "actions": ["observe", "log_patterns", "learn_workflows"],
        "supervisor_duties": [
            "Review AI's activity log daily",
            "Confirm AI's understanding of correct responses",
            "Provide feedback on observed patterns"
        ]
    },
    "assist": {
        "name": "Assist Mode",
        "description": "AI suggests responses but human approves before action.",
        "duration_days": 14,
        "color": "\033[93m",  # Yellow
        "actions": ["suggest_response", "await_approval", "log_approvals"],
        "supervisor_duties": [
            "Review and approve/reject each AI suggestion",
            "Provide reasoning for rejections",
            "Track AI suggestion accuracy rate"
        ]
    },
    "partial": {
        "name": "Partial Autonomy",
        "description": "AI handles routine tasks autonomously. Complex cases escalate.",
        "duration_days": 14,
        "color": "\033[95m",  # Purple
        "actions": ["handle_routine", "escalate_complex", "self_review"],
        "supervisor_duties": [
            "Review escalations daily",
            "Track routine vs complex task ratio",
            "Confirm AI handling edge cases correctly"
        ]
    },
    "full": {
        "name": "Full Autonomy",
        "description": "AI operates independently with monitoring.",
        "duration_days": None,  # Ongoing
        "color": "\033[92m",  # Green
        "actions": ["operate_independently", "monitor_metrics", "quarterly_review"],
        "supervisor_duties": [
            "Weekly performance review",
            "Monthly metrics analysis",
            "Quarterly strategy alignment"
        ]
    }
}

PHASE_ORDER = ["shadow", "assist", "partial", "full"]
RESET = "\033[0m"

def color(c, text):
    return f"{c}{text}{RESET}"

def load_employee(emp_dir):
    config_path = f"{emp_dir}/config.json"
    if not os.path.exists(config_path):
        print(f"ERROR: Employee config not found at {config_path}")
        print("Run: python3 intake.py --client 'Acme Corp' --role 'customer-service'")
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)

def save_employee(emp_dir, config):
    with open(f"{emp_dir}/config.json", "w") as f:
        json.dump(config, f, indent=2)

def log_event(emp_dir, phase, event_type, message):
    log_file = f"{emp_dir}/onboarding_log.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "type": event_type,
        "message": message
    }
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

def check_phase_progress(emp_dir, phase):
    """Check how the current phase is going."""
    phase_config = PHASES[phase]
    log_file = f"{emp_dir}/onboarding_log.jsonl"
    
    if not os.path.exists(log_file):
        return {"events_today": 0, "total_events": 0, "days_in_phase": 0}
    
    events = []
    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    
    phase_events = [e for e in events if e.get("phase") == phase]
    today = datetime.now().date()
    
    return {
        "events_today": sum(1 for e in phase_events if datetime.fromisoformat(e["timestamp"]).date() == today),
        "total_events": len(phase_events),
        "days_in_phase": 0  # Would track from phase start date
    }

def advance_phase(emp_dir, from_phase, to_phase):
    """Move employee to next onboarding phase."""
    config = load_employee(emp_dir)
    
    if from_phase not in PHASE_ORDER or to_phase not in PHASE_ORDER:
        print(f"ERROR: Invalid phase transition {from_phase} → {to_phase}")
        sys.exit(1)
    
    from_idx = PHASE_ORDER.index(from_phase)
    to_idx = PHASE_ORDER.index(to_phase)
    
    if to_idx != from_idx + 1:
        print(f"ERROR: Can only advance one phase at a time. {from_phase} → {to_phase} not allowed.")
        sys.exit(1)
    
    config["current_phase"] = to_phase
    config["phase_history"].append({
        "from": from_phase,
        "to": to_phase,
        "transition_date": datetime.now().isoformat()
    })
    
    save_employee(emp_dir, config)
    log_event(emp_dir, to_phase, "phase_advance", f"Advanced from {from_phase} to {to_phase}")
    
    phase = PHASES[to_phase]
    phase_name = phase['name']
    print(f"\n{color(phase['color'], '─'*60)}")
    print(f"  {color(phase['color'], f'✓ PHASE ADVANCED: {phase_name}')}")
    print(f"  {color(phase['color'], '─'*60)}")
    print(f"\n  {phase['description']}")
    print(f"\n  Supervisor duties:")
    for duty in phase["supervisor_duties"]:
        print(f"    • {duty}")
    print(f"\n  Duration: {phase['duration_days'] or 'Ongoing'} days")
    print(f"\n  Employee: {config.get('name', 'Unknown')}")
    print(f"  Company: {config.get('company', 'Unknown')}")
    print(f"{color(phase['color'], '─'*60)}\n")

def print_status(emp_dir):
    """Print current onboarding status."""
    config = load_employee(emp_dir)
    phase_key = config.get("current_phase", "shadow")
    phase = PHASES[phase_key]
    
    progress = check_phase_progress(emp_dir, phase_key)
    
    print(f"\n{color(phase['color'], '═'*60)}")
    print(f"  AI EMPLOYEE ONBOARDING STATUS")
    print(f"{color(phase['color'], '═'*60)}")
    print(f"\n  Employee: {config.get('name', 'Unknown')}")
    print(f"  Role:     {config.get('role', 'Unknown')}")
    print(f"  Company:  {config.get('company', 'Unknown')}")
    print(f"\n  Current phase: {color(phase['color'], phase['name'])}")
    print(f"  Description: {phase['description']}")
    print(f"\n  Phase progress:")
    print(f"    Total events: {progress['total_events']}")
    print(f"    Events today: {progress['events_today']}")
    
    if config.get("phase_history"):
        last = config["phase_history"][-1]
        print(f"\n  Last advance: {last['from']} → {last['to']} on {last['transition_date'][:10]}")
    
    # Progress bar
    current_idx = PHASE_ORDER.index(phase_key)
    bar = ""
    for i, p in enumerate(PHASE_ORDER):
        c = PHASES[p]["color"]
        if i < current_idx:
            bar += color(c, "■")
        elif i == current_idx:
            bar += color(c, "□")
        else:
            bar += "\033[90m□\033[0m"
    bar += f" {PHASE_ORDER[current_idx].upper()}"
    print(f"\n  Progress: {bar}")
    
    print(f"\n  Supervisor: {config.get('supervisor_name', 'Not assigned')}")
    print(f"  Supervisor email: {config.get('supervisor_email', 'Not set')}")
    print(f"\n  Next phase: {PHASE_ORDER[current_idx + 1] if current_idx < len(PHASE_ORDER) - 1 else 'FULLY DEPLOYED'}")
    print(f"{color(phase['color'], '═'*60)}\n")

def daily_checkin(emp_dir):
    """Daily supervisor check-in for onboarding."""
    config = load_employee(emp_dir)
    phase_key = config.get("current_phase", "shadow")
    phase = PHASES[phase_key]
    
    log_event(emp_dir, phase_key, "daily_checkin", "Supervisor daily review completed")
    
    print(f"\n{color(phase['color'], '─'*60)}")
    print(f"  Daily Check-in — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  Phase: {phase['name']}")
    print(f"{color(phase['color'], '─'*60)}")
    
    # Questions for supervisor
    print(f"\n  Supervisor review:")
    print(f"  1. Did the AI handle any tasks today? (y/n)")
    print(f"  2. Any escalations needed? (y/n)")
    print(f"  3. AI suggestion accuracy (0-100%)?")
    print(f"  4. Notes for improvement?")
    
    # For automation: just log a generic checkin
    log_event(emp_dir, phase_key, "supervisor_review", "Daily review logged")

def main():
    parser = argparse.ArgumentParser(description="Namakan AI Employee Onboarding")
    parser.add_argument("--employee", required=True, help="Employee directory or name")
    parser.add_argument("--phase", help=f"Set phase: {', '.join(PHASE_ORDER)}")
    parser.add_argument("--advance", action="store_true", help="Advance to next phase")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--checkin", action="store_true", help="Daily check-in")
    parser.add_argument("--clients-dir", default="./clients", help="Clients directory")
    args = parser.parse_args()
    
    # Find employee directory
    emp_slug = args.employee.lower().replace(" ", "-")
    emp_dir = os.path.join(args.clients_dir, emp_slug)
    
    if not os.path.exists(emp_dir):
        print(f"ERROR: Employee not found: {emp_dir}")
        print("Run: python3 intake.py --client 'Acme Corp' --role 'customer-service'")
        sys.exit(1)
    
    if args.status:
        print_status(emp_dir)
    elif args.checkin:
        daily_checkin(emp_dir)
    elif args.phase:
        config = load_employee(emp_dir)
        current = config.get("current_phase", "shadow")
        if args.phase == current:
            print(f"Already in {current} phase")
        else:
            advance_phase(emp_dir, current, args.phase)
    elif args.advance:
        config = load_employee(emp_dir)
        current = config.get("current_phase", "shadow")
        current_idx = PHASE_ORDER.index(current)
        if current_idx < len(PHASE_ORDER) - 1:
            advance_phase(emp_dir, current, PHASE_ORDER[current_idx + 1])
        else:
            print("Employee is already at full autonomy!")
    else:
        print_status(emp_dir)
        print("Usage:")
        print("  python3 onboarding.py --employee acme-cs --status")
        print("  python3 onboarding.py --employee acme-cs --advance")
        print("  python3 onboarding.py --employee acme-cs --phase assist")
        print("  python3 onboarding.py --employee acme-cs --checkin")

if __name__ == "__main__":
    main()
