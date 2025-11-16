#!/usr/bin/env python3
"""Generate LINE-friendly digests from prompt snapshots."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


@dataclass
class PromptRecord:
    page_id: str
    title: Optional[str]
    url: str
    archived: bool
    created_time: Optional[str]
    last_edited_time: Optional[str]
    properties: Dict[str, Any]

    def key(self) -> str:
        custom_id = self.properties.get("ID") or self.properties.get("Id")
        if isinstance(custom_id, str) and custom_id.strip():
            return custom_id.strip()
        return self.page_id or self.url

    def display_label(self) -> str:
        identifier = self.properties.get("ID") or self.page_id
        identifier_text = str(identifier) if identifier else self.page_id
        title = self.title or identifier_text
        if identifier_text and identifier_text not in title:
            return f"{identifier_text}: {title}"
        return title

    def category(self, preferred_field: Optional[str]) -> Optional[str]:
        if preferred_field and preferred_field in self.properties:
            value = self.properties[preferred_field]
            if isinstance(value, list):
                return str(value[0]) if value else None
            if isinstance(value, str):
                return value
        for key in ("カテゴリ", "Category", "カテゴリー"):
            value = self.properties.get(key)
            if isinstance(value, list):
                if value:
                    return str(value[0])
            elif value:
                return str(value)
        return None

    def last_touch(self) -> Optional[datetime]:
        for candidate in (self.last_edited_time, self.created_time):
            parsed = parse_timestamp(candidate)
            if parsed:
                return parsed
        return None


def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    sanitized = value.strip()
    if sanitized.endswith("Z"):
        sanitized = sanitized[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(sanitized)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


@dataclass
class SnapshotData:
    path: Path
    generated_at: datetime
    records: List[PromptRecord]
    category_field: Optional[str]


def load_snapshot(path: Path) -> SnapshotData:
    data = json.loads(path.read_text(encoding="utf-8"))
    generated_at = (
        parse_timestamp(data.get("generated_at"))
        or datetime.now(timezone.utc)
    )
    category_field = data.get("category_summary", {}).get("field")

    records: List[PromptRecord] = []
    for raw in data.get("records", []):
        properties = raw.get("properties", {})
        records.append(
            PromptRecord(
                page_id=raw.get("page_id") or raw.get("id") or raw.get("url"),
                title=raw.get("title"),
                url=raw.get("url", ""),
                archived=raw.get("archived", False),
                created_time=raw.get("created_time"),
                last_edited_time=raw.get("last_edited_time"),
                properties=properties,
            )
        )

    return SnapshotData(
        path=path,
        generated_at=generated_at,
        records=records,
        category_field=category_field,
    )


def discover_snapshots(directory: Path) -> List[Path]:
    if not directory.exists():
        return []
    return sorted(
        directory.glob("*.json"),
        key=lambda item: item.stat().st_mtime,
    )


def get_latest_snapshot(
    directory: Path,
    exclude: Optional[Path] = None,
) -> Optional[Path]:
    files = discover_snapshots(directory)
    files = [path for path in files if path != exclude]
    if not files:
        return None
    return files[-1]


def build_index(records: Iterable[PromptRecord]) -> Dict[str, PromptRecord]:
    return {record.key(): record for record in records}


def classify_records(
    current: SnapshotData,
    previous: Optional[SnapshotData],
    stale_days: int,
) -> Tuple[
    List[PromptRecord],
    List[PromptRecord],
    List[Tuple[PromptRecord, int]],
]:
    prev_index = build_index(previous.records) if previous else {}
    new_records: List[PromptRecord] = []
    updated_records: List[PromptRecord] = []
    stale_records: List[Tuple[PromptRecord, int]] = []
    reference_time = current.generated_at

    for record in current.records:
        if record.archived:
            continue
        previous_record = prev_index.get(record.key())
        if not previous_record:
            new_records.append(record)
        else:
            if (
                record.last_edited_time
                and previous_record.last_edited_time
                and record.last_edited_time != previous_record.last_edited_time
            ):
                updated_records.append(record)

        last_touch = record.last_touch()
        if (
            last_touch
            and reference_time - last_touch >= timedelta(days=stale_days)
        ):
            delta = reference_time - last_touch
            stale_records.append((record, delta.days))

    return new_records, updated_records, stale_records


def format_section(
    heading: str,
    entries: List[str],
    total_count: int,
) -> List[str]:
    lines = [f"■ {heading} ({total_count})"]
    if not entries:
        lines.append("- 該当なし")
        return lines
    lines.extend(entries)
    return lines


def format_records(
    records: List[PromptRecord],
    category_field: Optional[str],
    limit: int,
    include_age: bool = False,
    age_map: Optional[Dict[str, int]] = None,
) -> Tuple[List[str], int]:
    lines: List[str] = []
    for record in records[:limit]:
        category = record.category(category_field)
        pieces = [f"- {record.display_label()}"]
        if category:
            pieces.append(f"[{category}]")
        if include_age and age_map:
            days = age_map.get(record.key())
            if days is not None:
                pieces.append(f"{days}日未使用")
        lines.append(" ".join(pieces))

    remaining = max(0, len(records) - limit)
    return lines, remaining


def format_stale_records(
    records: List[Tuple[PromptRecord, int]],
    category_field: Optional[str],
    limit: int,
) -> Tuple[List[str], int]:
    lines: List[str] = []
    for record, days in records[:limit]:
        category = record.category(category_field)
        pieces = [f"- {record.display_label()}"]
        if category:
            pieces.append(f"[{category}]")
        pieces.append(f"{days}日更新なし")
        lines.append(" ".join(pieces))

    remaining = max(0, len(records) - limit)
    return lines, remaining


def build_digest(
    mode: str,
    current: SnapshotData,
    previous: Optional[SnapshotData],
    new_records: List[PromptRecord],
    updated_records: List[PromptRecord],
    stale_records: List[Tuple[PromptRecord, int]],
    limit: int,
    hub_link: Optional[str],
) -> Tuple[str, Dict[str, Any]]:
    header_time = current.generated_at.astimezone().strftime("%Y-%m-%d %H:%M")
    lines = [f"[Prompt Digest / {header_time} / {mode}]", ""]

    new_lines, new_remaining = format_records(
        new_records,
        current.category_field,
        limit,
    )
    lines.extend(format_section("新規", new_lines, len(new_records)))
    if new_remaining:
        lines.append(f"  … さらに {new_remaining} 件")
    lines.append("")

    updated_lines, updated_remaining = format_records(
        updated_records,
        current.category_field,
        limit,
    )
    lines.extend(format_section("更新", updated_lines, len(updated_records)))
    if updated_remaining:
        lines.append(f"  … さらに {updated_remaining} 件")
    lines.append("")

    stale_lines, stale_remaining = format_stale_records(
        stale_records,
        current.category_field,
        limit,
    )
    lines.extend(format_section("利用推奨", stale_lines, len(stale_records)))
    if stale_remaining:
        lines.append(f"  … さらに {stale_remaining} 件")
    lines.append("")

    lines.append(
        "→ 詳細: "
        + (hub_link or "prompt/PROMPT_KNOWLEDGE_HUB.md")
    )

    summary = {
        "generated_at": current.generated_at.isoformat(),
        "mode": mode,
        "current_snapshot": str(current.path),
        "previous_snapshot": str(previous.path) if previous else None,
        "counts": {
            "new": len(new_records),
            "updated": len(updated_records),
            "stale": len(stale_records),
        },
    }

    return "\n".join(lines).strip() + "\n", summary


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="スナップショットからLINEダイジェスト文を生成")
    parser.add_argument(
        "--snapshot-dir",
        default="data/prompt_snapshots",
        help="スナップショットのディレクトリ（デフォルト: data/prompt_snapshots）",
    )
    parser.add_argument(
        "--current",
        help="使用する最新スナップショットのパス（省略時は自動検出）",
    )
    parser.add_argument(
        "--previous",
        help="比較対象のスナップショット（省略時は直前ファイル）",
    )
    parser.add_argument(
        "--mode",
        choices=["daily", "weekly", "custom"],
        default="daily",
        help="ダイジェストのモード名（ヘッダー表示に使用）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="各セクションで表示する最大件数",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="利用推奨として扱う閾値（日数）",
    )
    parser.add_argument(
        "--hub-link",
        help="詳細リンクとして表示するURL/パス",
    )
    parser.add_argument(
        "--output",
        help="ダイジェスト文字列を書き出すファイルパス",
    )
    parser.add_argument(
        "--json-output",
        help="統計情報をJSONで保存するパス",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="標準出力への表示を抑制（ファイル出力のみ）",
    )
    return parser.parse_args(argv)


def resolve_snapshots(
    args: argparse.Namespace,
) -> Tuple[SnapshotData, Optional[SnapshotData]]:
    snapshot_dir = Path(args.snapshot_dir)

    current_path = (
        Path(args.current)
        if args.current
        else get_latest_snapshot(snapshot_dir)
    )
    if not current_path:
        raise SystemExit("スナップショットが見つかりませんでした")

    if args.previous:
        previous_path: Optional[Path] = Path(args.previous)
    else:
        previous_path = get_latest_snapshot(snapshot_dir, exclude=current_path)

    current = load_snapshot(current_path)
    previous = load_snapshot(previous_path) if previous_path else None
    return current, previous


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        current, previous = resolve_snapshots(args)
    except SystemExit as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1

    new_records, updated_records, stale_records = classify_records(
        current,
        previous,
        stale_days=args.stale_days,
    )

    digest_text, summary = build_digest(
        mode=args.mode,
        current=current,
        previous=previous,
        new_records=new_records,
        updated_records=updated_records,
        stale_records=stale_records,
        limit=args.limit,
        hub_link=args.hub_link,
    )

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(digest_text, encoding="utf-8")

    if args.json_output:
        Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_output).write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    if not args.quiet:
        print(digest_text)

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
