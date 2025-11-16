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


def _ensure_table(conn: sqlite3.Connection) -> None:
    """Create user_states table if missing."""
    conn.execute(
        (
            "CREATE TABLE IF NOT EXISTS user_states ("
            "user_id TEXT PRIMARY KEY,"
            "state TEXT,"
            "count INTEGER,"
            "theme TEXT,"
            "posts_data TEXT,"
            "current_index INTEGER,"
            "type TEXT,"
            "updated_at TEXT)"
        )
    )


def get_user_state(user_id: str) -> dict:
    """ユーザーの状態を取得"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    _ensure_table(conn)

    cursor.execute(
        (
            "SELECT state, count, theme, posts_data, current_index, type "
            "FROM user_states WHERE user_id = ?"
        ),
        (user_id,),
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
    # 初期レコードを挿入
    update_user_state(user_id, state="idle", current_index=0)
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
    _ensure_table(conn)

    cursor.execute("SELECT 1 FROM user_states WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()

    # Filter allowed columns
    allowed = {}
    for k, v in kwargs.items():
        if k in [
            "state",
            "count",
            "theme",
            "posts_data",
            "current_index",
            "type",
        ]:
            allowed[k] = v

    # Auto-reset current_index when posts_data is empty/null
    posts_data_value = allowed.get("posts_data")
    is_empty_posts = (
        posts_data_value is None
        or posts_data_value == ""
        or (
            isinstance(posts_data_value, str)
            and posts_data_value.strip() in ("[]", "null", "")
        )
    )
    if "posts_data" in allowed and is_empty_posts:
        # Force reset (override any existing value)
        allowed["current_index"] = 0

    if (
        allowed.get("state") in {"idle", "initial"}
        and "current_index" not in allowed
    ):
        allowed["current_index"] = 0

    if exists:
        if allowed:
            set_parts = [f"{k} = ?" for k in allowed.keys()]
            set_parts.append("updated_at = ?")
            values = list(allowed.values()) + [
                datetime.now().isoformat(),
                user_id,
            ]
            sql = (
                "UPDATE user_states SET "
                + ", ".join(set_parts)
                + " WHERE user_id = ?"
            )
            cursor.execute(sql, values)
    else:
        insert_values = (
            user_id,
            allowed.get("state", "idle"),
            allowed.get("count"),
            allowed.get("theme"),
            allowed.get("posts_data"),
            allowed.get("current_index", 0),
            allowed.get("type"),
            datetime.now().isoformat(),
        )
        # Break SQL into concatenated parts to satisfy line-length rules
        sql_insert = (
            "INSERT INTO user_states ("
            + "user_id, state, count, theme, posts_data, "
            + "current_index, type, updated_at) VALUES (?,?,?,?,?,?,?,?)"
        )
        cursor.execute(sql_insert, insert_values)

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
