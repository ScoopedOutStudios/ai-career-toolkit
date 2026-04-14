# Customization Guide

How to personalize ai-career-toolkit for your job search.

## Step 1: Define Your Role Thesis

The role thesis is the foundation of your search. It defines what you're looking for and what you'll filter on.

1. Copy the template: `cp templates/role-thesis.md ~/.ai-career-toolkit/role-thesis.md`
2. Fill in every section honestly — this is private, be specific
3. Pay special attention to the Quick Filter Checklist — the `opportunity-evaluator` skill uses it

## Step 2: Build Your Voice Pack

The voice pack makes `in-my-voice` work. Without it, rewrites will use a generic professional tone.

1. Copy the example: `cp -r config.example/voice-pack config/voice-pack`
2. Replace the placeholder content with your actual writing patterns
3. The easiest way to build a voice pack: ask your AI agent to analyze 5-10 samples of your writing (emails, LinkedIn posts, docs) and generate a profile

## Step 3: Configure Targeting

Edit `config/settings.yaml` to set your company targeting preferences:

```yaml
targeting:
  domains:
    - AI/ML
    - developer tools
  company_stages:
    - growth-stage
    - public-scale
  geo_remote:
    - remote-first
  role_level: Staff
  exclusions:
    - crypto
```

Then run the `target-list-generator` skill to build your initial company list.

## Step 4: Score Yourself on the Rubric

Use `templates/role-expectation-rubric.md` to assess your current level:

1. Score each of the 8 dimensions (1-5) with specific evidence
2. Identify your top 3 gaps
3. Build STAR stories that address those gaps using the `star-story` skill
4. Re-score monthly as you refine your stories and get interview feedback

## Step 5: Build Your Story Bank

Use `templates/interview-story-system.md` as your framework:

1. Map your experience to the 8 story templates
2. Use the `star-story` skill to draft each one
3. Prepare 2-minute and 5-minute versions
4. Use `mock-interview-loop` to practice and refine

## Ongoing Workflow

Refer to `workflow-docs/operating-workflow.md` for the full methodology:

- **Daily**: Pick up to 3 priorities, execute, close what's done
- **Weekly**: Review pipeline health, close stale opportunities, retier companies
- **Per-opportunity**: Run `opportunity-evaluator` before investing significant time
- **Per-interview**: Run mock loops, select stories, prepare questions
