---
name: strategic-design
description: Strategic programming step between agreed requirements and writing the feature. Takes an approved brief, maps the code changes the feature needs, and asks whether the code would be healthier if it were refactored first so the feature becomes a small, obvious change. Proposes a preparatory refactor (or says none is needed), gets it approved, and carries it out without changing behavior or the expected results of existing tests. Use when the user asks "should we refactor first", "do a strategic analysis", "design this before we build it", "prep refactor for this feature", "make the change easy first", or as the second phase of the implement skill.
---

# Strategic design

Tactical programming gets the feature working in the code as it stands and leaves the design a little worse each time. Strategic programming asks first what shape the code should have for this feature to fit well, and gets it into that shape before building. Make the change easy, then make the easy change.

This skill answers one question: **with this feature in it, would the code be healthier if we refactored first?** It then produces a plan the developer approves, and carries out the refactor part of it.

It needs an approved brief (goal, target behavior, acceptance criteria). Read it from `brief.md`. If there isn't one, or its status is still draft, run the `refine` skill first.

## The ask rule

No assumptions. Stop and ask the developer when:

- A decision isn't covered by the brief or the approved plan.
- Something unexpected happens: a test fails, the code behaves differently than the plan says, a step doesn't work.
- You want to do something the plan doesn't describe, however small.

Reading code, running tests and carrying out steps the approved plan already describes need no permission. When you ask, say what you found, the options, and what you recommend.

## Where the documents live

The brief and the plan are files, so they survive a long session and can be picked up in a new one. Each piece of work gets a folder named after the ticket key, or a short slug for free text:

- **In a home repo** (the current directory's `CLAUDE.md` says it is a home repo, as set up by the `home-repo` skill): `work/<key-or-slug>/` in the home repo. This holds even when the code changes land in other repos.
- **Anywhere else:** `.implement/<key-or-slug>/` at the root of the repo being worked on. Keep it out of git by adding `.implement/` to `.git/info/exclude`. Don't edit the repo's `.gitignore` for this.

The folder holds `brief.md` (written by `refine`) and `plan.md` (written by `strategic-design`). Each starts with a status line: `Status: draft`, or `Status: approved <YYYY-MM-DD>` once the developer has approved it. Only the developer's explicit approval sets it to approved. Any later change sets it back to draft until approved again.

Writing and updating these two files needs no permission. Don't commit them unless asked.

## 1. Map the tactical change

Work out what the feature would look like if it were built straight into the code as it is today. List every place that would change, with `file:line`, and what would change there. This is the baseline the refactor is judged against. Don't write any of it.

## 2. Judge the health of that change

Look at the tactical version and at the code around it. Signs that the code is the wrong shape for this feature:

- The same edit is needed in several places.
- It adds another branch to a conditional or type switch that already has several.
- A function or class picks up one more responsibility, or one more parameter or flag that only some callers use.
- The new behavior can't be tested without heavy setup or mocking.
- New code has to reach through layers, or copy knowledge that lives somewhere else.
- A name or abstraction stops being true once the feature exists.
- This is the second or third variant of something handled ad hoc each time.
- The code to change is hard enough to follow that the change itself is risky.

If you don't understand why the code is built the way it is, ask before judging it. Check ADRs and `git log` first.

## 3. Decide: refactor first, or not

For each problem found in step 2, ask what shape of code would make the feature a small, local change. Typical moves: extract a function or class, split a responsibility, move logic to the data it uses, introduce an interface so variants plug in, replace a conditional with polymorphism, add a seam that makes the code testable.

Rules for the proposal:

- **A pattern must earn its place.** Name a design pattern only when it removes a concrete problem from step 2. Never introduce one for its own sake or for features that might come later.
- **"No refactor needed" is a valid answer**, and often the right one. If the tactical change is already small and clean, say so and move on.
- **Stay inside the feature's path.** Refactor only code the feature touches. Report other debt you notice as a note; don't act on it.
- **Match the codebase.** Use the patterns and conventions the project already uses before bringing in new ones.
- **Weigh the cost.** A refactor that is larger or riskier than the feature needs a strong reason.

## 4. Check the safety net

A refactor is only safe if tests pin the current behavior.

- Find the tests that cover the code to be refactored and run them. They must be green before anything changes. If any are red, stop and ask.
- Where coverage is missing or thin, plan characterization tests: tests that pin what the code does today, written and green before the refactor starts. They record current behavior, including behavior that looks wrong. Report anything that looks wrong; don't fix it.

## 5. Present the plan and get it approved

Write `plan.md` next to the brief with the sections below, and post it in the chat as well:

- **Tactical version:** the changes from step 1, and what they cost the design.
- **Recommendation:** refactor first, or no refactor, with the reason in a sentence or two.
- **Refactor steps:** ordered, small, each one leaving the tests green. Empty if none.
- **Characterization tests:** which ones to add first, and what they pin.
- **Feature steps:** how the feature gets built once the code has its new shape. Ordered, each one tied to acceptance criteria from the brief.
- **Risks and open questions.**
- **Git:** branch name, and where the commits fall. Refactor commits and feature commits are always separate.

Wait for an explicit approval. The developer may take the refactor, reject it, or cut it down. Update the file and confirm again after any change, then set its status line once approved. If they reject the refactor, the feature steps follow the tactical version.

## 6. Carry out the refactor

Only after approval, and only if the plan has refactor steps. Work on a branch, never on the default branch.

1. Add the characterization tests. Run them. They must pass against the unchanged code.
2. Take one refactor step. Run the tests. Green means go on to the next step.
3. Commit where the plan says to.

Hard rules:

- **No behavior change.** A refactor changes structure only. No feature code in this phase.
- **Never change what an existing test expects.** Assertions, expected values and test data stay exactly as they are. That includes the characterization tests once they are written.
- **Mechanical test edits are allowed**, and only these: imports, renamed or moved symbols, and setup or wiring that moved code makes necessary. List every such edit in the report.
- **Never delete, skip or disable a test.**
- **A red test stops the work.** If a test can't stay green without changing what it asserts, either the refactor changed behavior or the test is tied to the old structure. Don't decide which. Stop and ask.
- **Don't go past the plan.** If the refactor turns out to need more than was approved, stop and ask.

## 7. Hand off

Report:

- What was refactored, and where.
- Test results before and after.
- Every mechanical test edit made.
- The feature steps, updated in `plan.md` if the refactor changed anything about them. A changed plan needs approval again.
- Debt noticed outside the feature's path.
