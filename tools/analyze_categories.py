#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

data_file = Path(__file__).parent / 'data_collection_output.json'
with open(data_file, 'r', encoding='utf-8') as f:
    all_data = json.load(f)

print("=" * 80)
print("全カテゴリのtopic構成")
print("=" * 80)

for i, category in enumerate(all_data):
    cat_name = category['category']
    topics = [item['topic'] for item in category['data']]
    
    print(f"\n【Category {i}】{cat_name} ({len(topics)} topics)")
    print("-" * 80)
    for j, topic in enumerate(topics, 1):
        print(f"  {j:2d}. {topic}")

print("\n" + "=" * 80)
print(f"総カテゴリ数: {len(all_data)}")
print(f"総topic数: {sum(len(cat['data']) for cat in all_data)}")
print("=" * 80)
