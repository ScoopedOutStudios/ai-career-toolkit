---
name: target-list-generator
description: Build a scored, tiered list of target companies for job search based on user-defined criteria. Uses research to find companies matching domains, stage, location, and role preferences. Outputs a structured TSV file. Use when starting a job search, expanding targets, or refreshing hiring signals.
---

# Target List Generator

## Purpose

Generate a comprehensive, scored list of target companies tailored to the user's job search criteria. Output is a structured TSV file that can be used for tracking, prioritization, and outreach planning.

## Inputs Required

1. **User criteria** — provided interactively or from config. Gather:
   - Domains of interest (e.g., AI/ML, developer tools, fintech, climate tech, healthcare, enterprise SaaS)
   - Company stage preferences (e.g., growth-stage, late-stage, public-scale, early-stage)
   - Geo/remote requirements (e.g., remote-first, NYC, SF Bay Area, hybrid OK)
   - Target role and level for **technical IC** search (e.g., Software Engineer, ML Engineer, SRE + Senior through Principal)
   - Exclusion criteria (e.g., no crypto, no defense, no pre-seed)
   - Optional: specific companies to include or research

   If `~/.ai-career-toolkit/role-thesis.md` or `config/role-thesis.md` exists, read it and align exclusions, must-haves, and non-negotiables with the user’s stated criteria (do not contradict their thesis without calling it out).

2. **Existing list** (optional) — if `~/.ai-career-toolkit/target-companies.tsv` exists, read it to avoid duplicates and build on prior work.

3. **Per-domain drafts** (recommended) — for each domain pass, write or update:

   `~/.ai-career-toolkit/source-lists/<domain-slug>-YYYY-MM-DD.tsv`

   using the same column schema as the canonical file. See [company-list-pipeline.md](../../workflow-docs/company-list-pipeline.md) for the full merge workflow.

## Output Schema

TSV file with these columns:

| Column | Description |
|--------|-------------|
| `Company` | Company display name |
| `Tier` | Priority tier: T1 (top priority), T2 (strong), T3 (worth watching) |
| `Primary Domain` | What the company builds / sector |
| `Stage` | Company maturity (seed, growth, late-stage, public-scale, nonprofit) |
| `Source List` | How this company was found (e.g., top-ai, hot-startups, user-added) |
| `Why Target` | One-line rationale for targeting this company |
| `Hiring Now` | Yes / No / Unknown — whether active engineering hiring is evident |
| `Hiring URL` | Link to careers page or relevant job board listing |
| `Geo / Remote` | Location and remote policy |
| `Last Checked` | Date this entry was last verified (YYYY-MM-DD) |

## Workflow

### Step 1: Gather Criteria

If criteria are not already in `config/settings.yaml`, ask the user interactively:
- "What domains or industries are you targeting?"
- "Any company stage preferences?"
- "Location or remote requirements?"
- "What level are you targeting?"
- "Any hard exclusions?"

### Step 2: Research by Domain

For each domain of interest, route to `research-guru` to find relevant companies:

- Require **source citations** for factual claims (funding, layoffs, careers page URLs). If the model cannot verify a careers URL or hiring signal, set `Hiring Now` to **Unknown** and avoid inventing links.
- Top companies in the domain (market leaders and fast risers)
- Companies with strong engineering culture or brand
- Companies with known active hiring in the target role level
- Mission-driven or high-impact companies in the domain

### Step 3: Score and Tier

For each company found, assess:
- **Domain fit**: How well does the company match the user's target domains?
- **Stage fit**: Does the company stage match preferences?
- **Role availability**: Is there evidence of relevant roles?
- **Engineering reputation**: Quality signals (tech blog, open source, known eng leaders)
- **Growth trajectory**: Is the company growing, stable, or contracting?

Assign tiers:
- **T1**: Strong domain fit + active hiring + good eng reputation + right stage
- **T2**: Good fit on most criteria with one gap
- **T3**: Interesting but speculative — worth monitoring

### Step 4: Check for Hiring Signals

For each company, check the careers page or job boards for:
- Open roles matching the user's target level and domain
- Engineering hiring volume signals
- Record the hiring URL and check date

### Step 5: Compile and Write

- Merge per-domain drafts from `~/.ai-career-toolkit/source-lists/` when present; otherwise merge from this run’s research only
- Merge with any existing `target-companies.tsv` (update existing rows, append new ones)
- Sort by tier (T1 first), then alphabetically within tier
- Write to `~/.ai-career-toolkit/target-companies.tsv`
- Report summary: total companies, count per tier, domains covered

## Required Output

1. **Summary**: Total companies found, breakdown by tier and domain
2. **TSV file**: Written to `~/.ai-career-toolkit/target-companies.tsv`
3. **Highlights**: Top 5 most promising new additions with brief rationale
4. **Gaps**: Domains or criteria where coverage is thin — suggest follow-up research

## Re-run Behavior

When re-running:
- Update `Hiring Now` and `Last Checked` for existing companies
- Add newly discovered companies
- Flag companies that have had layoffs or negative signals since last check
- Do not remove companies unless the user explicitly requests it
