# AI 小说项目脚手架

## 目标
在最小上下文条件下写长篇，尽量节省 token，同时保持剧情、人物和世界规则一致。

## 推荐执行顺序
1. 填写 `00_meta/project_brief.md`（题材、受众、长度、禁忌项）。
2. 填写 `01_outline/high_level_outline.md`（主线、转折、结局）。
3. 填写 `02_characters/character_cards.md` 与 `02_characters/relationships.md`。
4. 填写 `03_worldbuilding/world_rules.md`（不可违背规则）。
5. 填写 `01_outline/beat_sheet.md`（章节级目标和状态）。
6. 为每章建立 `01_outline/scene_cards/chXX_scene_plan.md`（场景卡）。
7. 前 1-3 章完成后，更新 `04_chapter_memory/front_3_chapters_overview.md` 与章节摘要。
8. 每章写作前运行 `08_tools/build_context_pack.ps1` 生成最小上下文包。
9. 每章写完后更新 `rolling_memory.md`、`canon_facts.md`、`open_questions.md`、`timeline_ledger.md`、`character_state.md`。
10. 每 10 章产出一份 `arc_memory_arcXX.md`（500-800 字压缩记忆），后续优先喂这份摘要。

## 最小上下文包（推荐）
每次生成章节时，优先使用自动生成的：
- `04_chapter_memory/context_pack_chXX.md`
- `05_prompts/chapter_prompt_template.md`
- `05_prompts/system_prompt_cn.md`
- `05_prompts/long_term_constraints.md`

## 自动打包命令
Windows（PowerShell）：
```powershell
powershell -ExecutionPolicy Bypass -File .\08_tools\build_context_pack.ps1 -Chapter 4 -CharacterNames "谢衡","苏明玥"
```

Windows / macOS / Linux（Python，推荐统一）：
```bash
python 08_tools/build_context_pack.py --chapter 4 --character-names 谢衡 苏明玥
```

macOS / Linux（Bash 包装）：
```bash
bash 08_tools/build_context_pack.sh --chapter 4 --character-names 谢衡 苏明玥
```

## Git 初始化（示例）
```bash
git init
git branch -M main
git remote add origin git@github.com:HoneyBury/novel.git
git add .
git commit -m "chore: initialize novel workspace"
```

## 发布快照（Tag `v.x.x`）
- 当你推送形如 `v1.0.0` 的 tag 时，GitHub Actions 会自动：
  - 打包当前仓库为 `novel-snapshot-v1.0.0.zip`
  - 上传到该 tag 的 GitHub Release 资产
  - 同时保留一份 workflow artifact

示例：
```bash
git tag v1.0.0
git push origin v1.0.0
```

## 跨设备维护
- 新电脑（尤其是 Mac）拉代码后如何在 Codex 继续维护，请看：
  - `docs/跨设备维护指南.md`

## 目录说明
- `00_meta/` 项目元信息与风格基线
- `01_outline/` 主线大纲、章节拍点、场景卡
- `02_characters/` 人物卡与关系网
- `03_worldbuilding/` 世界观规则、势力、地点
- `04_chapter_memory/` 章节摘要、滚动记忆、canon 事实、未决问题、时间线、人物状态、Arc 压缩记忆
- `05_prompts/` 写作与审校提示词模板
- `06_draft/` 章节草稿
- `07_quality/` 连续性与质量检查
- `08_tools/` 自动化脚本（上下文打包等）
- `99_archive/` 归档文件（按规则命名）
