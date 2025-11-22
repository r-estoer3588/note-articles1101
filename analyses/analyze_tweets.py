import csv
import sys
import re
from collections import Counter

def analyze_tweets(file_path):
    tweets = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    favs = int(row.get('favorite_count', 0))
                    rts = int(row.get('retweet_count', 0))
                    text = row.get('text', '')
                    tweets.append({'text': text, 'score': favs + rts * 2}) # Weight RTs higher
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Sort by score descending
    tweets.sort(key=lambda x: x['score'], reverse=True)
    
    top_tweets = tweets[:50] # Analyze top 50 for patterns
    
    print(f"Total tweets: {len(tweets)}")
    print(f"Analyzing top {len(top_tweets)} tweets...")
    
    patterns = []
    starts = []
    ends = []
    
    for t in top_tweets:
        text = t['text']
        # Normalize newlines
        lines = text.split('\n')
        lines = [l.strip() for l in lines if l.strip()]
        
        if not lines:
            continue
            
        starts.append(lines[0])
        if len(lines) > 1:
            ends.append(lines[-1])
            
        # Simple structure analysis
        patterns.append(f"Lines: {len(lines)}")

    print("\n--- Top 5 Tweets ---")
    for i, t in enumerate(top_tweets[:5]):
        print(f"{i+1}. Score: {t['score']}")
        print(t['text'])
        print("-" * 20)

    print("\n--- Tweets 11-30 ---")
    for i, t in enumerate(tweets[10:30]):
        print(f"{i+11}. Score: {t['score']}")
        print(t['text'])
        print("-" * 20)

    print("\n--- Common Starts (First lines) ---")
    # Simple n-gram analysis on starts
    start_phrases = []
    for s in starts:
        # Get first 10 chars or first phrase
        match = re.match(r'^(.+?)[はがを、。]', s)
        if match:
            start_phrases.append(match.group(1))
        else:
            start_phrases.append(s[:10])
            
    print(Counter(start_phrases).most_common(10))

    print("\n--- Common Ends (Last lines) ---")
    end_phrases = []
    for e in ends:
        if len(e) > 5:
            end_phrases.append(e[-10:]) # Last 10 chars
        else:
            end_phrases.append(e)
    print(Counter(end_phrases).most_common(10))
    
    print("\n--- Structural Analysis ---")
    # Check for "Statement -> Empty Line -> Explanation" pattern
    structure_count = 0
    for t in top_tweets:
        if '\n\n' in t['text']:
            structure_count += 1
    print(f"Tweets with paragraph breaks: {structure_count}/{len(top_tweets)}")

if __name__ == "__main__":
    file_path = r"c:\Repos\note-articles\input\TwExportly_azusa_ey_tweets_2025_11_22 (1).csv"
    analyze_tweets(file_path)
