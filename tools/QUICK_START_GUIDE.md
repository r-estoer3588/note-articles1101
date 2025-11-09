# 🚀 ホゲーアルゴリズム LINE Bot 実践セットアップガイド

**実際に動かすための具体的な手順書**

作成日: 2025年11月8日  
所要時間: 40-50分  
難易度: ★★★☆☆

---

## 📋 事前チェックリスト

作業を始める前に、以下を確認してください：

- [ ] Pythonがインストール済み（`python --version`で確認）
- [ ] pandasがインストール済み（`pip show pandas`で確認）
- [ ] `hogey_algorithm.py` が動作する（テスト実行済み）
- [ ] LINEアカウント（個人用）
- [ ] Googleアカウント
- [ ] PCでの作業環境（最初の設定のみ）

---

## 🎯 PHASE 1: LINE Developers設定（15分）

### ステップ1-1: プロバイダー作成

1. **LINE Developers Console** にアクセス
   ```
   https://developers.line.biz/console/
   ```

2. **ログイン**（LINEアカウントで）

3. **プロバイダー作成**
   - 「作成」ボタンをクリック
   - プロバイダー名: `ホゲーBot開発` （任意）
   - 作成ボタン

### ステップ1-2: Messaging APIチャネル作成

1. 作成したプロバイダーを選択

2. **新規チャネル作成** → **Messaging API**

3. チャネル情報入力:
   ```
   チャネル名: ホゲーアルゴリズムBot
   チャネル説明: X投稿自動生成Bot
   大業種: 個人
   小業種: 個人（その他）
   メールアドレス: （あなたのメアド）
   ```

4. 利用規約に同意して **作成**

### ステップ1-3: チャネル設定

作成したチャネルの **Messaging API設定** タブで：

#### A. Webhook設定
```
Webhook URL: （後で設定）
Webhookの利用: オン
```

#### B. 応答設定
```
応答メッセージ: オフ
あいさつメッセージ: オフ
Webhook: オン
```

#### C. チャネルアクセストークン発行
1. **チャネルアクセストークン（長期）** セクション
2. **発行** ボタンをクリック
3. 表示されたトークンをコピー
   ```
   例: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
4. **メモ帳に保存**（後で使います）

#### D. チャネルシークレット取得
1. **チャネル基本設定** タブ
2. **チャネルシークレット** をコピー
3. **メモ帳に保存**

- [ ] チャネルアクセストークン取得完了
- [ ] チャネルシークレット取得完了

---

## 📊 PHASE 2: Google Sheets設定（10分）

### ステップ2-1: スプレッドシート作成

1. **Google Sheets** にアクセス
   ```
   https://docs.google.com/spreadsheets/
   ```

2. **新規作成** → 空白のスプレッドシート

3. タイトル変更: `ホゲーアルゴリズム管理`

### ステップ2-2: シート1設定（ユーザー状態管理）

1. シート名を `ユーザー状態管理` に変更

2. A1セルから以下を入力:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| user_id | state | count | theme | posts_data | current_index | updated_at | type |

3. **フォーマット設定**:
   - 1行目を太字
   - 背景色を薄い青に設定
   - テキストを中央揃え

### ステップ2-3: シート2設定（投稿保存用）

1. **シート追加** （下部の+ボタン）

2. シート名: `投稿データ`

3. ヘッダー行:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| post_id | text | theme | education_type | created_at | posted | posted_at |

### ステップ2-4: スプレッドシートID取得

URLから取得:
```
https://docs.google.com/spreadsheets/d/【ここがID】/edit
例: 1A2B3C4D5E6F7G8H9I0J
```

**メモ帳に保存**: `SHEET_ID: 1A2B3C4D5E6F7G8H9I0J`

### ステップ2-5: サービスアカウント作成

1. **Google Cloud Console** にアクセス
   ```
   https://console.cloud.google.com/
   ```

2. **新しいプロジェクト** 作成
   ```
   プロジェクト名: HogeyBot
   ```

3. プロジェクトを選択

4. **APIとサービス** → **認証情報**

5. **認証情報を作成** → **サービスアカウント**
   ```
   名前: hogey-bot-service
   説明: LINE Bot用サービスアカウント
   ```

6. **キーを作成** → **JSON** を選択

7. JSONファイルがダウンロードされる
   ```
   例: hogeybotxxxxxx-xxxxxxxx.json
   ```

8. このJSONファイルを `c:\Repos\note-articles\tools\` に保存
   ```
   保存先: c:\Repos\note-articles\tools\google-service-account.json
   ```

### ステップ2-6: Sheetsに共有設定

1. JSONファイルを開く

2. `client_email` の値をコピー
   ```
   例: hogey-bot-service@hogeybotxxxxxx.iam.gserviceaccount.com
   ```

3. Google Sheetsに戻る

4. **共有** ボタン → メールアドレスを貼り付け

5. 権限: **編集者** に設定

6. **送信**（通知なしでOK）

### ステップ2-7: Google Sheets API有効化

1. Google Cloud Console → **APIとサービス** → **ライブラリ**

2. 検索: `Google Sheets API`

3. **有効にする**

- [ ] スプレッドシート作成完了
- [ ] サービスアカウント設定完了
- [ ] API有効化完了

---

## 🎨 PHASE 3: リッチメニュー画像作成（10分）

### ステップ3-1: HTMLファイルで画像生成

1. **rich_menu_template.html** をブラウザで開く
   ```powershell
   cd c:\Repos\note-articles\tools
   start rich_menu_template.html
   ```

2. ブラウザで開いたら **F12** を押す（開発者ツール）

3. **Ctrl + Shift + M** でデバイスモードに切り替え

4. **Dimensions** を `2500 x 1686` に設定

5. 画面いっぱいにメニューが表示されたら **スクリーンショット**
   - Windows: `Win + Shift + S` でスニッピングツール
   - または開発者ツールの「Capture screenshot」機能

6. 画像を保存: `rich_menu.png`

### ステップ3-2: リッチメニュー登録

1. LINE Developers Console → チャネル → **Messaging API設定**

2. **リッチメニュー** タブ → **作成**

3. 基本設定:
   ```
   タイトル: ホゲーメニュー
   表示期間: 常に表示
   メニューバーのテキスト: メニュー
   ```

4. テンプレート選択:
   ```
   大テンプレート
   6分割（2列×3行）
   ```

5. 画像アップロード:
   - `rich_menu.png` をアップロード

6. アクション設定（タップ領域ごと）:

   | 位置 | タイプ | テキスト | 説明 |
   |------|--------|----------|------|
   | A（左上） | テキスト | `menu:generate` | 投稿生成 |
   | B（右上） | テキスト | `menu:trilogy` | 3部作 |
   | C（左中） | テキスト | `menu:today` | 今日のテーマ |
   | D（右中） | テキスト | `menu:learn` | 学習実行 |
   | E（左下） | テキスト | `menu:status` | 状態確認 |
   | F（右下） | テキスト | `menu:help` | ヘルプ |

7. **保存**

8. 作成されたメニューの **公開** ボタンをクリック

- [ ] リッチメニュー画像作成完了
- [ ] リッチメニュー登録・公開完了

---

## 🔧 PHASE 4: n8n設定（15分）

### ステップ4-1: n8nインストール（未インストールの場合）

```powershell
# Node.jsが必要（未インストールの場合）
# https://nodejs.org/ からダウンロード

