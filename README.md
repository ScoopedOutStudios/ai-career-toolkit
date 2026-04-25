# ai-career-toolkit

Stop winging your job search. Run it like an engineering system.

## What This Does


| Without the toolkit                                 | With the toolkit                                                                                |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Manually researching each company in browser tabs   | `opportunity-evaluator` scores a company + role and gives you a pursue/park/skip recommendation |
| Spreadsheet of company names with no prioritization | `target-list-generator` builds a scored, tiered target list from your criteria                  |
| Generic resume sent everywhere                      | `hm-review` reviews your materials through recruiter and hiring manager lenses                  |
| Inconsistent interview answers                      | `mock-interview-loop` runs scored practice rounds with specific feedback                        |
| Rough notes that aren't interview-ready             | `star-story` converts experience into tight STAR narratives                                     |
| Outreach messages that sound like templates         | `social-content` + `in-my-voice` produce authentic, personal outreach                           |
| No idea what "Staff Engineer" means at company X    | `research-guru` digs up eng culture, comp data, hiring signals, and sentiment                   |


**Local files, no toolkit backend.** Your data stays on disk under `./config/` and `~/.ai-career-toolkit/`. This repo does not create accounts or run a server. When you use skills through Cursor, Claude Code, or another host, **that platform's normal data-handling and model-provider policies apply**.

## First value in ~30 minutes

