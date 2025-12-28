import os
from datetime import date

def init_daily_files():
    today = date.today().strftime("%Y-%m-%d")
    
    # Define paths based on script location (root/scripts/daily_init.py)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    timeline_dir = os.path.join(root_dir, "timeline")
    plan_dir = os.path.join(root_dir, "plan")
    
    # Ensure directories exist
    os.makedirs(timeline_dir, exist_ok=True)
    os.makedirs(plan_dir, exist_ok=True)
    
    # File paths
    timeline_file = os.path.join(timeline_dir, f"timeline_{today}.md")
    plan_file = os.path.join(plan_dir, f"plan_{today}.md")
    
    # Create timeline file if not exists
    if not os.path.exists(timeline_file):
        with open(timeline_file, "w") as f:
            f.write(f"# Timeline for {today}\n\n")
        print(f"Created: {timeline_file}")
    else:
        print(f"Exists: {timeline_file}")

    # Create plan file if not exists
    if not os.path.exists(plan_file):
        with open(plan_file, "w") as f:
            f.write(f"# Plan for {today}\n\n")
        print(f"Created: {plan_file}")
    else:
        print(f"Exists: {plan_file}")

if __name__ == "__main__":
    init_daily_files()
