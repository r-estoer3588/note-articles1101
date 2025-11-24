import os
import glob
import pandas as pd

# Define paths
input_dir = r"c:\Repos\note-articles\tools\outputs\buffer_split"
output_file = os.path.join(input_dir, "All_Weeks_Buffer_Import.csv")

# Pattern to match rewritten CSVs
# Note: Week1_Day1.csv is not "rewritten" but should be included if not already posted.
# User said "Week1_Day1 is already posted" (actually "Week1_Day1は既にリライト済みのため対象外" in handover, but user said "day1だけ投稿済" in chat).
# So we should exclude Week1_Day1.
# We will look for Week*_Day*_rewritten.csv

files = glob.glob(os.path.join(input_dir, "*_rewritten.csv"))


# Sort files to ensure correct order (Week1_Day2, Week1_Day3... Week2_Day8...)
# We need a custom sort key because standard string sort might do Week1, Week10...
def sort_key(filepath):
    filename = os.path.basename(filepath)
    # Extract Day number
    try:
        day_part = filename.split("_")[1]  # Day2
        day_num = int(day_part.replace("Day", ""))
        return day_num
    except:
        return 999


files.sort(key=sort_key)

print(f"Found {len(files)} files to merge.")

# Merge
dfs = []
for f in files:
    try:
        df = pd.read_csv(f)
        dfs.append(df)
    except Exception as e:
        print(f"Error reading {f}: {e}")

if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)
    # Rename columns to match Buffer native import format (lowercase snake_case)
    merged_df.columns = ["text", "image_url", "tags", "posting_time"]
    # Save
    merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Successfully merged {len(dfs)} files into {output_file}")
    print(f"Total posts: {len(merged_df)}")
else:
    print("No files found to merge.")
