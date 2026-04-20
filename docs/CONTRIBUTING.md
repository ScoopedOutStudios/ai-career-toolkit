# Contributing to ai-career-toolkit

Thanks for your interest in contributing. This toolkit is opinionated and maintained when useful — contributions that align with the project's goals are welcome.

**Environment:** bash on macOS, Linux, or WSL. There is no Node or Python requirement for core setup/install.

## What We're Looking For

- New skills that fill gaps in the job search workflow
- Improvements to existing skill instructions (clearer, more effective)
- Template improvements based on real interview feedback
- Platform support guides for new AI agent systems
- Bug fixes in setup/install scripts

## What We're Not Looking For

- Personal data, career details, or company-specific content
- Platform-specific features that break the agent-agnostic design
- Complex build tooling (this is markdown and bash — keep it simple)
- AI-generated PRs without meaningful review

## How to Contribute

1. Fork the repo
2. Create a branch for your change
3. Make your changes following the conventions below
4. Test: run `./setup.sh --dry-run` and `./scripts/install.sh --dry-run --platform cursor` (use `--platform claude-code` from a throwaway directory if you prefer — it only prints copy targets)
5. Submit a PR with a clear description of what changed and why

## Conventions

### Skills

- Follow the [Agent Skills](https://agentskills.io) format
- One directory per skill with a `SKILL.md` file
- YAML frontmatter must include `name` and `description`
- Description should explain when to use the skill (for agent discovery)
- Keep instructions clear and actionable

### Agents

- One `.md` file per agent in `agents/`
- YAML frontmatter: `name`, `description`, `readonly: true`
- Do not include platform-specific model slugs
- Document handoff rules to other agents/skills

### Templates

- Use `{{Placeholder}}` syntax for user-specific data
- No personal information, real company names, or dates that tie to a specific person
- Include clear instructions on how to fill out the template

### Privacy

- Never commit personal data, even as examples
- Use obviously-fake placeholder data in examples
- When in doubt, ask

## Code of Conduct

Be respectful, constructive, and focused on making the toolkit better for everyone.