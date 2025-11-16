# ホゲーアルゴリズム スマホ版 セットアップ手順

**スマホだけで完結する自動投稿システムの構築方法**

所要時間: 約30分

## 📋 必要なもの

- [ ] LINEアカウント
- [ ] Googleアカウント
- [ ] Xアカウント
- [ ] n8nアカウント（無料プランOK）
- [ ] PC（初回セットアップのみ）

## 🚀 ステップ1: LINE Bot作成（10分）

### 1-1. LINE Developersにログイン

1. https://developers.line.biz/ にアクセス
2. LINEアカウントでログイン
3. 「新規プロバイダー作成」をクリック
4. プロバイダー名: `ホゲーアルゴリズム` と入力

### 1-2. Messaging APIチャネル作成

1. 「新規チャネル作成」→「Messaging API」
2. 以下を入力:
   - チャネル名: `ホゲーBot`
   - チャネル説明: `投稿生成Bot`
   - 大業種/小業種: 適当に選択
   - メールアドレス: 自分のメール
3. 利用規約に同意して作成

### 1-3. 設定

「Messaging API設定」タブで以下を設定:

1. **Webhook URL**: 後でn8nのURLを設定（一旦スキップ）
2. **Webhookの利用**: ON
3. **応答メッセージ**: OFF
4. **Greeting messages**: OFF

### 1-4. アクセストークン取得

1. 「チャネルアクセストークン（長期）」を発行
2. トークンをコピーして保存（後で使用）

### 1-5. 友だち追加

1. QRコードをスマホで読み取り
2. 自分のLINEで友だち追加

## 🔧 ステップ2: n8n セットアップ（10分）

### 2-1. n8nアカウント作成

1. https://n8n.io/ にアクセス
2. 「Start free」をクリック
3. メールアドレスで登録（無料プラン）

### 2-2. 認証情報設定

#### LINE認証

1. n8n左メニュー「Credentials」
2. 「Add Credential」→「LINE」
3. 以下を入力:
   - Credential Name: `LINE Bot`
   - Channel Access Token: 先ほどコピーしたトークン
4. 保存

#### Google Sheets認証

1. 「Add Credential」→「Google Sheets OAuth2 API」
2. 「Connect my account」をクリック
3. Googleアカウントでログイン
4. 権限を許可

#### Twitter認証

1. 「Add Credential」→「Twitter OAuth2 API」
2. 「Connect my account」をクリック
3. Xアカウントでログイン
4. 権限を許可

### 2-3. ワークフローインポート

1. n8n左メニュー「Workflows」
2. 「Import from File」
3. `n8n_workflow_smartphone.json` を選択
4. インポート完了

### 2-4. ワークフロー設定変更

開いたワークフローで以下を修正:

#### Pythonパス設定（3箇所）

ノード「バズ投稿生成」「ストーリー生成」「学習実行」で:

```
変更前: c:\\Repos\\note-articles\\tools\\hogey_algorithm.py
変更後: YOUR_PC_PATH\\hogey_algorithm.py
```

#### Google SheetID設定

ノード「スプレッドシート保存」で:

```
変更前: YOUR_GOOGLE_SHEET_ID
変更後: 実際のSpreadsheet ID（後で取得）
```

#### LINE認証設定

各LINEノードで認証情報を選択:
- 「LINE Bot」を選択

### 2-5. Webhook URL取得

1. 「LINE Webhook」ノードをクリック
2. 「Test URL」をコピー
3. LINE Developersに戻る

### 2-6. LINE Webhook URL設定

1. LINE Developers → Messaging API設定
2. Webhook URL: n8nのURLをペースト
3. 「検証」をクリック（成功を確認）
4. 保存

## 📊 ステップ3: Google スプレッドシート作成（5分）

### 3-1. スプレッドシート作成

1. https://sheets.google.com/ にアクセス
2. 新規スプレッドシート作成
3. 名前: `ホゲーアルゴリズム投稿管理`

### 3-2. シート構成

「投稿管理」シートに以下の列を作成:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| post_id | text | theme | education_type | 投稿 | scheduled_datetime | likes | retweets |

### 3-3. Spreadsheet ID取得

URLから取得:
```
https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
                                      ↑ここをコピー
```

### 3-4. n8nに設定

1. n8nワークフローに戻る
2. 「スプレッドシート保存」ノード
3. `YOUR_GOOGLE_SHEET_ID` を実際のIDに変更
4. 保存

## ✅ ステップ4: 動作確認（5分）

### 4-1. n8nワークフロー有効化

1. ワークフロー右上の「Active」をON
2. 保存

### 4-2. LINEで動作確認

スマホのLINEで友だち追加したBotに送信:

```
生成 3 貧乏脱出
```

**期待される動作**:
1. 数秒待つ
2. Botから投稿が返信される
3. ボタンが表示される

### 4-3. エラーが出た場合

n8nの「Executions」でログ確認:

**よくあるエラー**:

1. **Pythonが実行できない**
   - n8nからPCへのアクセス権限確認
   - Pythonパスが正しいか確認

2. **LINE返信がない**
   - Webhook URLが正しいか確認
   - n8nワークフローがActiveか確認

