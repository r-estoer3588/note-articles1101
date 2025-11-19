# 錬金王スタイル記事リライトツール
# Articles 1-7の共通構造を使用してリライト

param(
    [Parameter(Position=0)]
    [string]$File,
    
    [Parameter()]
    [switch]$Help,
    
    [Parameter()]
    [switch]$Template,
    
    [Parameter()]
    [switch]$Examples,
    
    [Parameter()]
    [ValidateSet('1', '2', '3', 'universal')]
    [string]$Pattern = 'universal',
    
    [Parameter()]
    [switch]$ShowPrompt
)

$ErrorActionPreference = "Stop"

# ヘルプ表示
if ($Help) {
    Write-Host @"

🔱 錬金王スタイル記事リライトツール
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 使い方:
  renkin <ファイルパス>              記事をリライト（対話式）
  renkin -Template                   テンプレート構造を表示
  renkin -Examples                   応用例を表示
  renkin -Pattern <番号>             特定パターンで生成
  renkin -ShowPrompt                 プロンプトファイルを開く

🎨 パターン:
  1 = 外側の仕組み暴露型（Articles 1, 3, 4）
  2 = 内側の仕組み暴露型（Articles 2, 5）
  3 = 統合型（Articles 6, 7）
  universal = 汎用テンプレート（デフォルト）

📝 7つのPhase構造:
  Phase 1: 衝撃的オープニング（常識の破壊）
  Phase 2: 共感（読者の現状を言語化）
  Phase 3: 構造の暴露（3層構造で可視化）
  Phase 4: 絶望の提示（逃げ場のなさ）
  Phase 5: 希望の光（視点の転換）
  Phase 6: 解決策の提示（具体的な行動）
  Phase 7: 次回予告とCTA（期待値の最大化）

💡 使用例:
  renkin articles/my-article.md      # 記事をリライト
  renkin -Template                   # テンプレート確認
  renkin -Pattern 1                  # パターン1で生成
  renkin -Examples                   # 応用例を見る

🔑 キーフレーズ:
  「意味がわかりますか？」「違います」「やばすぎませんか？？？」
  「無理です」「.… .… .…」「…それでも」

📚 参考:
  プロンプト: prompt/note_renkinou_universal_template.md
  個別記事: prompt/note_renkinou_1.md ～ note_renkinou_7.md

"@ -ForegroundColor Cyan
    return
}

# プロンプトファイルを開く
if ($ShowPrompt) {
    $promptPath = Join-Path $PSScriptRoot "prompt\note_renkinou_universal_template.md"
    if (Test-Path $promptPath) {
        code $promptPath
        Write-Host "✅ プロンプトファイルを開きました: $promptPath" -ForegroundColor Green
    } else {
        Write-Host "❌ プロンプトファイルが見つかりません: $promptPath" -ForegroundColor Red
    }
    return
}

# テンプレート構造を表示
if ($Template) {
    Write-Host @"

🔱 錬金王スタイル 7つのPhase構造
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Phase 1: 衝撃的オープニング
   → 常識を疑わせ、「え？」という状態にする
   
   [衝撃的な問いかけ/断言]
   あなたは[誤解している状態]。
   いや、もっと正確に言うと。
   [さらに衝撃的な真実]。
   
   [衝撃的な数字] = [衝撃的な数字]
   この式、意味がわかりますか？

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟠 Phase 2: 共感
   → 「この人は私のことを分かってる」と思わせる
   
   あなたは[努力している]。
   なのに、[望む結果が出ていない]
   
   なぜでしょう？
   [誤解1]？　違います。
   [誤解2]？　それも違います。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟡 Phase 3: 構造の暴露
   → 見えなかった支配構造を見せる
   
   [対象]は3つの層で動いている。
   
   第1層：[日常レベルの仕組み]
   第2層：[支配者レベルの仕組み]
   第3層：[常識レベルの仕組み]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 Phase 4: 絶望の提示
   → 構造から逃れられないことを理解させる
   
   ここで思いませんか？
   「じゃあ、[逃避行動]すればいい」
   
   無理です。
   
   .… .… .…
   いいえ。何も変わってません。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔵 Phase 5: 希望の光
   → 絶望から希望へ転換し、解決策の存在を示す
   
   しかし、この不都合な世界の真実が見えた時点で、
   あなたは、もう「[支配される側]」だけではなくなってます。
   
   …それでも。まだ抗うというのなら。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟣 Phase 6: 解決策の提示
   → 何をすればいいか明確に示す
   
   唯一の方法は…
   「[解決策1]」と「[解決策2]」です。
   
   私がやったのは、この2つだけ。
   
   実はまだ「入口」なんですよね。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟤 Phase 7: 次回予告とCTA
   → 次回への期待値を作り、今すぐ行動させる
   
   [衝撃的な事例]
   知ってます？
   答えは… [シンプルな原因]です
   
   本質はその下にある「○○」ですよ。
   
   これは[テーマ]に抗う者たちの魂の聖火リレーです。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"@ -ForegroundColor Cyan
    return
}

