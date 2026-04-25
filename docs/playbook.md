# Playbook

A practical reference for using ai-career-toolkit day to day. What to ask, which skill handles it, and ready-to-paste prompts.

> **Prerequisite:** Run `ai-career-toolkit init` to set up your config files. The prompts below assume `config/settings.yaml` and `~/.ai-career-toolkit/role-thesis.md` are personalized. If they aren't, run `ai-career-toolkit init --personalize` first.

## Jobs-to-be-done → skill matrix

| I want to... | Skill | Agent (if routed) |
|--------------|-------|-------------------|
| Build a list of target companies | `target-list-generator` | `research-guru` for per-company intel |
| Evaluate a specific opportunity (pursue / park / skip) | `opportunity-evaluator` | `research-guru` for company research, `career-guide` for fit |
| Get my resume reviewed for a role | `hm-review` | — |
| Prepare for an interview (stories, mock practice, prep plan) | `interview-prep` | — |
| Draft a LinkedIn post or outreach message | `social-content` | `wordsmith-editor` for polish |
| Request a referral from a contact | `social-content` | — |
| Make my writing sound like me | `in-my-voice` | `wordsmith-editor` |
| Review/polish a draft (professional or technical) | `content-review` | `wordsmith-editor` |
| Research a company's eng culture and comp | _(ask directly)_ | `research-guru` |
| Get career strategy advice or compare offers | _(ask directly)_ | `career-guide` |

## Agent cheat sheet

The toolkit includes three agent personas. Your AI platform can delegate to them automatically, or you can invoke them by name.

### research-guru
**When:** You need factual evidence — company intel, comp data, hiring signals, market context.
**Returns:** Structured findings with source citations, confidence levels, and gaps.
**Handoffs:** Receives requests from `opportunity-evaluator` and `target-list-generator`.

### career-guide
**When:** You need strategic advice — role positioning, offer tradeoffs, career trajectory.
**Returns:** A recommendation, tradeoffs, risks, and 3 next actions.
**Handoffs:** Delegates to `research-guru` for evidence, `wordsmith-editor` for rewrites.

### wordsmith-editor
**When:** You need writing polished — resumes, outreach, LinkedIn, technical content.
**Returns:** Edited drafts with rationale for changes.
**Handoffs:** Uses `content-review`, `in-my-voice`, `social-content`, `hm-review` skills.

## Copy-paste prompts

These are ready to paste into your AI agent. Replace bracketed placeholders with your specifics.

### Target company list
> Build me a target company list for my configured domains. Use my settings in config/settings.yaml and my role thesis in ~/.ai-career-toolkit/role-thesis.md. Focus on companies that are actively hiring.

### Opportunity evaluation
> Evaluate this opportunity at [Company Name]. Here's the JD:
>
> [paste the full job description]
>
> Score it against my role thesis and give me a pursue/park/skip recommendation.

### Resume review
> Review my resume against this [Level] [Role] posting at [Company]. Here's the JD: [paste]. Here's my resume: [paste or path to file]. Give me both the recruiter screen and hiring manager perspectives.

### Interview prep — STAR story
> Write a STAR story about [brief description of your experience]. Make it tight enough for a 2-minute answer and include a 5-minute expanded version.

### Interview prep — mock practice
> Run a mock interview for a [interview type: systems design / behavioral / coding] panel at [Company]. I'm interviewing for a [Level] [Role] position. Score my answers 1-5 and give specific feedback.

### Interview prep — full prep plan
> I have an interview at [Company] next week for a [Level] [Role] role. Build me a prep plan: select my best STAR stories, identify gaps, and create a day-of checklist.

### Outreach and referrals
> Draft a referral request to send to my contact at [Company]. I'm interested in their [team/role]. Use my voice pack for tone.

### Company deep dive
> Research [Company Name] as a potential employer. I want: engineering culture signals, growth trajectory, leadership stability, comp positioning, and any red flags. Cite your sources.

### Career strategy
> I have offers from [Company A] and [Company B]. Compare them against my role thesis and give me a recommendation with explicit tradeoffs.

## Skill discovery and fallback

Your AI agent automatically routes requests to the right skill based on what you ask. Most of the time this works without any special syntax.

**If the wrong skill runs** (or no skill is invoked), name it explicitly:

> "Use the `interview-prep` skill to build a STAR story from these rough notes."

> "Use the `opportunity-evaluator` skill to score this role."

You can also invoke agents by name:

> "Ask `research-guru` to find engineering culture signals for [Company]."

> "Ask `career-guide` whether I should pursue this offer."

## Key config files

| File | What it does | How to edit |
|------|-------------|-------------|
| `config/settings.yaml` | Targeting criteria (role, level, domains, geo, exclusions) | `ai-career-toolkit init --personalize` or edit directly |
| `~/.ai-career-toolkit/role-thesis.md` | Your role thesis (must-haves, non-negotiables, value prop) | Edit directly — this is your most impactful file |
| `config/voice-pack/` | Your writing style profile | Ask your agent to generate from writing samples |
| `~/.ai-career-toolkit/target-companies.tsv` | Generated/curated target company list | Generated by `target-list-generator`, editable |
