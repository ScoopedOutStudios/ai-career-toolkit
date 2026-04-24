# Getting Started

You've run `ai-career-toolkit init` and have a working setup. This guide helps you go deeper.

## What init set up

`init` created two locations on your machine:

| Location | What lives here | Tracked by git? |
|----------|----------------|-----------------|
| **Toolkit root** (e.g. `~/ai-career-toolkit/`) | Skills, agents, templates, scripts, `config/settings.yaml` | Only the repo itself; `config/` is gitignored |
| **`~/.ai-career-toolkit/`** | Your role thesis, target company lists, interview notes, weekly reviews | No — this is private to you |

**Why two directories?** The toolkit root contains the shared, version-controlled code. Your personal career data stays outside the repo so you never accidentally commit it to a public fork.

## Deepen your personalization

`init` collected the basics (role, level, domains). These additional files make the toolkit significantly more effective:

### Voice pack (~15 min)

The voice pack powers the `in-my-voice` skill. Without it, rewrites use a generic professional tone.

1. Edit the files in `config/voice-pack/` (created by setup with starter content).
2. Replace placeholder content with your actual writing patterns.
3. Fastest approach: ask your AI agent to "analyze these 5-10 writing samples and generate a voice profile" — paste emails, LinkedIn posts, or docs you've written.

See [customization-guide.md](customization-guide.md) for details.

### Full role thesis (~10 min)

`init` seeded the Must-Haves and Non-Negotiables. Fill in the rest of `~/.ai-career-toolkit/role-thesis.md`:

- **Value Proposition** — 2-3 sentences on what you uniquely bring + 3-5 proof points. Used by `hm-review` and `career-guide`.
- **Nice-to-Haves** — preferred industry, product stage, company stage. Feeds `target-list-generator` tier scoring.
- **Quick Filter Checklist** — `opportunity-evaluator` uses this for fast pass/fail screening.

### Story bank (~30 min to start)

Use `templates/interview-story-system.md` as the framework:

1. Map your experience to the 8 story templates.
2. Use the `star-story` skill to draft each one.
3. Prepare 2-minute and 5-minute versions.
4. Use `mock-interview-loop` to practice and refine.

### Self-assessment (~15 min)

Use `templates/role-expectation-rubric.md` to score yourself across 8 dimensions (1-5). This surfaces your top gaps so you can build targeted STAR stories.

## Your first prompts

Paste any of these into your AI agent. They reference your config files automatically.

**Build your target list:**
> "Build me a target company list for my configured domains. Use my settings in config/settings.yaml and my role thesis."

**Evaluate a specific opportunity:**
> "Evaluate this opportunity at [Company Name]. Here's the JD: [paste the full job description]"

**Review your resume:**
> "Review my resume against this Staff Engineer posting at [Company]. Here's the JD: [paste]. Here's my resume: [paste or point to file]."

**Practice for an interview:**
> "Run a mock interview for a systems design panel at [Company]. Focus on distributed systems."

**Draft outreach:**
> "Draft a referral request to send to my contact at [Company]. I'm interested in their [team/role]. Use my voice pack."

For the full skill and agent reference, see the [Playbook](playbook.md).

## Ongoing workflow

Refer to `workflow-docs/operating-workflow.md` for the full methodology:

- **Daily**: Pick up to 3 priorities, execute, close what's done.
- **Weekly**: Review pipeline health, close stale opportunities, retier companies.
- **Per-opportunity**: Run `opportunity-evaluator` before investing significant time.
- **Per-interview**: Run mock loops, select stories, prepare questions.

For building and merging target company lists, see [company-list-pipeline.md](../workflow-docs/company-list-pipeline.md).

## Re-running and updating

| Situation | Command |
|-----------|---------|
| Changing your job search targets | `ai-career-toolkit personalize` |
| Pulled new toolkit updates | `ai-career-toolkit install --platform cursor` (or `claude-code`) |
| Something seems broken | `ai-career-toolkit verify` |
| Starting fresh or filling gaps | `ai-career-toolkit init` (idempotent — skips what's already done) |
