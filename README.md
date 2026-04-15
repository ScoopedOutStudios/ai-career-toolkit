# ai-career-toolkit

Stop winging your job search. Run it like an engineering system.

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


All of this runs locally on your machine. No data leaves your control. No accounts to create.

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

## Quick Start (~10 minutes)

### 1. Clone

```bash
git clone https://github.com/ScoopedOutStudios/ai-career-toolkit.git
cd ai-career-toolkit
```

### 2. Setup

```bash
./setup.sh
```

This creates two directories:

- `./config/` — your local toolkit settings (gitignored, stays in repo)
- `~/.ai-career-toolkit/` — your personal career data (outside the repo entirely)

### 3. Customize

- Edit `config/settings.yaml` with your target role, level, domains, and preferences
- Fill out `~/.ai-career-toolkit/role-thesis.md` with your target role details
- Optionally customize `config/voice-pack/` with your writing style (see [customization guide](docs/customization-guide.md))

### 4. Install into your AI platform

```bash
# Auto-detect platform
./scripts/install.sh

# Or specify explicitly
./scripts/install.sh --platform cursor
./scripts/install.sh --platform claude-code
```

### 5. Start using it

Open your AI agent and talk naturally:

- "Evaluate this opportunity at Stripe — here's the JD: [paste]"
- "Build me a target company list for AI infrastructure roles"
- "Review my resume against this Staff Engineer posting"
- "Run a mock interview for a systems design panel"
- "Write a STAR story about my service mesh migration project"
- "Draft a referral request to send to my contact at Datadog"

The agent discovers and invokes the right skills automatically based on your request.

## Platform Support


| Platform    | Status     | Install Method                                                                  |
| ----------- | ---------- | ------------------------------------------------------------------------------- |
| Cursor      | Supported  | `./scripts/install.sh --platform cursor`                                        |
| Claude Code | Supported  | `./scripts/install.sh --platform claude-code`                                   |
| Others      | Compatible | Skills use standard Agent Skills format; see [platform guides](docs/platforms/) |


Marketplace publishing (Cursor, Claude Code, Codex) is planned for future releases.

## Data Privacy

This toolkit is designed with privacy as a core principle:

- **No personal data in the repo.** All personal information stays in gitignored `config/` or in `~/.ai-career-toolkit/`.
- **Two-tier storage.** Toolkit settings in `./config/` (project-scoped), personal career data in `~/.ai-career-toolkit/` (identity-scoped, outside any repo).
- **Templates use placeholders.** `{{YourName}}`, `{{Company}}`, etc.
- **Privacy rules included.** `rules/job-artifact-privacy.mdc` enforces sanitization guardrails when your agent writes career artifacts.

## Project Structure

```
ai-career-toolkit/
├── skills/              # AI agent skills (SKILL.md format)
├── agents/              # Agent definitions
├── templates/           # Reusable career frameworks
├── rules/               # Agent behavior rules
├── workflow-docs/       # Job search methodology
├── config/              # Your local settings (gitignored)
├── config.example/      # Example config to copy and customize
├── docs/                # Platform guides and customization
├── scripts/             # Install scripts
├── setup.sh             # First-run setup
├── LICENSE              # MIT
└── README.md
```

## Current Focus

This release targets **software engineering and tech roles** (IC track: Mid through Principal). Support for non-tech roles (sales, marketing, product, design, ops) is tracked in [#1](https://github.com/ScoopedOutStudios/ai-career-toolkit/issues/1).

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md).

## License

MIT