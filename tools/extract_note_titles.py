import os

INPUT_FILE = r'c:\Repos\note-articles\tools\manual_refine_weeks_7_8_enriched.py'

def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    titles = set()
    for i, line in enumerate(lines):
        if "具体的な方法はNoteで公開中" in line:
            # Look backwards for the title
            for j in range(i-1, max(-1, i-10), -1):
                prev_line = lines[j].strip()
                if prev_line.startswith("「") and prev_line.endswith("」"):
                    titles.add(prev_line)
                    break
                if prev_line == '"""' or prev_line == "'''":
                    continue
                if not prev_line:
                    continue

    print("Found Note Articles referenced in Weeks 7-8:")
    for t in sorted(titles):
        print(f"- {t}")

if __name__ == "__main__":
    main()