# 応用例を表示
if ($Examples) {
    Write-Host @"

🎯 錬金王スタイル 応用例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 例1: 副業で稼げない人向け
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1 (オープニング):
  あなたは騙されています。
  
  月5万円 ＝ 年間60万円
  
  この式、意味がわかりますか？
  多くの人が「副業で月5万」を目標にします。
  でも、その60万円、誰の懐に入るか知ってますか？

Phase 2 (共感):
  あなたは頑張ってる。
  
  毎日副業してますよね
  スキルアップもしてる。SNS発信もやってる。
  
  でも、稼げない。
  
  なぜでしょう？
  努力が足りない？　違います。
  やり方が悪い？　それも違います。

Phase 3 (構造):
  副業の世界は3つの層で動いている。
  
  第1層：プラットフォームの手数料
  - note → 10-15%
  - Brain → 12-24%
  - Kindle → 35-70%
  
  第2層：広告費の中抜き
  - Google広告 → 32%が中抜き
  - Facebook広告 → 平均30%
  
  第3層：「副業=小遣い稼ぎ」の常識
  - 学校は教えない
  - 会社は推奨しない
  - メディアは「月5万」を刷り込む

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 例2: ダイエットが続かない人向け
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1 (オープニング):
  あなたは操られています。
  
  100万円 = 1kg
  
  この式、意味がわかりますか？
  
  日本のダイエット市場は年間1兆円。
  国民の半数がダイエット経験者。
  
  つまり、1人が1kg痩せるために
  平均100万円が市場に流れているんです。
  
  でも、リバウンド率は95%。
  
  印刷ミスじゃありません。

Phase 2 (共感):
  あなたは頑張ってる。
  
  糖質制限もやってる。
  ジムにも通ってる。
  YouTubeの筋トレ動画も見てる。
  
  でも、痩せない。続かない。
  
  なぜでしょう？
  意志が弱い？　違います。
  知識が足りない？　それも違います。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 あなたのテーマで試してみましょう！

"@ -ForegroundColor Cyan
    return
}

# ファイルが指定されていない場合
if (-not $File) {
    Write-Host @"

🔱 錬金王スタイル記事リライトツール
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使い方: renkin <ファイルパス>

例:
  renkin articles/my-article.md
  renkin -Template
  renkin -Examples
  renkin -Help

"@ -ForegroundColor Yellow
    return
}

# ファイルの存在確認
if (-not (Test-Path $File)) {
    Write-Host "❌ ファイルが見つかりません: $File" -ForegroundColor Red
    return
}

Write-Host @"

🔱 錬金王スタイル記事リライト開始
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 対象ファイル: $File
🎨 パターン: $Pattern

"@ -ForegroundColor Cyan

# 記事を読み込み
$content = Get-Content $File -Raw -Encoding UTF8

Write-Host "📖 記事を読み込みました（$($content.Length) 文字）`n" -ForegroundColor Green

# パターン別のガイド
$patternGuide = switch ($Pattern) {
    '1' {
        @"
📐 パターン1: 外側の仕組み暴露型
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
オープニング: 所有/流れ/演出の本質
↓
共感: お金が残らない現実
↓
構造: プラットフォーム/税/手数料
↓
絶望: 逃げられない理由
↓
希望: 所有する側に回る方法
↓
解決策: マーケティング学習
↓
次回: さらに深い層へ
"@
    }
    '2' {
        @"
📐 パターン2: 内側の仕組み暴露型
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
オープニング: 認知の歪み/生きること=マーケティング
↓
共感: 思い通りに動かされている
↓
構造: 錯覚/心理トリック/4工程
↓
絶望: 無意識に操られている
↓
希望: 仕組みを理解すれば使える
↓
解決策: マーケティングの4工程
↓
次回: Stage 2へ
"@
    }
    '3' {
        @"
📐 パターン3: 統合型
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
警告: 衝撃的な内容
↓
オープニング: 26人=38億人
↓
共感: 頑張ってるのに金持ちになれない
↓
3層構造: 監視/金融/常識
↓
絶望の極限: AIの未来予測、抵抗も無駄
↓
壊すべきは内側: 10の固定概念
↓
希望: 自分経済圏
↓
解決策: 3つの戦略（概要）
↓
次回: 個人ファンド（核心）
"@
    }
    default {
        @"
📐 汎用テンプレート（7つのPhase）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 1: 衝撃的オープニング
Phase 2: 共感
Phase 3: 構造の暴露
Phase 4: 絶望の提示
Phase 5: 希望の光
Phase 6: 解決策の提示
Phase 7: 次回予告とCTA
"@
    }
}

