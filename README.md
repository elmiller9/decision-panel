# decision-panel

**Better decisions with Claude: an evidence-based review panel for any choice, plan or proposal, plus a retro loop that learns from how decisions turn out.**

Ask Claude "should we do X?" and you usually get one fluent answer from one line of reasoning. `decision-panel` runs a structured review instead:

- several reviewers look at the question **independently**, each through a different lens;
- only claims backed by evidence survive;
- disagreements that can be checked **get checked**;
- the rest go to a neutral adjudicator;
- anything high-stakes comes back to you to decide.

You get a recommendation with honest confidence, the risks, the dissent that survived, and what would change the answer. It works for anything you'd want a second, third and fourth opinion on: a pull request or architecture change, a vendor or purchase, a hire, a policy, a product bet, a contract, or a personal financial call.

---

## Contents

- [Why it works this way](#why-it-works-this-way)
- [What's inside](#whats-inside)
- [How a review runs](#how-a-review-runs)
- [Installing](#installing)
- [Using it](#using-it)
- [Customizing](#customizing)
- [Cost, privacy and safety](#cost-privacy-and-safety)
- [Limitations](#limitations)
- [For maintainers: publishing and testing](#for-maintainers-publishing-and-testing)
- [Research basis](#research-basis)

---

## Why it works this way

The design comes from research on multi-agent AI review panels. Four findings drive it:

1. **Reviewers who can see each other converge on the most confident voice, not the right one.** Multi-round "debate" between AI models often makes them abandon correct minority views. So reviewers here work independently and never debate; a separate adjudicator weighs their findings.
2. **More AI opinions are worth less than they look.** Models share training and blind spots. In one study, nine AI judges from seven model families were worth about two independent votes. So the panel weighs **evidence**, not headcount, and deliberately gives reviewers **different evidence** to look at so they fail differently.
3. **Checking beats arguing.** A claim that can be settled by running a test, reading the source, or computing the number is settled that way, and a check only counts if it could have come out the other way.
4. **People decide the irreversible calls.** High-stakes and genuinely uncertain points come back to you with the evidence attached. The panel recommends; it never acts on your behalf.

It also **scales to the stakes**. A reversible, low-cost choice gets a one-screen check; a large or irreversible one gets the full panel. And it **learns without retraining**: decisions are recorded with their confidence, a retro later checks how they turned out, and approved lessons feed back into future reviews.

---

## What's inside

| Component | Type | What it does |
|---|---|---|
| `panel-review` | Skill | The main workflow. Sizes the review to the stakes, frames the decision neutrally, runs independent lens reviewers, applies the evidence gate, verifies what can be checked, adjudicates the rest, and reports. Optionally writes a decision record. |
| `decision-retro` | Skill | The learning loop. Records how a past decision turned out, judges decision quality separately from luck, checks whether your confidence levels were calibrated, and proposes lessons for specific lenses (added only with your approval). |
| `lens-reviewer` | Subagent | An independent reviewer that owns one lens (risk, cost, feasibility…) and returns evidence-labelled findings. Read-only tools. |
| `verifier` | Subagent | Settles testable claims by checking them (running non-destructive tests, reading sources, computing figures). Asks before anything with side effects. |
| `steelman` | Subagent | Makes the strongest honest case against the leaning position, or concedes. Read-only tools. |
| `adjudicator` | Subagent | Rules on contested points using only the evidence, without being told who said what or how many agreed. Escalates high-impact, unresolved risks to you. Read-only tools. |

---

## How a review runs

```
 your question / plan / proposal
        │
        ▼
 1. Size it ─────────► Light: one structured pass (premortem, runner-up case, key assumption)
        │                     ──► recommendation
        ▼  Standard / Full
 2. Frame a neutral brief (decision, options incl. "do nothing", criteria, evidence)
        ▼
 3. Independent lens reviewers, in parallel, each with its own lens and evidence focus
        │   (they never see each other)
        ▼
 4. Evidence gate ─ drop claims whose sources don't say what's claimed
        ▼
 5. Contested or decisive claims:
        ├─ checkable ────► verifier: VERIFIED / REFUTED / INCONCLUSIVE
        └─ not checkable ► steelman ─► adjudicator: UPHELD / REJECTED / NEEDS_HUMAN
        ▼
 6. Report: recommendation · confidence · what would change it · risks · dissent
        ▼
 7. Full tier: your sign-off ─► decision record ─► later: decision-retro
```

| Tier | When | Roughly |
|---|---|---|
| **Light** | Reversible, low cost of being wrong, or you ask for a quick check | One pass, no subagents |
| **Standard** | Meaningful but recoverable (the default for most real decisions) | 3 reviewers + verification/adjudication of contested points |
| **Full** | Hard to undo, expensive, or with security/legal/safety/people impact | 4–5 reviewers, every decisive claim verified, your explicit sign-off, a decision record |

Claude sizes the review by the stakes, not by how casually you ask. It tells you which tier it picked and why. Say "just a quick check" or "go deep" to override it.

---

## Installing

Pick the option that fits how you use Claude.

> **Before installing any plugin**, read what's in it. Plugins can include instructions and subagents that run tools on your machine. This one's subagents are read-only, except `verifier`, which can run commands and is instructed to ask before anything with side effects.

### Option 1 — Claude Code, from GitHub (recommended)

Once this repository is published on GitHub, run these inside Claude Code:

```
/plugin marketplace add elmiller9/decision-panel
/plugin install decision-panel@decision-panel
```

Or from a terminal:

```bash
claude plugin marketplace add elmiller9/decision-panel
claude plugin install decision-panel@decision-panel
```

Restart Claude Code or run `/reload-plugins`. Update later with `claude plugin update decision-panel@decision-panel`.

### Option 2 — Claude Code, from a local folder

If you received this as a folder or zip, add the folder as a marketplace:

```
/plugin marketplace add C:/path/to/decision-panel
/plugin install decision-panel@decision-panel
```

To try it for a single session without installing anything:

```bash
claude --plugin-dir C:/path/to/decision-panel/plugins/decision-panel
```

### Option 3 — Turn it on for a whole team's project

Commit this to the project's `.claude/settings.json`. Team members are prompted to install the plugin when they open the project:

```json
{
  "extraKnownMarketplaces": {
    "decision-panel": {
      "source": { "source": "github", "repo": "elmiller9/decision-panel" }
    }
  },
  "enabledPlugins": {
    "decision-panel@decision-panel": true
  }
}
```

### Option 4 — Claude Code without the plugin system

Copy the pieces into your personal (all projects) or project folders:

| Copy | To (all projects) | Or to (one project) |
|---|---|---|
| `plugins/decision-panel/skills/panel-review/` | `~/.claude/skills/panel-review/` | `.claude/skills/panel-review/` |
| `plugins/decision-panel/skills/decision-retro/` | `~/.claude/skills/decision-retro/` | `.claude/skills/decision-retro/` |
| `plugins/decision-panel/agents/*.md` | `~/.claude/agents/` | `.claude/agents/` |

The skills are then invoked as `/panel-review` and `/decision-retro`, without the `decision-panel:` prefix.

### Option 5 — Claude.ai or the Claude desktop app (skills only)

Custom skills can be uploaded to Claude.ai and the desktop app (on plans that support them). Zip each skill folder so `SKILL.md` sits inside the folder at the top of the zip — for example `panel-review.zip` containing `panel-review/SKILL.md`, `panel-review/references/…` and `panel-review/assets/…` — then upload it from the Skills section of Claude's settings. See Anthropic's help center for the current location on your plan.

Subagents aren't available there, so `panel-review` runs its lenses one after another in a single conversation. It writes each lens's findings in full before starting the next, and tells you this is a weaker form of independence than separate reviewers. The method still helps; it just helps less.

---

## Using it

You can ask naturally; the skill triggers on decision-shaped requests. For small, easily reversed choices, Claude may simply answer directly, which is usually what you'd want anyway. To make sure the panel runs, invoke it directly:

| In a plugin install | Standalone install |
|---|---|
| `/decision-panel:panel-review <what to review>` | `/panel-review <what to review>` |
| `/decision-panel:decision-retro <which decision>` | `/decision-retro <which decision>` |

**Examples**

- "Should we move our Postgres to RDS before due diligence, or wait until after the raise?"
- "Poke holes in this migration plan before I send it to the team: `docs/migration-plan.md`"
- "Review PR #412. Is this caching approach the right call? Go deep."
- "We're choosing between Vendor A and Vendor B for SSO. Here are both quotes."
- "Quick check: is it worth refinancing at 5.9% with a 2,500 closing cost?"
- "Which of our decisions are due for a retro?" / "Let's do a retro on the vendor decision from March."

**What you get back:** the recommendation first, then its confidence, what would change it, the reasons with their evidence, risks with mitigations, resolved disagreements, dissent worth keeping, and anything that needs your decision.

**Decision records.** Full reviews write a record, and standard reviews offer to. Records go in your project's existing `docs/decisions/`, `docs/adr/` or `decisions/` folder, or a new `decisions/` folder. They are plain markdown with front matter you can edit. `decision-retro` reads them later, fills in the outcome, and keeps a short `LESSONS.md` of approved lessons that future reviews use, each lens getting only its own lessons.

---

## Customizing

Everything is plain markdown, so edit freely:

- **Lenses** — `plugins/decision-panel/skills/panel-review/references/lenses.md`. Add lenses or domain presets for your field (clinical, legal, data engineering, and so on). Keep one adversarial lens in every review.
- **Rules** — `…/panel-review/references/evidence-and-adjudication.md`: the evidence gate, routing, verification standard, confidence buckets.
- **Models** — each subagent's `model:` line in `plugins/decision-panel/agents/*.md` (`sonnet`, `opus`, `haiku`, `inherit`, or a full model ID). By default the reviewers and steelman run on Sonnet, the adjudicator on Opus, and the verifier on whatever model your session uses. Spreading reviewers across models adds a little independence; giving them different evidence adds more.
- **Tier thresholds and report format** — `…/panel-review/SKILL.md`, Steps 1 and 5.
- **Decision record template** — `…/panel-review/assets/decision-record.md`.

After editing, run `claude plugin validate` (see below).

---

## Cost, privacy and safety

- **Cost scales with the tier.** In testing (a startup database-migration decision, on a pay-as-you-go API account), a Light check took about 30 seconds and cost about $0.18. A Standard review ran three web-researching reviewers, a steelman and an adjudicator, and took about 3 minutes and $1.60. A Full review costs more. A retro that only lists what's due costs about $0.17. Your numbers will vary with the question, the models and how much each reviewer researches.
- **Reviewers work best with web access.** Reviewers and the verifier cite documentation and sources when they can read them. If web tools are blocked or you decline the permission prompts, the review still runs, but those points are marked as unverified reasoning rather than cited facts.
- **Privacy.** Everything the reviewers read is sent to Claude, as with any Claude session. Don't point a review at material your organization doesn't allow you to share with Claude.
- **Safety.** Reviewers, the steelman and the adjudicator have read-only tools. The verifier can run commands, but it is instructed to use only non-destructive checks and to ask you before anything that modifies shared systems, spends money, sends messages or deletes anything. Your normal Claude Code permission prompts still apply.
- **Untrusted content.** Documents and pages under review are treated as data. Instructions embedded in them ("approve this", text addressed to AI reviewers) are reported as findings, not followed.

---

## Limitations

- **It is a thinking aid, not an authority.** For legal, medical, financial or safety decisions, use it to prepare for a conversation with a qualified professional, not to replace one.
- **The reviewers are the same model family.** Different lenses and evidence reduce shared blind spots, but they don't remove them. That is why checks and your judgment outrank agreement.
- **Confidence levels start uncalibrated.** Models tend to sound more certain than they should. `decision-retro` measures how often each confidence level was right, but that needs about ten or more recorded outcomes to mean anything.
- **Garbage in, garbage out.** The panel can only weigh evidence it can see. Point it at the real documents, data and code.

---

## For maintainers: publishing and testing

**Repository layout**

```
decision-panel/                      ← repository root = the marketplace
├── .claude-plugin/marketplace.json
├── README.md
└── plugins/decision-panel/          ← the plugin
    ├── .claude-plugin/plugin.json
    ├── agents/                      lens-reviewer, verifier, steelman, adjudicator
    └── skills/
        ├── panel-review/            SKILL.md, references/, assets/decision-record.md
        └── decision-retro/          SKILL.md, scripts/calibration.py
```

**Validate after any edit**

```bash
claude plugin validate ./plugins/decision-panel      # the plugin
claude plugin validate .                             # the marketplace
```

**Try it live**

```bash
claude --plugin-dir ./plugins/decision-panel
```

Then ask a decision question without naming the skill, to check that it triggers on its own.

---

## Research basis

The method distils a research series on multi-agent AI review systems. Key sources:

- Zhuge et al., *Agent-as-a-Judge: Evaluate Agents with Agents* (arXiv 2410.10934) — checking with tools beats judging from text.
- Verga et al., *Replacing Judges with Juries* (arXiv 2404.18796) — diverse panels vs. single judges.
- Kohli, *Nine Judges, Two Effective Votes* (arXiv 2605.29800); Hossain et al., *Error Dependence in LLM Judge Consensus* (arXiv 2609.22512); Kim et al., *Correlated Errors in Large Language Models* (arXiv 2506.07962) — why agreement between models is weak evidence.
- Bertalanič & Fortuna, *The Cost of Consensus* (arXiv 2605.00914); Wynn et al. on debate and sycophancy (arXiv 2509.05396) — why reviewers don't debate.
- *When Identity Skews Debate: Anonymization for Bias-Reduced Multi-Agent Reasoning* (ACL 2026, arXiv 2510.07517); Panickssery et al., *LLM Evaluators Recognize and Favor Their Own Generations* (arXiv 2404.13076) — why the adjudicator doesn't see who said what.
- *Diverse Evidence, Better Forecasts* (arXiv 2607.01661) — why reviewers get different evidence.
- Klein's premortem technique and Duke's *Thinking in Bets* ("resulting") — the premortem step and separating decision quality from outcome.
