import csv
from pathlib import Path


def split_buffer_csv(input_file, posts_per_file=10):
    """Buffer CSVを指定された投稿数ごとに分割"""
    input_path = Path(input_file)
    output_dir = input_path.parent / "buffer_split"
    output_dir.mkdir(exist_ok=True)
    
    # 元のファイル名から週情報を取得
    week_label = input_path.stem.replace("_buffer_import", "")
    
    # CSVを読み込み
    with open(input_path, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # 分割して出力
    total_files = 0
    for i in range(0, len(rows), posts_per_file):
        chunk = rows[i:i + posts_per_file]
        file_num = (i // posts_per_file) + 1
        output_file = output_dir / f"{week_label}_part{file_num:03d}.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Text", "Image URL", "Tags", "Posting Time"],
                quoting=csv.QUOTE_ALL
            )
            writer.writeheader()
            writer.writerows(chunk)
        
        total_files += 1
        print(f"✅ {output_file.name}: {len(chunk)}投稿")
    
    return total_files


if __name__ == "__main__":
    outputs_dir = Path(__file__).parent / "outputs"
    buffer_files = list(outputs_dir.glob("*_buffer_import.csv"))
    
    total_parts = 0
    for buffer_file in sorted(buffer_files):
        print(f"\n📂 {buffer_file.name} を分割中...")
        parts = split_buffer_csv(buffer_file, posts_per_file=10)
        total_parts += parts
    
    print(f"\n🎉 合計 {total_parts} ファイルに分割完了")
    print(f"📁 出力先: {outputs_dir / 'buffer_split'}")
