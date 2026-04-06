# Prompt Constraints (Token-Saving)

## Input Constraints
- Only pass relevant characters for current chapter.
- Limit recent events to last 2-3 chapters.
- Always include current volume file + current volume memory.
- Always include `faction_memory.md` when multiple势力出场。
- Keep each constraint line <= 20 words (or short Chinese phrase).
- Prefer bullet points over long paragraphs.

## Output Constraints
- Enforce target word range (4000-6000 Chinese characters/words per chapter).
- Require a fixed output structure.
- Require end-of-chapter hook.
- Require chapter summary and continuity facts.
- Require at least one stage-relevant ensemble/civilian scene when chapter belongs to群像推进段。

## Compression Rules
- Replace repeated background with one-line labels.
- Keep rolling memory under 300-500 Chinese characters.
- Keep each volume memory under 800-1200 Chinese characters.
- Keep faction memory focused on status/职位/影响，不写剧情复述。
- Prefer latest `arc_memory_arcXX.md` over old full chapters.
- Archive old details into `99_archive/` instead of passing every time.
