"""
Buffer用CSV形式修正スクリプト
リライト版CSVファイルに適切な改行を挿入してBuffer互換形式にする
"""

import csv
from pathlib import Path


def add_line_breaks(text):
    """テキストに適切な改行を追加 - シンプルバージョン"""
    # 既に改行が多い場合はそのまま返す
    if text.count('\n') > 3:
        return text
    
    # 文を分割
    text = text.replace('。', '。\n')
    text = text.replace('？', '？\n')
    text = text.replace('！', '！\n')
    
    # 過剰な改行を整理
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    
    return text.strip()

def process_csv_file(input_path):
    """CSVファイルを処理"""
    output_path = input_path
    rows = []
    
    # CSVを読み込み
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Textフィールドに改行を追加
            if 'Text' in row:
                row['Text'] = add_line_breaks(row['Text'])
            rows.append(row)
    
    # 処理済みCSVを書き込み
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    
    print(f"✓ {input_path.name}")

def main():
    base_dir = Path(r"c:\Repos\note-articles\tools\outputs\buffer_split")
    
    # 処理対象ファイルのリスト
    files_to_process = [
        # Week1
        "Week1_Day3_rewritten.csv",
        "Week1_Day4_rewritten.csv",
        "Week1_Day5_rewritten.csv",
        "Week1_Day6_rewritten.csv",
        "Week1_Day7_rewritten.csv",
        # Week2
        "Week2_Day8_rewritten.csv",
        "Week2_Day9_rewritten.csv",
        "Week2_Day10_rewritten.csv",
        "Week2_Day11_rewritten.csv",
        "Week2_Day12_rewritten.csv",
        "Week2_Day13_rewritten.csv",
        "Week2_Day14_rewritten.csv",
        # Week3
        "Week3_Day15_rewritten.csv",
        "Week3_Day16_rewritten.csv",
        "Week3_Day17_rewritten.csv",
        "Week3_Day18_rewritten.csv",
        "Week3_Day19_rewritten.csv",
        "Week3_Day20_rewritten.csv",
        "Week3_Day21_rewritten.csv",
    ]
    
    print("CSV形式修正開始...")
    for filename in files_to_process:
        file_path = base_dir / filename
        if file_path.exists():
            process_csv_file(file_path)
        else:
            print(f"✗ {filename} が見つかりません")
    
    print(f"\n完了！{len(files_to_process)}ファイルを処理しました")

if __name__ == "__main__":
    main()
