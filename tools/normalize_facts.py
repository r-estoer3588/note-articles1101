# -*- coding: utf-8 -*-
"""
factsスタイル正規化スクリプト
- data_collection_output.json の facts 文面を一括整形
- 主な処理:
  * 数字範囲のハイフン -> 波ダッシュ(〜) 置換 (例: 5-10% -> 5〜10%)
  * ASCIIチルダ ~ を 〜 に（数値の範囲に限る）
  * -> を → に統一
  * %, pt, 円 の直前スペース除去
  * ± の直後スペース除去 (± 0.2 -> ±0.2)
  * 4桁以上の整数に桁区切り(,)を付与（ただし直後が 万/億/兆 の場合は除外）
  * 連続スペースの圧縮

出力:
  - 上書き保存 (バックアップファイルを作成)
  - 変更件数を標準出力
"""
from __future__ import annotations
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / 'data_collection_output.json'

# 正規表現の準備
RE_RANGE_HYPHEN = re.compile(r"(?<=\d)\s*-\s*(?=\d)")
RE_RANGE_TILDE_ASCII = re.compile(r"(?<=\d)\s*~\s*(?=\d)")
# 全角チルダ(～)を波ダッシュ(〜)へ
RE_WAVE_TILDE_FULL = re.compile(r"～")
RE_ARROW_ASCII = re.compile(r"->")
RE_SPACE_BEFORE_PERCENT = re.compile(r"\s+%")
RE_SPACE_BEFORE_PT = re.compile(r"\s+pt\b")
RE_SPACE_BEFORE_YEN = re.compile(r"\s+円")
# 数字と単位の間の不要スペース削除
RE_NUMBER_SPACE_UNIT = re.compile(r"(?<=\d)\s+(?=(?:%|pt|円|h|時間|分|秒|人|件|回|年|ヶ月|月|週|日|kg|g|km|m|cm|mm)\b)")
RE_NUMBER_SPACE_UNIT_SLASH = re.compile(r"(?<=\d)\s+(?=(?:h|回|人|件|年|月|週|日)/)")
RE_PLUSMINUS_SPACE = re.compile(r"±\s*")
RE_MULTI_SPACE = re.compile(r"\s{2,}")
RE_INT4PLUS = re.compile(r"\d{4,}")

KANJI_UNITS = set("万億兆")


def add_thousand_separators(text: str) -> str:
    """4桁以上の連続数字にカンマを付与。ただし直後が 万/億/兆 の場合は除外。
    例: 3000円 -> 3,000円 / 3000万円 (直後が万) -> 3000万円 (変更なし)
    時刻や小数は RE_INT4PLUS で拾わない or 条件で弾く。
    """
    def repl(m: re.Match) -> str:
        s = m.group(0)
        start, end = m.span()
        # 直後の1文字を確認（範囲外は空文字）
        following = text[end:end+1]
        # 直後が 万/億/兆 の場合は対象外
        if following and following in KANJI_UNITS:
            return s
        # 小数部は今回のREでは対象外（\d{4,}のため）
        try:
            n = int(s)
        except ValueError:
            return s
        return f"{n:,}"

    # マッチ位置に依存するため、一旦全置換
    # ただし再置換でズレないように re.sub を用いる
    return RE_INT4PLUS.sub(repl, text)


def normalize_fact_line(line: str) -> str:
    orig = line
    s = line

    # 数値範囲のハイフンを 〜 へ
    s = RE_RANGE_HYPHEN.sub("〜", s)
    # ASCIIチルダ ~ を 〜 へ（数値範囲に限定）
    s = RE_RANGE_TILDE_ASCII.sub("〜", s)
    # 全角チルダ(～)も 〜 へ
    s = RE_WAVE_TILDE_FULL.sub("〜", s)
    # 矢印を統一
    s = RE_ARROW_ASCII.sub("→", s)
    # 記号前スペース除去
    s = RE_SPACE_BEFORE_PERCENT.sub("%", s)
    s = RE_SPACE_BEFORE_PT.sub("pt", s)
    s = RE_SPACE_BEFORE_YEN.sub("円", s)
    # 数字+単位の間のスペース除去
    s = RE_NUMBER_SPACE_UNIT.sub("", s)
    s = RE_NUMBER_SPACE_UNIT_SLASH.sub("", s)
    # ±の後ろスペース除去
    s = RE_PLUSMINUS_SPACE.sub("±", s)
    # 桁区切り（安全側ルール）
    s = add_thousand_separators(s)
    # 連続スペースを1つに
    s = RE_MULTI_SPACE.sub(" ", s)
    # 前後空白除去
    s = s.strip()

    return s if s != orig else orig


def main() -> None:
    with INPUT.open('r', encoding='utf-8') as f:
        data = json.load(f)

    changed = 0
    total = 0

    for cat in data:
        if not isinstance(cat, dict):
            continue
        items = cat.get('data', [])
        for item in items:
            facts = item.get('facts') if isinstance(item, dict) else None
            if not isinstance(facts, list):
                continue
            for i, fact in enumerate(facts):
                if not isinstance(fact, str):
                    continue
                total += 1
                new_fact = normalize_fact_line(fact)
                if new_fact != fact:
                    facts[i] = new_fact
                    changed += 1

    # バックアップ作成
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = INPUT.with_name(f"data_collection_output_backup_{ts}.json")
    shutil.copy2(INPUT, backup_path)

    # 上書き保存（インデント2・日本語可）
    with INPUT.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"facts total: {total}, changed: {changed}")


if __name__ == '__main__':
    main()
