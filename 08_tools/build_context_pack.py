#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import List


def read_file_or_empty(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def get_latest_arc_memory_text(chapter_memory_dir: Path) -> str:
    candidates = sorted(chapter_memory_dir.glob("arc_memory_arc*.md"), reverse=True)
    if not candidates:
        return ""
    return candidates[0].read_text(encoding="utf-8")


def get_beat_line(beat_text: str, target_chapter: int) -> str:
    pattern = re.compile(r"^\|\s*" + re.escape(str(target_chapter)) + r"\s*\|", re.MULTILINE)
    for line in beat_text.splitlines():
        if pattern.match(line.strip()):
            return line
    return "(未在 beat_sheet 中找到该章节，请先补充章节拍点。)"


def split_h2_blocks(text: str) -> List[str]:
    matches = list(re.finditer(r"(?ms)^##\s.*?(?=^##\s|\Z)", text))
    if not matches:
        return [text.strip()] if text.strip() else []
    return [m.group(0).strip() for m in matches]


def get_character_section(cards_text: str, names: List[str]) -> str:
    if not names:
        return cards_text.strip()

    blocks = split_h2_blocks(cards_text)
    selected: List[str] = []

    for block in blocks:
        if any(name in block for name in names):
            selected.append(block)

    if not selected:
        return cards_text.strip()

    unique_selected: List[str] = []
    for block in selected:
        if block not in unique_selected:
            unique_selected.append(block)
    return "\n\n".join(unique_selected)


def build_content(project_root: Path, chapter: int, character_names: List[str]) -> str:
    chapter_memory_dir = project_root / "04_chapter_memory"

    project_brief = read_file_or_empty(project_root / "00_meta" / "project_brief.md")
    style_guide = read_file_or_empty(project_root / "00_meta" / "style_guide.md")
    outline = read_file_or_empty(project_root / "01_outline" / "high_level_outline.md")
    beat_sheet = read_file_or_empty(project_root / "01_outline" / "beat_sheet.md")
    char_cards = read_file_or_empty(project_root / "02_characters" / "character_cards.md")
    rolling_memory = read_file_or_empty(chapter_memory_dir / "rolling_memory.md")
    canon_facts = read_file_or_empty(chapter_memory_dir / "canon_facts.md")
    open_questions = read_file_or_empty(chapter_memory_dir / "open_questions.md")
    timeline_ledger = read_file_or_empty(chapter_memory_dir / "timeline_ledger.md")
    character_state = read_file_or_empty(chapter_memory_dir / "character_state.md")
    long_term_constraints = read_file_or_empty(project_root / "05_prompts" / "long_term_constraints.md")
    latest_arc_memory = get_latest_arc_memory_text(chapter_memory_dir)
    front_3 = read_file_or_empty(chapter_memory_dir / "front_3_chapters_overview.md") if chapter <= 3 else ""

    beat_line = get_beat_line(beat_sheet, chapter)
    character_section = get_character_section(char_cards, character_names)
    chapter_padded = f"{chapter:02d}"
    now_text = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    names_text = "、".join(character_names) if character_names else "(未指定，已包含完整人物卡)"

    parts = [
        f"# 第{chapter_padded}章 最小上下文包",
        "",
        f"- 生成时间：{now_text}",
        f"- 目标章节：第{chapter} 章",
        f"- 人物筛选：{names_text}",
        "",
        "## 章节目标（来自 beat_sheet）",
        beat_line,
        "",
        "## 项目简报",
        project_brief.rstrip(),
        "",
        "## 风格指南",
        style_guide.rstrip(),
        "",
        "## 高层大纲",
        outline.rstrip(),
        "",
        "## 当前滚动记忆",
        rolling_memory.rstrip(),
        "",
        "## 已确认事实（Canon）",
        canon_facts.rstrip(),
        "",
        "## 未决问题",
        open_questions.rstrip(),
        "",
        "## 时间线总账",
        timeline_ledger.rstrip(),
        "",
        "## 人物状态快照",
        character_state.rstrip(),
        "",
        "## 长期约束协议",
        long_term_constraints.rstrip(),
        "",
        "## 相关人物卡",
        character_section.rstrip(),
    ]

    if latest_arc_memory.strip():
        parts += ["", "## 最近 Arc 压缩记忆", latest_arc_memory.rstrip()]

    if front_3.strip():
        parts += ["", "## 前三章总览（早期章节）", front_3.rstrip()]

    parts += [
        "",
        "## 使用说明",
        "1. 将本文件与 `05_prompts/chapter_prompt_template.md` 一起提交给模型。",
        "2. 若仍超长，先删减“项目简报”里的非关键背景，再删减人物卡的无关角色。",
        "3. 每章写作必须遵守 `05_prompts/long_term_constraints.md` 与 `07_quality/chapter_exit_gate.md`。",
        "4. 章节完成后立即更新 `rolling_memory.md`、`canon_facts.md`、`open_questions.md`、`timeline_ledger.md`、`character_state.md`。",
        "",
    ]

    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="生成小说章节最小上下文包（跨平台）。")
    parser.add_argument("--chapter", type=int, required=True, help="章节号，例如 1")
    parser.add_argument("--character-names", nargs="*", default=[], help="本章相关角色名，多个空格分隔")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="项目根目录，默认脚本上级目录",
    )
    args = parser.parse_args()

    if args.chapter < 1 or args.chapter > 999:
        raise SystemExit("--chapter 必须在 1-999 之间")

    project_root = args.project_root.resolve()
    chapter_padded = f"{args.chapter:02d}"
    output_path = project_root / "04_chapter_memory" / f"context_pack_ch{chapter_padded}.md"

    content = build_content(project_root, args.chapter, args.character_names)
    output_path.write_text(content, encoding="utf-8", newline="\n")

    print(f"Context pack generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
