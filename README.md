# Stack-Score

**Rate any tech stack before you build.**

Data-driven. Offline. Zero API calls. 50+ technologies scored.

```bash
$ stack-score "next.js tailwind supabase stripe vercel"
```

> Built by NOUMENON — AI agents that debate, evolve, and build.

![PyPI](https://img.shields.io/pypi/v/stack-score)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## Why This Exists

Developers argue about tech stacks every day. "Next.js or Astro?"
"Supabase or Firebase?" "Vercel or Cloudflare?" This tool gives
a data-driven answer with a 0-100 score across 7 dimensions.

## Install

```bash
pip install stack-score
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
```

## Output

```
  STACK-SCORE v1.0.0

  Stack: next.js, tailwind, supabase, stripe, vercel

  Dimension        Score   Notes
  Compatibility    95/100  All tools work well together
  Security         72/100  2 CVEs: CVE-2025-29927, GHSA-v36f
  Community        98/100  All have massive communities
  Performance      90/100  Excellent performance characteristics
  Cost at Scale    85/100  Manageable costs at scale
  Learning Curve   80/100  Moderate learning curve
  Maintenance      88/100  All actively maintained in 2026

  Overall: ████████████████████░ 87/100 STRONG

  Warnings:
    • Patch to >= 15.1.4 (CVE-2025-66478, CVE-2025-29927)
    • Enable RLS on ALL tables — 170+ apps exposed without it

  Proven Combos:
    • next.js + tailwind + supabase: The most common SaaS starter stack

  Suggestions:
    • Consider adding: Sentry (error monitoring)
    • Consider adding: Resend (email)
```

## 7 Scoring Dimensions

| Dimension | What It Measures |
|-----------|-----------------|
| Compatibility | How well the tools work together |
| Security | Known CVEs and vulnerabilities |
| Community | GitHub stars, maintenance, ecosystem |
| Performance | Speed, efficiency, benchmarks |
| Cost at Scale | How costs grow with users |
| Learning Curve | Ease of adoption |
| Maintenance | Active development status |

## 50+ Technologies

Frameworks, databases, CSS, payments, hosting, ORMs, auth, monitoring,
mobile, and developer tools — all with scoring data.

## 10 Proven Stacks

Pre-scored stack combinations for common use cases:
SaaS, blog, API backend, e-commerce, mobile app, CLI tool, landing page,
T3 stack, Django full-stack, and edge-first.

## License

MIT

---

Part of the NOUMENON ecosystem.
