import csv
from pathlib import Path
from datetime import datetime


def split_buffer_csv(input_file, posts_per_file=10, start_day=1):
    """Buffer CSVを指定された投稿数ごとに分割
    
    Args:
        input_file: 入力CSVファイル
        posts_per_file: ファイルあたりの投稿数
        start_day: 開始Day番号（Week1-4なら1、Week5なら29など）
    """
    input_path = Path(input_file)
    output_dir = input_path.parent / "buffer_split"
    output_dir.mkdir(exist_ok=True)
    
    # CSVを読み込み
    with open(input_path, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # 開始日を取得（最初の投稿の日付）
    if not rows:
        return 0
    
    # "2025-11-23 08:43" -> "2025-11-23"
    first_date_str = rows[0]["Posting Time"].split()[0]
    start_date = datetime.strptime(first_date_str, "%Y-%m-%d")
    
    # 分割して出力
    total_files = 0
    
    for i in range(0, len(rows), posts_per_file):
        chunk = rows[i:i + posts_per_file]
        
        # チャンクの最初の投稿の日付からDay番号を計算
        chunk_date_str = chunk[0]["Posting Time"].split()[0]
        chunk_date = datetime.strptime(chunk_date_str, "%Y-%m-%d")
        days_elapsed = (chunk_date - start_date).days
        current_day = start_day + days_elapsed
        
        # Week番号を計算（7日ごと）
        week_num = ((current_day - 1) // 7) + 1
        
        output_file = output_dir / f"Week{week_num}_Day{current_day}.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Text", "Image URL", "Tags", "Posting Time"],
                quoting=csv.QUOTE_ALL
            )
            writer.writeheader()
            writer.writerows(chunk)
        
        total_files += 1
        print(f"[OK] {output_file.name}: {len(chunk)}投稿")
        i += posts_per_file
    
    return total_files


if __name__ == "__main__":
    outputs_dir = Path(__file__).parent / "outputs"
    
    # Week別のファイルと開始Day番号のマッピング
    buffer_configs = [
        ("Week1-4_Day1-28_buffer_import.csv", 1),
        ("Week5_Day29-35_buffer_import.csv", 29),
        ("Week6_Day36-42_buffer_import.csv", 36),
        ("Week7-8_Day43-60_buffer_import.csv", 43),
    ]
    
    total_parts = 0
    for filename, start_day in buffer_configs:
        buffer_file = outputs_dir / filename
        if buffer_file.exists():
            print(f"\n[*] {filename} を分割中... (Day {start_day}~)")
            parts = split_buffer_csv(
                buffer_file,
                posts_per_file=10,
                start_day=start_day
            )
            total_parts += parts
    
    print(f"\n[OK] 合計 {total_parts} ファイルに分割完了")
    print(f"[-->] 出力先: {outputs_dir / 'buffer_split'}")
