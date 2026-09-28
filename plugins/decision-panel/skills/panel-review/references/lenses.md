# Lens catalog

A lens is a question a reviewer is responsible for. Pick 3 lenses for a standard review and 4-5 for a full one. Choose the ones that could change the outcome, not the ones that are easy to fill in. Always include at least one lens that looks for reasons the leading option fails (Risk or Contrarian); a panel of lenses that can only agree is not a review.

Each lens has an **evidence focus**: the material that reviewer is handed or told to go find first. Giving reviewers different evidence is what makes them disagree for real reasons instead of restating each other (the "information asymmetry" finding from the research this plugin is based on).

## Core lenses (domain-agnostic)

| Lens | The question it owns | Evidence focus | Typical findings |
|---|---|---|---|
| **Feasibility** | Will it actually work as described, with the people, skills, time and tools available? | The plan or artifact itself, dependencies, prior attempts | Missing steps, wrong assumptions about how a tool/process behaves, hidden prerequisites |
| **Risk & failure modes** | It's six months later and this went badly. What happened? (premortem) | Past incidents, known failure patterns, edge cases, what's hard to undo | Single points of failure, irreversible steps, likely-but-unplanned-for scenarios |
| **Cost & resources** | What does it really cost, including time, attention, maintenance and what we give up? | Prices, estimates, historical overruns, ongoing costs | Underestimated effort, recurring costs, opportunity cost, lock-in |
| **People & stakeholders** | Who is affected, who has to agree, who has to do the work, and what are their incentives? | Org context, owners, users, communication so far | Unconsulted owners, adoption risk, fairness issues, incentive mismatches |
| **Security, privacy & compliance** | What could be exposed, misused or non-compliant? | Data flows, access, regulations/policies that apply | Data exposure, excessive permissions, legal/contractual conflicts |
| **Long-term & reversibility** | What does this commit us to, and how hard is it to change course later? | Contracts, architecture, dependencies, exit paths | Lock-in, second-order effects, maintenance burden, one-way doors |
| **Outside view** | How do decisions like this usually turn out? What's the base rate? | Reference classes, benchmarks, industry data, our own track record | Optimism bias, planning fallacy, "this time is different" reasoning |
| **Contrarian** | What is the strongest case for the option we are leaning *against* — including doing nothing or waiting? | The rejected options and the status quo | A better alternative, a cheaper partial step, a reason to wait |

## Domain presets

Start from a preset, then swap lenses to fit. These are suggestions, not rules.

| Domain | Suggested lenses |
|---|---|
| Code change / pull request | Feasibility (correctness), Security, Risk (failure modes, rollback), Long-term (maintainability) |
| Architecture / system design | Feasibility, Risk (failure modes, scaling), Cost (build + run), Long-term (coupling, lock-in), Security |
| Tool, vendor or purchase | Cost (total cost of ownership), Long-term (lock-in, exit), Risk (vendor viability), People (adoption), Contrarian (build/keep current) |
| Process or policy change | People, Feasibility, Risk (unintended incentives), Outside view |
| Hiring, team or org decision | People, Risk, Long-term, Outside view (what predicts success here) |
| Product or strategy | Outside view (evidence from customers/market), Feasibility (execution capacity), Cost (opportunity cost), Contrarian |
| Personal or financial | Risk (downside, liquidity), Long-term (reversibility), Outside view (base rates), Contrarian (do nothing / wait) |
| Written document, proposal or argument | Feasibility (does the logic hold?), Outside view (is the evidence representative?), Contrarian (strongest objection), People (how will the audience read it?) |

## Making lenses genuinely different

Same-family models tend to make the same mistakes, so agreement between reviewers is weak evidence on its own. Push them apart deliberately:

- **Different evidence.** Give each lens its own evidence focus from the table above, not one shared pile.
- **Different questions.** A lens owns a question; it should not also try to answer the other lenses' questions.
- **Different models, when you can choose.** If the environment lets you pick a model per reviewer, spread the lenses across tiers (for example one on the most capable model, the rest on a faster one). This is a small extra source of independence, not a substitute for the two points above.
- **At least one adversarial lens.** Risk or Contrarian, every time.
