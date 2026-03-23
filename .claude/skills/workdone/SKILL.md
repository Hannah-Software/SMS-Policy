---
name: workdone
description: Summarize the current session's work and append it to WorkDoneSummary.md. Use when the user says "log work", "work done", "session summary", or is wrapping up a session.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Work Done Summary — Session Logger

Generate a structured session summary and **append** it to `WorkDoneSummary.md` in the repo root. If the file doesn't exist, create it with the standard header first.

## Step 1: Gather Data

Run these commands to collect session metrics:

1. **PRs merged this session**: `gh pr list --state merged --limit 20 --json number,title,additions,deletions,changedFiles,mergedAt` — filter to PRs merged today (or since session start if known).
2. **Recent commits**: `git log --oneline -20` to identify which commits belong to this session.
3. **Per-PR stats**: For each PR, run `gh pr view <number> --json additions,deletions,changedFiles,title` to get exact line counts.
4. **Total lines in touched files**: `wc -l` on all files that were created or modified across the session's PRs.
5. **Test counts**: Check if tests were added by looking at test file diffs. Run `python -m pytest tests/ --co -q 2>/dev/null | tail -1` to get total test count.
6. **CI status**: Confirm all PRs passed CI by checking `gh pr view <number> --json statusCheckRollup`.

## Step 2: Determine Grouping

- If multiple PRs were **worked on together** (same feature, dependent changes), group them under one entry.
- If PRs were **independent** (different features, cleanup, docs), list them as separate sub-entries within the session.
- Use your knowledge of the conversation to determine grouping — files edited in the same task go together.

## Step 3: Create or Append

**If `WorkDoneSummary.md` does NOT exist**, create it with this header:

```markdown
# Work Done Summary

Each entry represents a single chat session with Claude Code. Entries are grouped by session when PRs were worked on together, or split when they were independent.
```

**Then append** the new entry using the exact format below.

## Entry Format

Each session entry MUST follow this exact structure:

```markdown
---

## YYYY-MM-DD HH:MM AM/PM — <Short Session Title>

| Metric | Value |
|--------|-------|
| **Date/Time** | YYYY-MM-DD ~HH:MM AM/PM EST |
| **Session Title** | <Descriptive title of what was accomplished> |
| **Chat Messages** | <N> user prompts, <N> responses |
| **PRs Shipped** | #X, #Y, #Z |
| **New Lines of Code** | +<additions> / -<deletions> (net <+/-net>) |
| **Total Lines in Touched Files** | <total wc -l of all files created/modified> |
| **New Tests Added** | <count> (in `<test file(s)>`) or "None" |
| **Tests in CI** | Yes/No — <details on which checks passed> |

### Scope

<1-2 sentence summary of what was tackled in this session and why.>

### Changes

#### PR #<N> — <PR title>
*<Note: e.g. "Main planned work" or "Independent fix, shipped separately">*

| File | Action | Lines |
|------|--------|-------|
| `path/to/file.py` | Created/Modified | <+N lines — brief description of what changed> |
| `path/to/other.py` | Modified | <description> |

**Stats:** +<additions> / -<deletions> across <N> files

<Repeat for each PR in the session>

### Verification

- <Test command run> — <result>
- <Import/smoke check> — <result>
- All <N> PRs passed CI (`test (3.14)` + `docker-build`) before merge

### Context

<1-2 sentences on how this session fits into the larger project. Reference prior sessions/PRs if relevant.>
```

## Important Rules

- **NEVER overwrite** existing content — always append after the last entry.
- Use `---` (horizontal rule) to separate entries.
- Count chat messages by reviewing the conversation history (user prompts and your responses).
- If no PRs were shipped (e.g. research-only session), still log the entry but note "No PRs — research/planning session" in the metrics table.
- If no tests were added, write "None" for New Tests Added.
- For the **Chat Messages** count, give your best estimate from the conversation.
- Format all numbers with commas for readability (e.g. 1,226 not 1226).
- Always confirm the append was successful by reading back the last few lines of the file.
- **After writing the entry**, print the FULL entry to the screen so the user can review what was logged. Display it as-is (raw markdown) so it's readable in the terminal.
