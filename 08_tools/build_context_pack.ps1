param(
    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 999)]
    [int]$Chapter,

    [string[]]$CharacterNames
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot

function ProjectPath {
    param([string[]]$Segments)
    $path = $projectRoot
    foreach ($segment in $Segments) {
        $path = Join-Path $path $segment
    }
    return $path
}

function Read-FileOrEmpty {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        return Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    }
    return ''
}

function Get-LatestArcMemoryText {
    param([string]$DirPath)
    if (-not (Test-Path -LiteralPath $DirPath)) {
        return ''
    }
    $file = Get-ChildItem -LiteralPath $DirPath -File -Filter 'arc_memory_arc*.md' |
        Sort-Object Name -Descending |
        Select-Object -First 1
    if ($null -eq $file) {
        return ''
    }
    return Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
}

function Get-BeatLine {
    param(
        [string]$BeatText,
        [int]$TargetChapter
    )
    $lines = $BeatText -split "`r?`n"
    $pattern = '^\|\s*' + $TargetChapter + '\s*\|'
    $line = $lines | Where-Object { $_ -match $pattern } | Select-Object -First 1
    if ($null -ne $line -and $line.Trim().Length -gt 0) {
        return $line
    }
    return '(未在 beat_sheet 中找到该章节，请先补充章节拍点。)'
}

function Get-CharacterSection {
    param(
        [string]$CardsText,
        [string[]]$Names
    )

    if ($null -eq $Names -or @($Names).Count -eq 0) {
        return $CardsText.Trim()
    }

    $matches = [regex]::Matches($CardsText, '(?ms)^##\s.*?(?=^##\s|\z)')
    if ($matches.Count -eq 0) {
        return $CardsText.Trim()
    }

    $blocks = @()
    foreach ($m in $matches) {
        $blocks += $m.Value.Trim()
    }

    $selected = @()
    foreach ($name in $Names) {
        $escaped = [regex]::Escape($name)
        $hit = $blocks | Where-Object { $_ -match $escaped }
        if ($hit) {
            $selected += $hit
        }
    }

    $selected = @($selected | Select-Object -Unique)
    if (@($selected).Count -eq 0) {
        return $CardsText.Trim()
    }

    return ($selected -join "`n`n")
}

$projectBrief = Read-FileOrEmpty (ProjectPath @('00_meta', 'project_brief.md'))
$styleGuide = Read-FileOrEmpty (ProjectPath @('00_meta', 'style_guide.md'))
$outline = Read-FileOrEmpty (ProjectPath @('01_outline', 'high_level_outline.md'))
$beatSheet = Read-FileOrEmpty (ProjectPath @('01_outline', 'beat_sheet.md'))
$charCards = Read-FileOrEmpty (ProjectPath @('02_characters', 'character_cards.md'))
$rollingMemory = Read-FileOrEmpty (ProjectPath @('04_chapter_memory', 'rolling_memory.md'))
$canonFacts = Read-FileOrEmpty (ProjectPath @('04_chapter_memory', 'canon_facts.md'))
$openQuestions = Read-FileOrEmpty (ProjectPath @('04_chapter_memory', 'open_questions.md'))
$timelineLedger = Read-FileOrEmpty (ProjectPath @('04_chapter_memory', 'timeline_ledger.md'))
$characterState = Read-FileOrEmpty (ProjectPath @('04_chapter_memory', 'character_state.md'))
$longTermConstraints = Read-FileOrEmpty (ProjectPath @('05_prompts', 'long_term_constraints.md'))
$latestArcMemory = Get-LatestArcMemoryText -DirPath (ProjectPath @('04_chapter_memory'))
$front3 = if ($Chapter -le 3) {
    Read-FileOrEmpty (ProjectPath @('04_chapter_memory', 'front_3_chapters_overview.md'))
}
else {
    ''
}

$beatLine = Get-BeatLine -BeatText $beatSheet -TargetChapter $Chapter
$characterSection = Get-CharacterSection -CardsText $charCards -Names $CharacterNames
$chapterPadded = '{0:D2}' -f $Chapter
$nowText = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
$namesText = if ($CharacterNames -and @($CharacterNames).Count -gt 0) {
    ($CharacterNames -join '、')
}
else {
    '(未指定，已包含完整人物卡)'
}

$outputPath = ProjectPath @('04_chapter_memory', ("context_pack_ch{0}.md" -f $chapterPadded))

$content = @"
# 第${chapterPadded}章 最小上下文包

- 生成时间：$nowText
- 目标章节：第$Chapter 章
- 人物筛选：$namesText

## 章节目标（来自 beat_sheet）
$beatLine

## 项目简报
$projectBrief

## 风格指南
$styleGuide

## 高层大纲
$outline

## 当前滚动记忆
$rollingMemory

## 已确认事实（Canon）
$canonFacts

## 未决问题
$openQuestions

## 时间线总账
$timelineLedger

## 人物状态快照
$characterState

## 长期约束协议
$longTermConstraints

## 相关人物卡
$characterSection
"@

if ($latestArcMemory.Trim().Length -gt 0) {
    $content += @"

## 最近 Arc 压缩记忆
$latestArcMemory
"@
}

if ($front3.Trim().Length -gt 0) {
    $content += @"

## 前三章总览（早期章节）
$front3
"@
}

$content += @"

## 使用说明
1. 将本文件与 `05_prompts/chapter_prompt_template.md` 一起提交给模型。
2. 若仍超长，先删减“项目简报”里的非关键背景，再删减人物卡的无关角色。
3. 每章写作必须遵守 `05_prompts/long_term_constraints.md` 与 `07_quality/chapter_exit_gate.md`。
4. 章节完成后立即更新 `rolling_memory.md`、`canon_facts.md`、`open_questions.md`、`timeline_ledger.md`、`character_state.md`。
"@

Set-Content -LiteralPath $outputPath -Value $content -Encoding UTF8
Write-Output "Context pack generated: $outputPath"
