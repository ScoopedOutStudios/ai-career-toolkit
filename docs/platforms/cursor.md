# Using ai-career-toolkit with Cursor

## Installation

Run the install script:

```bash
./scripts/install.sh --platform cursor
```

This copies:
- Skills to `~/.cursor/skills/<skill-name>/SKILL.md`
- Agents to `~/.cursor/agents/<agent-name>.md`

Restart Cursor or reload the window if skills and agents don't appear immediately.

## How It Works

Cursor natively supports the Agent Skills format. Once installed:

- **Skills** are automatically discovered by Cursor's agent and can be invoked by name or triggered by matching descriptions.
- **Agents** appear as available sub-agents that can be delegated to.
- **Rules** in `rules/` can be copied to your project's `.cursor/rules/` directory for project-level behavior.

## Project-Level Setup

If you want the toolkit's rules active in a specific project:

```bash
mkdir -p .cursor/rules
cp /path/to/ai-career-toolkit/rules/*.mdc .cursor/rules/
```

## Using Skills

In Cursor's agent mode, you can invoke skills naturally:

- "Evaluate this role at Stripe" — triggers `opportunity-evaluator`
- "Review my resume" — triggers `hm-review`
- "Let's practice for my interview" — triggers `mock-interview-loop`

## Updating

When the toolkit is updated, re-run the install script to copy the latest versions:

```bash
cd /path/to/ai-career-toolkit
git pull
./scripts/install.sh --platform cursor
```
