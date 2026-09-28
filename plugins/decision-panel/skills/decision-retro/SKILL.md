---
name: decision-retro
description: Close the loop on past decisions — record how a decision actually turned out, judge whether it was a sound decision given what was known at the time (separately from whether it worked out), check whether past confidence levels were calibrated, and turn the misses into lessons that future panel reviews use. Use when the user wants to review, revisit or follow up on an earlier decision ("how did that call turn out", "let's do a retro on the vendor choice", "we reversed that decision", "which decisions are due for review", "are my confidence levels any good"), when a decision record's revisit date has passed, or when a revisit trigger has fired.
---

# Decision retro

Decisions improve when their outcomes are fed back. This skill is the learning loop for `panel-review`: it reads decision records, captures what actually happened, separates **decision quality** from **outcome luck**, measures whether stated confidence matched reality, and proposes lessons for specific review lenses. Lessons change future reviews only once the user approves them.

Nothing here retrains a model. Learning happens through a written record that future reviews read: decision records, a calibration tally, and a short, curated lessons file.

## Step 1 — Find the decision log

Look for decision records (`DR-*.md` files with YAML front matter) in the project's decision folder: `docs/decisions/`, `docs/adr/` or `decisions/`, in that order. `panel-review` writes them; the front matter fields this skill uses are `id`, `title`, `date`, `status` (`decided` / `resolved` / `reversed` / `superseded`), `decision`, `confidence` (`high` / `moderate` / `lean` / `low`), `revisit_by`, `outcome` and `decision_quality`. The body has sections for options, key evidence, key assumptions, dissent, revisit triggers and an empty "Outcome" section for this skill to fill in.

- If the user named a decision, open that record.
- If they asked what's due, list records whose `status` is `decided` and whose `revisit_by` date has passed or is within two weeks, most overdue first.
- If there is no log, say so. Offer to record the decision retrospectively (reconstructed from what the user tells you, marked as reconstructed) or to start a log going forward.

## Step 2 — Capture the outcome

Ask the user, or gather from the evidence they point you to:

- **What happened?** Concretely, with dates and numbers where they exist.
- **Did the key assumptions hold?** Go through the record's "Key assumptions" one by one.
- **Did any revisit trigger fire?** Was it acted on?
- **What do we know now that we didn't then?** And could it reasonably have been known at the time?

Prefer evidence to recollection. Memory rewrites decisions after the fact, so read the actual metrics, tickets, messages or documents when they're available.

## Step 3 — Judge the decision, not just the result

Good decisions sometimes turn out badly and bad ones sometimes turn out well. Judging a decision only by its outcome ("resulting") teaches the wrong lessons, so score the two separately:

- **Outcome**: `as-expected`, `better`, `worse` or `mixed`, compared with what the record predicted.
- **Decision quality**: `sound` or `flawed`, judged **only on what was known or reasonably knowable at the time**. It's flawed if a material risk was visible but missed, the evidence was misread, a checkable assumption went unchecked, or the stated confidence was out of proportion to the evidence.

When outcome and quality disagree (a sound decision with a bad outcome, or a flawed one that got lucky), say so explicitly. Those cases teach the most.

## Step 4 — Update the record

Fill in the record's `outcome` and `decision_quality` fields and set `status` (`resolved`, `reversed` or `superseded`). Write the "Outcome" section: what happened, which assumptions held or failed, and the quality judgement with its reasoning. Show the user the change before saving. The record is theirs.

## Step 5 — Check calibration (when there's enough history)

Once **ten or more** records are resolved, tally them by stated confidence. If Python is available, run the bundled script (`scripts/calibration.py` in this skill's folder; in Claude Code the path is below):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/calibration.py" <decision-folder>
```

Otherwise count by hand: for each confidence bucket, how many decisions had an `as-expected` or `better` outcome. Compare with what the bucket claims (High ≈ 85%+, Moderate ≈ 65–85%, Lean ≈ 50–65%). With fewer than about five decisions in a bucket, say the numbers are too thin to conclude anything.

If a bucket is consistently wrong — for example "High" decisions working out only 60% of the time — that is the most valuable finding a retro produces. Report it plainly, and propose a lesson that tightens what "High" requires.

## Step 6 — Propose lessons

From flawed decisions, surprises and miscalibration, draft **at most three** lessons per retro. A useful lesson is:

- **Specific and actionable**: "Cost lens: include migration and retraining effort. It was left out of three of the last four tool decisions." Not "consider costs more carefully."
- **Filed under one lens** — the lens that should have caught it: Feasibility, Risk & failure modes, Cost & resources, People & stakeholders, Security privacy & compliance, Long-term & reversibility, Outside view, or Contrarian. `panel-review` hands each lens only its own lessons. Spreading every lesson to every reviewer would make the reviewers think alike, which is the failure the panel design avoids.
- **Evidenced**: it names the decision record(s) it came from.

**Show the proposed lessons to the user and add only the ones they approve.** Lessons steer every future review, so a wrong one does lasting damage. Append approved lessons to `LESSONS.md` in the decision folder, in this format:

```markdown
## <Lens name>
- <Lesson> — source: <DR ids> — added: <YYYY-MM-DD> — review by: <date ~6 months out>
```

When a retro finds that a lesson has stopped applying, or has been wrong, propose removing it the same way. The lessons file should stay short enough to read in a minute.

## Output

End with a short summary: the outcome, the quality judgement and why, any calibration finding, and the lessons added (or proposed and declined).
