# ai-career-toolkit

Stop winging your job search. Run it like an engineering system.

## Prerequisites

- **bash** and a Unix-like environment (macOS, Linux, or [WSL](https://learn.microsoft.com/en-us/windows/wsl/) on Windows). Install into Cursor/Claude still uses `scripts/install.sh` (bash).
- An AI coding agent that supports **[Agent Skills](https://agentskills.io)** — tested paths are **Cursor** and **Claude Code**.
- If `setup.sh` or `scripts/install.sh` fails with “permission denied”, run `bash setup.sh` / `bash scripts/install.sh …` or mark them executable once (`chmod +x setup.sh scripts/install.sh`).
- **Optional (recommended onboarding):** **Python 3.10+** if you use the `ai-career-toolkit` CLI (`pipx` / `pip`) for guided `init`, `verify`, and `install` — same idea as [Solo OS](https://github.com/ScoopedOutStudios/solo-os). The skills themselves stay markdown + bash; Python is only the installer UX.

## The Problem

Most job searches are chaos: scattered notes in Google Docs, inconsistent interview prep, copy-pasting the same ChatGPT prompts, losing track of which companies you've contacted, and writing cover letters that sound like everyone else's. You know how to build disciplined systems at work — but your career search doesn't get the same rigor.

## What This Does

ai-career-toolkit is a set of AI agent skills, templates, and workflow frameworks that turn your job search into a structured, repeatable process. Install the skills into your AI coding agent (Cursor, Claude Code, or any system that supports [Agent Skills](https://agentskills.io)), and you get:


| Without the toolkit                                 | With the toolkit                                                                                |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Manually researching each company in browser tabs   | `opportunity-evaluator` scores a company + role and gives you a pursue/park/skip recommendation |
| Spreadsheet of company names with no prioritization | `target-list-generator` builds a scored, tiered target list from your criteria                  |
| Generic resume sent everywhere                      | `hm-review` reviews your materials through recruiter and hiring manager lenses                  |
| Inconsistent interview answers                      | `mock-interview-loop` runs scored practice rounds with specific feedback                        |
| Rough notes that aren't interview-ready             | `star-story` converts experience into tight STAR narratives                                     |
| Outreach messages that sound like templates         | `social-content` + `in-my-voice` produce authentic, personal outreach                           |
| No idea what "Staff Engineer" means at company X    | `research-guru` digs up eng culture, comp data, hiring signals, and sentiment                   |


**Local files, no toolkit backend.** Your generated notes and config live on disk under `./config/` and `~/.ai-career-toolkit/`. This repo does not create accounts or run a server. When you use skills through Cursor, Claude Code, or another host, **that platform’s normal data-handling and model-provider policies apply** (retention, logging, training — check their settings).

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

A tool-agnostic methodology for running a disciplined job search (works with any tracking tool or just local files):

- Opportunity pipeline stages with conversion benchmarks
- Daily operating cadence with WIP limits (Today: max 3, This Week: max 8)
- Weekly review process with health metrics
- Tier-based company targeting (T1/T2/T3 with outreach priorities)
- **[Company list pipeline](workflow-docs/company-list-pipeline.md)** — profile → per-domain research → merged `target-companies.tsv` (v1 stays simple: no scoring scripts)

## Quick Start (~10 minutes)

Pick **one** path: **pip/pipx + CLI** (guided `init` / `verify`) or **git clone + shell scripts** (no Python required for setup).

### Path A — pip / pipx + CLI (recommended)

Install the package (isolates CLI tools; same pattern as Solo OS):

```bash
pipx install git+https://github.com/ScoopedOutStudios/ai-career-toolkit.git
# or: python3 -m pip install --user git+https://github.com/ScoopedOutStudios/ai-career-toolkit.git
```

Guided setup materializes skills/agents/rules into a directory (default **`~/ai-career-toolkit`** when you install from PyPI, or your **git checkout** when you use `pip install -e .` from a clone), creates `config/` there, and creates **`~/.ai-career-toolkit/`** for private notes:

```bash
ai-career-toolkit init              # interactive prompts; use -y / --yes for CI-style defaults
ai-career-toolkit verify            # layout, config, data home; add --ide cursor to check ~/.cursor/*
ai-career-toolkit install --platform cursor   # runs scripts/install.sh (bash)
```

Useful options:

- `init --workspace /path` — install directory for the toolkit tree (skills, `scripts/`, etc.).
- `init --data-home /path` — override personal data root (default: `~/.ai-career-toolkit` or `AI_CAREER_TOOLKIT_HOME`).
- `verify --workspace /path` — validate a specific toolkit root.
- `verify --format json` — machine-readable check list.

After `init`, set **`AI_CAREER_TOOLKIT_ROOT`** to your toolkit directory (the CLI prints an `export` line) so docs and automation resolve the same path.

### Path B — git clone + bash

### 1. Clone

```bash
git clone https://github.com/ScoopedOutStudios/ai-career-toolkit.git
cd ai-career-toolkit
```

### 2. Setup

```bash
./setup.sh
# or: bash setup.sh
```

This creates two areas:

- `./config/` — your local toolkit settings (gitignored, stays next to the clone)
- `~/.ai-career-toolkit/` — your personal career data (outside the repo), including `source-lists/` for per-domain company drafts

### 3. Customize

- Edit `config/settings.yaml` with your target role, level, domains, and preferences
- Fill out `~/.ai-career-toolkit/role-thesis.md` with your target role details
- Optionally customize `config/voice-pack/` with your writing style (see [customization guide](docs/customization-guide.md))

### 4. Install into your AI platform

The install script copies **skills**, **agents**, and **rules** (privacy + writing quality).

**Cursor** (global install under `~/.cursor/`):

```bash
cd /path/to/ai-career-toolkit
./scripts/install.sh --platform cursor
# or auto-detect if ~/.cursor exists:
./scripts/install.sh
```

**Claude Code** — run from the **project where you want `.claude/`** (your job-search notes repo or monorepo root), not only from inside the toolkit clone:

```bash
cd /path/to/your-job-search-workspace
/path/to/ai-career-toolkit/scripts/install.sh --platform claude-code
```

Paths like `.claude/skills` are relative to your **current working directory**. See [Claude Code guide](docs/platforms/claude-code.md).

### 5. Start using it

Open your AI agent and talk naturally:

- "Evaluate this opportunity at Stripe — here's the JD: [paste]"
- "Build me a target company list for AI infrastructure roles"
- "Review my resume against this Staff Engineer posting"
- "Run a mock interview for a systems design panel"
- "Write a STAR story about my service mesh migration project"
- "Draft a referral request to send to my contact at Datadog"

The agent discovers and invokes the right skills automatically based on your request.

After you pull updates, re-run `./scripts/install.sh` for your platform so skills, agents, and rules stay in sync.

### If something goes wrong

- **“Could not auto-detect platform”** — pass `--platform cursor` or `--platform claude-code` explicitly.
- **Claude Code: skills missing** — you probably ran `install.sh` from the wrong directory; `cd` to the project that should own `.claude/` and re-run with the absolute path to `scripts/install.sh`.
- **Skills don’t update** — restart Cursor / reload the window, or start a new Claude Code session.

## First value in ~30 minutes

1. Complete **Quick Start** through install (Path A: `ai-career-toolkit init` then `ai-career-toolkit install --platform cursor`, or Path B: `setup.sh` + `scripts/install.sh`).
2. Fill at least **Quick Filter** and **Must-haves** in `~/.ai-career-toolkit/role-thesis.md`.
3. Set `targeting.domains` and your level in `config/settings.yaml` under your **toolkit root** (e.g. `~/ai-career-toolkit/config/settings.yaml` if you used the CLI default).
4. In your agent, ask for a **target company list** for one domain (triggers `target-list-generator` → `research-guru`).
5. Paste a real job description and ask for an **opportunity evaluation** (triggers `opportunity-evaluator`).

You should have a TSV under `~/.ai-career-toolkit/target-companies.tsv` and one structured pursue/park/skip write-up. That is the smallest “system is real” loop.

## Platform Support


| Platform    | Status     | Install Method                                                                  |
| ----------- | ---------- | ------------------------------------------------------------------------------- |
| Cursor      | Supported  | `./scripts/install.sh --platform cursor`                                        |
| Claude Code | Supported  | `./scripts/install.sh --platform claude-code`                                   |
| Others      | Compatible | Skills use standard Agent Skills format; see [platform guides](docs/platforms/) |


Marketplace publishing (Cursor, Claude Code, Codex) is planned for future releases.

## Data Privacy

Design goals:

- **No personal data in the git-tracked tree by default.** Keep real resumes, comp, recruiter names, and employer-specific notes in `~/.ai-career-toolkit/` or another private location — not in a public fork.
- **Two-tier storage.** Toolkit settings in `./config/` (next to the clone, gitignored), personal career data in `~/.ai-career-toolkit/` (outside the clone).
- **Templates use placeholders.** `{{YourName}}`, `{{Company}}`, etc.
- **Rules ship with the toolkit.** `install.sh` copies `rules/*.mdc` into your Cursor or Claude Code rules path so agents default to safer handling of sensitive artifacts. You are still responsible for what you paste into any cloud-hosted model.

**Honest trust boundary:** the toolkit does not phone home, but **your AI platform may process prompts** according to its own policies. Treat pasted JDs and resumes as sensitive.

## Sharing this project (e.g. LinkedIn)

Short narrative that matches v1:

- Local-first **skills + templates** for **software and technical IC** job searches (Mid–Principal).
- Covers **target companies**, **opportunity triage**, **resume/application review**, and **interview prep** — not a hosted ATS or a scoring product.
- **Open source** — clone, run `setup.sh`, install into Cursor or Claude Code, and iterate in the open.

Link the repo; invite issues and improvements that stay within the [v1 scope](#current-focus-v1-scope) so feedback stays actionable.

## Project Structure

```
ai-career-toolkit/
├── ai_career_toolkit/   # Python CLI (init / verify / install) — optional pip install
├── pyproject.toml       # Package metadata (hatchling)
├── skills/              # AI agent skills (SKILL.md format)
├── agents/              # Agent definitions
├── templates/           # Reusable career frameworks
├── rules/               # Agent behavior rules
├── workflow-docs/       # Job search methodology
├── config/              # Your local settings (gitignored)
├── config.example/      # Example config to copy and customize
├── docs/                # Platform guides and customization
├── scripts/             # Install scripts
├── setup.sh             # First-run setup (bash)
├── LICENSE              # MIT
└── README.md
```

## Current focus (v1 scope)

**In scope for this public release**

- **Software engineering and technical IC** roles (individual contributor track, roughly **Mid through Principal**): e.g. backend, frontend, full-stack, platform, infrastructure, SRE, data engineering, ML engineering — roles where the workflow and rubric fit naturally.
- **Artifacts:** Agent Skills, agent personas, templates, workflow docs, bash setup/install — **no** hosted service, **no** company-list scoring scripts or automated ATS integrations in v1.

**Explicitly out of scope for v1**

- Non-technical job families (sales, marketing, non-technical PM, etc.) — discussion in [#1](https://github.com/ScoopedOutStudios/ai-career-toolkit/issues/1).
- Manager-only career tracks as a first-class path (some content may still be useful; the kit is IC-calibrated).
- Marketplace packaging (may come later).

Prioritize companies with **tiers**, **role thesis**, and `**opportunity-evaluator`** — not a separate scoring pipeline.

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md).

## License

MIT