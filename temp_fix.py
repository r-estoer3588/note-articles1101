from pathlib import Path
WORKFLOW_PATH = Path('c:/Repos/note-articles/workflows/Notes to Notion Auto Organizer (Schedule Fixed).json')
RAW_PATTERN = (
  'JSON形式で返してください:\\n{"category": "カテゴリ名", "tags": ["タグ1"]}\\n\\n'
  'ファイル名: ${inputData.fileName}\\n内容: ${inputData.fileContent}`\n      }\n    ],\n'
)
ESCAPED_REPLACEMENT = (
  'JSON形式で返してください:\\n{\\"category\\": \\"カテゴリ名\\", \\"tags\\": '
  '[\\"タグ1\\"]}\\n\\nファイル名: ${inputData.fileName}\\n内容: '
  '${inputData.fileContent}`\n      }\n    ],\n'
)

text = WORKFLOW_PATH.read_text(encoding='utf-8')
if RAW_PATTERN not in text:
  raise SystemExit('pattern not found in workflow file')

WORKFLOW_PATH.write_text(text.replace(RAW_PATTERN, ESCAPED_REPLACEMENT, 1), encoding='utf-8')
