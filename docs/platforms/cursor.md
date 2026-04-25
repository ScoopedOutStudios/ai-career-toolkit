# Using ai-career-toolkit with Cursor

## Installation

**Preferred (CLI):**

```bash
ai-career-toolkit install --platform cursor
```

**Or with the script directly:**

```bash
cd /path/to/ai-career-toolkit
./scripts/install.sh --platform cursor
```

By default, this installs to `.cursor/` in the **current directory** (workspace-local):

- Skills to `.cursor/skills/<skill-name>/SKILL.md`
- Agents to `.cursor/agents/<agent-name>.md`
- Rules to `.cursor/rules/*.mdc`

To install globally (available in all Cursor workspaces), pass `--scope global`:

```bash
ai-career-toolkit install --platform cursor --scope global
# Installs to ~/.cursor/skills/, ~/.cursor/agents/, ~/.cursor/rules/
```

Restart Cursor or reload the window if skills, agents, or rules don't appear immediately.

## How It Works

Cursor natively supports the Agent Skills format. Once installed:

- **Skills** are automatically discovered by Cursor's agent and can be invoked by name or triggered by matching descriptions.
- **Agents** appear as available sub-agents that can be delegated to.
- **Rules** apply privacy and writing-quality guardrails to agent interactions.

## Local vs Global Install

| Scope | Location | When to use |
|-------|----------|-------------|
| **local** (default) | `.cursor/{skills,agents,rules}/` in current directory | Workspace-specific setup; keeps toolkit scoped to one project |
| **global** | `~/.cursor/{skills,agents,rules}/` | Available across all Cursor workspaces without per-project installs |

If you use the **local** scope, run the install command from the directory you open in Cursor.

## Using Skills

In Cursor's agent mode, you can invoke skills naturally:

- "Evaluate this role at Stripe" — triggers `opportunity-evaluator`
- "Review my resume" — triggers `hm-review`
- "Let's practice for my interview" — triggers `mock-interview-loop`

## Updating

When the toolkit is updated, re-run the install to copy the latest versions:

```bash
cd /path/to/ai-career-toolkit
git pull
ai-career-toolkit install --platform cursor
```
