#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "00_meta/project_brief.md",
    "01_outline/volumes/volume_index.md",
    "01_outline/volumes/volume_01_初遇与觉醒.md",
    "04_chapter_memory/timeline_ledger.md",
    "04_chapter_memory/character_state.md",
    "04_chapter_memory/faction_memory.md",
    "04_chapter_memory/volume_memory/volume_01_memory.md",
    "04_chapter_memory/context_pack_ch01.md",
    "04_chapter_memory/context_pack_ch02.md",
    "05_prompts/system_prompt_cn.md",
    "05_prompts/chapter_prompt_template.md",
    "05_prompts/long_term_constraints.md",
    "07_quality/chapter_exit_gate.md",
    "08_tools/build_context_pack.py",
    "08_tools/build_context_pack.ps1",
]


def assert_exists(rel_path: str) -> None:
    path = ROOT / rel_path
    if not path.exists():
        raise AssertionError(f"Missing required file: {rel_path}")


def assert_contains(rel_path: str, needle: str) -> None:
    path = ROOT / rel_path
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        raise AssertionError(f"Expected text not found in {rel_path}: {needle}")


def main() -> int:
    for rel in REQUIRED_FILES:
        assert_exists(rel)

    assert_contains("05_prompts/chapter_prompt_template.md", "4000-6000")
    assert_contains("05_prompts/system_prompt_cn.md", "4000-6000")
    assert_contains("05_prompts/long_term_constraints.md", "每章字数范围固定在 `4000-6000`")
    assert_contains("05_prompts/long_term_constraints.md", "每卷 40-50 万字")
    assert_contains("04_chapter_memory/context_pack_ch01.md", "长期约束协议")
    assert_contains("04_chapter_memory/context_pack_ch01.md", "时间线总账")
    assert_contains("04_chapter_memory/context_pack_ch02.md", "人物状态快照")
    assert_contains("04_chapter_memory/context_pack_ch02.md", "当前卷记忆")
    assert_contains("04_chapter_memory/context_pack_ch02.md", "势力记忆（跨卷）")

    print("Workspace validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise
