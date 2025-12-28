#!/usr/bin/env python3
"""Timeline Logger - Directly write entries to timeline table files."""

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path


def get_timeline_path(base_dir: str, date: str = None) -> Path:
    """Get timeline file path for given date."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    return Path(base_dir) / f"timeline_{date}.md"


def get_task_file_path(base_dir: str) -> Path:
    """Get current task state file path (stored in timeline directory)."""
    return Path(base_dir) / ".current_task.json"


def ensure_timeline_exists(timeline_path: Path):
    """Create timeline file with header if it doesn't exist."""
    timeline_path.parent.mkdir(parents=True, exist_ok=True)
    if not timeline_path.exists():
        header = "| 开始时间 | 结束时间 | ⏱ 耗时 | 📝 事项内容 | 🏷️ 标签/备注 |\n"
        header += "| :--- | :--- | :--- | :--- | :--- |\n"
        timeline_path.write_text(header, encoding="utf-8")


def add_timeline_entry(
    base_dir: str,
    start_time: str,
    end_time: str,
    duration_str: str,
    content: str,
    tag: str,
    date: str = None,
):
    """Add an entry to the timeline table."""
    timeline_path = get_timeline_path(base_dir, date)
    ensure_timeline_exists(timeline_path)
    
    entry = f"| {start_time} | {end_time} | {duration_str} | {content} | {tag} |\n"
    
    with open(timeline_path, "a", encoding="utf-8") as f:
        f.write(entry)
    
    return {"status": "success", "path": str(timeline_path)}


def start_task(base_dir: str, task_name: str, time: str = None, date: str = None):
    """Start a new task and record start time."""
    task_file = get_task_file_path(base_dir)
    
    if time is None:
        time = datetime.now().strftime("%H:%M")
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Ensure directory exists
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    # Check if there's an ongoing task
    current_task = {}
    if task_file.exists():
        try:
            current_task = json.loads(task_file.read_text())
        except json.JSONDecodeError:
            current_task = {}
    
    if current_task.get("name"):
        print(f"⚠️ 有未完成的任务: {current_task['name']} (开始于 {current_task['start_time']})")
        print("请先完成或暂停当前任务")
        return {"status": "has_ongoing_task", "task": current_task}
    
    # Save new task
    new_task = {
        "name": task_name,
        "start_time": time,
        "start_datetime": datetime.now().isoformat(),
        "date": date,
    }
    task_file.write_text(json.dumps(new_task, ensure_ascii=False, indent=2))
    
    print(f"💪 加油！已记录开始时间 {time}")
    return {"status": "started", "task": new_task}


def finish_task(base_dir: str, status: str = "done", time: str = None, notes: str = None):
    """Finish current task and add to timeline."""
    task_file = get_task_file_path(base_dir)
    
    if time is None:
        time = datetime.now().strftime("%H:%M")
    
    if not task_file.exists():
        print("⚠️ 没有进行中的任务")
        return {"status": "no_task"}
    
    try:
        current_task = json.loads(task_file.read_text())
    except json.JSONDecodeError:
        print("⚠️ 任务文件格式错误")
        return {"status": "error"}
    
    if not current_task.get("name"):
        print("⚠️ 没有进行中的任务")
        return {"status": "no_task"}
    
    # Calculate duration
    start_time = current_task["start_time"]
    start_h, start_m = map(int, start_time.split(":"))
    end_h, end_m = map(int, time.split(":"))
    
    total_start_mins = start_h * 60 + start_m
    total_end_mins = end_h * 60 + end_m
    duration_mins = total_end_mins - total_start_mins
    
    if duration_mins < 0:
        duration_mins += 24 * 60  # Handle overnight
    
    hours = duration_mins // 60
    mins = duration_mins % 60
    duration_str = f"{hours}h{mins}m" if hours > 0 else f"{mins}m"
    
    # Build timeline entry
    task_date = current_task.get("date", datetime.now().strftime("%Y-%m-%d"))
    status_text = "完成" if status == "done" else "暂停"
    content = f"{status_text} {current_task['name']}"
    tag = "完成" if status == "done" else "暂停"
    if notes:
        tag = f"{tag} ({notes})"
    
    # Add to timeline
    add_timeline_entry(
        base_dir,
        start_time,
        time,
        duration_str,
        content,
        tag,
        task_date,
    )
    
    # Clear current task
    task_file.write_text("{}")
    
    emoji = "✅" if status == "done" else "⏸️"
    print(f"{emoji} 辛苦了！{start_time}-{time} ({duration_str})")
    
    # Add encouragement based on duration
    if duration_mins >= 240:
        print("🎉 工作超过4小时了，好好休息一下！")
    elif duration_mins >= 120:
        print("👍 干得漂亮！记得适当休息")
    
    return {
        "status": "finished",
        "task": current_task["name"],
        "start_time": start_time,
        "end_time": time,
        "duration": duration_str,
        "duration_mins": duration_mins,
    }