# n8nインストール
npm install -g n8n
```

### ステップ4-2: n8n起動

```powershell
# n8n起動
n8n start

# または
npx n8n
```

ブラウザで自動的に開く: http://localhost:5678

### ステップ4-3: 初回セットアップ

初回起動時:
1. アカウント作成
   ```
   メールアドレス: （任意）
   パスワード: （任意）
   ```

2. ログイン

### ステップ4-4: ワークフローインポート

1. 左メニュー → **Workflows**

2. 右上の **Import from File** （または **+ Add workflow** → **Import**）

3. `n8n_workflow_menu_complete.json` を選択

4. ワークフローが読み込まれる

### ステップ4-5: 認証情報設定

#### Google Sheets認証

1. **ユーザー状態取得** ノードをクリック

2. **Credentials** → **+ Create New**

3. **Credential Type**: Google Sheets Service Account

4. **Service Account Email** と **Private Key** を入力:
   - `google-service-account.json` ファイルを開く
   - `client_email` をコピー → Service Account Email に貼り付け
   - `private_key` をコピー → Private Key に貼り付け

5. **Save**

#### 同じ認証情報を他のGoogle Sheetsノードにも適用

- **ユーザー状態更新** ノード
- その他のGoogle Sheetsノード

### ステップ4-6: 設定値の更新

以下のノードで実際の値に置き換え:

#### 1. ユーザー状態取得ノード
```javascript
sheetId: "YOUR_SHEET_ID"
↓
sheetId: "実際のスプレッドシートID"
```

#### 2. ユーザー状態更新ノード
```javascript
sheetId: "YOUR_SHEET_ID"
↓
sheetId: "実際のスプレッドシートID"
```

#### 3. LINE返信ノード
```javascript
Authorization: "Bearer YOUR_CHANNEL_ACCESS_TOKEN"
↓
Authorization: "Bearer 実際のチャネルアクセストークン"
```

#### 4. Python実行ノード
```javascript
command: "cd c:\\Repos\\note-articles\\tools && python hogey_algorithm.py ..."
```
パスが正しいか確認（必要に応じて変更）

### ステップ4-7: Webhook URL取得

1. **LINE Webhook** ノードをクリック

2. **Webhook URL** が表示される
   ```
   例: http://localhost:5678/webhook/hogey-bot
   ```

3. このURLをコピー

4. LINE Developers Console → **Messaging API設定** → **Webhook URL** に貼り付け

5. **検証** ボタンをクリック（成功すればOK）

### ステップ4-8: ワークフロー有効化

1. n8nの右上 **Inactive** を **Active** に切り替え

2. 緑色になれば有効化成功

- [ ] n8nインストール完了
- [ ] ワークフローインポート完了
- [ ] 認証情報設定完了
- [ ] Webhook URL設定完了
- [ ] ワークフロー有効化完了

---

## 🧪 PHASE 5: 動作確認（10分）

### ステップ5-1: Bot友だち追加

1. LINE Developers Console → **Messaging API設定**

2. **QRコード** をスマホでスキャン

3. 友だち追加

### ステップ5-2: リッチメニュー確認

スマホのLINEアプリで:
1. Botのトーク画面を開く
2. 画面下部にリッチメニューが表示されているか確認

### ステップ5-3: 基本動作テスト

#### テスト1: ヘルプ表示
1. **❓ヘルプ** をタップ
2. 使い方が表示される → ✅

#### テスト2: 投稿生成（完全フロー）
1. **📝投稿生成** をタップ
2. 「何件生成しますか？」表示 → **3件** をタップ
3. 「テーマを選んでください」表示 → **💼副業** をタップ
4. ⏳ 生成中メッセージ表示
5. 投稿1/3 が表示される
6. **➡️次へ** をタップ → 投稿2/3 表示
7. **➡️次へ** をタップ → 投稿3/3 表示

**期待される結果**:
- 各ステップでボタンが表示される
- 投稿が正しくフォーマットされている
- プログレスバーが表示される

#### テスト3: 今日のテーマ
1. **📚今日** をタップ
2. 今日の曜日に応じたテーマが表示される
3. **5件** をタップ
4. 投稿が生成される

#### テスト4: エラーハンドリング
1. トーク画面に適当な文字を入力（例: `あいうえお`）
2. 「メニューから操作してください」的なメッセージが返る

### ステップ5-4: ログ確認

n8nの管理画面で:
1. **Executions** タブ
2. 実行履歴が表示される
3. エラーがないか確認

---

## 🎉 完成！

すべてのテストが成功したら、ボタン操作だけで使えるLINE Botの完成です！

### 使い方のおさらい

```
[リッチメニュー]
  ↓ タップ
