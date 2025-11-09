#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Bot State Manager using SQLite
ユーザーの状態をSQLiteで管理
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "line_bot_states.db"


def get_user_state(user_id: str) -> dict:
    """ユーザーの状態を取得"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT state, count, theme, posts_data, current_index, type FROM user_states WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "user_id": user_id,
            "state": row[0] or "idle",
            "count": row[1],
            "theme": row[2],
            "posts_data": row[3],
            "current_index": row[4] or 0,
            "type": row[5]
        }
    else:
        # 新規ユーザー
        return {
            "user_id": user_id,
            "state": "idle",
            "count": None,
            "theme": None,
            "posts_data": None,
            "current_index": 0,
            "type": None
        }


def update_user_state(user_id: str, **kwargs) -> dict:
    """ユーザーの状態を更新"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 既存レコードがあるか確認
    cursor.execute("SELECT 1 FROM user_states WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()
    
    if exists:
        # UPDATE
        set_parts = []
        values = []
        for key, value in kwargs.items():
            if key in ["state", "count", "theme", "posts_data", "current_index", "type"]:
                set_parts.append(f"{key} = ?")
                values.append(value)
        
        if set_parts:
            set_parts.append("updated_at = ?")
            values.append(datetime.now().isoformat())
            values.append(user_id)
            
            sql = f"UPDATE user_states SET {', '.join(set_parts)} WHERE user_id = ?"
            cursor.execute(sql, values)
    else:
        # INSERT
        columns = ["user_id"] + list(kwargs.keys())
        placeholders = ["?"] * len(columns)
        values = [user_id] + list(kwargs.values())
        
        sql = f"INSERT INTO user_states ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        cursor.execute(sql, values)
    
    conn.commit()
    conn.close()
    
    return get_user_state(user_id)


def reset_user_state(user_id: str):
    """ユーザーの状態をリセット"""
    return update_user_state(
        user_id,
        state="idle",
        count=None,
        theme=None,
        posts_data=None,
        current_index=0,
        type=None
    )


if __name__ == "__main__":
    # テスト
    test_user = "test_user_123"
    
    print("1. 初期状態取得:")
    state = get_user_state(test_user)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    
    print("\n2. 状態更新:")
    state = update_user_state(test_user, state="waiting_count", count=5)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    
    print("\n3. テーマ追加:")
    state = update_user_state(test_user, theme="ビジネス", state="waiting_theme")
    print(json.dumps(state, ensure_ascii=False, indent=2))
    
    print("\n4. リセット:")
    state = reset_user_state(test_user)
    print(json.dumps(state, ensure_ascii=False, indent=2))
