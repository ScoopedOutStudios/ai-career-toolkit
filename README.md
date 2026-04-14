# ai-career-toolkit

AI-powered career toolkit: skills, frameworks, and templates for structured job search — works with any agentic AI system.

## What This Is

A collection of composable AI agent skills, templates, and workflow documentation for running a disciplined, structured job search. Designed to work with **any AI agentic system** that supports skills and sub-agents (Cursor, Claude Code, and others).

Currently focused on **software engineering and tech roles**. Non-tech role support is planned as a future milestone.

## What's Included

### Skills (9)

AI agent skills that follow the [Agent Skills](https://agentskills.io) format (`SKILL.md` with YAML frontmatter):

| Skill | Purpose |
|-------|---------|
| **opportunity-evaluator** | Evaluate a company + role with structured scoring and pursue/park/skip recommendation |
| **target-list-generator** | Build a scored, tiered list of target companies from your criteria |
| **hm-review** | Dual-lens resume/application review (recruiter + hiring manager perspective) |
| **mock-interview-loop** | Iterative mock interviews with 1-5 scoring and feedback |
| **star-story** | Build and refine STAR stories for behavioral interviews |
| **social-content** | LinkedIn posts, recruiter outreach, referral requests, follow-ups |
| **content-review** | Structured editorial review with rewrite and rationale |
| **tech-content-review** | Technical writing review with audience-adaptive calibration |
| **in-my-voice** | Rewrite content to match your personal voice using a voice pack |

### Agents (3)

Agent definitions that orchestrate skills:

| Agent | Role |
|-------|------|
| **career-guide** | Career strategy, role positioning, offer tradeoffs |
| **interview-prep-coach** | Interview readiness, story building, mock practice |
| **wordsmith-editor** | Editorial specialist for all job-search writing |

### Templates (5)

Reusable frameworks for career planning:

- **Role Thesis** — Define your target role, value prop, and search criteria
- **Role Expectation Rubric** — Multi-level IC track scoring (Mid through Principal)
- **Interview Story System** — STAR story bank framework with interview loop mapping
- **AI Leverage Case Sheet** — Templates for discussing AI usage in interviews
- **Cover Letter** — Clean, professional template with placeholders

### Workflow Documentation

Tool-agnostic methodology for running a job search:
- Pipeline stages and health metrics
- Daily operating cadence with WIP limits
- Weekly review process
- Tier-based company targeting

## Quick Start

### 1. Clone

```bash
git clone https://github.com/ScoopedOutStudios/ai-career-toolkit.git
cd ai-career-toolkit
```

### 2. Setup

```bash
./setup.sh
```

This creates:
- `./config/` — your local toolkit settings (gitignored)
- `~/.ai-career-toolkit/` — your personal career data (outside the repo)

### 3. Customize

- Edit `config/settings.yaml` with your preferences
- Fill out `~/.ai-career-toolkit/role-thesis.md` with your target role
- Optionally build your voice pack in `config/voice-pack/`

### 4. Install into your AI platform

```bash
# Auto-detect platform
./scripts/install.sh

# Or specify explicitly
./scripts/install.sh --platform cursor
./scripts/install.sh --platform claude-code
```

### 5. Use

In your AI agent, invoke skills by name:

- "Evaluate this opportunity at ExampleCorp" (triggers `opportunity-evaluator`)
- "Build me a target company list for AI/ML roles" (triggers `target-list-generator`)
- "Review my resume for this role" (triggers `hm-review`)
- "Let's do a mock interview for a Staff Engineer panel" (triggers `mock-interview-loop`)
- "Help me write a STAR story about my distributed systems project" (triggers `star-story`)

## Platform Support

| Platform | Status | Install Method |
|----------|--------|----------------|
| Cursor | Supported | `./scripts/install.sh --platform cursor` |
| Claude Code | Supported | `./scripts/install.sh --platform claude-code` |
| Others | Compatible | Skills use standard Agent Skills format; see `docs/platforms/` |

## Data Privacy

This toolkit is designed with privacy as a core principle:

- **No personal data in the repo.** All personal information stays in gitignored `config/` or in `~/.ai-career-toolkit/`.
- **Two-tier storage.** Toolkit settings in `./config/` (project-scoped), personal career data in `~/.ai-career-toolkit/` (identity-scoped, outside any repo).
- **Templates use placeholders.** `{{YourName}}`, `{{Company}}`, etc.
- **Privacy rules included.** `rules/job-artifact-privacy.mdc` enforces sanitization guardrails.

## Project Structure

```
ai-career-toolkit/
├── skills/              # AI agent skills (SKILL.md format)
├── agents/              # Agent definitions
├── templates/           # Reusable career frameworks
├── rules/               # Agent behavior rules
├── workflow-docs/       # Job search methodology
├── config/              # Your local settings (gitignored)
├── config.example/      # Example config to copy
├── docs/                # Platform guides and customization
├── scripts/             # Setup and install scripts
├── setup.sh             # First-run setup
├── LICENSE              # MIT
└── README.md
```

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md).

## License

MIT