3. **認証エラー**
   - 各APIの認証情報を再確認

## 🎯 ステップ5: スマホからテスト

### 5-1. 基本コマンド

```
生成 5 人生逆転
```

→ 5件の投稿が生成される

### 5-2. ボタン操作

返信された投稿で:

1. 「この投稿をXに投稿」タップ → 即座にX投稿
2. 「スプレッドシートに保存」タップ → 後で投稿可能
3. 「次の投稿を見る」タップ → 次の案を表示

### 5-3. スプレッドシートから投稿

1. スマホでGoogle スプレッドシートアプリを開く
2. 「ホゲーアルゴリズム投稿管理」を開く
3. 投稿したい行の「投稿」列に `○` を入力
4. 10分以内に自動投稿される

## 🔄 ステップ6: 自動化設定（オプション）

### 6-1. 毎朝自動生成

n8nで新規ワークフロー作成:

```json
{
  "nodes": [
    {
      "name": "Schedule",
      "type": "scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{
            "field": "cronExpression",
            "expression": "0 7 * * *"
          }]
        }
      }
    },
    {
      "name": "Python実行",
      "type": "executeCommand",
      "parameters": {
        "command": "python",
        "arguments": "hogey_algorithm.py --count 3 --json"
      }
    },
    {
      "name": "LINE通知",
      "type": "line",
      "parameters": {
        "resource": "notification",
        "message": "🐶 今日の投稿案が届きました！"
      }
    }
  ]
}
```

設定:
- 毎朝7時に3件生成
- LINEで通知
- スプレッドシートに自動保存

### 6-2. 曜日別テーマ自動化

Functionノードに追加:

```javascript
const themes = {
  0: '時間の使い方',     // 日曜
  1: 'ギャンブル依存',   // 月曜
  2: 'ブラック企業',     // 火曜
  3: '無駄遣い',         // 水曜
  4: 'SNS依存',          // 木曜
  5: '疲労',             // 金曜
  6: '人間関係'          // 土曜
};
const today = new Date().getDay();
return { json: { theme: themes[today] } };
```

### 6-3. スプレッドシート監視自動投稿

n8nで新規ワークフロー作成:

```
Schedule(10分毎)
→ Google Sheets読込
→ 「投稿」列が○の行を抽出
→ X投稿
→ 「投稿」列を「完了」に更新
```

## 📱 日常の使い方

### 通勤中

```
生成 3 副業
```

→ スマホで確認 → 気に入った投稿をタップで即投稿

### 昼休み

1. Google スプレッドシートアプリで投稿案確認
2. テキスト編集（微調整）
3. 「投稿」列に○

### 夜

```
学習
```

→ その日の反応を学習して次回に反映

## 🎨 便利なコマンド

```
生成 5 貧乏脱出       # 5件生成
ストーリー 人生逆転    # 3部作生成
今日 3                # 曜日別テーマで3件
学習                  # CSV学習実行
状態                  # 今日の状況確認
```

## 🔐 セキュリティ設定（推奨）

### LINE User ID制限

1. LINEで自分のUser IDを確認:
   - Botに「ユーザーID」と送信
   - n8nのログで確認

2. n8nワークフロー「コマンド解析」を編集:

```javascript
const allowedUsers = ['YOUR_USER_ID'];
const userId = event.source.userId;

if (!allowedUsers.includes(userId)) {
  return {
    json: {
      error: 'Unauthorized',
      message: '認証エラー'
    }
  };
}
```

## 📈 データ蓄積方法

### 手動でCSV追加

1. 自分の投稿を `my_posts.csv` に追加:
   ```csv
   post_id,text,datetime,likes,retweets,comments
   1,"投稿本文",2025-11-08 12:00,150,30,5
   ```

2. 参考アカウントを `bench_posts.csv` に追加

3. LINEで `学習` コマンド実行

### X API自動取得（上級）

n8nで別ワークフロー作成:
- 毎日1回実行
- X APIで自分の投稿を取得
- Google Sheetsに自動追記
- 学習実行

## 🆘 トラブルシューティング

### Q: LINEが反応しない

A: 以下を確認:
1. n8nワークフローがActive
2. Webhook URLが正しい
3. LINE Bot設定でWebhook ON

### Q: Pythonが実行できない

A: 
1. n8nがPCにアクセスできるか確認
2. ローカルn8nの場合、パス設定確認
3. クラウドn8nの場合、Execute Commandは使えない
   → Python Anywhereなどを併用

### Q: 投稿が生成されない

A:
1. n8nの実行ログを確認
2. Pythonのエラーメッセージを確認
3. hogey_algorithm.pyが最新か確認

## 🎉 完成！

これでスマホだけで完結するホゲーアルゴリズムが完成しました。

**通勤中でも、布団の中でも、投稿生成→確認→投稿まで完結。**

---

次のステップ:
1. ✅ 1週間使ってデータ蓄積
2. ✅ 反応の良い投稿パターンを確認
3. ✅ 学習を回して精度向上
4. ✅ 自動化を強化

質問があれば `SMARTPHONE_GUIDE.md` を参照してください。
