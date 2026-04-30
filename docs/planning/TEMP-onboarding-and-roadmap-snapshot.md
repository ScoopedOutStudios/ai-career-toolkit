# HISTORICAL — Onboarding, playbook, and roadmap snapshot

> **This document is historical.** It was used during initial planning and most items have been implemented. For canonical guidance, see:
> - [docs/playbook.md](../playbook.md) — skill/agent reference and prompts (built)
> - [docs/GETTING_STARTED.md](../GETTING_STARTED.md) — post-init setup guide (built)
> - [README.md](../../README.md) — quick start and value narrative (updated)

**Status:** Historical — kept for backlog reference only.  
**Created:** 2026-04-20  
**Purpose:** Single place for (1) simplified value-first onboarding, (2) user context requirements, and (3) backlog items from prior Ideas / Roadmap / Build Loop artifacts that are **not** done or need verification.

---

## 1. Problem statement

- **Gap A:** Users do not see how **skills** and **sub-agents** map to real jobs-to-be-done or how to invoke them.
- **Gap B:** **Getting started** over-indexes on plumbing (`init` / `install` / `verify`) instead of **first value** (personalized prompts + minimum context).
- **Goal:** One clear story: **Orient → (light) Setup → Personalize → First win**, with setup as a sidebar, not the hero.

---

## 2. Proposed onboarding shape (simplified)


| Layer           | User outcome                     | Primary artifacts (proposed)                                                     |
| --------------- | -------------------------------- | -------------------------------------------------------------------------------- |
| **Orient**      | Understand what this is / is not | Short README lead; link **Playbook**                                             |
| **Setup**       | IDE + files on disk              | Collapsed “Setup” page: Path A (pip/CLI) vs Path B (git/bash); `verify` optional |
| **Personalize** | Outputs are about *them*         | **Tier 0 checklist** (see §4) + links to `settings.yaml` + `role-thesis.md`      |
| **First win**   | One useful artifact today        | One **copy-paste prompt** for JD eval *or* target list (Playbook §)              |


**Principle:** `init` / `install` / `verify` stay; they are **not** positioned as the product value.

---

## 3. Playbook (DONE — see docs/playbook.md)

Single user-facing doc, e.g. `docs/playbook.md`, containing:

1. **Jobs-to-be-done → skill (+ optional agent)** matrix.
2. **Four agents** cheat sheet: when to use, what they return, handoffs (`research-guru`, `career-guide`, `interview-prep-coach`, `wordsmith-editor`).
3. **Copy-paste prompts** (5–8) that reference `config/settings.yaml` and `~/.ai-career-toolkit/role-thesis.md`.
4. **Fallback:** “If the wrong skill runs, name the skill explicitly.”

**README change (planned):** Hero = outcomes + link to Playbook + Tier 0; long install moves under Setup.

---

## 4. Key user inputs (for usefulness)

### Tier 0 — Minimum viable context (~15 min)


| Input                         | Location                            | Why                   |
| ----------------------------- | ----------------------------------- | --------------------- |
| Level + track (IC)            | `settings.yaml` + thesis            | Rubric / JD alignment |
| Domains                       | `settings.yaml` `targeting.domains` | Lists + research      |
| Remote/geo + rough comp floor | Thesis must-haves                   | Filters               |
| Exclusions                    | Thesis + `settings.yaml`            | Noise reduction       |


### Tier 1 — Strong personalization


| Input            | Location                              | Why                         |
| ---------------- | ------------------------------------- | --------------------------- |
| Full role thesis | `~/.ai-career-toolkit/role-thesis.md` | Evaluator, career narrative |
| Voice pack       | `voice-pack`                          | Outreach, `in-my-voice`     |
| Story bank       | Templates + notes                     | STAR + mocks                |
| Target TSV       | `target-companies.tsv`                | Pipeline                    |


### Tier 2 — Ongoing

Opportunity notes, weekly reviews, offer tradeoffs (`career-guide`).

---

## 5. Phased execution (this initiative)


| Phase  | Deliverable                                                                                        |
| ------ | -------------------------------------------------------------------------------------------------- |
| **P1** | `docs/playbook.md` + slim `docs/GETTING_STARTED.md` (orient + Tier 0 + link playbook + link setup) |
| **P2** | README restructure (value first, setup second)                                                     |
| **P3** | Optional CLI bridge: post-`verify` hint or `onboarding` subcommand printing Tier 0 + first prompt  |
| **P4** | Sanitized example session (transcript or doc)                                                      |


