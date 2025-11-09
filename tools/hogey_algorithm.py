"""
ホゲーアルゴリズム - 泥人間ペルソナ向けX投稿自動生成システム

機能:
- CSV学習（自分の投稿 + 強者アカウント投稿）
- 6つの教育タイプ × 8テンプレ × バズ構成
- 3部作ストーリー型投稿生成
- 自律型学習ループ
"""

import pandas as pd
import random
import json
from typing import List, Dict, Any, Tuple
from collections import Counter
from datetime import datetime, timedelta
import re


class HogeyAlgorithm:
    """ホゲーアルゴリズム実装クラス"""
    
    # 6つの教育タイプ
    EDUCATION_TYPES = [
        "目的の教育",  # なぜそれをやるのか
        "問題の教育",  # 現状のヤバさに気づかせる
        "価値の教育",  # 価値・意義を理解させる
        "信頼の教育",  # 発信者を信用させる
        "親近感の教育",  # 距離を縮める
        "行動の教育"   # 一歩を踏み出させる
    ]
    
    # フレームワーク
    FRAMEWORKS = [
        "ジョブ理論",
        "PASONA法則",
        "HARM構成",
        "6つの教育"
    ]
    
    # 泥人間あるある（フックワード候補）
    DORONIN_PHRASES = [
        "ホゲーっと生きてる",
        "コンビニ飯とビール2本",
        "寝落ち泥人間",
        "仕事終わりにフラフラ",
        "残高274円の夜",
        "冷めたカップ麺",
        "脳みそバグる",
        "気づいたら何も変わってない",
        "明日も同じ朝が来る",
        "毎日ビール開けてX眺めて寝る"
    ]
    
    # 語尾候補
    ENDINGS = [
        "試してみて",
        "これで変われる",
        "やってみるといい",
        "今日からできる",
        "そろそろ浮上しようぜ",
        "足を動かせば沈まない",
        "お前も、そろそろ動こうぜ",
        "あの夜で終わったんだ"
    ]
    
    # 固有名詞
    PROPER_NOUNS = [
        "X", "note", "ChatGPT", "n8n", "Canva",
        "スマホ", "コンビニ", "ビール"
    ]
    
    def __init__(self):
        self.learned_patterns = {
            'hooks': list(self.DORONIN_PHRASES),
            'endings': list(self.ENDINGS),
            'nouns': list(self.PROPER_NOUNS),
            'high_score_words': []
        }
    
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """CSV読み込み"""
        try:
            df = pd.read_csv(filepath, encoding='utf-8-sig')
            return df
        except Exception as e:
            print(f"CSV読み込みエラー: {e}")
            return pd.DataFrame()
    
    def analyze_post(self, text: str) -> Dict[str, Any]:
        """投稿テキストを分析"""
        words = re.findall(r'\w+', text)
        
        # 語尾抽出（最後の5文字程度）
        ending_candidate = text[-10:].strip() if len(text) > 10 else text
        
        # 数字を抽出
        numbers = re.findall(r'\d+', text)
        
        # 固有名詞の出現
        found_nouns = [n for n in self.PROPER_NOUNS if n in text]
        
        return {
            'words': words,
            'ending': ending_candidate,
            'numbers': numbers,
            'nouns': found_nouns,
            'length': len(text),
            'line_breaks': text.count('\n')
        }
    
    def learn_from_csv(self, my_posts_path: str = None, bench_posts_path: str = None):
        """CSV学習メソッド"""
        all_patterns = {
            'hooks': [],
            'endings': [],
            'nouns': [],
            'high_score_words': []
        }
        
        # 自分の投稿を学習
        if my_posts_path:
            my_df = self.load_csv(my_posts_path)
            if not my_df.empty and 'text' in my_df.columns:
                # スコアリング
                if 'likes' in my_df.columns and 'retweets' in my_df.columns:
                    my_df['score'] = my_df['likes'] + my_df['retweets'] * 2
                else:
                    my_df['score'] = 1
                
                # 高スコア投稿を優先分析
                top_posts = my_df.nlargest(min(20, len(my_df)), 'score')
                
                for text in top_posts['text']:
                    analysis = self.analyze_post(str(text))
                    all_patterns['high_score_words'].extend(analysis['words'])
                    all_patterns['nouns'].extend(analysis['nouns'])
        
        # 強者アカウント投稿を学習
        if bench_posts_path:
            bench_df = self.load_csv(bench_posts_path)
            if not bench_df.empty and 'text' in bench_df.columns:
                # スコアリング
                if 'likes' in bench_df.columns and 'retweets' in bench_df.columns:
                    bench_df['score'] = bench_df['likes'] + bench_df['retweets'] * 2
                else:
                    bench_df['score'] = 1
                
                # 高スコア投稿を優先分析
                top_posts = bench_df.nlargest(min(30, len(bench_df)), 'score')
                
                for text in top_posts['text']:
                    analysis = self.analyze_post(str(text))
                    all_patterns['high_score_words'].extend(analysis['words'])
                    all_patterns['nouns'].extend(analysis['nouns'])
        
        # 学習済みパターンを更新
        if all_patterns['high_score_words']:
            word_counter = Counter(all_patterns['high_score_words'])
            top_words = [w for w, c in word_counter.most_common(50) if len(w) > 1]
            self.learned_patterns['high_score_words'] = top_words
        
        if all_patterns['nouns']:
            noun_counter = Counter(all_patterns['nouns'])
            self.learned_patterns['nouns'] = list(set(
                self.learned_patterns['nouns'] + 
                [n for n, c in noun_counter.most_common(20)]
            ))
        
        print(f"学習完了: {len(self.learned_patterns['high_score_words'])}個の頻出ワード")
        print(f"固有名詞: {len(self.learned_patterns['nouns'])}種類")
    
    def generate_buzz_post(self, theme: str = "人生逆転", 
                          education_type: str = None,
                          framework: str = None) -> Dict[str, Any]:
        """バズ構成投稿を生成（7行以内）"""
        
        # ランダム選択
        if not education_type:
            education_type = random.choice(self.EDUCATION_TYPES)
        if not framework:
            framework = random.choice(self.FRAMEWORKS)
        
        # フック選択
        hook = random.choice(self.learned_patterns['hooks'])
        ending = random.choice(self.learned_patterns['endings'])
        
        # 数字を入れる
        number = random.choice([3, 5, 7, 30, 50, 100, 274, "半年", "1年"])
        
        # バズ構成（7行構成）
        lines = []
        
        # 1-2行目: 起承（共感フック）
        lines.append(f"{hook}。")
        lines.append(f"気づいたら何も変わってない。")
        lines.append("")
        
        # 3-4行目: 転結（問題提起・気づき）
        if education_type == "問題の教育":
            lines.append(f"でもある日、「このままじゃ終われない」って思った。")
        elif education_type == "親近感の教育":
            lines.append(f"俺も昔はそうだった。")
        else:
            lines.append(f"{number}日で変われる方法があるんだ。")
        
        lines.append("")
        
        # 5-6行目: 応用（具体策・ストーリー）
        lines.append(f"あの時から少しずつ変えた。")
        lines.append(f"情報に金を払うようにして、人生が動き出した。")
        lines.append("")
        
        # 7行目: 独創的な締め
        lines.append(f"{ending}。")
        
        text = "\n".join(lines)
        
        return {
            "text": text,
            "education_type": education_type,
            "framework": framework,
            "hook": hook,
            "ending": ending,
            "theme": theme,
            "structure": "7行バズ構成"
        }
    
    def generate_story_trilogy(self, theme: str = "停滞からの逆転") -> List[Dict[str, Any]]:
        """3部作ストーリー型投稿を生成"""
        
        trilogy = []
        
        # ① 起（共感・導入）
        part1 = {
            "part": "① 起",
            "purpose": "共感・導入",
            "text": f"""夜中2時。
冷めたカップ麺すすりながら、
{random.choice(self.learned_patterns['nouns'])}で他人の成功話見てた。

何も変わらんまま、
明日も同じ朝が来ると思ってた。""",
            "education_type": "親近感の教育"
        }
        trilogy.append(part1)
        
        # ② 転（崩壊・気づき）
        part2 = {
            "part": "② 転",
            "purpose": "崩壊・気づき",
            "text": f"""でもある日、上司が笑いながら言った。
「お前、夢とかないの？」

頭の中が真っ白になった。
あの瞬間、「このままじゃ終われない」って思った。""",
            "education_type": "問題の教育"
        }
        trilogy.append(part2)
        
        # ③ 解（逆転・希望）
        part3 = {
            "part": "③ 解",
            "purpose": "逆転・希望",
            "text": f"""あの時から少しずつ変えた。
情報に金を払うようにして、
気づけば人生が静かに動き出した。

泥の中でも、足を動かせば沈まない。
{random.choice(self.learned_patterns['endings'])}。""",
            "education_type": "行動の教育"
        }
        trilogy.append(part3)
        
        return {
            "series_name": f"ホゲー{theme}編",
            "theme": theme,
            "posts": trilogy
        }
    
    def generate_posts_batch(self, count: int = 10, theme: str = "人生逆転") -> pd.DataFrame:
        """複数投稿を一括生成してCSV形式で出力"""
        posts = []
        
        for i in range(count):
            # ランダムでバズ投稿 or 3部作の1つを選択
            if random.random() < 0.7:  # 70%はバズ投稿
                post = self.generate_buzz_post(theme=theme)
                post_id = i + 1
                posts.append({
                    'post_id': post_id,
                    'text': post['text'],
                    'education_type': post['education_type'],
                    'framework': post['framework'],
                    'hook': post['hook'],
                    'ending': post['ending'],
                    'theme': theme,
                    'structure': post['structure'],
                    'hashtags': '#げすいぬ #底辺脱出',
                    'scheduled_datetime': (datetime.now() + timedelta(hours=i*2)).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        df = pd.DataFrame(posts)
        return df
    
    def save_posts_csv(self, df: pd.DataFrame, output_path: str):
        """生成投稿をCSV保存"""
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"投稿生成完了: {output_path} ({len(df)}件)")


def main():
    """メイン実行関数（CLI対応）"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ホゲーアルゴリズム')
    parser.add_argument('--theme', default='人生逆転', help='投稿テーマ')
    parser.add_argument('--count', type=int, default=10, help='生成件数')
    parser.add_argument('--type', default='buzz',
                       choices=['buzz', 'trilogy', 'demo'],
                       help='生成タイプ')
    parser.add_argument('--learn', action='store_true',
                       help='CSV学習を実行')
    parser.add_argument('--my-posts', default='my_posts.csv',
                       help='自分の投稿CSV')
    parser.add_argument('--bench-posts', default='bench_posts.csv',
                       help='強者アカウントCSV')
    parser.add_argument('--output', default='generated_posts.csv',
                       help='出力ファイル名')
    parser.add_argument('--json', action='store_true',
                       help='JSON形式で出力')
    
    args = parser.parse_args()
    
    # インスタンス作成
    hogey = HogeyAlgorithm()
    
    # CSV学習
    if args.learn:
        print("CSV学習実行中...")
        hogey.learn_from_csv(
            my_posts_path=args.my_posts,
            bench_posts_path=args.bench_posts
        )
    
    # デモモード
    if args.type == 'demo':
        print("=" * 50)
        print("ホゲーアルゴリズム デモ実行")
        print("=" * 50)
        
        # バズ投稿生成
        print("\n【バズ投稿生成】")
        post = hogey.generate_buzz_post(theme=args.theme)
        print(post['text'])
        print(f"\n教育タイプ: {post['education_type']}")
        print(f"フレームワーク: {post['framework']}")
        
        # 3部作ストーリー生成
        print("\n" + "=" * 50)
        print("【3部作ストーリー生成】")
        print("=" * 50)
        trilogy = hogey.generate_story_trilogy(theme=args.theme)
        for p in trilogy['posts']:
            print(f"\n{p['part']} - {p['purpose']}")
            print("-" * 40)
            print(p['text'])
            print(f"教育タイプ: {p['education_type']}")
        
        return
    
    # 3部作生成
    if args.type == 'trilogy':
        result = hogey.generate_story_trilogy(theme=args.theme)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for p in result['posts']:
                print(f"\n{p['part']}")
                print(p['text'])
                print()
        return
    
    # バズ投稿一括生成
    df = hogey.generate_posts_batch(count=args.count, theme=args.theme)
    
    if args.json:
        print(json.dumps(df.to_dict('records'),
                        ensure_ascii=False, indent=2))
    else:
        hogey.save_posts_csv(df, args.output)
        print(f"\n生成完了: {args.output} ({len(df)}件)")


if __name__ == "__main__":
    main()
