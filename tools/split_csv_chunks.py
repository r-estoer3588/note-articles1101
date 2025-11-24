import os
import pandas as pd
import math

# Define paths
input_file = (
    r"c:\Repos\note-articles\tools\outputs\buffer_split\All_Weeks_Buffer_Import.csv"
)
output_dir = r"c:\Repos\note-articles\tools\outputs\buffer_split"

# Read the merged CSV
try:
    df = pd.read_csv(input_file)
    total_posts = len(df)
    print(f"Total posts: {total_posts}")

    # Split into chunks of 100
    chunk_size = 100
    num_chunks = math.ceil(total_posts / chunk_size)

    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size
        chunk_df = df[start_idx:end_idx]

        output_filename = f"Buffer_Import_Part{i+1}.csv"
        output_path = os.path.join(output_dir, output_filename)

        chunk_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Created {output_filename} with {len(chunk_df)} posts.")

except Exception as e:
    print(f"Error: {e}")
