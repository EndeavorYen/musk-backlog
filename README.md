# musk-backlog

> **TL;DR** — Turn a musk-algorithm evaluation report into forge-agnostic work items, then stop. Not an implementation pipeline. Not a PR/MR.

This is an independent agent skill. It is **not affiliated with** Elon Musk, SpaceX, Tesla, xAI, or Walter Isaacson.

Works as a Grok skill. The same `SKILL.md` copies onto Claude, Cursor, and Hermes.

## Quick start

Clone, install, then say `musk-backlog` or `/musk-backlog` and point at a musk-algorithm report (conversation, paste, or a path you named). Explicit invocation always. It does **not** auto-run after a musk report.

```powershell
.\scripts\install.ps1 grok
```

```bash
./scripts/install.sh grok
```

Use `claude`, `cursor`, `hermes`, or `all` instead of `grok`. You get a work-item table in the conversation. Tracker create is optional and only when the git remote is GitHub or GitLab with a usable tracker and credentials. Then it stops.

## Complementary

Use **[musk-algorithm](https://github.com/EndeavorYen/musk-algorithm-skill)** `/musk-algorithm` for *should this exist, who owns it, and in what order do we touch it?*

Use this skill for *turn that musk report into forge-agnostic work items, then stop.*

Use **[just-ten-more](https://github.com/EndeavorYen/just-ten-more)** `/just-ten-more` for *what is still wrong, with evidence — list up to 10 challenges, no edits, no review log.* A list-only round lives in the conversation. It is not the loop's log.

Use `/just-ten-more-loop` for *fix or block, write `.just-ten-more/review-log.jsonl` in the repository under review, then hunt again until a round finds none.*

| | musk-algorithm | musk-backlog | just-ten-more | just-ten-more-loop |
| --- | --- | --- | --- | --- |
| Job | First-principles evaluation | Map a musk report to work items, then stop | Evidence-backed hunt, list only | Evidence-backed hunt-fix loop |
| Sequence | Five steps **in order** | Map, list the table, optional tracker create | One round of up to 10 challenges | Rounds until a round finds none |
| Default | Structured report in the conversation; no evaluation file | Conversation table; then stop | List in the conversation; no review log | Fixes or blockers, plus a log |
| Edits | Only if asked, after 1–2 keep it | None | None | Fix in the same round |

Do not merge them.

## Install

One argument: `grok` | `claude` | `cursor` | `hermes` | `all`. Default `all`. Unknown platform is rejected.

| Platform | Skill root |
| --- | --- |
| grok | `~/.grok/skills/musk-backlog/` |
| claude | `~/.claude/skills/musk-backlog/` |
| cursor | `~/.cursor/skills/musk-backlog/` |
| hermes | `~/.hermes/skills/musk-backlog/` |

```text
# Windows
.\scripts\install.ps1 grok
.\scripts\install.ps1 claude
.\scripts\install.ps1 cursor
.\scripts\install.ps1 hermes
.\scripts\install.ps1 all

# Unix
./scripts/install.sh grok
./scripts/install.sh claude
./scripts/install.sh cursor
./scripts/install.sh hermes
./scripts/install.sh all
```

If `GROK_HOME` is set, the grok target is `$GROK_HOME/skills/musk-backlog/`.
If `HERMES_HOME` is set, the hermes target is `$HERMES_HOME/skills/musk-backlog/`.

Claude and Cursor always use the home paths in the table.

The destination contains `SKILL.md` and `README.md`. Restart the agent if it was already running.

Confirm:

```powershell
Test-Path "$env:USERPROFILE\.grok\skills\musk-backlog\SKILL.md"
```

```bash
test -f ~/.grok/skills/musk-backlog/SKILL.md && echo installed
```

Uninstall: delete the skill directory. Nothing else is registered.

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.grok\skills\musk-backlog"
```

```bash
rm -rf ~/.grok/skills/musk-backlog
```

Repeat for claude, cursor, and hermes if you installed `all`. If you used `GROK_HOME` or `HERMES_HOME`, delete those paths instead.

## Usage

Name this skill. Explicit invocation always. It does not auto-run after a musk report.

**Explicit (always):** `/musk-backlog`, or `musk-backlog` / `musk backlog` / `open work items from the musk report` / `musk report to issues`. Point at the musk-algorithm report in the conversation, a paste, or a path you named. Missing report: it stops. It does not re-run musk-algorithm and does not invent a report.

Forge-agnostic: git remote + default branch. Classify GitHub, GitLab, or other-or-none. Do not assume GitHub because a GitHub MCP exists. Create tracker items only when that forge has a usable tracker and credentials. No tracker is still success: the conversation table is the output. Then stop.

This skill does not implement, does not open a PR/MR, and does not start musk-algorithm, just-ten-more, or just-ten-more-loop.

Typical asks:

- `/musk-backlog` on the musk report above.
- Open work items from the musk report.
- musk report to issues (GitHub or GitLab only if that remote exists).

## Layout

```
SKILL.md                     Agent prompt
README.md                    This file
ARCHITECTURE.md              Maintainer layout and data flow
scripts/install.ps1          Windows installer
scripts/install.sh           Unix installer (git 100755, LF)
tests/                       Structural + install acceptance
```

Installed skill root: `SKILL.md`, `README.md`. There is no `review-log.py`.
