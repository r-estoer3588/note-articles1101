import pandas as pd
import json
import os
from datetime import datetime
import argparse
import requests

# Configuration
SCHEDULE_FILE = (
    r"c:\Repos\note-articles\research_ideas\relationship"
    r"\600_posts_schedule.csv"
)
STATE_FILE = r"c:\Repos\note-articles\tools\posting_state.json"
START_DATE_FILE = r"c:\Repos\note-articles\tools\start_date.json"
ENV_FILE = r"c:\Repos\note-articles\tools\.env"


def load_env():
    """Load environment variables from .env file manually"""
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def send_line_notify(message):
    """Send notification to LINE Notify"""
    token = os.environ.get("LINE_NOTIFY_TOKEN")
    if not token:
        print("LINE_NOTIFY_TOKEN not found. Skipping notification.")
        return

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        print("LINE notification sent.")
    except Exception as e:
        print(f"Failed to send LINE notification: {e}")


def send_discord_notify(message):
    """Send notification to Discord Webhook"""
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        # Silent return if not configured
        return

    data = {"content": message}
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print("Discord notification sent.")
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")


def load_schedule():
    return pd.read_csv(SCHEDULE_FILE)


def get_start_date():
    if os.path.exists(START_DATE_FILE):
        with open(START_DATE_FILE, 'r') as f:
            data = json.load(f)
            return datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    else:
        # Default to today if not set
        today = datetime.now().date()
        set_start_date(today)
        return today


def set_start_date(date_obj):
    with open(START_DATE_FILE, 'w') as f:
        json.dump({'start_date': date_obj.strftime('%Y-%m-%d')}, f)


def get_posted_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"posted_ids": []}


def save_posted_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def post_content(row):
    """
    Simulates posting to Threads.
    In a real scenario, this would call the Threads API.
    """
    content = row['Content']
    post_type = row['Type']
    time_slot = row['Time']

    print("--- POSTING TO THREADS ---")
    print(f"Time: {time_slot}")
    print(f"Type: {post_type}")
    print(f"Content:\n{content}")
    print("--------------------------")

    # Here you would add the actual API call
    # e.g., threads_api.post(content)
    
    # Send LINE notification
    notify_msg = (
        f"\n[Threads Auto Post]\n"
        f"Time: {time_slot}\n"
        f"Type: {post_type}\n"
        f"Content: {content[:50]}..."
    )
    send_line_notify(notify_msg)
    send_discord_notify(notify_msg)
    
    return True


def main():
    load_env()
    parser = argparse.ArgumentParser(
        description="Auto-poster for Relationship Threads Account"
    )
    parser.add_argument(
        '--check', action='store_true', help="Check for posts to send now"
    )
    parser.add_argument(
        '--reset-start-date', help="Reset the start date (YYYY-MM-DD)"
    )
    args = parser.parse_args()

    if args.reset_start_date:
        new_start = datetime.strptime(args.reset_start_date, '%Y-%m-%d').date()
        set_start_date(new_start)
        print(f"Start date set to {new_start}")
        return

    start_date = get_start_date()
    today = datetime.now().date()

    # Calculate current Day number (1-based)
    days_diff = (today - start_date).days
    current_day_num = days_diff + 1

    if current_day_num < 1:
        print("Campaign hasn't started yet.")
        return

    print(f"Campaign Day: {current_day_num}")

    df = load_schedule()

    # Filter for current day
    todays_posts = df[df['Day'] == current_day_num]

    if todays_posts.empty:
        print(f"No posts scheduled for today (Day {current_day_num}).")
        return

    current_time = datetime.now().time()
    state = get_posted_state()

    for index, row in todays_posts.iterrows():
        post_id = f"Day{row['Day']}_No{row['No']}"

        if post_id in state['posted_ids']:
            continue

        # Parse scheduled time
        scheduled_time_str = row['Time']
        try:
            scheduled_time = datetime.strptime(
                scheduled_time_str, '%H:%M'
            ).time()
        except ValueError:
            continue  # Skip invalid time formats

        # Check if it's time to post
        if current_time >= scheduled_time:
            success = post_content(row)
            if success:
                state['posted_ids'].append(post_id)
                save_posted_state(state)
                print(f"Successfully posted {post_id}")


if __name__ == "__main__":
    main()
