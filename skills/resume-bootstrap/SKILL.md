---
name: resume-bootstrap
description: Build a first-pass config/settings.yaml targeting block and ~/.ai-career-toolkit/role-thesis.md from the user's resume (Markdown file, PDF, or URL). Use when onboarding to ai-career-toolkit, refreshing search criteria from an updated resume, or avoiding blank templates before target-list-generator / opportunity-evaluator.
---

# Resume bootstrap (first-pass personalization)

## Purpose

Turn resume content into **editable drafts** of toolkit personalization:

| Output | Location |
|--------|----------|
| Targeting criteria | `config/settings.yaml` (`targeting.*`) |
| Role thesis | `~/.ai-career-toolkit/role-thesis.md` |

This is a **first pass**. The user must review for accuracy (especially comp, level, and exclusions). Never treat inferred numbers or preferences as facts without confirmation.

## Inputs (pick one path)

1. **Markdown** — Read from workspace path or pasted content.
2. **PDF** — Read via the host environment (PDF-aware file read, `pdftotext`, or ask the user to paste plain text if extraction fails).
3. **URL** — Fetch HTML/PDF career profile or hosted resume. Prefer primary sources (personal site, PDF link). Respect robots/terms; if blocked, ask the user to download and provide a path.

If the resume contains **PII you should not persist** (full address, IDs), omit those from generated artifacts entirely.

## Privacy

- Write drafts under **`config/`** and **`~/.ai-career-toolkit/`** only — **not** into git-tracked paths inside the toolkit repo unless the user explicitly asks (and understands the risk).
- Do **not** echo raw resume contents back in chat unless the user needs a snippet for debugging; summarize what you inferred instead.

## Mapping rules

### settings.yaml (`targeting`)

Align lists with the **same vocabulary** interactive `init --personalize` uses so downstream skills stay consistent:

**Role** — Pick the closest label from:

`Software Engineer`, `Backend Engineer`, `Frontend Engineer`, `Full-Stack Engineer`, `Platform / Infrastructure Engineer`, `Site Reliability Engineer (SRE)`, `Data Engineer`, `ML Engineer`, `DevOps Engineer`, or `Other` with a short custom title.

**Level** — Infer from titles and scope (years alone are weak signals). Pick closest:

`Mid-level`, `Senior`, `Staff`, `Sr Staff`, `Principal`, `Distinguished`.

If ambiguous between two levels, choose the **lower** level and note uncertainty in your summary.

**domains** — Map resume themes to zero or more of:

`AI/ML`, `Developer tools`, `Cloud infrastructure`, `Enterprise SaaS`, `Fintech`, `Healthcare / biotech`, `Climate tech`, `Cybersecurity`, `Edtech`, `E-commerce / marketplace`, plus free-text lines only when nothing fits (mirror how lists work in YAML).

**geo_remote** — From explicit resume/geo cues:

`Remote-first`, `Hybrid`, `Onsite`, `Anywhere US`, `NYC`, `SF Bay Area`, `Seattle`, `Austin`, `London`, or short custom entries.

**company_stages** — Only if resume or stated preference implies it; otherwise leave commented / empty per existing file style.

**exclusions** — Only infer from explicit negatives (“no crypto”, etc.). Otherwise leave empty; do not invent dealbreakers.

When updating YAML, **preserve** unrelated keys (`platform`, `skills`, comments). Use the same nested structure as `config.example/settings.yaml`. For line-oriented edits, follow the patterns implied by how `settings.yaml` is maintained in-repo (scalar `role:` / `level:`, list blocks under `domains`, `geo_remote`, `exclusions`).

### role-thesis.md

Start from `templates/role-thesis.md` (or merge into existing content):

- Replace **every** `<!-- ... -->` placeholder with concise, resume-grounded prose (no fabrication — if unknown, write `TBD — confirm` rather than guessing comp).
- **Target Role** — Level, domains, team type consistent with `settings.yaml`.
- **Value proposition / Proof points** — Pull from headline + strongest bullets; keep proof points measurable where possible.
- **Must-Haves / Nice-to-Haves / Non-Negotiables** — Infer only where resume implies; flag `[infer]` items needing user confirmation.

## Workflow

1. **Acquire text** from MD path, PDF path, or URL.
2. **Extract signals**: titles, scope, domains, industries, leadership/IC, remote/geo, notable employers, metrics.
3. **Draft `settings.yaml` mutations** — Show a unified diff or before/after snippet for user approval **or** apply directly if the user asked you to write files.
4. **Draft full `role-thesis.md`** — Same approval rule.
5. **Summarize**: bullets for confirmed vs inferred vs `TBD`.
6. **Next steps**: Run `ai-career-toolkit verify`; optionally `ai-career-toolkit init --personalize` to reconcile menus with YAML; then target-list playbook prompts.

## Overwrite policy

- If `settings.yaml` or `role-thesis.md` already has non-template content, **do not overwrite silently**. Offer merge (append/update sections) or write `.bak` copies beside originals before replacing.
- If files are still obviously template placeholders, full replacement is OK after user confirms.

## Required response format

1. **Sources** — MD path / PDF path / URL (hostname only is fine).
2. **Proposed targeting summary** — Role, level, domains, geo, exclusions (if any).
3. **Files written or proposed** — Paths only.
4. **Confidence** — High / medium / low per major field.
5. **User checklist** — 3–7 bullets they must verify manually.

## Why this is a skill, not only a CLI command

Structured inference (domains, tier, thesis narrative) requires judgment; a dumb CLI cannot safely produce `role-thesis.md` without an LLM. A future optional **`ai-career-toolkit resume-text`** helper could extract PDF plain text only — useful for piping — but it does **not** replace this skill.
