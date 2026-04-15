---
name: opportunity-evaluator
description: Evaluate a company and role as a potential career opportunity. Parses job descriptions, researches the company as an employer, scores against the user's role thesis and expectation rubric, and produces a pursue/park/skip recommendation. Use when a new opportunity surfaces and needs structured evaluation.
---

# Opportunity Evaluator

## Purpose

Take a company name and job description (JD) and produce a structured, bidirectional evaluation — assessing both "will they want me?" and "do I want them?" — with a clear action recommendation.

## Inputs Required

1. **Company name** (required)
2. **Job description** — URL or pasted text (required)
3. **User's role thesis** — from `~/.ai-career-toolkit/role-thesis.md` or `config/role-thesis.md` (auto-load if available)
4. **Role expectation rubric** — from `templates/role-expectation-rubric.md` (auto-load)

## Workflow

### Step 1: Parse the Job Description

Extract structured signals from the JD:

- Target level (IC vs manager, seniority band)
- Scope indicators (team size, org breadth, problem complexity)
- Domain and tech stack
- Key responsibilities and success criteria
- Location / remote policy
- Compensation signals (if listed)
- Red flags (vague scope, unrealistic expectations, title inflation)

### Step 2: Quick Filter

Score the opportunity against the user's role thesis (if available). Check each criterion:

- Level match
- Domain alignment
- Must-have requirements met
- Non-negotiable criteria satisfied
- Location/remote fit

Produce a filter score (pass/fail with notes). If the role thesis is not available, skip this step and note that the user should create one using `templates/role-thesis.md`.

### Step 3: Company-as-Employer Research

Research the company from an employee/candidate perspective. Route to `research-guru` to gather:

- Engineering culture signals (RFC culture, IC career ladder, open-source presence, tech blog quality)
- Growth trajectory (funding, revenue growth, recent hires vs layoffs)
- Leadership stability (CTO/VP Eng tenure, recent departures)
- Employee sentiment (Glassdoor, Blind, Levels.fyi signals)
- Compensation positioning (market rate alignment)
- Work-life balance and retention signals

### Step 4: Rubric Scoring

Score the opportunity against the role expectation rubric dimensions:

1. Scope of Impact
2. Ambiguity Handling opportunity
3. Technical Direction opportunity
4. Cross-Functional Influence
5. Business Outcome Linkage
6. Multiplication Effect
7. Operational Quality
8. AI-Native Practice

Rate each dimension 1-5 based on JD signals and company research. Flag dimensions that cannot be assessed from available information.

### Step 5: Bidirectional Fit Assessment

Assess mutual fit:

- **Their perspective**: Does the user's background align with what they need?
- **User's perspective**: Does this role advance career trajectory? Does the company environment match preferences?
- **Growth potential**: Will this role stretch toward the user's target level?
- **Strategic timing**: Why this company now?

### Step 6: Composite Recommendation

Produce one of:

- **Strong Pursue** — high fit across all dimensions, act immediately
- **Pursue with Conditions** — good fit with noted concerns, worth exploring (list conditions to validate)
- **Park** — interesting but not a priority right now (note what would change the assessment)
- **Skip** — clear misalignment on critical criteria (explain why)

## Required Output

1. **JD Summary** — parsed signals in structured format
2. **Quick Filter Score** — pass/fail with criterion-level notes
3. **Company Profile** — employer research findings
4. **Rubric Scorecard** — dimension scores with evidence
5. **Fit Assessment** — bidirectional analysis
6. **Recommendation** — one of: Strong Pursue / Pursue with Conditions / Park / Skip
7. **Next Actions** — what to do if pursuing (tailor resume, find referral, prep for screen, etc.)

## Agent Routing

- Route company research to `research-guru`
- Route role-fit analysis through `career-guide` if available
- Route materials readiness check through `hm-review` if the user wants to assess their application strength