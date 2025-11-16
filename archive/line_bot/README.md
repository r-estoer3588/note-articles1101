# LINE Bot Assets (Archived)

2025-11-16: The LINE bot automation effort was discontinued. All related source code, workflows, test data, and setup scripts were relocated here to keep the main workspace clean while preserving references for future investigation.

Contents snapshot:

- `tools/line_bot_api.py`, `line_bot_state_manager.py`, `line_bot_helper.py`
- Historical n8n workflows (`n8n_workflow_menu_sqlite*.json`, smartphone variant) and operational docs (`LINE_MENU_GUIDE.md`, `N8N_*GUIDE.md`, etc.)
- Setup and test artifacts (`setup-bot.ps1`, `test_flask.py`, `test_webhook.json`, `run-line-bot-stack.ps1`)

Nothing under `tools/` now depends on these files. If the LINE bot needs to be revived, restore the necessary files from this folder.