Write-Host $patternGuide -ForegroundColor Cyan
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

# 対話式でテーマ設定
Write-Host "📝 リライトのテーマ設定" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Yellow

$theme = Read-Host "テーマ（例: 副業で稼げない理由）"
$enemy = Read-Host "敵・障害（例: プラットフォーム手数料、常識）"
$goal = Read-Host "目指す状態（例: 自分経済圏の構築）"

Write-Host "`n✅ テーマ設定完了" -ForegroundColor Green
Write-Host "  テーマ: $theme" -ForegroundColor White
Write-Host "  敵: $enemy" -ForegroundColor White
Write-Host "  目標: $goal" -ForegroundColor White

# Phase別の要素を入力
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📋 Phase別の要素を入力してください" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Yellow

$phase1 = Read-Host "Phase 1: 衝撃的な数字/事実（例: 月5万=年60万）"
$phase2 = Read-Host "Phase 2: 読者の現状（例: 毎日副業してる、スキルアップしてる）"
$phase3 = Read-Host "Phase 3: 3層構造（例: プラットフォーム/広告/常識）"
$phase4 = Read-Host "Phase 4: 逃げられない理由（例: 生活必需品、依存関係）"
$phase5 = Read-Host "Phase 5: 視点転換（例: 構造が見えれば使える側に）"
$phase6 = Read-Host "Phase 6: 解決策（例: 自分経済圏、マーケティング学習）"
$phase7 = Read-Host "Phase 7: 次回予告（例: 個人ファンドの作り方）"

# サマリー表示
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📊 リライト設計サマリー" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Yellow

Write-Host "🎯 テーマ: $theme" -ForegroundColor White
Write-Host "⚔️  敵: $enemy" -ForegroundColor White
Write-Host "🏆 目標: $goal" -ForegroundColor White
Write-Host ""
Write-Host "🔴 Phase 1: $phase1" -ForegroundColor Red
Write-Host "🟠 Phase 2: $phase2" -ForegroundColor DarkYellow
Write-Host "🟡 Phase 3: $phase3" -ForegroundColor Yellow
Write-Host "🟢 Phase 4: $phase4" -ForegroundColor Green
Write-Host "🔵 Phase 5: $phase5" -ForegroundColor Blue
Write-Host "🟣 Phase 6: $phase6" -ForegroundColor Magenta
Write-Host "🟤 Phase 7: $phase7" -ForegroundColor DarkYellow

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

# 次のステップを案内
Write-Host "💡 次のステップ:" -ForegroundColor Yellow
Write-Host "  1. 上記の設計をもとに記事をリライト" -ForegroundColor White
Write-Host "  2. 各Phaseに対応するキーフレーズを選択" -ForegroundColor White
Write-Host "  3. Before/After、数字、具体例を挿入" -ForegroundColor White
Write-Host ""
Write-Host "🔑 必須キーフレーズ:" -ForegroundColor Yellow
Write-Host "  ✓ 「意味がわかりますか？」" -ForegroundColor White
Write-Host "  ✓ 「違います」（繰り返し）" -ForegroundColor White
Write-Host "  ✓ 「やばすぎませんか？？？」" -ForegroundColor White
Write-Host "  ✓ 「無理です」" -ForegroundColor White
Write-Host "  ✓ 「.… .… .…」" -ForegroundColor White
Write-Host "  ✓ 「…それでも」" -ForegroundColor White
Write-Host ""
Write-Host "📚 参考プロンプト:" -ForegroundColor Yellow
Write-Host "  prompt/note_renkinou_universal_template.md" -ForegroundColor White
Write-Host ""

# プロンプトを開くか確認
$openPrompt = Read-Host "プロンプトファイルを開きますか？ (y/n)"
if ($openPrompt -eq 'y') {
    $promptPath = Join-Path $PSScriptRoot "prompt\note_renkinou_universal_template.md"
    code $promptPath
    Write-Host "✅ プロンプトファイルを開きました" -ForegroundColor Green
}

Write-Host "`n✨ リライト設計が完了しました！" -ForegroundColor Green
