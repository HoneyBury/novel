# Prompt Constraints (Token-Saving)

## Input Constraints
- Only pass relevant characters for current chapter.
- Limit recent events to last 2-3 chapters.
- Keep each constraint line <= 20 words (or short Chinese phrase).
- Prefer bullet points over long paragraphs.

## Output Constraints
- Enforce target word range (4000-6000 Chinese characters/words per chapter).
- Require a fixed output structure.
- Require end-of-chapter hook.
- Require chapter summary and continuity facts.

## Compression Rules
- Replace repeated background with one-line labels.
- Keep rolling memory under 300-500 Chinese characters.
- Prefer latest `arc_memory_arcXX.md` over old full chapters.
- Archive old details into `99_archive/` instead of passing every time.
