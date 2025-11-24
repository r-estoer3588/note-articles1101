import os
import csv
import json
from datetime import datetime, timedelta
import webbrowser

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "tools", "monitoring", "monitoring_data.csv")
STREAK_FILE = os.path.join(BASE_DIR, "tools", "monitoring", "streak.json")
DASHBOARD_URL = "http://localhost:8000/dashboard.html"  # Assuming local server


def load_streak():
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, "r") as f:
            return json.load(f)
    return {"current_streak": 0, "last_log_date": None, "best_streak": 0}


def save_streak(data):
    with open(STREAK_FILE, "w") as f:
        json.dump(data, f)


def update_streak(streak_data):
    today = datetime.now().strftime("%Y-%m-%d")
    last_date_str = streak_data.get("last_log_date")

    if last_date_str == today:
        print("💡 今日は既に報告済みです。記録を上書きします。")
        return streak_data["current_streak"]

    if last_date_str:
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
        yesterday = datetime.now() - timedelta(days=1)
        if last_date.date() == yesterday.date():
            streak_data["current_streak"] += 1
        else:
            print("💔 連続記録が途切れました... ストリークはリセットされます。")
            streak_data["current_streak"] = 1
    else:
        streak_data["current_streak"] = 1

    streak_data["last_log_date"] = today
    if streak_data["current_streak"] > streak_data.get("best_streak", 0):
        streak_data["best_streak"] = streak_data["current_streak"]

    save_streak(streak_data)
    return streak_data["current_streak"]


def append_to_csv(data):
    file_exists = os.path.exists(DATA_FILE)
    headers = [
        "Date",
        "Followers",
        "Followers_Change",
        "Likes",
        "Reposts",
        "Replies",
        "Profile_Clicks",
        "Note_PV",
    ]

    # Check if we need to update an existing row for today
    rows = []
    if file_exists:
        with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    today = datetime.now().strftime("%Y-%m-%d")
    updated = False

    # Calculate change from yesterday
    followers_change = 0
    if rows:
        last_row = rows[-1]
        if last_row["Date"] != today:
            try:
                last_followers = int(last_row["Followers"])
                followers_change = int(data["Followers"]) - last_followers
            except:
                pass

    new_row = {
        "Date": today,
        "Followers": data["Followers"],
        "Followers_Change": followers_change,
        "Likes": data["Likes"],
        "Reposts": data["Reposts"],
        "Replies": data["Replies"],
        "Profile_Clicks": data["Profile_Clicks"],
        "Note_PV": data["Note_PV"],
    }

    # Update or Append
    final_rows = []
    for row in rows:
        if row["Date"] == today:
            final_rows.append(new_row)
            updated = True
        else:
            final_rows.append(row)

    if not updated:
        final_rows.append(new_row)

    with open(DATA_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(final_rows)


def main():
    print("\n" + "=" * 50)
    print(" 🔥 DAILY REPORT: Threads Growth Campaign 🔥")
    print("=" * 50 + "\n")

    streak_data = load_streak()
    current_streak = streak_data["current_streak"]
    print(f"現在のストリーク: {current_streak}日 🔥")
    if streak_data.get("best_streak"):
        print(f"最高記録: {streak_data['best_streak']}日 🏆")
    print("-" * 30)

    # Ask for date (default to today)
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"\n日付を選択してください (デフォルト: {today_str})")
    date_input = input("入力形式 YYYY-MM-DD (Enterで今日): ").strip()

    if not date_input:
        target_date = today_str
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            target_date = date_input
        except ValueError:
            print("❌ 日付形式が正しくありません。今日の記録として進めます。")
            target_date = today_str

    # Ask for commitment check
    print(f"\n【行動チェック ({target_date})】")
    done = input("Q. この日は30分のエンゲージメントを実施しましたか？ (y/n): ").lower()

    if done != "y":
        print("\n⚠️ 正直な申告ありがとうございます。")
        if target_date == today_str:
            print(
                "今日は「No Zero Day」ルールに基づき、今すぐ1いいねだけでもしてきてください。"
            )
            input("完了したらEnterキーを押してください...")
        else:
            print("過去の日付のため、記録のみ行います。")

    print("\n【成果入力】")
    try:
        followers = input("フォロワー数: ")
        likes = input("今日のいいね数（自分がした数ではなく、された数）: ")
        # If user doesn't know, default to 0
        if not likes:
            likes = "0"

        # Optional metrics
        print("\n(以下は分かれば入力。分からなければEnter)")
        reposts = input("リポスト数: ") or "0"
        replies = input("返信数: ") or "0"
        clicks = input("プロフィールクリック数: ") or "0"
        notepv = input("noteのPV数: ") or "0"

        data = {
            "Followers": followers,
            "Likes": likes,
            "Reposts": reposts,
            "Replies": replies,
            "Profile_Clicks": clicks,
            "Note_PV": notepv,
        }

        append_to_csv(data)
        new_streak = update_streak(streak_data)

        print("\n" + "=" * 50)
        print(f"✅ 記録完了！ ストリーク更新: {new_streak}日目")
        print("明日も頑張りましょう！")
        print("=" * 50)

        # Open Dashboard
        # webbrowser.open(DASHBOARD_URL) # Uncomment if server is running

    except ValueError:
        print("❌ エラー: 数字で入力してください。")


if __name__ == "__main__":
    main()
