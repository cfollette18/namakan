#!/usr/bin/env python3
"""
AI Employee Performance Monitor
Tracks KPIs, flags issues, triggers retraining.
Usage: python3 monitor.py --employee acme-cs-agent --report
"""
import argparse, json, os, sys
from datetime import datetime, timedelta

def load_employee(emp_dir):
    config_path = f"{emp_dir}/config.json"
    if not os.path.exists(config_path):
        print(f"ERROR: Employee not found: {config_path}")
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)

def load_logs(emp_dir):
    log_file = f"{emp_dir}/onboarding_log.jsonl"
    events = []
    if os.path.exists(log_file):
        with open(log_file) as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
    return events

def compute_metrics(events, days=7):
    """Compute performance metrics from event logs."""
    cutoff = datetime.now() - timedelta(days=days)
    recent = [e for e in events if datetime.fromisoformat(e["timestamp"]) > cutoff]
    
    # Categorize events
    tasks_completed = sum(1 for e in recent if e.get("type") in ("task_completed", "handle_routine"))
    escalations = sum(1 for e in recent if e.get("type") in ("escalate", "escalation"))
    errors = sum(1 for e in recent if e.get("type") == "error")
    checkins = sum(1 for e in recent if e.get("type") == "daily_checkin")
    
    total_actions = tasks_completed + escalations
    escalation_rate = escalations / total_actions if total_actions > 0 else 0
    error_rate = errors / total_actions if total_actions > 0 else 0
    
    return {
        "period_days": days,
        "total_events": len(recent),
        "tasks_completed": tasks_completed,
        "escalations": escalations,
        "errors": errors,
        "escalation_rate": round(escalation_rate, 3),
        "error_rate": round(error_rate, 3),
        "checkins": checkins,
        "tasks_per_day": round(tasks_completed / days, 1)
    }

def check_retraining_triggers(metrics, thresholds=None):
    """Check if any retraining triggers are hit."""
    if thresholds is None:
        thresholds = {
            "escalation_rate_high": 0.20,      # >20% escalations = too uncertain
            "error_rate_high": 0.10,           # >10% errors = too unreliable
            "tasks_per_day_low": 1.0,           # <1 task/day = not enough volume
        }
    
    triggers = []
    
    if metrics["escalation_rate"] > thresholds["escalation_rate_high"]:
        triggers.append({
            "type": "escalation_rate_high",
            "message": f"Escalation rate {metrics['escalation_rate']:.1%} exceeds {thresholds['escalation_rate_high']:.1%}",
            "severity": "high",
            "action": "Review escalated cases, identify patterns, retrain with more examples"
        })
    
    if metrics["error_rate"] > thresholds["error_rate_high"]:
        triggers.append({
            "type": "error_rate_high",
            "message": f"Error rate {metrics['error_rate']:.1%} exceeds {thresholds['error_rate_high']:.1%}",
            "severity": "high",
            "action": "Audit error logs, fix data quality issues, retrain model"
        })
    
    if metrics["tasks_per_day"] < thresholds["tasks_per_day_low"] and metrics["total_events"] > 10:
        triggers.append({
            "type": "volume_low",
            "message": f"Only {metrics['tasks_per_day']:.1f} tasks/day — low adoption",
            "severity": "medium",
            "action": "Review if AI is correctly handling requests, check user satisfaction"
        })
    
    return triggers

def print_report(emp_dir, metrics, triggers, output_json=None):
    c = {
        "green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m",
        "blue": "\033[94m", "reset": "\033[0m"
    }
    
    def color(tag, text):
        return f"{c.get(tag, '')}{text}{c['reset']}"
    
    config = load_employee(emp_dir)
    
    print(f"\n{color('blue', '═'*60)}")
    print(f"  AI EMPLOYEE PERFORMANCE REPORT")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{color('blue', '═'*60)}")
    print(f"\n  Employee:  {config.get('name', 'Unknown')}")
    print(f"  Role:      {config.get('role', 'Unknown')}")
    print(f"  Company:   {config.get('company', 'Unknown')}")
    print(f"  Phase:     {config.get('current_phase', 'unknown')}")
    
    print(f"\n  ─── Metrics (last {metrics['period_days']} days) ───")
    print(f"    Tasks completed:    {metrics['tasks_completed']}")
    print(f"    Escalations:        {metrics['escalations']}")
    print(f"    Errors:             {metrics['errors']}")
    print(f"    Tasks per day:      {metrics['tasks_per_day']}")
    print(f"    Escalation rate:    {metrics['escalation_rate']:.1%} ", end="")
    if metrics["escalation_rate"] > 0.20:
        print(color("red", "⚠ HIGH"))
    elif metrics["escalation_rate"] > 0.10:
        print(color("yellow", "⚠ MEDIUM"))
    else:
        print(color("green", "✓ OK"))
    
    print(f"    Error rate:          {metrics['error_rate']:.1%} ", end="")
    if metrics["error_rate"] > 0.10:
        print(color("red", "⚠ HIGH"))
    elif metrics["error_rate"] > 0.05:
        print(color("yellow", "⚠ MEDIUM"))
    else:
        print(color("green", "✓ OK"))
    
    if triggers:
        print(f"\n  {color('red', '─'*40)}")
        print(f"  {color('red', '⚠ RETRAINING TRIGGERS DETECTED')}")
        print(f"  {color('red', '─'*40)}")
        for t in triggers:
            sev = color("red", "🔴 HIGH") if t["severity"] == "high" else color("yellow", "🟡 MED")
            print(f"\n    {sev} {t['message']}")
            print(f"    Action: {t['action']}")
    else:
        print(f"\n  {color('green', '✓ No retraining triggers — performance nominal')}")
    
    print(f"\n  Supervisor: {config.get('supervisor_name', 'Not assigned')}")
    print(f"{color('blue', '═'*60)}\n")
    
    if output_json:
        with open(output_json, "w") as f:
            json.dump({"metrics": metrics, "triggers": triggers, "config": config}, f, indent=2)
        print(f"  Report saved to: {output_json}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--employee", required=True)
    parser.add_argument("--report", action="store_true", help="Generate weekly report")
    parser.add_argument("--days", type=int, default=7, help="Report period in days")
    parser.add_argument("--output", help="Save JSON report")
    parser.add_argument("--clients-dir", default="./clients")
    args = parser.parse_args()
    
    emp_slug = args.employee.lower().replace(" ", "-")
    emp_dir = os.path.join(args.clients_dir, emp_slug)
    
    if not os.path.exists(emp_dir):
        print(f"ERROR: Employee not found: {emp_dir}")
        sys.exit(1)
    
    events = load_logs(emp_dir)
    metrics = compute_metrics(events, days=args.days)
    triggers = check_retraining_triggers(metrics)
    
    if args.report or args.output:
        print_report(emp_dir, metrics, triggers, args.output)
    else:
        # Quick status
        print(f"Employee: {emp_dir}")
        print(f"Tasks: {metrics['tasks_completed']} | Escalations: {metrics['escalations']} | Errors: {metrics['errors']}")
        print(f"Escalation rate: {metrics['escalation_rate']:.1%} | Error rate: {metrics['error_rate']:.1%}")
        if triggers:
            print(f"⚠ {len(triggers)} retraining trigger(s) detected — run with --report for details")
        else:
            print("✓ Performance nominal")

if __name__ == "__main__":
    main()
