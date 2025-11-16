#!/usr/bin/env python3
"""Notion prompt snapshot exporter.

This utility fetches the Prompt Library database from Notion and stores a
flattened snapshot so other jobs (audits, LINE digests, etc.) can run without
hitting the API. It intentionally works in offline mode as well so previously
captured snapshots can be re-exported to CSV or summarized again.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

try:  # Optional dependency so --help or --input-file still works without it.
    from notion_client import Client  # type: ignore
except ImportError:  # pragma: no cover - handled at runtime when needed
    Client = None  # type: ignore

# -----------------------------------------------------------------------------
# Data containers
# -----------------------------------------------------------------------------


@dataclass
class SnapshotRecord:
    """Flattened representation of a Notion page."""

    page_id: str
    title: Optional[str]
    url: str
    archived: bool
    created_time: str
    last_edited_time: str
    properties: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_id": self.page_id,
            "title": self.title,
            "url": self.url,
            "archived": self.archived,
            "created_time": self.created_time,
            "last_edited_time": self.last_edited_time,
            "properties": self.properties,
        }


@dataclass
class SnapshotPayload:
    """Full snapshot structure that is saved to disk."""

    generated_at: str
    source: str
    database_id: Optional[str]
    record_count: int
    property_keys: List[str]
    category_summary: Optional[Dict[str, Any]]
    records: List[SnapshotRecord]

    def to_serializable(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "source": self.source,
            "database_id": self.database_id,
            "record_count": self.record_count,
            "property_keys": self.property_keys,
            "category_summary": self.category_summary,
            "records": [record.to_dict() for record in self.records],
        }


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_snapshot_from_file(input_path: Path) -> SnapshotPayload:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    records = [
        SnapshotRecord(
            page_id=record.get("page_id", ""),
            title=record.get("title"),
            url=record.get("url", ""),
            archived=record.get("archived", False),
            created_time=record.get("created_time", ""),
            last_edited_time=record.get("last_edited_time", ""),
            properties=record.get("properties", {}),
        )
        for record in data.get("records", [])
    ]
    return SnapshotPayload(
        generated_at=data.get("generated_at", iso_now()),
        source=data.get("source", "file"),
        database_id=data.get("database_id"),
        record_count=len(records),
        property_keys=data.get("property_keys", []),
        category_summary=data.get("category_summary"),
        records=records,
    )


def fetch_from_notion(
    api_key: str,
    database_id: str,
    page_size: int = 100,
    limit: Optional[int] = None,
) -> List[Mapping[str, Any]]:
    if Client is None:  # pragma: no cover - runtime guard
        raise RuntimeError(
            "notion-client がインストールされていません。"
            " `pip install -r requirements.txt` を実行してください。"
        )

    client = Client(auth=api_key)
    cursor: Optional[str] = None
    results: List[Mapping[str, Any]] = []

    while True:
        payload: Dict[str, Any] = {
            "database_id": database_id,
            "page_size": max(1, min(page_size, 100)),
        }
        if cursor:
            payload["start_cursor"] = cursor

        response = client.databases.query(**payload)
        results.extend(response.get("results", []))

        if limit and len(results) >= limit:
            return results[:limit]

        if not response.get("has_more"):
            break

        cursor = response.get("next_cursor")

    return results


def get_rich_text(blocks: Optional[Iterable[Mapping[str, Any]]]) -> str:
    if not blocks:
        return ""
    buffer: List[str] = []
    for block in blocks:
        if not isinstance(block, Mapping):
            continue
        text = block.get("plain_text") or block.get("text", {}).get("content")
        if text:
            buffer.append(str(text))
    return "".join(buffer).strip()


def flatten_property(prop: Mapping[str, Any]) -> Any:
    prop_type = prop.get("type")
    value = prop.get(prop_type) if prop_type else None

    if prop_type in {"rich_text", "title"}:
        return get_rich_text(value if isinstance(value, Sequence) else None)
    if prop_type == "select":
        return value["name"] if value else None
    if prop_type == "status":
        return value["name"] if value else None
    if prop_type == "multi_select":
        if not isinstance(value, list):
            return []
        return [
            item.get("name")
            for item in value
            if isinstance(item, Mapping) and item.get("name")
        ]
    if prop_type == "people":
        if not isinstance(value, list):
            return []
        people: List[str] = []
        for person in value:
            if not isinstance(person, Mapping):
                continue
            people.append(str(person.get("name") or person.get("id")))
        return people
    if prop_type == "url":
        return value
    if prop_type == "email":
        return value
    if prop_type == "phone_number":
        return value
    if prop_type == "checkbox":
        return bool(value)
    if prop_type == "number":
        return value
    if prop_type == "date":
        if not isinstance(value, Mapping):
            return None
        return {
            "start": value.get("start"),
            "end": value.get("end"),
            "time_zone": value.get("time_zone"),
        }
    if prop_type == "files":
        if not isinstance(value, list):
            return []
        files: List[str] = []
        for item in value:
            if not isinstance(item, Mapping):
                continue
            if item.get("name"):
                files.append(str(item["name"]))
            else:
                external_url = item.get("external", {}).get("url")
                file_url = item.get("file", {}).get("url")
                if external_url:
                    files.append(str(external_url))
                elif file_url:
                    files.append(str(file_url))
        return files
    if prop_type == "relation":
        if not isinstance(value, list):
            return []
        return [rel.get("id") for rel in value if isinstance(rel, Mapping)]
    if prop_type == "formula":
        if not isinstance(value, Mapping):
            return None
        formula_type = value.get("type", "string")
        return value.get(formula_type)
    if prop_type == "rollup":
        if isinstance(value, Mapping):
            rollup_type = value.get("type")
            if rollup_type == "number":
                return value.get("number")
            if rollup_type == "date":
                return value.get("date")
            if rollup_type == "array":
                array_items = value.get("array", [])
                flattened_items: List[Any] = []
                for item in array_items:
                    if not isinstance(item, Mapping):
                        continue
                    inner_type = item.get("type")
                    if not isinstance(inner_type, str):
                        continue
                    nested_prop: Dict[str, Any] = {
                        "type": inner_type,
                        inner_type: item.get(inner_type),
                    }
                    flattened_items.append(flatten_property(nested_prop))
                return flattened_items
        return value

    return value


def flatten_properties(properties: Mapping[str, Any]) -> Dict[str, Any]:
    flattened: Dict[str, Any] = {}
    for name, prop in properties.items():
        flattened[name] = flatten_property(prop)
    return flattened


def infer_title(
    page: Mapping[str, Any],
    flattened: Mapping[str, Any],
) -> Optional[str]:
    properties = page.get("properties", {})
    for name, prop in properties.items():
        if prop.get("type") == "title":
            text = flatten_property(prop)
            if text:
                return str(text)
    # fallback: common property names
    for key in ("タイトル", "Title", "name", "Name", "プロンプト"):
        if key in flattened and flattened[key]:
            return str(flattened[key])
    return None


def build_snapshot(
    records: Iterable[Mapping[str, Any]],
    source: str,
    database_id: Optional[str],
) -> SnapshotPayload:
    flattened_records: List[SnapshotRecord] = []
    property_names: set[str] = set()

    for page in records:
        properties = flatten_properties(page.get("properties", {}))
        property_names.update(properties.keys())
        flattened_records.append(
            SnapshotRecord(
                page_id=page.get("id", ""),
                title=infer_title(page, properties),
                url=page.get("url", ""),
                archived=page.get("archived", False),
                created_time=page.get("created_time", ""),
                last_edited_time=page.get("last_edited_time", ""),
                properties=properties,
            )
        )

    category_summary = summarize_categories(flattened_records)

    return SnapshotPayload(
        generated_at=iso_now(),
        source=source,
        database_id=database_id,
        record_count=len(flattened_records),
        property_keys=sorted(property_names),
        category_summary=category_summary,
        records=flattened_records,
    )


def summarize_categories(
    records: Iterable[SnapshotRecord],
) -> Optional[Dict[str, Any]]:
    category_key = infer_category_key(records)
    if not category_key:
        return None

    counter: Counter[str] = Counter()
    for record in records:
        value = record.properties.get(category_key)
        if isinstance(value, list):
            for item in value:
                if item:
                    counter[str(item)] += 1
        elif value:
            counter[str(value)] += 1

    return {
        "field": category_key,
        "counts": sorted(
            counter.items(),
            key=lambda item: (-item[1], item[0]),
        ),
    }


def infer_category_key(records: Iterable[SnapshotRecord]) -> Optional[str]:
    candidates = ["カテゴリ", "カテゴリー", "category", "Category"]
    for record in records:
        for candidate in candidates:
            if candidate in record.properties:
                return candidate
    return None


def write_json(
    payload: SnapshotPayload,
    path: Path,
    pretty: bool = False,
) -> None:
    ensure_output_dir(path.parent)
    if pretty:
        path.write_text(
            json.dumps(
                payload.to_serializable(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    else:
        path.write_text(
            json.dumps(payload.to_serializable(), ensure_ascii=False),
            encoding="utf-8",
        )


def stringify_value(value: Any) -> str:
    if isinstance(value, list):
        if all(isinstance(item, str) for item in value):
            return "; ".join(item for item in value if item)
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return str(value)


def write_csv(payload: SnapshotPayload, path: Path) -> None:
    ensure_output_dir(path.parent)
    property_keys = payload.property_keys
    fieldnames = [
        "page_id",
        "title",
        "url",
        "archived",
        "created_time",
        "last_edited_time",
        *property_keys,
    ]
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for record in payload.records:
            row = {
                "page_id": record.page_id,
                "title": record.title or "",
                "url": record.url,
                "archived": record.archived,
                "created_time": record.created_time,
                "last_edited_time": record.last_edited_time,
            }
            for key in property_keys:
                row[key] = stringify_value(record.properties.get(key))
            writer.writerow(row)


def choose_output_paths(args: argparse.Namespace) -> Dict[str, Optional[Path]]:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    default_stem = f"prompt_snapshot_{timestamp}"

    if args.output:
        output_path = Path(args.output)
        if output_path.suffix:
            stem = output_path.stem
            parent = (
                output_path.parent
                if output_path.parent != Path("")
                else Path(args.output_dir)
            )
            json_path = (
                output_path
                if output_path.suffix.lower() == ".json"
                else parent / f"{stem}.json"
            )
            csv_path = parent / f"{stem}.csv"
        else:
            parent = output_path
            json_path = parent / f"{default_stem}.json"
            csv_path = parent / f"{default_stem}.csv"
    else:
        parent = Path(args.output_dir)
        json_path = parent / f"{default_stem}.json"
        csv_path = parent / f"{default_stem}.csv"

    targets: Dict[str, Optional[Path]] = {"json": None, "csv": None}
    if args.format in {"json", "both"}:
        targets["json"] = json_path
    if args.format in {"csv", "both"}:
        targets["csv"] = csv_path
    return targets


def print_summary(payload: SnapshotPayload) -> None:
    print("📦 Snapshot summary")
    print(f"  Records         : {payload.record_count}")
    print(f"  Generated at    : {payload.generated_at}")
    if payload.database_id:
        print(f"  Database ID     : {payload.database_id}")
    if payload.property_keys:
        properties = ", ".join(payload.property_keys)
    else:
        properties = "-"
    print(f"  Property fields : {properties}")
    if payload.category_summary:
        field = payload.category_summary["field"]
        counts = payload.category_summary["counts"]
        readable = ", ".join(f"{name} ({count})" for name, count in counts)
        print(f"  Categories ({field}): {readable}")
    print()


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NotionのプロンプトDBをスナップショット化します")
    parser.add_argument(
        "--output-dir",
        default="data/prompt_snapshots",
        help="スナップショットを保存するディレクトリ（デフォルト: data/prompt_snapshots）",
    )
    parser.add_argument(
        "--output",
        help="ファイル名またはディレクトリを直接指定（例: exports/today.json）",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "both"],
        default="json",
        help="保存フォーマットを選択",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="取得する最大件数（指定しなければ全件）",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Notion APIの1ページあたり件数（最大100）",
    )
    parser.add_argument(
        "--input-file",
        help="既存スナップショットJSONを読み込み再出力（Notion API不要）",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="JSONをインデント付きで保存",
    )
    parser.add_argument(
        "--api-key",
        help="Notion APIキー（未指定時は NOTION_API_KEY 環境変数を使用）",
    )
    parser.add_argument(
        "--database-id",
        help="NotionデータベースID（未指定時は NOTION_DATABASE_ID 環境変数を使用）",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="サマリー出力を抑制",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if args.input_file:
        payload = load_snapshot_from_file(Path(args.input_file))
    else:
        api_key = args.api_key or os.getenv("NOTION_API_KEY")
        database_id = args.database_id or os.getenv("NOTION_DATABASE_ID")
        if not api_key or not database_id:
            print(
                "❌ NOTION_API_KEY / NOTION_DATABASE_ID を設定してください",
                file=sys.stderr,
            )
            return 1
        raw_pages = fetch_from_notion(
            api_key,
            database_id,
            page_size=args.page_size,
            limit=args.limit,
        )
        payload = build_snapshot(
            raw_pages,
            source="notion",
            database_id=database_id,
        )

    targets = choose_output_paths(args)
    if targets["json"]:
        write_json(payload, targets["json"], pretty=args.pretty)
    if targets["csv"]:
        write_csv(payload, targets["csv"])

    if not args.silent:
        print_summary(payload)
        for label, path in targets.items():
            if path:
                print(f"✅ {label.upper()} saved to {path}")

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