[件数選択] 3件/5件/10件/20件
  ↓ タップ
[テーマ選択] 💰貧乏脱出/💼副業/...
  ↓ タップ
⏳ 生成中...
  ↓
🐶 投稿1/5 表示
  ↓
[🚀 X投稿] [💾 保存] [➡️ 次へ] [🗑️ 破棄]
```

**コマンド不要。全てボタンで完結。**

---

## 📱 日常の使い方

### 平日の朝（通勤中）
1. LINEを開く
2. **📚今日** をタップ
3. **10件** をタップ
4. 生成された投稿を確認
5. 気に入ったものを **💾保存**

### 帰宅後（PCで）
1. Google Sheetsを開く
2. 保存した投稿を確認
3. 予約投稿設定

### 週末（学習）
1. **🎓学習** をタップ
2. 確認して実行
3. 最新のトレンドを学習

---

## 🆘 トラブルシューティング

### ボタンが表示されない
```
原因: リッチメニューが公開されていない
対処: LINE Developers Consoleでリッチメニューを公開
```

### 生成されない
```
原因1: n8nが起動していない
対処: PowerShellで `n8n start`

原因2: Pythonパスが間違っている
対処: n8nのPython実行ノードでパス確認

原因3: Google Sheets権限エラー
対処: サービスアカウントのメアドをSheets共有に追加
```

### Webhook URLエラー
```
原因: ローカルホストは外部からアクセスできない
対処: 
  方法1: ngrokを使う（開発用）
  方法2: VPSにn8nをデプロイ（本番用）
```

#### ngrokの使い方（開発用）
```powershell
# ngrokインストール
# https://ngrok.com/ からダウンロード

# 起動
ngrok http 5678

# 表示されたURLをWebhook URLに設定
# 例: https://xxxx-xxx-xxx-xxx.ngrok-free.app/webhook/hogey-bot
```

### タイムアウトする
```
原因: 生成に時間がかかる
対処: n8nの設定でタイムアウトを延長
  Settings → Timeout → 300秒に設定
```

---

## 📚 次のステップ（オプション）

### X (Twitter) 投稿機能追加
1. X Developer Portalでアプリ作成
2. APIキー取得
3. n8nに「X投稿」ノード追加
4. `action=post` 時に実行

### 自動学習設定
1. n8nで「Cron」ノード追加
2. 毎日2:00 AMに実行設定
3. CSV学習を自動実行

### VPSデプロイ（24時間稼働）
1. VPS契約（さくら、AWS、など）
2. n8nをDockerでデプロイ
3. ドメイン設定
4. SSL証明書設定

---

## 📝 メモ欄

**あなたの設定情報**:

```
チャネルアクセストークン: _______________________
チャネルシークレット: _______________________
スプレッドシートID: _______________________
Webhook URL: _______________________
サービスアカウントメール: _______________________
```

---

**作成日**: 2025年11月8日  
**バージョン**: 1.0  
**次回更新予定**: 機能追加時

完成おめでとうございます！🎉
