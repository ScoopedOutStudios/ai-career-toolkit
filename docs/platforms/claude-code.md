# Using ai-career-toolkit with Claude Code

## Installation

**Important:** Claude Code installs skills into the current working directory's `.claude/` folder. Run the install command from the root of the project where you want to use the toolkit.

```bash
cd /path/to/your-project
/path/to/ai-career-toolkit/scripts/install.sh --platform claude-code
```

This copies:
- Skills to `.claude/skills/<skill-name>/SKILL.md` in the current directory
- Agents to `.claude/agents/<agent-name>.md` in the current directory

## How It Works

Claude Code supports Agent Skills via `.claude/skills/` directories and sub-agent definitions via `.claude/agents/`. Once installed:

- **Skills** are discovered automatically when Claude Code reads your project context.
- **Agents** (sub-agents) can be delegated to by name.

## Project-Level Rules

Claude Code uses `CLAUDE.md` and `.claude/rules/` for project instructions. To add the toolkit's rules:

```bash
mkdir -p .claude/rules
cp /path/to/ai-career-toolkit/rules/*.mdc .claude/rules/
```

Or reference them from your `CLAUDE.md`:

```markdown
## Career Toolkit Rules
See .claude/rules/ for job-search artifact privacy and writing quality guidelines.
```

## Using Skills

In Claude Code, invoke skills naturally in conversation:

- "Evaluate this role at Stripe" — triggers `opportunity-evaluator`
- "Review my resume for this Staff Engineer role" — triggers `hm-review`
- "Run a mock interview for a systems design panel" — triggers `mock-interview-loop`

## Updating

When the toolkit is updated, pull the latest and re-run the install from your project directory:

```bash
cd /path/to/ai-career-toolkit
git pull

cd /path/to/your-project
/path/to/ai-career-toolkit/scripts/install.sh --platform claude-code
```