---

## 6. Inventory: repo & GitHub — open / deferred themes

Sourced from [README.md](../../README.md) and public issue links. **Verify in GitHub** for current state.


| Item                                      | Type             | Notes                                                                                                                                                |
| ----------------------------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Non-tech roles expansion**              | GitHub issue     | [Issue #1](https://github.com/rohitnandwate/ai-career-toolkit/issues/1) — sales, marketing, product, design, ops; v1 explicitly **out of scope** |
| **Marketplace publishing**                | Roadmap / README | “Planned for future releases” (Cursor, Claude Code, Codex) — **not started**                                                                         |
| **Manager / EM-first tracks**             | Scope            | README: not first-class; IC-calibrated — **content gap** if EM audience grows                                                                        |
| **Hosted CRM / ATS / scoring automation** | Non-goal         | Launch plan: no `score_companies.py`-style pipeline in v1 — **deferred** unless demand                                                               |
| **“Other” Agent Skills hosts**            | Doc gap          | README: compatible in principle; **no** first-class guide for ChatGPT-only / Gemini-only users                                                       |


---

## 7. Inventory: Cursor plan files (local, may be stale)

These live under the maintainer’s Cursor plans directory, not in this repo. Titles are for lookup.

### 7.1 `AI Career Toolkit Launch` (launch plan)

- **File:** `~/.cursor/plans/ai_career_toolkit_launch_5d9627b2.plan.md` (or equivalent path on your machine)
- **Frontmatter todos:** All marked **completed** (trust copy, install/rules, golden path, release hygiene, distribution, company-list pipeline doc).
- **Still relevant deferred themes (content of plan, not open todos):** marketplace, non-tech roles, scoring automation — align with §6 above.

### 7.2 `ai-career-toolkit repo setup` (original scaffold plan)

- **File:** `~/.cursor/plans/ai-career-toolkit_repo_setup_48d6ee5e.plan.md`
- **Note:** Frontmatter shows many todos as `pending` / `in_progress`; the **repository has since shipped** most of this (skills, agents including `research-guru`, setup/install, docs, company-list pipeline doc, Python CLI). Treat frontmatter as **historical**, not source of truth.
- **Items that may still be genuinely open or need verification:**


| Original todo (paraphrased)                                                         | Likely status       | Action                                              |
| ----------------------------------------------------------------------------------- | ------------------- | --------------------------------------------------- |
| Generalize rubric to multi-track (IC, EM, Staff+, Principal)                        | **Partial**         | Template exists; EM track not first-class in README |
| `cleanup-family-hq` — remove `tools/cursor-career-stack/`, point README to new repo | **Unknown**         | Verify in `family-hq` repo                          |
| Pre-commit / grep for PII patterns                                                  | **Not in OSS repo** | Optional hygiene backlog                            |
| `verify-install` fresh-clone test                                                   | **Ongoing**         | Keep in release checklist                           |


---

## 8. Gaps discovered in recent UX review (for triage)

- **Skill discovery:** Users may not know how to **name** a skill if auto-routing fails.
- **Windows:** Bash/WSL still a hard dependency for `install.sh`.
- **Two-directory model:** Toolkit root vs `~/.ai-career-toolkit` confuses first-timers; Playbook + Tier 0 should explain once.
- **Research quality:** Target lists and company intel depend on host web access; docs should set expectations (citations, `Unknown`).

---

## 9. Suggested next step

1. Create GitHub **epic issue** “Value-first onboarding + Playbook” linking this doc (or copy §2–§5 into the issue body).
2. Close or update **stale** plan file todos in Cursor so they don’t conflict with repo reality.
3. Delete this file after content lives in `docs/playbook.md` + `docs/GETTING_STARTED.md` + updated README.

---

## Document history


| Date       | Change                                                                                                           |
| ---------- | ---------------------------------------------------------------------------------------------------------------- |
| 2026-04-20 | Initial snapshot: onboarding plan + backlog inventory from README, launch plan, repo setup plan, recent UX notes |
