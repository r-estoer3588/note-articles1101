import csv
import re
import sys
import os
from datetime import datetime, timedelta

# Week別のタイムテーブル（曜日ごとの投稿時刻）
WEEKLY_SCHEDULE = {
    "Monday": ["07:03", "08:12", "10:05", "12:11", "15:08", "17:45", "20:02", "21:15", "22:05", "23:11"],
    "Tuesday": ["07:06", "08:09", "10:15", "12:04", "15:12", "17:52", "20:08", "21:21", "22:11", "23:05"],
    "Wednesday": ["07:02", "08:15", "10:08", "12:15", "15:05", "17:55", "20:04", "21:12", "22:08", "23:15"],
    "Thursday": ["07:04", "08:11", "12:08", "15:09", "17:48", "20:06", "21:18", "22:15", "23:08"],  # 9投稿
    "Friday": ["07:01", "08:08", "10:04", "12:12", "15:15", "18:05", "20:01", "21:05", "22:20", "23:25"],
    "Saturday": ["08:38", "10:13", "12:07", "14:18", "16:23", "19:12", "20:29", "21:37", "22:48", "23:33"],
    "Sunday": ["08:43", "10:17", "12:13", "15:07", "18:18", "20:14", "21:04", "22:07", "23:13"],  # 9投稿
}

# 曜日のインデックス（月曜=0）
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def parse_post_content(raw_text):
    """投稿本文を抽出"""
    body_match = re.search(r'【本文】\n(.*)', raw_text, re.DOTALL)
    if body_match:
        content = body_match.group(1).strip()
    else:
        content = raw_text.strip()
    
    content = content.replace('（改行）', '\n')
    return content


def get_scheduled_time(post_date, post_index_in_day):
    """指定日の曜日と1日内の投稿順序から時刻を取得"""
    weekday = post_date.weekday()  # 0=Monday
    weekday_name = WEEKDAY_NAMES[weekday]
    
    time_slots = WEEKLY_SCHEDULE[weekday_name]
    
    # その日の投稿数を超えた場合は最後の時刻を使用
    if post_index_in_day >= len(time_slots):
        return time_slots[-1]
    
    return time_slots[post_index_in_day]


def export_week_to_buffer(data_file, start_date_str, week_label, day_offset=0):
    """指定されたWeekのデータをBuffer用CSVにエクスポート
    
    Args:
        data_file: データファイル名
        start_date_str: カレンダー上の開始日
        week_label: Week1-6 / Week7-8 などのラベル
        day_offset: Day番号のオフセット（Week7-8なら42）
    """
    # データファイルをインポート
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    module_name = os.path.splitext(os.path.basename(data_file))[0]
    module = __import__(module_name)
    updates = module.updates
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    output_file = os.path.join("outputs", f"{week_label}_buffer_import.csv")
    
    os.makedirs("outputs", exist_ok=True)
    
    rows = []
    
    # ソートされたキー
    sorted_keys = sorted(
        updates.keys(),
        key=lambda x: (int(x.split('_')[0][3:]), x.split('_')[1])
    )
    
    # 日ごとの投稿をカウント
    day_post_counts = {}
    
    for key in sorted_keys:
        day_str, _ = key.split('_')
        day_num = int(day_str[3:])
        
        # 日付を計算（開始日からの相対）
        offset = (day_num - day_offset - 1) if day_offset == 0 else (day_num - day_offset - 1)
        post_date = start_date + timedelta(days=offset)
        
        # その日の投稿インデックスを取得
        date_key = post_date.strftime("%Y-%m-%d")
        if date_key not in day_post_counts:
            day_post_counts[date_key] = 0
        
        post_index = day_post_counts[date_key]
        day_post_counts[date_key] += 1
        
        # スケジュールから時刻を取得
        time_str = get_scheduled_time(post_date, post_index)
        
        # 本文を抽出
        raw_content = updates[key]
        post_text = parse_post_content(raw_content)
        
        # Buffer用の日時フォーマット (YYYY-MM-DD HH:MM)
        datetime_str = f"{post_date.strftime('%Y-%m-%d')} {time_str}"
        
        # タグ（Week番号をタグとして使用）
        tags = week_label
        
        rows.append({
            "Text": post_text,
            "Image URL": "",  # 空欄（後で手動追加想定）
            "Tags": tags,
            "Posting Time": datetime_str
        })
    
    # CSV出力（UTF-8 BOM）
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Text", "Image URL", "Tags", "Posting Time"],
            quoting=csv.QUOTE_ALL  # 全フィールドをダブルクォートで囲む
        )
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ {week_label}: {len(rows)}投稿を {output_file} に出力")
    return len(rows)


if __name__ == "__main__":
    # Week別のエクスポート設定（Day 1-60完全版）
    exports = [
        {
            "data_file": "manual_refine_week1_4.py",
            "start_date": "2025-11-23",
            "week_label": "Week1-4_Day1-28",
            "day_offset": 0  # Day 1から開始
        },
        {
            "data_file": "manual_refine_week5.py",
            "start_date": "2025-12-21",  # Week 5は Week 4の28日後
            "week_label": "Week5_Day29-35",
            "day_offset": 28  # Day 29から開始
        },
        {
            "data_file": "manual_refine_week6.py",
            "start_date": "2025-12-28",  # Week 6は Week 5の7日後
            "week_label": "Week6_Day36-42",
            "day_offset": 35  # Day 36から開始
        },
        {
            "data_file": "manual_refine_weeks_7_8_enriched.py",
            "start_date": "2026-01-04",  # Week 7は Week 6の7日後
            "week_label": "Week7-8_Day43-60",
            "day_offset": 42  # Day 43から開始
        }
    ]
    
    total_posts = 0
    
    for config in exports:
        count = export_week_to_buffer(
            config["data_file"],
            config["start_date"],
            config["week_label"],
            config.get("day_offset", 0)
        )
        total_posts += count
    
    print(f"\n🎉 合計 {total_posts} 投稿をBuffer用CSVに出力しました")
    print("📅 データ範囲: Day 1-60 (60日間・完全版)")
    print("📌 BufferのCSVインポート機能で各ファイルを取り込んでください")

