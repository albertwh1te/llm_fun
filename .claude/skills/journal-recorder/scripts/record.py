#!/usr/bin/env python3
"""记录想法和观点到journal日志文件"""

import argparse
import os
from datetime import datetime
from pathlib import Path


def get_journal_file(journal_dir: Path, date: datetime) -> Path:
    """获取当天的journal文件路径"""
    filename = f"journal_{date.strftime('%Y-%m-%d')}.md"
    return journal_dir / filename


def add_record(journal_dir: Path, content: str, record_type: str = "THOUGHT"):
    """添加记录到journal文件
    
    Args:
        journal_dir: journal目录路径
        content: 记录内容
        record_type: 记录类型 (THOUGHT, FEELING, IDEA, LEARNING, NOTE)
    """
    now = datetime.now()
    journal_file = get_journal_file(journal_dir, now)
    
    # 确保目录存在
    journal_dir.mkdir(parents=True, exist_ok=True)
    
    # 格式化时间
    time_str = now.strftime("%Y-%m-%d %H:%M")
    
    # 构建记录条目
    entry = f"{time_str} {content}\n{record_type}\n\n"
    
    # 如果文件不存在，创建并添加标题
    if not journal_file.exists():
        header = f"# Journal - {now.strftime('%Y-%m-%d')}\n\n"
        with open(journal_file, 'w', encoding='utf-8') as f:
            f.write(header)
    
    # 追加记录
    with open(journal_file, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    return journal_file


def main():
    parser = argparse.ArgumentParser(description='记录想法和观点到journal')
    parser.add_argument('--journal-dir', type=str, required=True,
                        help='journal目录路径')
    parser.add_argument('content', type=str, help='记录内容')
    parser.add_argument('--type', type=str, default='THOUGHT',
                        choices=['THOUGHT', 'FEELING', 'IDEA', 'LEARNING', 'NOTE'],
                        help='记录类型')
    
    args = parser.parse_args()
    
    journal_dir = Path(args.journal_dir)
    journal_file = add_record(journal_dir, args.content, args.type)
    
    print(f"✅ 已记录到 {journal_file}")


if __name__ == '__main__':
    main()
