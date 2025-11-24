import json
import csv
import os
import datetime
import sys
import urllib.request
import urllib.error

# 設定ファイルのパス
CONFIG_FILE = 'config.json'
DATA_FILE = 'monitoring_data.csv'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} が見つかりません。")
        print("以下の形式で config.json を作成し、BufferのAccess Tokenを設定してください。")
        print('{\n  "access_token": "YOUR_ACCESS_TOKEN_HERE"\n}')
        return None
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def get_buffer_data(access_token):
    # プロファイル情報の取得（フォロワー数など）
    url = "https://api.bufferapp.com/1/profiles.json?access_token=" + access_token
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        print(f"API Error: {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_sent_updates(access_token, profile_id):
    # 過去の投稿データの取得（エンゲージメント集計用）
    # 直近100件を取得
    url = f"https://api.bufferapp.com/1/profiles/{profile_id}/updates/sent.json?access_token={access_token}&count=100"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('updates', [])
    except Exception as e:
        print(f"Warning: Could not fetch updates for profile {profile_id}: {e}")
        return []

def update_csv(metrics):
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    # 既存のデータを読み込む
    rows = []
    header = []
    file_exists = os.path.exists(DATA_FILE)
    
    if file_exists:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                rows = list(reader)
    
    if not header:
        header = ['Date', 'Followers', 'Followers_Change', 'Likes', 'Reposts', 'Replies', 'Profile_Clicks', 'Note_PV']

    # 今日のデータが既にあるか確認
    today_row_index = -1
    for i, row in enumerate(rows):
        if row[0] == today:
            today_row_index = i
            break
    
    # 前日のフォロワー数を取得（増減計算用）
    prev_followers = 0
    if today_row_index != -1 and today_row_index > 0:
        prev_followers = int(rows[today_row_index - 1][1])
    elif today_row_index == -1 and len(rows) > 0:
        prev_followers = int(rows[-1][1])
        
    followers_change = metrics['followers'] - prev_followers
    
    # 新しい行データ
    new_row = [
        today,
        str(metrics['followers']),
        str(followers_change),
        str(metrics['likes']),
        str(metrics['reposts']),
        str(metrics['replies']),
        str(metrics['clicks']),
        '0' # Note PVはBufferからは取れないので0（手動入力用）
    ]
    
    if today_row_index != -1:
        # 更新（Note PVは既存の値を維持するように配慮）
        current_pv = rows[today_row_index][7]
        new_row[7] = current_pv
        rows[today_row_index] = new_row
        print(f"Updated data for {today}")
    else:
        # 追加
        rows.append(new_row)
        print(f"Added data for {today}")
    
    # 書き込み
    with open(DATA_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def main():
    print("Fetching data from Buffer API...")
    config = load_config()
    if not config:
        return

    profiles = get_buffer_data(config['access_token'])
    if not profiles:
        print("Failed to fetch profile data.")
        return

    total_metrics = {
        'followers': 0,
        'likes': 0,
        'reposts': 0,
        'replies': 0,
        'clicks': 0
    }

    # 今日（深夜0時以降）の投稿のエンゲージメントを集計するのは難しいので、
    # ここでは「全プロファイルの現在のフォロワー数」と
    # 「過去24時間に投稿された記事のエンゲージメント」を集計するロジックにするか、
    # あるいはシンプルに「全期間の累計」から「前回の累計」を引く...のはDBがないと無理。
    # なので、今回は「フォロワー数」を正確に取得し、
    # エンゲージメントは「直近の投稿（今日の日付のもの）」の合計を集計する。
    
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    
    print(f"Found {len(profiles)} profiles.")
    
    for profile in profiles:
        # フォロワー数
        followers = profile.get('statistics', {}).get('followers', 0)
        total_metrics['followers'] += followers
        
        # 投稿データの取得と集計
        updates = get_sent_updates(config['access_token'], profile['id'])
        
        for update in updates:
            # 投稿日時 (Unix timestamp)
            sent_at = update.get('sent_at')
            if sent_at:
                sent_date = datetime.datetime.fromtimestamp(sent_at).strftime('%Y-%m-%d')
                
                # 今日の投稿のみを集計対象にする
                if sent_date == today_str:
                    stats = update.get('statistics', {})
                    total_metrics['likes'] += stats.get('favorites', 0) + stats.get('likes', 0)
                    total_metrics['reposts'] += stats.get('retweets', 0) + stats.get('reposts', 0) # Twitter uses retweets
                    total_metrics['replies'] += stats.get('replies', 0)
                    total_metrics['clicks'] += stats.get('clicks', 0)

    print("\n--- Summary for Today ---")
    print(f"Total Followers: {total_metrics['followers']}")
    print(f"Today's Likes: {total_metrics['likes']}")
    print(f"Today's Reposts: {total_metrics['reposts']}")
    print(f"Today's Replies: {total_metrics['replies']}")
    print(f"Today's Clicks: {total_metrics['clicks']}")
    print("-------------------------")
    
    update_csv(total_metrics)
    print("\nDone! monitoring_data.csv has been updated.")
    print("Note: 'Note PV' cannot be fetched from Buffer API and remains 0 (or unchanged).")

if __name__ == "__main__":
    main()
