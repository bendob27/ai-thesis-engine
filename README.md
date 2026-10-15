# AI Thesis Engine

The engine I use to invest my own money: a thematic long/short book on AI and the physical world. Compute, power, grids, memory, robotics, space.

It runs as a Claude Code skill. I write the thesis and make every call. The engine does the research, holds me to my own rules and keeps score.

## How it works

- **A written thesis.** Five falsifiable hypotheses, each with a conviction score, the indicators to watch, the facts that would kill it and a dated change log. `research/thesis.md`
- **The same analysis every time.** Every company goes through one template: what the price already assumes, a pre-mortem, the strongest case against, and a size. A separate agent that never saw the bull case tries to kill it. `research/frameworks.md`, `research/playbook.md`
- **Binding risk rules.** Position and theme caps, a drawdown ladder, staged buying, and nothing sold without my say. `risk/risk-rules.md`
- **Computed, not chosen.** The most it may pay for a company comes out of a formula, not a target price. `data/buy_cap.py`
- **It keeps score.** Every decision, including every company it passed on, is graded against the index. `data/decision_grader.py`
- **Numbers that tie out.** Data comes from filings, and the tools refuse to print a figure they cannot reconcile to the company's own reported total. `data/fact_pack.py`, `data/funding_clock.py`
- **Views move slowly.** News goes into an evidence log. Convictions only move at a quarterly review, on a sustained signal and with my sign-off.

## Layout

Organised like a small fund, one folder per desk:

- `research/` thesis, playbook, analysis templates, coverage universe
- `risk/` the binding limits
- `data/` data and decision tools, a selection
- `commands/` the slash commands: /research, /analyze, /news, /review, /size and more
- `book/` journal, positions, orders and broker sync, private

## What is not here

The book, my risk profile, the evidence log, the broker connection and the alerting and dashboard jobs stay private. The engine proposes, I approve every buy and sell.

## Run it

1. Copy this folder to `~/.claude/skills/ai-thesis/` and `commands/` to `.claude/commands/` in your project.
2. `pip install yfinance`, and set `SEC_UA="Your Name your@email"` for SEC requests.
3. Start Claude Code and run `/onboard`. It asks for your drawdown budget and portfolio size before it sizes anything.

Decision support for my own account. Not investment advice.
