import requests
import json
import datetime
import os


class XApiClient:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "User-Agent": "v2UserLookupPython",
        }

    def get_user_metrics(self, user_id):
        """
        指定されたユーザーの公開メトリクス（フォロワー数など）を取得
        """
        url = f"{self.base_url}/users/{user_id}"
        params = {"user.fields": "public_metrics"}

        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            if response.status_code != 200:
                print(
                    f"Error fetching user metrics: {response.status_code} {response.text}"
                )
                return None

            data = response.json()
            if "data" in data:
                return data["data"]["public_metrics"]
            return None
        except Exception as e:
            print(f"Exception fetching user metrics: {e}")
            return None

    def get_todays_engagement(self, user_id):
        """
        今日の投稿のエンゲージメント合計を取得
        注意: Basic Tier以上が必要。Free Tierでは動作しません。
        """
        # 今日の00:00:00 (JST) をISO形式で取得
        # X APIはUTCなので変換が必要
        # JST = UTC+9
        now = datetime.datetime.now()
        today_start_jst = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_start_utc = today_start_jst - datetime.timedelta(hours=9)
        start_time = today_start_utc.isoformat() + "Z"

        url = f"{self.base_url}/users/{user_id}/tweets"
        params = {
            "start_time": start_time,
            "tweet.fields": "public_metrics,created_at",
            "max_results": 100,  # 1日100ツイート以内と仮定
            "exclude": "retweets,replies",  # 純粋な投稿のみを集計する場合。返信も含めるなら外す
        }
        # 返信も含めて集計したい場合が多いのでexcludeは外すか調整
        # ここでは「自分の投稿」への反応を見たいので、exclude=retweetsのみにする（リツイートは自分の言葉ではないため）
        params["exclude"] = "retweets"

        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            if response.status_code != 200:
                print(f"Error fetching tweets: {response.status_code} {response.text}")
                return None

            data = response.json()

            metrics = {"likes": 0, "reposts": 0, "replies": 0, "quotes": 0}

            if "data" in data:
                for tweet in data["data"]:
                    m = tweet["public_metrics"]
                    metrics["likes"] += m.get("like_count", 0)
                    metrics["reposts"] += m.get("retweet_count", 0)
                    metrics["replies"] += m.get("reply_count", 0)
                    metrics["quotes"] += m.get("quote_count", 0)

            # リポスト数には引用リツイートも含めるのが一般的
            metrics["reposts"] += metrics["quotes"]

            return metrics

        except Exception as e:
            print(f"Exception fetching tweets: {e}")
            return None


def load_env_file(env_path):
    config = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    return config


def fetch_x_data():
    # .env file path (parent directory of tools/monitoring -> tools/.env)
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
    )

    config = load_env_file(env_path)

    bearer_token = config.get("X_BEARER_TOKEN")

    # Try to find username/id
    # Priority: X_USER_ID -> AI_NARRATIVE_USERNAME -> GETHNOTE_USERNAME
    user_id = config.get("X_USER_ID")
    username = config.get("AI_NARRATIVE_USERNAME") or config.get("GETHNOTE_USERNAME")

    if username and username.startswith("@"):
        username = username[1:]

    if not bearer_token:
        return {"error": "X_BEARER_TOKEN not found in .env"}

    client = XApiClient(bearer_token)

    # If we have username but no ID, fetch ID
    if not user_id and username:
        print(f"Fetching user ID for {username}...")
        try:
            url = f"https://api.twitter.com/2/users/by/username/{username}"
            headers = {"Authorization": f"Bearer {bearer_token}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                if "data" in user_data:
                    user_id = user_data["data"]["id"]
                    print(f"Found User ID: {user_id}")
            else:
                print(
                    f"Error fetching user ID for {username}: {response.status_code} {response.text}"
                )
        except Exception as e:
            print(f"Exception fetching user ID for {username}: {e}")

    if not user_id:
        return {
            "error": "Could not determine User ID (set X_USER_ID or AI_NARRATIVE_USERNAME in .env)"
        }

    # 1. ユーザーメトリクス（フォロワー数）
    user_metrics = client.get_user_metrics(user_id)
    if not user_metrics:
        return {"error": "Failed to fetch user metrics"}

    # 2. 今日のエンゲージメント
    engagement = client.get_todays_engagement(user_id)
    if not engagement:
        engagement = {"likes": 0, "reposts": 0, "replies": 0}

    return {
        "status": "success",
        "data": {
            "followers": user_metrics["followers_count"],
            "likes": engagement["likes"],
            "reposts": engagement["reposts"],
            "replies": engagement["replies"],
        },
    }


if __name__ == "__main__":
    # Test run
    result = fetch_x_data()
    print(json.dumps(result, indent=2))
