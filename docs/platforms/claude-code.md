# Using ai-career-toolkit with Claude Code

## Installation

**Important:** Claude Code installs skills into the current working directory's `.claude/` folder. Run the install command from the root of the project where you want to use the toolkit.

**Preferred (CLI):**

```bash
cd /path/to/your-project
ai-career-toolkit init --platform claude-code
```

If you've already run `init` and just need to refresh after a `git pull`:

```bash
cd /path/to/your-project
ai-career-toolkit init --reinstall --platform claude-code
```

**Or with the script directly:**

```bash
cd /path/to/your-project
/path/to/ai-career-toolkit/scripts/install.sh --platform claude-code
```

This copies:
- Skills to `.claude/skills/<skill-name>/SKILL.md` in the current directory
- Agents to `.claude/agents/<agent-name>.md` in the current directory
- Rules to `.claude/rules/*.mdc` in the current directory

## How It Works

Claude Code supports Agent Skills via `.claude/skills/` directories and sub-agent definitions via `.claude/agents/`. Once installed:

- **Skills** are discovered automatically when Claude Code reads your project context.
- **Agents** (sub-agents) can be delegated to by name.

## Project-Level Rules

Claude Code uses `CLAUDE.md` and `.claude/rules/` for project instructions. The install command copies `rules/*.mdc` into `.claude/rules/` when you run it from your project root.

To refresh rules manually:

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
- "Help me prepare for my interview" — triggers `interview-prep`

## Updating

When the toolkit is updated, pull the latest and re-run the install from your project directory:

```bash
cd /path/to/ai-career-toolkit
git pull

cd /path/to/your-project
ai-career-toolkit init --reinstall --platform claude-code
```
