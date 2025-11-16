#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Bot State Manager API
n8nから呼び出すためのローカルAPIサーバー
"""

from flask import Flask, request, jsonify
from line_bot_state_manager import get_user_state, update_user_state, reset_user_state

app = Flask(__name__)

@app.route('/api/state/<user_id>', methods=['GET'])
def get_state(user_id):
    """ユーザー状態取得"""
    try:
        state = get_user_state(user_id)
        return jsonify(state)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/state/<user_id>', methods=['POST'])
def update_state(user_id):
    """ユーザー状態更新"""
    try:
        data = request.json
        state = update_user_state(user_id, **data)
        return jsonify(state)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/state/<user_id>/reset', methods=['POST'])
def reset_state(user_id):
    """ユーザー状態リセット"""
    try:
        state = reset_user_state(user_id)
        return jsonify(state)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """ヘルスチェック"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5679, debug=False)
