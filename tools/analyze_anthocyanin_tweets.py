"""アントシアニンさんの図解ポスト分析ツール"""

import pandas as pd
import re
from collections import Counter
import json
from pathlib import Path

def main():
    # CSVファイル読み込み
    csv_path = Path(__file__).parent.parent / 'input' / 'TwExportly_antoshia2n_tweets_2025_11_23.csv'
    df = pd.read_csv(csv_path)

    # 基本統計
    total_tweets = len(df)
    print('=== 基本統計 ===')
    print(f'総ツイート数: {total_tweets}')
    print(f'期間: {df["created_at"].min()} 〜 {df["created_at"].max()}')
    print()

    # 図解関連ポストの抽出（複数パターン）
    keywords = ['図解', 'ずかい', 'ズカイ', 'Canva', 'デザイン', 'テンプレ', 'バズ', 'インプ']
    pattern = '|'.join(keywords)

    df['is_zukai'] = df['text'].fillna('').str.contains(pattern, case=False, regex=True)
    zukai_df = df[df['is_zukai']].copy()

    print('=== 図解関連ポスト ===')
    print(f'図解関連: {len(zukai_df)} 件 ({len(zukai_df)/total_tweets*100:.1f}%)')
    print()

    # メディア付き分析
    zukai_df['has_media'] = zukai_df['media_type'].notna()
    zukai_with_media = zukai_df[zukai_df['has_media']]

    print('=== メディア分析 ===')
    print(f'図解関連でメディア付き: {len(zukai_with_media)} 件')
    print(f'図解関連でメディア率: {len(zukai_with_media)/len(zukai_df)*100:.1f}%')
    print()

    # エンゲージメント分析（図解関連）
    print('=== 図解関連のエンゲージメント統計 ===')
    for col in ['favorite_count', 'retweet_count', 'reply_count', 'view_count']:
        if col in zukai_df.columns:
            avg = zukai_df[col].mean()
            median = zukai_df[col].median()
            max_val = zukai_df[col].max()
            print(f'{col}: 平均={avg:.1f}, 中央値={median:.1f}, 最大={max_val}')
    print()

    # 投稿タイプ分析
    print('=== 投稿タイプ分析 ===')
    type_counts = zukai_df['type'].value_counts()
    for t, count in type_counts.items():
        print(f'{t}: {count} 件 ({count/len(zukai_df)*100:.1f}%)')
    print()

    # テキスト長分析
    zukai_df['text_length'] = zukai_df['text'].fillna('').str.len()
    print('=== テキスト長分析（図解関連） ===')
    print(f'平均: {zukai_df["text_length"].mean():.1f} 文字')
    print(f'中央値: {zukai_df["text_length"].median():.1f} 文字')
    print()

    # 頻出単語分析（図解関連）
    all_text = ' '.join(zukai_df['text'].fillna(''))
    words = re.findall(r'[ぁ-んァ-ヶー一-龥]+', all_text)
    word_freq = Counter([w for w in words if len(w) > 1])

    print('=== 頻出単語 TOP30（図解関連） ===')
    for word, count in word_freq.most_common(30):
        print(f'{word}: {count}回')
    print()

    # URL分析
    zukai_df['has_url'] = zukai_df['urls'].notna() & (zukai_df['urls'] != '')
    url_rate = zukai_df['has_url'].sum() / len(zukai_df) * 100
    print('=== URL分析（図解関連） ===')
    print(f'URL付きポスト: {zukai_df["has_url"].sum()} 件 ({url_rate:.1f}%)')
    print()

    # 高エンゲージメントポスト（図解関連、いいね100以上）
    high_engagement = zukai_df[zukai_df['favorite_count'] >= 100].sort_values('favorite_count', ascending=False)
    print('=== 高エンゲージメントポスト（いいね100以上） ===')
    print(f'該当数: {len(high_engagement)} 件')
    if len(high_engagement) > 0:
        print('\nTOP10:')
        for idx, row in high_engagement.head(10).iterrows():
            text_preview = row['text'][:80].replace('\n', ' ')
            print(f'- いいね{row["favorite_count"]}, RT{row["retweet_count"]}, View{row["view_count"]}: {text_preview}...')
    print()

    # 絵文字分析
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # 顔文字
        u"\U0001F300-\U0001F5FF"  # 記号とピクトグラフ
        u"\U0001F680-\U0001F6FF"  # 交通と地図記号
        u"\U0001F1E0-\U0001F1FF"  # 旗
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    zukai_df['emoji_count'] = zukai_df['text'].fillna('').apply(lambda x: len(emoji_pattern.findall(x)))
    zukai_df['has_emoji'] = zukai_df['emoji_count'] > 0
    
    print('=== 絵文字使用分析（図解関連） ===')
    print(f'絵文字使用ポスト: {zukai_df["has_emoji"].sum()} 件 ({zukai_df["has_emoji"].sum()/len(zukai_df)*100:.1f}%)')
    print(f'平均絵文字数: {zukai_df["emoji_count"].mean():.2f}個')
    print()

    # 時間帯分析
    zukai_df['created_datetime'] = pd.to_datetime(zukai_df['created_at'])
    zukai_df['hour'] = zukai_df['created_datetime'].dt.hour
    
    print('=== 投稿時間帯分析（図解関連） ===')
    hour_counts = zukai_df['hour'].value_counts().sort_index()
    for hour, count in hour_counts.items():
        print(f'{hour:02d}時台: {count}件')
    print()

    # 構造パターン分析
    print('=== 投稿構造パターン分析（図解関連） ===')
    zukai_df['has_question'] = zukai_df['text'].fillna('').str.contains('[？?]')
    zukai_df['has_exclamation'] = zukai_df['text'].fillna('').str.contains('[！!]')
    zukai_df['has_bullet'] = zukai_df['text'].fillna('').str.contains('[✔️✅▪️・]')
    zukai_df['has_arrow'] = zukai_df['text'].fillna('').str.contains('[→⇒⬇︎⬆︎]')
    
    print(f'疑問符使用: {zukai_df["has_question"].sum()}件 ({zukai_df["has_question"].sum()/len(zukai_df)*100:.1f}%)')
    print(f'感嘆符使用: {zukai_df["has_exclamation"].sum()}件 ({zukai_df["has_exclamation"].sum()/len(zukai_df)*100:.1f}%)')
    print(f'箇条書き記号使用: {zukai_df["has_bullet"].sum()}件 ({zukai_df["has_bullet"].sum()/len(zukai_df)*100:.1f}%)')
    print(f'矢印使用: {zukai_df["has_arrow"].sum()}件 ({zukai_df["has_arrow"].sum()/len(zukai_df)*100:.1f}%)')
    print()

    # noteリンク分析
    zukai_df['has_note_link'] = zukai_df['urls'].fillna('').str.contains('note.com')
    print('=== noteリンク分析（図解関連） ===')
    print(f'noteリンク付き: {zukai_df["has_note_link"].sum()}件 ({zukai_df["has_note_link"].sum()/len(zukai_df)*100:.1f}%)')
    print()

    # キーフレーズ分析
    print('=== 高エンゲージメント投稿のキーフレーズ ===')
    if len(high_engagement) > 0:
        high_text = ' '.join(high_engagement.head(20)['text'].fillna(''))
        high_words = re.findall(r'[ぁ-んァ-ヶー一-龥]+', high_text)
        high_word_freq = Counter([w for w in high_words if len(w) > 1])
        for word, count in high_word_freq.most_common(15):
            print(f'{word}: {count}回')

if __name__ == '__main__':
    main()