def get_current_task(base_dir: str):
    """Get current ongoing task."""
    task_file = get_task_file_path(base_dir)
    
    if not task_file.exists():
        return None
    
    try:
        task = json.loads(task_file.read_text())
        return task if task.get("name") else None
    except json.JSONDecodeError:
        return None


def log_sleep(base_dir: str, start_time: str, end_time: str, notes: str = None, date: str = None):
    """Log sleep record to timeline."""
    # Parse times
    start_h, start_m = map(int, start_time.replace("点", ":").replace("：", ":").split(":"))
    end_h, end_m = map(int, end_time.replace("点", ":").replace("：", ":").split(":"))
    
    # Normalize times
    start_time_str = f"{start_h:02d}:{start_m:02d}"
    end_time_str = f"{end_h:02d}:{end_m:02d}"
    
    # Calculate duration
    total_start_mins = start_h * 60 + start_m
    total_end_mins = end_h * 60 + end_m
    duration_mins = total_end_mins - total_start_mins
    
    if duration_mins < 0:
        duration_mins += 24 * 60
    
    hours = duration_mins // 60
    mins = duration_mins % 60
    duration_str = f"{hours}h{mins}m" if mins > 0 else f"{hours}h"
    
    # Build tag
    tag = "睡眠"
    if duration_mins < 360:  # Less than 6 hours
        tag = "睡眠 (⚠️ 睡眠不足)"
    elif duration_mins < 420:  # Less than 7 hours
        tag = "睡眠 (睡眠时间偏少)"
    if notes:
        tag = f"{tag}; {notes}"
    
    # Add to timeline
    add_timeline_entry(base_dir, start_time_str, end_time_str, duration_str, "睡眠", tag, date)
    
    print(f"😴 已记录睡眠: {duration_str}")
    if duration_mins < 360:
        print("💤 睡眠不太足哦，注意休息！")
    
    return {"duration_mins": duration_mins, "duration_str": duration_str}


