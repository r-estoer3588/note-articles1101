# Threads API セットアップ完了プロンプト

## 🎯 目的
レス卒先輩の21days自動投稿キャンペーンの投稿パフォーマンスを分析し、22日目以降の投稿品質を改善するため、Threads APIを連携する。

## 📋 現在の状況
- ✅ Meta Developer アカウント作成済み
- ✅ ビジネスポートフォリオ「レス卒先輩分析ツール」作成済み
- ⏳ **次のステップ**: アプリにThreads APIを追加

## 🔧 実行すべき作業

### Step 1: アプリダッシュボードに移動
1. https://developers.facebook.com/apps/ を開く
2. 作成したアプリをクリック

### Step 2: Threads APIを追加
1. アプリダッシュボードで「プロダクトを追加」をクリック
2. 「Threads API」を見つけて「設定」をクリック
3. 「Get Started」または「開始する」をクリック

### Step 3: アクセストークン取得
1. Threads API > Settings または クイックスタートに移動
2. 「User Access Token Generator」または「アクセストークン生成」を探す
3. 必要なスコープを選択:
   - `threads_basic` (基本情報取得)
   - `threads_manage_insights` (投稿分析用)
4. 「Generate Token」をクリック
5. **レス卒先輩のThreadsアカウントでログイン・認証**

### Step 4: トークンとユーザーIDを環境変数に設定
取得したトークンを以下のファイルに追加:
```bash
# c:\Repos\note-articles\tools\.env に追加
THREADS_ACCESS_TOKEN=取得したアクセストークン
THREADS_USER_ID=取得したユーザーID
```

### Step 5: 分析ツール実行
```bash
# PowerShell で実行
cd c:\Repos\note-articles\tools
python threads_performance_analyzer.py --analyze --learn
```

## 🎯 期待される結果
1. 過去15日間の投稿データを取得
2. 100閲覧以上・いいね獲得投稿を特定
3. 高パフォーマンス投稿のパターンを分析
4. 22日目以降の投稿改善プロンプトを生成

## 🚨 重要ポイント
- **Threadsアカウント**: 必ず「レス卒先輩」のアカウントで認証すること
- **スコープ権限**: 投稿データ取得には `threads_manage_insights` が必須
- **トークン管理**: 60日で期限切れするため、長期トークンに変換推奨

---
**現在地**: ビジネスポートフォリオ作成完了  
**次のアクション**: アプリダッシュボードでThreads API追加

実行してください！