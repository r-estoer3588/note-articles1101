"""
X API v2 運用分析ツール
AI Narrative Studio & GETHNOTE 向け

必要なライブラリ:
pip install tweepy pandas matplotlib seaborn python-dotenv
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

# 日本語フォント設定（Windows環境）
plt.rcParams['font.sans-serif'] = ['MS Gothic']
plt.rcParams['axes.unicode_minus'] = False


class XAnalyzer:
    """X API v2を使った運用分析クラス"""
    
    def __init__(self, bearer_token: str):
        """
        初期化
        
        Args:
            bearer_token: X API v2 Bearer Token
        """
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.data_cache = []
        
    def fetch_user_tweets(
        self, 
        username: str, 
        max_results: int = 100,
        start_time: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        指定ユーザーの投稿データを取得
        
        Args:
            username: Xのユーザー名（@なし）
            max_results: 取得する投稿数（最大100件/リクエスト）
            start_time: 取得開始日時（Noneの場合は過去30日）
            
        Returns:
            投稿データのDataFrame
        """
        # ユーザーID取得
        user = self.client.get_user(username=username)
        if not user.data:
            raise ValueError(f"ユーザー {username} が見つかりません")
        
        user_id = user.data.id
        
        # デフォルトは過去30日
        if start_time is None:
            start_time = datetime.utcnow() - timedelta(days=30)
        
        # 投稿取得
        tweets = self.client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            start_time=start_time,
            tweet_fields=[
                'created_at', 'public_metrics', 'entities', 
                'attachments', 'referenced_tweets'
            ],
            expansions=['attachments.media_keys'],
            media_fields=['type', 'duration_ms', 'public_metrics']
        )
        
        if not tweets.data:
            return pd.DataFrame()
        
        # DataFrameに変換
        records = []
        for tweet in tweets.data:
            record = {
                'tweet_id': tweet.id,
                'created_at': tweet.created_at,
                'text': tweet.text,
                'like_count': tweet.public_metrics['like_count'],
                'retweet_count': tweet.public_metrics['retweet_count'],
                'reply_count': tweet.public_metrics['reply_count'],
                'quote_count': tweet.public_metrics['quote_count'],
                'impression_count': tweet.public_metrics.get('impression_count', 0),
            }
            
            # メディア種別判定
            if hasattr(tweet, 'attachments') and tweet.attachments:
                media_keys = tweet.attachments.get('media_keys', [])
                if media_keys and tweets.includes and 'media' in tweets.includes:
                    media_types = [m.type for m in tweets.includes['media'] if m.media_key in media_keys]
                    record['media_type'] = media_types[0] if media_types else 'none'
                else:
                    record['media_type'] = 'none'
            else:
                record['media_type'] = 'none'
            
            # スレッド判定（返信ツイートかどうか）
            if hasattr(tweet, 'referenced_tweets') and tweet.referenced_tweets:
                is_reply = any(ref.type == 'replied_to' for ref in tweet.referenced_tweets)
                record['is_thread'] = is_reply
            else:
                record['is_thread'] = False
            
            records.append(record)
        
        df = pd.DataFrame(records)
        
        # 追加の計算フィールド
        df['engagement_total'] = (
            df['like_count'] + 
            df['retweet_count'] + 
            df['reply_count'] + 
            df['quote_count']  # 引用RTを追加
        )
        df['posting_hour'] = df['created_at'].dt.hour
        df['posting_day'] = df['created_at'].dt.day_name()
        df['rt_like_ratio'] = df['retweet_count'] / (df['like_count'] + 1)  # ゼロ除算回避
        
        return df
    
    def calculate_engagement_rate(
        self, 
        df: pd.DataFrame, 
        follower_count: int
    ) -> pd.DataFrame:
        """
        エンゲージメント率を計算
        
        Args:
            df: 投稿データのDataFrame
            follower_count: フォロワー数
            
        Returns:
            ER列が追加されたDataFrame
        """
        df = df.copy()
        df['engagement_rate'] = (df['engagement_total'] / follower_count) * 100
        return df
    
    def analyze_by_media_type(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        メディア種別ごとの分析
        
        Args:
            df: 投稿データのDataFrame
            
        Returns:
            集計結果のDataFrame
        """
        summary = df.groupby('media_type').agg({
            'tweet_id': 'count',
            'like_count': 'mean',
            'retweet_count': 'mean',
            'reply_count': 'mean',
            'engagement_rate': 'mean',
            'rt_like_ratio': 'mean'
        }).round(2)
        
        summary.columns = ['投稿数', '平均いいね', '平均RT', '平均返信', '平均ER(%)', 'RT/いいね比']
        return summary.sort_values('平均ER(%)', ascending=False)
    
    def analyze_by_time(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        時間帯別の分析
        
        Args:
            df: 投稿データのDataFrame
            
        Returns:
            時間帯別集計結果のDataFrame
        """
        # 時間帯を3時間区切りで分類
        df = df.copy()
        df['time_slot'] = pd.cut(
            df['posting_hour'], 
            bins=[0, 6, 9, 12, 15, 18, 21, 24],
            labels=['深夜(0-6)', '朝(6-9)', '午前(9-12)', '昼(12-15)', '夕方(15-18)', '夜(18-21)', '深夜(21-24)'],
            include_lowest=True
        )
        
        summary = df.groupby('time_slot').agg({
            'tweet_id': 'count',
            'engagement_rate': 'mean',
            'like_count': 'mean',
            'retweet_count': 'mean'
        }).round(2)
        
        summary.columns = ['投稿数', '平均ER(%)', '平均いいね', '平均RT']
        return summary
    
    def create_heatmap(
        self, 
        df: pd.DataFrame, 
        metric: str = 'engagement_rate',
        output_path: Optional[str] = None
    ):
        """
        時間帯×曜日のヒートマップ作成
        
        Args:
            df: 投稿データのDataFrame
            metric: 可視化する指標（'engagement_rate', 'like_count'など）
            output_path: 保存先パス（Noneの場合は表示のみ）
        """
        # 時間帯区分
        df = df.copy()
        df['time_slot'] = pd.cut(
            df['posting_hour'], 
            bins=[0, 6, 9, 12, 15, 18, 21, 24],
            labels=['0-6', '6-9', '9-12', '12-15', '15-18', '18-21', '21-24'],
            include_lowest=True
        )
        
        # ピボットテーブル作成
        pivot = df.pivot_table(
            values=metric,
            index='time_slot',
            columns='posting_day',
            aggfunc='mean'
        )
        
        # 曜日順を調整
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot = pivot.reindex(columns=[d for d in day_order if d in pivot.columns])
        
        # ヒートマップ描画
        plt.figure(figsize=(12, 6))
        sns.heatmap(
            pivot, 
            annot=True, 
            fmt='.2f', 
            cmap='YlOrRd',
            cbar_kws={'label': metric}
        )
        plt.title(f'{metric} ヒートマップ（時間帯 × 曜日）')
        plt.xlabel('曜日')
        plt.ylabel('時間帯')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def get_top_tweets(
        self, 
        df: pd.DataFrame, 
        metric: str = 'engagement_rate',
        top_n: int = 10
    ) -> pd.DataFrame:
        """
        高パフォーマンス投稿の抽出
        
        Args:
            df: 投稿データのDataFrame
            metric: ランキング基準の指標
            top_n: 上位何件取得するか
            
        Returns:
            上位投稿のDataFrame
        """
        return df.nlargest(top_n, metric)[
            ['created_at', 'text', metric, 'like_count', 'retweet_count', 'media_type']
        ]
    
    def generate_monthly_report(
        self,
        df: pd.DataFrame,
        account_name: str,
        follower_count: int,
        output_dir: str = './reports'
    ):
        """
        月次レポート自動生成
        
        Args:
            df: 投稿データのDataFrame
            account_name: アカウント名
            follower_count: フォロワー数
            output_dir: レポート出力先ディレクトリ
        """
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. サマリー統計
        summary = {
            'アカウント': account_name,
            '分析期間': f"{df['created_at'].min()} 〜 {df['created_at'].max()}",
            '総投稿数': len(df),
            'フォロワー数': follower_count,
            '平均ER(%)': df['engagement_rate'].mean(),
            '総いいね数': df['like_count'].sum(),
            '総RT数': df['retweet_count'].sum(),
            '総返信数': df['reply_count'].sum()
        }
        
        summary_df = pd.DataFrame([summary]).T
        summary_df.to_csv(f'{output_dir}/{timestamp}_{account_name}_summary.csv', encoding='utf-8-sig')
        
        # 2. メディア別分析
        media_analysis = self.analyze_by_media_type(df)
        media_analysis.to_csv(f'{output_dir}/{timestamp}_{account_name}_media_analysis.csv', encoding='utf-8-sig')
        
        # 3. 時間帯別分析
        time_analysis = self.analyze_by_time(df)
        time_analysis.to_csv(f'{output_dir}/{timestamp}_{account_name}_time_analysis.csv', encoding='utf-8-sig')
        
        # 4. トップ10投稿
        top_tweets = self.get_top_tweets(df, 'engagement_rate', 10)
        top_tweets.to_csv(f'{output_dir}/{timestamp}_{account_name}_top_tweets.csv', encoding='utf-8-sig', index=False)
        
        # 5. ヒートマップ
        self.create_heatmap(
            df, 
            'engagement_rate',
            f'{output_dir}/{timestamp}_{account_name}_heatmap.png'
        )
        
        print(f"✅ レポート生成完了: {output_dir}/")
        return summary


# 使用例
if __name__ == '__main__':
    # 環境変数から認証情報読み込み
    load_dotenv()
    BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
    
    if not BEARER_TOKEN:
        print("エラー: .envファイルに X_BEARER_TOKEN を設定してください")
        exit(1)
    
    # アナライザー初期化
    analyzer = XAnalyzer(BEARER_TOKEN)
    
    # 環境変数からアカウント情報取得
    ai_narrative_username = os.getenv(
        'X_USERNAME_AI_NARRATIVE', 'ai_narrative25'
    )
    gethinu_username = os.getenv('X_USERNAME_GETHINU', 'gethinu')
    ai_narrative_followers = int(
        os.getenv('X_FOLLOWERS_AI_NARRATIVE', '500')
    )
    gethinu_followers = int(os.getenv('X_FOLLOWERS_GETHINU', '200'))
    
    # === AI Narrative Studio の分析例 ===
    print("📊 AI Narrative Studio の分析を開始...")
    try:
        # 投稿データ取得（過去30日、最大100件）
        ai_narrative_df = analyzer.fetch_user_tweets(
            username=ai_narrative_username,
            max_results=100
        )
        
        # エンゲージメント率計算
        ai_narrative_df = analyzer.calculate_engagement_rate(
            ai_narrative_df, ai_narrative_followers
        )
        
        # 月次レポート生成
        analyzer.generate_monthly_report(
            df=ai_narrative_df,
            account_name='AI_Narrative_Studio',
            follower_count=ai_narrative_followers
        )
        
        print("\n【メディア別分析】")
        print(analyzer.analyze_by_media_type(ai_narrative_df))
        
        print("\n【時間帯別分析】")
        print(analyzer.analyze_by_time(ai_narrative_df))
        
    except Exception as e:
        print(f"エラー: {e}")
    
    # === GETHNOTE の分析例 ===
    print("\n\n📊 GETHNOTE の分析を開始...")
    try:
        gethnote_df = analyzer.fetch_user_tweets(
            username=gethinu_username,
            max_results=100
        )
        
        gethnote_df = analyzer.calculate_engagement_rate(
            gethnote_df, gethinu_followers
        )
        
        analyzer.generate_monthly_report(
            df=gethnote_df,
            account_name='GETHNOTE',
            follower_count=gethinu_followers
        )
        
        print("\n【トップ10投稿】")
        print(analyzer.get_top_tweets(gethnote_df, 'engagement_rate', 10))
        
    except Exception as e:
        print(f"エラー: {e}")
