# Job Search Operating Workflow

A tool-agnostic methodology for running a structured, disciplined job search. This workflow can be implemented with any tracking tool (local files, spreadsheet, Notion, Linear, GitHub Projects, or paper).

## System Overview

The workflow has five components:

1. **Capture** — Record every opportunity, interview, prep task, and review as a discrete item.
2. **Triage** — Daily prioritization into a small "today" set.
3. **Execute** — Focus on today's items in priority order.
4. **Review** — Weekly health checks and strategy adjustments.
5. **Target** — Ongoing company research and outreach pipeline.

## Opportunity Pipeline

Each opportunity moves through these stages:

```
Applied → Recruiter Screen → HM Screen → Panel → Offer
                                                    ↓
                                              Accept / Decline / Negotiate

(Any stage can exit to → Closed: rejected, withdrew, or no response)
```

### Pipeline Health Checks (Weekly)

| Metric | Target | How to Check |
|--------|--------|--------------|
| Active opportunities | 8-15 | Count open items at any pipeline stage |
| Recruiter screens scheduled | 2+ per week | Count items at Recruiter Screen stage |
| HM+ conversion | 30%+ of screens | Track stage transitions |
| Stale opportunities (>14 days, no action) | 0 | Flag items with no recent update |

## Daily Operating Cadence

Run every morning (20-30 minutes planning, then focused execution):

1. **Select today's priorities** — Pick up to 3 items to focus on today.
2. **Verify each item has:** a clear next action and a due date.
3. **Check for blockers** — Move blocked items to a waiting state with the dependency noted.
4. **Execute** — Work items in priority order.
5. **End of day** — Close finished items. Note wins, misses, and carryovers.

### Prioritization Signals

| Signal | Weight |
|--------|--------|
| Overdue (due date passed) | Highest |
| Due today | High |
| Due tomorrow | Medium |
| High priority label | Medium |
| Currently blocked/waiting | Deprioritize until unblocked |

### WIP Limits

| Category | Limit | Rationale |
|----------|-------|-----------|
| Today | 3 | Focus; finish before starting new work |
| This Week | 8 | Visible queue without overwhelm |
| Waiting | Unlimited | Each must note the dependency and owner |

## Weekly Review (Friday)

1. **Record wins** — What moved forward this week?
2. **Check pipeline health** — Review metrics against targets above.
3. **Close stale items** — Opportunities with no movement in 14+ days get an explicit close reason.
4. **Pick next week's priorities** — Select top 5 items for the coming week.
5. **Retier company list** — Update tiers based on response rate, stage movement, and new intel.
6. **Define experiments** — Set 1-3 small experiments for the week (targeting, messaging, prep focus).

## Tier-Based Company Targeting

### Tier Definitions

| Tier | Criteria | Outreach Priority |
|------|----------|-------------------|
| **T1** | Strong role fit + known referral path + active headcount | Immediate; personalized outreach |
| **T2** | Good role fit + public posting or warm lead | This week; tailored application |
| **T3** | Interesting but speculative fit or no clear entry point | Backlog; opportunistic |

### Targeting Workflow

1. **Define role thesis** — Use `templates/role-thesis.md` to lock target level, domain, and criteria.
2. **Build target list** — Use `target-list-generator` skill or manually curate a tiered company list.
3. **Lock outreach queue** — Freeze the outreach order for the current cycle.
4. **Execute outreach** — Referrals, direct applications, follow-ups.
5. **Weekly retier** — Update tiers based on response signals and new information.

## Prep and Interview Readiness

### Readiness Flow

```
Market Calibration → Gap Analysis → Story Bank → Interview-Ready
```

1. **Market calibration** — Understand current expectations for your target level using `templates/role-expectation-rubric.md`.
2. **Gap analysis** — Score yourself on the rubric. Identify the top 3-5 gaps to close.
3. **Story bank** — Build interview stories using `templates/interview-story-system.md` and the `star-story` skill.
4. **Interview-ready** — Per-interview prep using the `mock-interview-loop` skill.

### Per-Interview Prep

For each scheduled interview:
1. Research the company using `opportunity-evaluator` skill.
2. Select 3-5 stories most relevant to the role and interview type.
3. Run a mock loop targeting the expected question themes.
4. Prepare 2-3 thoughtful questions to ask the interviewer.

## Privacy Rules

| What | Where to Store | Never Store In |
|------|---------------|----------------|
| Recruiter names | Local private files only | Versioned/shared docs |
| Compensation details | Local private files only | Versioned/shared docs |
| Personal identifiers | Local private files only | Versioned/shared docs |
| Sanitized status + next action | Tracking tool of choice | — |
| Reusable templates | This toolkit repo | — |

## Local File Structure

If using local files for tracking (recommended default):

```
~/.ai-career-toolkit/
├── role-thesis.md              # Your filled role thesis
├── target-companies.tsv        # Generated or curated company list
├── opportunities/
│   ├── company-a-staff-eng.md  # One file per active opportunity
│   └── company-b-principal.md
├── interview-notes/
│   ├── company-a-recruiter-screen.md
│   └── company-a-hm-screen.md
└── weekly-reviews/
    ├── 2026-W15.md
    └── 2026-W16.md
```