def parse_timeline_entries(timeline_path: Path) -> list:
    """Parse timeline file and return entries."""
    if not timeline_path.exists():
        return []
    
    entries = []
    with open(timeline_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines[2:]:  # Skip header
        line = line.strip()
        if not line or not line.startswith("|"):
            continue
        
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 5:
            start_time, end_time, duration, content, tag = parts[:5]
            
            # Parse duration
            duration_mins = 0
            if duration:
                h_match = re.search(r"(\d+)h", duration)
                m_match = re.search(r"(\d+)m", duration)
                if h_match:
                    duration_mins += int(h_match.group(1)) * 60
                if m_match:
                    duration_mins += int(m_match.group(1))
            
            entries.append({
                "start_time": start_time,
                "end_time": end_time,
                "duration_str": duration,
                "duration_mins": duration_mins,
                "content": content,
                "tag": tag,
            })
    
    return entries


def format_duration(mins: int) -> str:
    """Format duration in minutes to human readable string."""
    if mins == 0:
        return "0m"
    hours = mins // 60
    minutes = mins % 60
    if hours > 0 and minutes > 0:
        return f"{hours}h{minutes}m"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{minutes}m"


def get_today_summary(base_dir: str) -> str:
    """Get a brief summary of today's activities."""
    date = datetime.now().strftime("%Y-%m-%d")
    timeline_path = get_timeline_path(base_dir, date)
    entries = parse_timeline_entries(timeline_path)
    
    if not entries:
        return "今天还没有记录"
    
    # Calculate work time (exclude sleep)
    work_mins = sum(e["duration_mins"] for e in entries if "睡眠" not in e["tag"])
    sleep_mins = sum(e["duration_mins"] for e in entries if "睡眠" in e["tag"])
    
    summary = f"今日共 {len(entries)} 条记录"
    if work_mins > 0:
        summary += f"，工作 {format_duration(work_mins)}"
    if sleep_mins > 0:
        summary += f"，睡眠 {format_duration(sleep_mins)}"
    
    # List work entries
    work_entries = [e for e in entries if "睡眠" not in e["tag"]]
    if work_entries:
        summary += "\n主要活动:\n"
        for e in work_entries[:5]:
            summary += f"- {e['content']} ({e['duration_str']})\n"
    
    return summary


def get_weekly_summary(base_dir: str, end_date: str = None) -> str:
    """Get weekly summary."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    end = datetime.strptime(end_date, "%Y-%m-%d")
    start = end - timedelta(days=6)
    
    daily_stats = {}
    total_work_mins = 0
    total_entries = 0
    
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        timeline_path = get_timeline_path(base_dir, date_str)
        entries = parse_timeline_entries(timeline_path)
        
        work_mins = sum(e["duration_mins"] for e in entries if "睡眠" not in e["tag"])
        daily_stats[date_str] = {
            "work_mins": work_mins,
            "entries": len(entries),
        }
        total_work_mins += work_mins
        total_entries += len(entries)
        current += timedelta(days=1)
    
    summary = f"# 周报 {start.strftime('%Y-%m-%d')} ~ {end_date}\n\n"
    summary += f"**总工作时长**: {format_duration(total_work_mins)}\n"
    summary += f"**总记录数**: {total_entries}\n\n"
    summary += "| 日期 | 工作时长 | 记录数 |\n"
    summary += "|------|----------|--------|\n"
    
    for date_str in sorted(daily_stats.keys()):
        stats = daily_stats[date_str]
        summary += f"| {date_str} | {format_duration(stats['work_mins'])} | {stats['entries']} |\n"
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="Timeline Logger")
    parser.add_argument("--base-dir", default="./timeline", help="Base directory for timeline files")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Start task
    start_parser = subparsers.add_parser("start", help="Start a task")
    start_parser.add_argument("task", help="Task name")
    start_parser.add_argument("--time", help="Start time (HH:MM)")
    start_parser.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Finish task
    finish_parser = subparsers.add_parser("finish", help="Finish current task")
    finish_parser.add_argument("--status", choices=["done", "pause"], default="done")
    finish_parser.add_argument("--time", help="End time (HH:MM)")
    finish_parser.add_argument("--notes", help="Notes")
    
    # Current task
    subparsers.add_parser("current", help="Show current task")
    
    # Sleep
    sleep_parser = subparsers.add_parser("sleep", help="Log sleep")
    sleep_parser.add_argument("start", help="Sleep start time")
    sleep_parser.add_argument("end", help="Sleep end time")
    sleep_parser.add_argument("--notes", help="Notes")
    sleep_parser.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Today summary
    subparsers.add_parser("today", help="Show today's summary")
    
    # Weekly summary
    weekly_parser = subparsers.add_parser("weekly", help="Show weekly summary")
    weekly_parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    if args.command == "start":
        start_task(args.base_dir, args.task, args.time, getattr(args, 'date', None))
    elif args.command == "finish":
        finish_task(args.base_dir, args.status, args.time, args.notes)
    elif args.command == "current":
        task = get_current_task(args.base_dir)
        if task:
            print(f"📍 当前任务: {task['name']} (开始于 {task['start_time']})")
        else:
            print("没有进行中的任务")
    elif args.command == "sleep":
        log_sleep(args.base_dir, args.start, args.end, args.notes, getattr(args, 'date', None))
    elif args.command == "today":
        print(get_today_summary(args.base_dir))
    elif args.command == "weekly":
        print(get_weekly_summary(args.base_dir, getattr(args, 'end_date', None)))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
