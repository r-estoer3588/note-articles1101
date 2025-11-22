"""Day 1-28 SNS投稿データの統合とCSV更新ユーティリティ"""

import importlib
import sys
from pathlib import Path
from typing import Dict

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def _load_updates(module_name: str, attr_name: str) -> Dict[str, str]:
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)


updates_week1_day2_7 = _load_updates(
    "outputs.week1_day2_7_posts", "updates_week1_day2_7"
)
updates_week2_day8_14 = _load_updates(
    "outputs.week2_day8_14_posts", "updates_week2_day8_14"
)
updates_week3_day15_21 = _load_updates(
    "outputs.week3_day15_21_posts", "updates_week3_day15_21"
)
updates_week4_day22_28 = _load_updates(
    "outputs.week4_day22_28_posts", "updates_week4_day22_28"
)

# Week 1: Day 1（基準データ）
updates_week1_day1_7: Dict[str, str] = {
    "Day1_07:00": """【画像文字案】
喧嘩はしていない。会話も、まあ、ある。
でも、ふとした瞬間。
この「静かな距離」に気づいてしまった朝は、
少しだけ胸が痛む。

【本文】
「ゴミ出しといたよ」「ありがとう」。

（改行）

でも、ふとした瞬間。
スマホを見ている彼の背中が、ひどく遠くに感じることはありませんか？
同じ部屋にいるのに、まるで違う惑星に住んでいるみたい。

（改行）

この「静かな距離」に気づいてしまった朝は、少しだけ胸が痛む。""",
    "Day1_08:00": """おはようございます。
今朝の「行ってきます」、相手の目を見て言いましたか？
私は背中に向かって言ってしまいました。
明日は1秒でいいから、目を合わせよう。自戒を込めて。""",
    "Day1_10:00": """【質問】
夫が「今、一番食べたいもの」即答できますか？

（改行）

私は自信満々に「唐揚げ」って答えたら、
「最近は胃もたれするから刺身がいい」って言われました。
情報の更新、止まってませんか？""",
    "Day1_12:00": """「疲れたね」を「ありがとう」に変えるだけで、空気は1秒で変わる。

（改行）

業務連絡だけのLINE画面を見て、ため息をつくのはもう終わりにしませんか？
今日のお昼休み、スタンプ1個でいい。「お疲れ様」のねぎらいを送ってみる。

（改行）

それだけで、夜の食卓の温度が少し上がるはずです。""",
    "Day1_15:00": """「戦友」としては100点満点。
でも「恋人」としては赤点。

（改行）

そんな通知表を突きつけられた気分になる瞬間、ありませんか？
子育てというプロジェクトを回すパートナーとしては最高。
でも、ふと「私、女として見られてる？」って不安になる。""",
    "Day1_17:00": """「牛乳買ってきて」は秒で送れるのに、
「早く帰ってきて」の7文字が送れない。
送信ボタンの上で親指が止まる夕暮れ。""",
    "Day1_20:00": """離婚したいわけじゃない。
ただ、昔みたいに「何でもないこと」で笑い合いたいだけ。

（改行）

そんな「プチレス予備軍」のあなたへ。
私が関係を修復するために実践した、夜の会話レシピをNoteにまとめました。
現状把握から始めてみませんか？

（改行）

▼記事はプロフのリンクから
#夜専用レス手前の会話レシピ""",
    "Day1_21:00": """子どもが寝た後のリビング。
静寂の中で、スマホのタップ音だけが響く。

（改行）

この「音」が、私たちの会話の代わりになってしまった。
画面の中の誰かとは繋がっているのに、
隣にいるあなたとは繋がれない。""",
    "Day1_22:00": """隣で寝息を立てる夫。
その背中に手を伸ばそうとして、引っ込める。

（改行）

触れたいのか、触れられたいのか。
自分でもわからなくなる夜。
ただ、温もりだけが欲しいのに。""",
    "Day1_23:00": """明日は今日より1mmだけ、心の距離が縮まりますように。
おやすみなさい。
同じ空の下、同じ悩みを抱えるあなたへ。""",
}

# 既存データとのマージ
updates: Dict[str, str] = {}
updates.update(updates_week1_day1_7)
updates.update(updates_week1_day2_7)
updates.update(updates_week2_day8_14)
updates.update(updates_week3_day15_21)
updates.update(updates_week4_day22_28)

CSV_PATH = (
    Path(__file__).resolve().parents[1]
    / "research_ideas"
    / "relationship"
    / "600_posts_schedule.csv"
)


def apply_updates(csv_path: Path) -> None:
    df = pd.read_csv(csv_path)
    updates_count = 0

    for key, content in updates.items():
        day_str, time_str = key.split("_")
        day = int(day_str.replace("Day", ""))
        mask = (df["Day"] == day) & (df["Time"] == time_str)
        if mask.any():
            df.loc[mask, "Content"] = content
            updates_count += 1
            print(f"Updated {key}")
        else:
            print(f"Warning: Could not find row for {key}")

    if updates_count > 0:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"Successfully saved {updates_count} updates to {csv_path}")
    else:
        print("No updates were applied.")


if __name__ == "__main__":
    apply_updates(CSV_PATH)
