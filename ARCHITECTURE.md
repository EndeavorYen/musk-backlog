# musk-backlog architecture

Independent Grok skill. Same `SKILL.md` copies to Claude, Cursor, and Hermes. Complementary to [musk-algorithm](https://github.com/EndeavorYen/musk-algorithm-skill) and [just-ten-more](https://github.com/EndeavorYen/just-ten-more): never merge them. Live path is `/musk-backlog`, not `/musk-algorithm`. `just-ten-more` lists challenges and writes no review log. `just-ten-more-loop` is the hunt-fix loop.

| | musk-algorithm | musk-backlog | just-ten-more | just-ten-more-loop |
|---|---|---|---|---|
| Job | First-principles evaluation of a requirement, design, process, or system | Forge-agnostic work items from a musk report, then stop | Evidence-backed hunt, list only | Evidence-backed hunt-fix review loop |
| Sequence | Musk's five steps **in order** | Map keep/change/delete-work, list table, optional tracker | One round of up to 10 challenges | Rounds until a round finds none |
| Default output | Structured evaluation report in the conversation; no evaluation file | Conversation table; optional tracker create; then stop | List in the conversation; no review log | Fixes (or blockers) plus a review log |
| Helper | None | None | None | `scripts/review-log.py` + `.just-ten-more/` |

musk-algorithm helper is None. just-ten-more helper is None. Only just-ten-more-loop ships `scripts/review-log.py`. musk-backlog does not copy `review-log.py`.

## File tree

```
LICENSE                     MIT, EndeavorYen 2026 (do not rewrite)
ARCHITECTURE.md             This file: layout, ownership, data flow
SKILL.md                    Agent prompt (YAML frontmatter + English body)
README.md                   Human story + install
scripts/install.ps1         Windows installer
scripts/install.sh          Unix installer (git 100755, LF-only)
tests/check_skill.py        Structural + install acceptance
tests/test_skill_contract.py  Thin pytest wrapper around check_skill.py
.gitignore                  __pycache__/, .pytest_cache/, .grok/, .just-ten-more/
.gitattributes              scripts/install.sh text eol=lf
```

Installed skill root (`musk-backlog/`): `SKILL.md`, `README.md`. Not installed: `LICENSE`, `ARCHITECTURE.md`, `scripts/`, `tests/`. There is no `references/` and no `review-log.py`.

## What each file owns

- **SKILL.md** — When to run (explicit invocation always; do not auto-load only because a musk report appeared), input (conversation, paste, or a path they named; missing report -> stop), mapping (keep / change / drop is no work item / delete-work), forge (git remote; GitHub, GitLab, other-or-none; conversation table is success), report table, then stop. Entire repo is English. Runtime may still speak the user's language. Do not start musk-algorithm, just-ten-more, or just-ten-more-loop.
- **README.md** — What it is, complementary four skills, when it triggers, quick start, install table, `GROK_HOME` / `HERMES_HOME`.
- **scripts/install.ps1**, **scripts/install.sh** — Copy `SKILL.md`, optional `README.md`, and `references/` if present. One positional arg: `grok | claude | cursor | hermes | all` (default `all`). No `review-log.py`. Shape matches musk-algorithm (neither ships that helper). just-ten-more-loop ships `scripts/review-log.py`.
- **tests/check_skill.py** — Named PASS/FAIL checks: frontmatter, mapping, forge, then stop, English-only repo files, installers, LF on `install.sh`, git mode `100755`, README paths, complementary claims, tempdir install (never the real home).
- **tests/test_skill_contract.py** — `pytest` exec of `check_skill.py`; assert returncode 0.

## Data flow

```
trigger (musk-backlog, /musk-backlog, musk backlog, explicit invocation always)
    -> load SKILL.md (agent)
    -> require a musk-algorithm report (conversation, paste, or a path they named)
    -> missing report: stop (do not re-run musk-algorithm; do not invent a report)
    -> map keep / change / drop / delete-work
    -> list the report table in the conversation
    -> classify git remote as GitHub, GitLab, or other-or-none
    -> optional tracker create only if that forge has a usable tracker and credentials
    -> no tracker / no credentials / other-or-none: conversation table is success
    -> stop
```

Do not implement. Do not open a PR/MR. Do not merge this skill into musk-algorithm. Live path is `/musk-backlog`, not `/musk-algorithm`.

## Install destinations

Repo root is the parent of `scripts/`. Home: sh `$HOME`; ps1 `$env:USERPROFILE` else `$HOME`.

| Target | Destination |
| --- | --- |
| grok | `$GROK_HOME/skills/musk-backlog` if set, else `$HOME/.grok/skills/musk-backlog` |
| hermes | `$HERMES_HOME/skills/musk-backlog` if set, else `$HOME/.hermes/skills/musk-backlog` |
| claude | `$HOME/.claude/skills/musk-backlog` (no env override) |
| cursor | `$HOME/.cursor/skills/musk-backlog` (no env override) |

`all` = grok, claude, cursor, hermes in that order. Unknown platform: ps1 `ValidateSet` / throw; sh usage and exit 2.

Tests prove install in a tempdir with `USERPROFILE=HOME=tmp` and `GROK_HOME` / `HERMES_HOME` popped. Do not install into the real user home from tests or from this design pass.
