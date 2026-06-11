# Stack-Score

**Rate any tech stack before you build.**

A curated, opinionated scoring database. Offline. Zero API calls.
43 technologies scored across 7 dimensions.

```bash
$ stack-score "next.js tailwind supabase stripe vercel"
```

> Built by NOUMENON — AI agents that debate, evolve, and build.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## Why This Exists

Developers argue about tech stacks every day. "Next.js or Astro?"
"Supabase or Firebase?" "Vercel or Cloudflare?" This tool gives an
opinionated 0-100 answer across 7 dimensions, instantly and offline.

## What the Data Is

The scores come from a hand-curated database (`src/stack_score/database.py`)
maintained by the authors — learning-curve, performance, and cost ratings
are editorial judgments, not live benchmarks. `github_stars` values are
point-in-time snapshots (last refreshed 2026-06-11) and drift over time.
CVE entries are verified against the GitHub Advisory Database at curation
time; always check current advisories before deploying.

## Install

```bash
pip install git+https://github.com/Noumenon-ai/stack-score.git
```

## Usage

```bash
# Score a stack
stack-score "next.js tailwind supabase"

# Compare alternatives
stack-score "react vs vue vs svelte"

# Deep dive on one tech
stack-score "next.js" --detail

# Show top 10 proven stacks
stack-score --popular

# Best stack for a use case
stack-score --for "ecommerce"
stack-score --for "saas"
stack-score --for "blog"

# Version
stack-score --version
```

## Output

Real output from v1.0.1:

```
$ stack-score "next.js tailwind supabase stripe vercel"

╭────────────────────╮
│ STACK-SCORE v1.0.1 │
╰────────────────────╯

  Stack: next.js, tailwind, supabase, stripe, vercel

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Dimension      ┃   Score ┃ Notes                                  ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Compatibility  │  85/100 │ All tools work well together           │
│ Security       │  72/100 │ 2 CVEs: CVE-2025-29927, CVE-2025-48370 │
│ Community      │  98/100 │ All have massive communities           │
│ Performance    │  90/100 │ Excellent performance characteristics  │
│ Cost at Scale  │  72/100 │ Manageable costs at scale              │
│ Learning Curve │  62/100 │ Moderate learning curve                │
│ Maintenance    │ 100/100 │ All actively maintained in 2026        │
└────────────────┴─────────┴────────────────────────────────────────┘

  Overall: ████████████████░░░░ 83/100 STRONG

  Warnings:
    • Patch to >= 15.2.3 (CVE-2025-29927)
    • Enable RLS on ALL tables — many apps have been exposed without it
    • Update @supabase/auth-js to >= 2.70.0 (CVE-2025-48370, low severity)
    • Verify webhook signatures with stripe.webhooks.constructEvent()
    • Can get expensive at 1M+ requests — watch bandwidth costs

  Proven Combos:
    • next.js + stripe + supabase + tailwind + vercel: The most common SaaS
      starter stack in 2026

  Suggestions:
    • Consider adding: Sentry (error monitoring)
    • Consider adding: Resend (email)
```

Comparison mode, also real output:

```
$ stack-score "react vs vue vs svelte"

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Dimension      ┃    react     ┃     vue      ┃  sveltekit   ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Compatibility  │     100      │     100      │     100      │
│ Security       │      72      │     100      │     100      │
│ Community      │      98      │      98      │      85      │
│ Performance    │      80      │      90      │     100      │
│ Cost at Scale  │     100      │     100      │      90      │
│ Learning Curve │      50      │      70      │      60      │
│ Maintenance    │     100      │     100      │     100      │
│ Overall        │ 86 EXCELLENT │ 94 EXCELLENT │ 91 EXCELLENT │
└────────────────┴──────────────┴──────────────┴──────────────┘
```

## 7 Scoring Dimensions

| Dimension | What It Measures |
|-----------|-----------------|
| Compatibility | Curated pairs-well-with / conflicts-with relationships |
| Security | Known CVEs (verified against the GitHub Advisory Database) |
| Community | GitHub stars (snapshot) and maintenance status |
| Performance | Editorial 1-10 performance rating |
| Cost at Scale | Editorial 1-10 rating of how costs grow with users |
| Learning Curve | Editorial 1-10 ease-of-adoption rating |
| Maintenance | Active development status |

Rating bands: 85+ EXCELLENT, 70-84 STRONG, 50-69 DECENT, 30-49 WEAK,
below 30 AVOID.

## 43 Technologies

Frameworks, databases, CSS, payments, hosting, ORMs, auth, monitoring,
mobile, CLI tooling, and developer tools — all with curated scoring data.

## 10 Proven Stacks

Pre-defined stack combinations for common use cases:
SaaS, blog, API backend, e-commerce, mobile app, CLI tool, landing page,
T3 stack, Django full-stack, and edge-first.

## License

MIT

---

Built by [Noumenon](https://github.com/Noumenon-ai)
