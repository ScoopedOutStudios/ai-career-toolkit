---
name: in-my-voice
description: Rewrite and refine content to match the user's personal voice using a review-then-rewrite workflow. Use when text sounds generic, AI-like, or not personal enough, and when consistent voice is required across professional writing.
---

# In My Voice

## Purpose

Make writing personal, credible, and human while removing generic cookie-cutter phrasing.

## Defaults

- Workflow: review first, then rewrite.
- Tone profile: executive-warm (confident, concise, approachable).
- Anti-generic strictness: balanced (remove obvious AI phrasing, keep useful standard terms).

## Voice Pack

This skill uses a personal voice pack stored locally. Look for your voice pack in these locations (in order of priority):

1. `~/.ai-career-toolkit/voice-pack/` (preferred — stays outside any repo)
2. `config/voice-pack/` (inside this toolkit clone — fine for non-sensitive starter samples)

If no voice pack exists, run from-scratch calibration prompts and produce a provisional voice profile. See `config.example/voice-pack/` for the expected structure.

## Use When

- A draft sounds generic, impersonal, or over-polished.
- Voice consistency is needed across resume, outreach, posts, and technical content.
- The user asks for "make it sound like me."

## Workflow

1. Diagnose what sounds generic or off-voice.
2. Identify voice targets from current voice-pack rules/examples.
3. Rewrite while preserving meaning and factual claims.
4. Show short rationale for key voice edits.
5. Propose one reusable rule to add back to the voice pack.

## Required Output

- Off-voice findings
- In-my-voice rewrite
- Why this matches voice profile
- Proposed voice-pack update (optional)
