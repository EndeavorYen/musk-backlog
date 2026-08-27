#!/usr/bin/env python3
"""Structural acceptance checks for musk-backlog. Run from the skill root."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
README_PATH = ROOT / "README.md"
SOURCES_PATH = ROOT / "references" / "sources.md"

CJK = re.compile(r"[\u4e00-\u9fff]")


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    rest = text[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
    elif rest.startswith("\n"):
        rest = rest[1:]
    match = re.search(r"\n---\s*(?:\n|$)", rest)
    if not match:
        return "", text
    return rest[: match.start()], rest[match.end() :]


def markdown_row(text: str, start: str) -> list[str]:
    line = next((ln for ln in text.splitlines() if ln.startswith(start)), "")
    if not line.strip():
        return []
    return [part.strip() for part in line.strip().strip("|").split("|")]


def _posix_shell() -> str | None:
    if os.name != "nt":
        return "bash"
    git_bash = Path(r"C:\Program Files\Git\bin\bash.exe")
    if git_bash.is_file():
        return str(git_bash)
    return None


def _run(cmd: list[str], env: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


def _run_install(platform: str, env: dict) -> subprocess.CompletedProcess[str]:
    if os.name == "nt":
        return _run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts" / "install.ps1"),
                platform,
            ],
            env,
        )
    return _run(["bash", str(ROOT / "scripts" / "install.sh"), platform], env)


def _copied_equal(dest: Path, src: Path) -> bool:
    return dest.is_file() and src.is_file() and dest.read_bytes() == src.read_bytes()


def main() -> int:
    skill = read_text(SKILL_PATH) or ""
    readme = read_text(README_PATH) or ""
    fm, body = split_frontmatter(skill)
    body_l = body.lower()
    fm_l = fm.lower()
    checks: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        checks.append((name, bool(ok)))

    check("SKILL.md frontmatter name musk-backlog", bool(re.search(r"(?m)^name:\s*musk-backlog\s*$", fm)))
    check("description contains musk-backlog", "musk-backlog" in fm)
    check("description contains musk backlog", "musk backlog" in fm)
    check("description contains /musk-backlog", "/musk-backlog" in fm)
    check("description says explicit invocation always", "explicit invocation always" in fm_l)
    check(
        "description says do not use to implement",
        "do not use to implement" in fm_l or "not to implement" in fm_l,
    )
    check("description contains open work items from the musk report", "open work items from the musk report" in fm_l)
    check("description contains musk report to issues", "musk report to issues" in fm_l)
    check("description forbids opening a PR/MR", "pr/mr" in fm_l)
    check("description forbids running just-ten-more", "just-ten-more" in fm_l)
    check("description forbids re-running musk-algorithm", "musk-algorithm" in fm_l)

    check("body mapping keep", "keep" in body_l)
    check("body mapping change", "change" in body_l)
    check(
        "body mapping drop is no work item",
        "drop is no work item" in body_l or ("drop" in body_l and "no work item" in body_l),
    )
    check("body mapping delete-work", "delete-work" in body_l)
    check("body mentions accelerate:no", "accelerate:no" in body_l.replace(" ", ""))
    check("body mentions automate:no", "automate:no" in body_l.replace(" ", ""))

    check("body forge git remote", "git remote" in body_l)
    check("body forge GitHub", "github" in body_l)
    check("body forge GitLab", "gitlab" in body_l)
    check(
        "body forge other-or-none or no tracker",
        "other-or-none" in body_l or "no tracker" in body_l,
    )
    check("body conversation table is success", "conversation table is success" in body_l)
    check(
        "body never invent GitHub",
        "never invent a github" in body_l or "never invent github" in body_l,
    )
    check(
        "body do not assume GitHub because MCP exists",
        "do not assume github because" in body_l and "mcp" in body_l,
    )
    check("body then stop", "then stop" in body_l)
    check(
        "body does not open a pull request or merge request",
        "does not open a pull request" in body_l and "merge request" in body_l,
    )
    check("body does not start musk-algorithm", "do not start musk-algorithm" in body_l)
    check(
        "body does not start just-ten-more",
        "do not start a just-ten-more hunt or just-ten-more-loop" in body_l
        or re.search(r"do not start\s+just-ten-more", body_l) is not None,
    )
    check("SKILL.md mentions just-ten-more-loop", "just-ten-more-loop" in body)
    check(
        "SKILL.md says just-ten-more does not write a review log",
        "does not write a review log" in body_l,
    )
    check("SKILL.md says just-ten-more does not fix", "it does not fix" in body_l)
    check(
        "SKILL.md forbids starting just-ten-more-loop",
        "do not start a just-ten-more hunt or just-ten-more-loop" in body_l,
    )
    check(
        "SKILL.md does not equate the hunt-fix loop with just-ten-more",
        re.search(r"that loop is just-ten-more(?!-loop)", body_l) is None,
    )
    check(
        "SKILL.md routes list-only asks to just-ten-more",
        re.search(r"stop this skill\s+and use just-ten-more(?!-loop)", body_l) is not None,
    )
    check(
        "SKILL.md routes hunt-fix-log asks to just-ten-more-loop",
        re.search(r"stop this skill\s+and use just-ten-more-loop", body_l) is not None,
    )
    check(
        "SKILL.md routes evaluate asks to musk-algorithm",
        re.search(r"stop this skill\s+and use musk-algorithm", body_l) is not None,
    )
    check("SKILL.md report table has id column", "id" in body_l and "source" in body_l)
    check("SKILL.md report table source keep/change/delete-work", "source is keep, change, or delete-work" in body_l)
    check("SKILL.md report table tracker github/gitlab/none", "tracker is github, gitlab, or none" in body_l)
    check("SKILL.md missing report stops", "missing report" in body_l and "stop" in body_l)
    check("SKILL.md does not invent a report", "do not invent a report" in body_l)
    check("SKILL.md does not write a file to preserve memory", "do not write a file to preserve memory" in body_l)
    check(
        "SKILL.md does not auto-load only because a musk report appeared",
        "do not auto-load only because a musk report appeared" in body_l,
    )
    check("no review-log.py in this skill", not (ROOT / "scripts" / "review-log.py").is_file())

    english_files = [
        SKILL_PATH,
        README_PATH,
        ROOT / "ARCHITECTURE.md",
        ROOT / "scripts" / "install.ps1",
        ROOT / "scripts" / "install.sh",
        ROOT / "tests" / "check_skill.py",
        ROOT / "tests" / "test_skill_contract.py",
    ]
    if SOURCES_PATH.is_file():
        english_files.append(SOURCES_PATH)
    for path in english_files:
        text = read_text(path) or ""
        check(f"{path.relative_to(ROOT).as_posix()} is English", not CJK.search(text))
    check("SKILL.md body is English", not CJK.search(body))
    check("README mentions musk-algorithm", "musk-algorithm" in readme)
    check("README mentions just-ten-more", "just-ten-more" in readme)
    check("README mentions just-ten-more-loop", "just-ten-more-loop" in readme)
    check("README says just-ten-more has no review log", "no review log" in readme.lower())
    check(
        "README says a list-only round is not the loop's log",
        "not the loop's log" in readme.lower(),
    )
    readme_default = markdown_row(readme, "| Default |")
    check("README Default row has five columns", len(readme_default) == 5)
    check(
        "README musk-algorithm Default is conversation, no evaluation file",
        len(readme_default) == 5
        and "conversation" in readme_default[1].lower()
        and "no evaluation file" in readme_default[1].lower(),
    )
    check(
        "README just-ten-more Default is no review log",
        len(readme_default) == 5
        and "no review log" in readme_default[3].lower()
        and "plus a log" not in readme_default[3].lower(),
    )
    check(
        "README just-ten-more-loop Default includes a log",
        len(readme_default) == 5 and "plus a log" in readme_default[4].lower(),
    )
    readme_edits = markdown_row(readme, "| Edits |")
    check(
        "README just-ten-more Edits is None",
        len(readme_edits) == 5 and readme_edits[3] == "None",
    )
    check(
        "README musk-backlog Edits is None",
        len(readme_edits) == 5 and readme_edits[2] == "None",
    )
    check(
        "README just-ten-more-loop Edits is fix in the same round",
        len(readme_edits) == 5 and "fix in the same round" in readme_edits[4].lower(),
    )
    arch = read_text(ROOT / "ARCHITECTURE.md") or ""
    check("ARCHITECTURE mentions just-ten-more-loop", "just-ten-more-loop" in arch)
    check("ARCHITECTURE live path is /musk-backlog", "/musk-backlog" in arch)
    check("ARCHITECTURE live path is not /musk-algorithm", "not `/musk-algorithm`" in arch or "not /musk-algorithm" in arch)
    helper_cols = markdown_row(arch, "| Helper |")
    check("ARCHITECTURE helper row has five columns", len(helper_cols) == 5)
    check(
        "ARCHITECTURE musk-algorithm helper is None",
        len(helper_cols) == 5 and helper_cols[1] == "None",
    )
    check(
        "ARCHITECTURE musk-backlog helper is None",
        len(helper_cols) == 5 and helper_cols[2] == "None",
    )
    check(
        "ARCHITECTURE just-ten-more helper is None",
        len(helper_cols) == 5 and helper_cols[3] == "None",
    )
    check(
        "ARCHITECTURE loop helper is review-log.py",
        len(helper_cols) == 5 and "review-log.py" in helper_cols[4],
    )
    arch_default = markdown_row(arch, "| Default output |")
    check(
        "ARCHITECTURE musk-algorithm Default output is conversation, no evaluation file",
        len(arch_default) == 5
        and "conversation" in arch_default[1].lower()
        and "no evaluation file" in arch_default[1].lower(),
    )
    check(
        "ARCHITECTURE just-ten-more Default output is no review log",
        len(arch_default) == 5
        and "no review log" in arch_default[3].lower()
        and "review log" not in arch_default[3].lower().replace("no review log", ""),
    )
    check(
        "ARCHITECTURE just-ten-more-loop Default output includes a review log",
        len(arch_default) == 5 and "review log" in arch_default[4].lower(),
    )
    gitignore = read_text(ROOT / ".gitignore") or ""
    check(".gitignore lists .just-ten-more/", ".just-ten-more/" in gitignore)
    ignore_proc = subprocess.run(
        ["git", "check-ignore", "-q", "--", ".just-ten-more/review-log.jsonl"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    check(
        "git ignores .just-ten-more/review-log.jsonl",
        ignore_proc.returncode == 0,
    )
    check("scripts/install.ps1 exists", (ROOT / "scripts" / "install.ps1").is_file())
    check("scripts/install.sh exists", (ROOT / "scripts" / "install.sh").is_file())
    check("install.sh has no CR", b"\r" not in (ROOT / "scripts" / "install.sh").read_bytes())
    gitattributes = read_text(ROOT / ".gitattributes") or ""
    check("gitattributes forces install.sh LF", "scripts/install.sh" in gitattributes and "eol=lf" in gitattributes)
    mode = subprocess.run(
        ["git", "ls-files", "-s", "scripts/install.sh"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    check("install.sh is executable in git", mode.stdout.startswith("100755"))
    check("README install path", "~/.grok/skills/musk-backlog/" in readme)
    check("README documents GROK_HOME", "GROK_HOME" in readme)
    check("README hermes install path", "~/.hermes/skills/musk-backlog/" in readme)
    check("README documents HERMES_HOME", "HERMES_HOME" in readme)

    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "dest"
        dest.mkdir()
        env = {
            **{k: v for k, v in os.environ.items()},
            "USERPROFILE": str(dest),
            "HOME": str(dest),
        }
        env.pop("GROK_HOME", None)
        env.pop("HERMES_HOME", None)
        proc = _run_install("grok", env)
        installed = dest / ".grok" / "skills" / "musk-backlog"
        src_skill = SKILL_PATH.read_text(encoding="utf-8") if SKILL_PATH.is_file() else ""
        src_readme = README_PATH.read_text(encoding="utf-8") if README_PATH.is_file() else ""
        check(
            "install grok copies SKILL.md",
            proc.returncode == 0 and (installed / "SKILL.md").is_file(),
        )
        check("install grok copies README.md", (installed / "README.md").is_file())
        check(
            "copied SKILL.md matches source",
            _copied_equal(installed / "SKILL.md", SKILL_PATH) and bool(src_skill),
        )
        check(
            "copied README.md matches source",
            _copied_equal(installed / "README.md", README_PATH) and bool(src_readme),
        )
        if SOURCES_PATH.is_file():
            copied_sources = installed / "references" / "sources.md"
            check("install grok copies references/sources.md", copied_sources.is_file())
            check(
                "copied references/sources.md matches source",
                _copied_equal(copied_sources, SOURCES_PATH),
            )

        proc_all = _run_install("all", env)
        check("install all succeeds", proc_all.returncode == 0)
        check(
            "install all copies claude SKILL.md",
            (dest / ".claude" / "skills" / "musk-backlog" / "SKILL.md").is_file(),
        )
        check(
            "install all copies cursor SKILL.md",
            (dest / ".cursor" / "skills" / "musk-backlog" / "SKILL.md").is_file(),
        )
        check(
            "install all copies hermes SKILL.md",
            (dest / ".hermes" / "skills" / "musk-backlog" / "SKILL.md").is_file(),
        )

        hhome = dest / "custom-hermes"
        env_hermes = {**env, "HERMES_HOME": str(hhome)}
        proc_hermes = _run_install("hermes", env_hermes)
        hermes_installed = hhome / "skills" / "musk-backlog"
        check(
            "HERMES_HOME dest copies SKILL.md",
            proc_hermes.returncode == 0 and (hermes_installed / "SKILL.md").is_file(),
        )

        ghome = dest / "custom-grok"
        env_home = {**env, "GROK_HOME": str(ghome)}
        proc_home = _run_install("grok", env_home)
        grok_installed = ghome / "skills" / "musk-backlog"
        check(
            "GROK_HOME dest copies SKILL.md",
            proc_home.returncode == 0 and (grok_installed / "SKILL.md").is_file(),
        )
        check(
            "GROK_HOME dest copies README.md",
            (grok_installed / "README.md").is_file(),
        )
        if SOURCES_PATH.is_file():
            check(
                "GROK_HOME dest copies references/sources.md",
                (grok_installed / "references" / "sources.md").is_file(),
            )

        if os.name == "nt":
            bad_ps = _run_install("nope", env)
            check("install.ps1 rejects unknown platform", bad_ps.returncode != 0)

        shell = _posix_shell()
        if shell is None and os.name == "nt":
            check("install.sh checks skipped without posix shell", True)
        else:
            check("posix shell available to test install.sh", shell is not None)
        if shell:
            bad_sh = _run([shell, str(ROOT / "scripts" / "install.sh"), "nope"], env)
            check("install.sh rejects unknown platform", bad_sh.returncode != 0)
            sh_home = dest / "sh-home"
            sh_home.mkdir()
            env_sh = {**env, "HOME": str(sh_home)}
            env_sh.pop("GROK_HOME", None)
            proc_sh = _run([shell, str(ROOT / "scripts" / "install.sh"), "grok"], env_sh)
            sh_skill = sh_home / ".grok" / "skills" / "musk-backlog" / "SKILL.md"
            check(
                "install.sh grok copies SKILL.md",
                proc_sh.returncode == 0 and sh_skill.is_file(),
            )
            if SOURCES_PATH.is_file():
                sh_sources = sh_home / ".grok" / "skills" / "musk-backlog" / "references" / "sources.md"
                check("install.sh grok copies references/sources.md", sh_sources.is_file())

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
