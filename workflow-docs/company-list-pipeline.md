# Company list pipeline (profile → research → merge)

This toolkit does **not** ship a scoring engine or posting-sync scripts. You get a **simple, repeatable loop**: define your profile, run research per domain, merge into one TSV, refresh hiring metadata occasionally, and go deeper with `opportunity-evaluator` when you are ready to invest time in a company.

## 1. Inputs (your profile)

| Artifact | Purpose |
| -------- | ------- |
| `config/settings.yaml` | Domains, company stages, geo/remote, exclusions, target role/level |
| `~/.ai-career-toolkit/role-thesis.md` | Must-haves, non-negotiables, compensation floor, narrative fit |

`setup.sh` creates `~/.ai-career-toolkit/` and seeds `role-thesis.md` and `target-companies.tsv` when missing.

## 2. Per-domain passes (optional but recommended)

For each domain in `settings.yaml` → `targeting.domains`:

1. Run **`target-list-generator`** (or ask your agent to follow that skill).
2. Have **`research-guru`** propose companies with **citations** for careers URLs and hiring claims.
3. Save an intermediate TSV under:

   `~/.ai-career-toolkit/source-lists/<domain-slug>-YYYY-MM-DD.tsv`

   Use a filesystem-safe slug (e.g. `ai-ml`, `developer-tools`). Same column schema as the canonical file (see `target-list-generator` skill).

Intermediate files make it easy to redo one domain without losing the rest.

## 3. Canonical merged list

Merge into:

`~/.ai-career-toolkit/target-companies.tsv`

Rules of thumb:

- **Dedupe** on normalized company name (ignore legal suffix noise, `Inc.`, region in parentheses where obvious).
- **Preserve** the best-known metadata when rows conflict (prefer the row with a verified careers URL and recent `Last Checked`).
- Set **`Source List`** to something traceable (`domain:ai-ml`, `user-added`, etc.).
- Use **`Hiring Now` = Unknown** when you cannot verify; do not guess.

## 4. Prioritization (no scorer)

- Use **T1 / T2 / T3** tiers in the TSV.
- Apply **role-thesis** filters for quick rejects.
- Run **`opportunity-evaluator`** for companies where you might actually apply.

## 5. Freshness

Weekly or before a batch of applications:

- Update **`Hiring Now`**, **`Hiring URL`**, **`Last Checked`** for rows you care about.
- Re-run **`target-list-generator`** or a focused `research-guru` pass for stale T1s.

## Privacy

Keep all filled lists and notes under **`~/.ai-career-toolkit/`** (or another private directory). Do not commit real target lists or employer-specific research to a public repo.