1. **Install** the toolkit (pip/pipx or git clone — see [Quick Start](#quick-start) below).
2. **Run `ai-career-toolkit init`** — one command that sets up files, collects your targeting criteria (role, level, domains), installs into your AI platform, and verifies everything.
3. **Paste the prompts** it gives you into your agent — build a scored target company list, then evaluate a specific opportunity with a JD.

## Quick Start

Pick **one** path:

### Path A — pip / pipx + CLI (recommended)

```bash
pipx install git+https://github.com/ScoopedOutStudios/ai-career-toolkit.git
# or: python3 -m pip install --user git+https://github.com/ScoopedOutStudios/ai-career-toolkit.git

ai-career-toolkit init
```

`init` walks you through everything: personalization (interactive menus for role, level, domains, must-haves), platform install (Cursor / Claude Code with local or global scope), and verification. Re-running `init` is safe — it skips completed steps and fills in anything missing.

### Path B — git clone + bash

```bash
git clone https://github.com/ScoopedOutStudios/ai-career-toolkit.git
cd ai-career-toolkit
./setup.sh                       # scaffold config + data directories
pip install -e .                 # optional: enables the CLI for verify/personalize
ai-career-toolkit init           # personalize + install + verify in one step
```

### After setup

Open your AI agent and talk naturally:

- "Evaluate this opportunity at Stripe — here's the JD: [paste]"
- "Build me a target company list for AI infrastructure roles"
- "Review my resume against this Staff Engineer posting"
- "Run a mock interview for a systems design panel"
- "Write a STAR story about my service mesh migration project"
- "Draft a referral request to send to my contact at Datadog"

The agent discovers and invokes the right skills automatically. For more prompts, see the [Playbook](docs/playbook.md). For deeper setup (voice pack, story bank, rubric), see [Getting Started](docs/GETTING_STARTED.md).

After you pull updates, re-run `ai-career-toolkit install --platform <name>` so skills, agents, and rules stay in sync. By default, Cursor installs go to `.cursor/` in your current directory (workspace-local); pass `--scope global` to install to `~/.cursor/` instead.

### CLI commands

| Command | When to use | What it does |
|---------|-------------|--------------|
| `init` | First time, or to fill gaps | Full flow: scaffold + personalize + install + verify + first prompt |
| `personalize` | Changing targets mid-search | Interactive menus for role, level, domains, geo, exclusions; seeds role thesis |
| `install --platform X [--scope local\|global]` | After `git pull` | Re-copies skills/agents/rules to your platform (default: workspace-local) |
| `verify` | Anytime, diagnostics | Checks layout, config, personalization, and platform install |

### If something goes wrong

- **"Could not auto-detect platform"** — pass `--platform cursor` or `--platform claude-code` to `init` or `install`.
- **Claude Code: skills missing** — you probably ran `install.sh` from the wrong directory; `cd` to the project that should own `.claude/` and re-run with the absolute path to `scripts/install.sh`.
- **Skills don't update** — restart Cursor / reload the window, or start a new Claude Code session.

## Prerequisites

- **bash** and a Unix-like environment (macOS, Linux, or [WSL](https://learn.microsoft.com/en-us/windows/wsl/) on Windows). A native PowerShell alternative is not yet available.
- An AI coding agent that supports **[Agent Skills](https://agentskills.io)** — tested paths are **Cursor** and **Claude Code**.
- **Python 3.10+** for the CLI (`pipx` / `pip`). The skills themselves are markdown + bash; Python is only for setup tooling.
- If `setup.sh` or `scripts/install.sh` fails with "permission denied", run `bash setup.sh` / `bash scripts/install.sh …` or `chmod +x setup.sh scripts/install.sh`.

## What's Inside

### Skills (9)

AI agent skills that follow the [Agent Skills](https://agentskills.io) format:


| Skill                     | What it does                                                                          |
| ------------------------- | ------------------------------------------------------------------------------------- |
| **opportunity-evaluator** | Evaluate a company + role with structured scoring and pursue/park/skip recommendation |
| **target-list-generator** | Build a scored, tiered list of target companies from your criteria                    |
| **hm-review**             | Dual-lens resume/application review (recruiter + hiring manager perspective)          |
| **mock-interview-loop**   | Iterative mock interviews with 1-5 scoring and feedback                               |
| **star-story**            | Build and refine STAR stories for behavioral interviews                               |
| **social-content**        | LinkedIn posts, recruiter outreach, referral requests, follow-ups                     |
| **content-review**        | Structured editorial review with rewrite and rationale                                |
| **tech-content-review**   | Technical writing review with audience-adaptive calibration                           |
| **in-my-voice**           | Rewrite content to match your personal voice using a voice pack                       |


### Agents (4)

Agent definitions that orchestrate skills and handle handoffs:


| Agent                    | Role                                                      |
| ------------------------ | --------------------------------------------------------- |
| **career-guide**         | Career strategy, role positioning, offer tradeoffs        |
| **interview-prep-coach** | Interview readiness, story building, mock practice        |
| **research-guru**        | Company intel, compensation benchmarking, market research |
| **wordsmith-editor**     | Editorial specialist for all job-search writing           |


### Templates (5)

Reusable frameworks you fill in once and reference throughout your search:

- **Role Thesis** — Define your target role, value prop, must-haves, and dealbreakers
- **Role Expectation Rubric** — Multi-level IC track scoring (Mid through Principal) based on public frameworks
- **Interview Story System** — STAR story bank framework with interview loop mapping
- **AI Leverage Case Sheet** — Templates for discussing AI usage in interviews credibly
- **Cover Letter** — Clean, professional template with placeholders

### Workflow Documentation

A tool-agnostic methodology for running a disciplined job search:

- Opportunity pipeline stages with conversion benchmarks
- Daily operating cadence with WIP limits (Today: max 3, This Week: max 8)
- Weekly review process with health metrics
- Tier-based company targeting (T1/T2/T3 with outreach priorities)
- **[Company list pipeline](workflow-docs/company-list-pipeline.md)** — profile → per-domain research → merged `target-companies.tsv`

## Platform Support


| Platform    | Status     | Install Method | Default scope |
| ----------- | ---------- | -------------- | ------------- |
| Cursor      | Supported  | `ai-career-toolkit init --platform cursor` or `./scripts/install.sh --platform cursor` | Workspace-local (`.cursor/`). Pass `--scope global` for `~/.cursor/` |
| Claude Code | Supported  | `ai-career-toolkit init --platform claude-code` or `./scripts/install.sh --platform claude-code` | Always workspace-local (`.claude/`) |
| Others      | Compatible | Skills use standard Agent Skills format; see [platform guides](docs/platforms/) | — |


Marketplace publishing (Cursor, Claude Code, Codex) is planned for future releases.

## Data Privacy

Design goals:

- **No personal data in the git-tracked tree by default.** Keep real resumes, comp, recruiter names, and employer-specific notes in `~/.ai-career-toolkit/` or another private location — not in a public fork.
- **Two-tier storage.** Toolkit settings in `./config/` (next to the clone, gitignored), personal career data in `~/.ai-career-toolkit/` (outside the clone).
- **Templates use placeholders.** `{{YourName}}`, `{{Company}}`, etc.
- **Rules ship with the toolkit.** `install.sh` copies `rules/*.mdc` into your Cursor or Claude Code rules path so agents default to safer handling of sensitive artifacts. You are still responsible for what you paste into any cloud-hosted model.

**Honest trust boundary:** the toolkit does not phone home, but **your AI platform may process prompts** according to its own policies. Treat pasted JDs and resumes as sensitive.

## Project Structure

```
ai-career-toolkit/
├── ai_career_toolkit/   # Python CLI (init / verify / install / personalize)
├── pyproject.toml       # Package metadata (hatchling)
├── skills/              # AI agent skills (SKILL.md format)
├── agents/              # Agent definitions
├── templates/           # Reusable career frameworks
├── rules/               # Agent behavior rules
├── workflow-docs/       # Job search methodology
├── config/              # Your local settings (gitignored)
├── config.example/      # Example config to copy and customize
├── docs/                # Platform guides, playbook, getting started
├── scripts/             # Install scripts
├── setup.sh             # First-run setup (bash)
├── LICENSE              # MIT
└── README.md
```

## Current focus (v1 scope)

**In scope for this public release**

- **Software engineering and technical IC** roles (individual contributor track, roughly **Mid through Principal**): backend, frontend, full-stack, platform, infrastructure, SRE, data engineering, ML engineering.
- **Artifacts:** Agent Skills, agent personas, templates, workflow docs, CLI setup tooling — **no** hosted service, **no** scoring scripts or automated ATS integrations in v1.

**Explicitly out of scope for v1**

- Non-technical job families (sales, marketing, non-technical PM, etc.) — discussion in [#1](https://github.com/ScoopedOutStudios/ai-career-toolkit/issues/1).
- Manager-only career tracks as a first-class path (some content may still be useful; the kit is IC-calibrated).
- Marketplace packaging (may come later).

## Sharing this project (e.g. LinkedIn)

Short narrative that matches v1:

- Local-first **skills + templates** for **software and technical IC** job searches (Mid–Principal).
- Covers **target companies**, **opportunity triage**, **resume/application review**, and **interview prep** — not a hosted ATS or a scoring product.
- **Open source** — clone, run `ai-career-toolkit init`, and iterate in the open.

Link the repo; invite issues and improvements that stay within the [v1 scope](#current-focus-v1-scope) so feedback stays actionable.

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md).

## License

MIT
