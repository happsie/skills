---
name: quick-fix
description: Make a small, local change without the full implement workflow, held to the same standards. For when the cause and the fix are known and nothing needs deciding, such as a typo, a wrong value, a missing check or a bug in one place. Checks the change against the glossary and the ADRs, writes a short spec the developer approves once, builds it test-first in a worktree, then hands over to deliver for the independent checks and the pull request. Use when the user says "quick fix", "small fix", "just fix this", "tiny change", "one-liner", "fix this typo", "bump this value". Input is free text or a ticket key from any tracker (Jira, GitHub, Linear, ...). Not for an unknown cause (investigate), and not for work that needs a decision, a new domain term, a refactor or a migration (implement). Stops and hands over to implement when the fix turns out bigger than it looked.
---

# Quick fix

The `implement` workflow has four approvals and a row of subagents. That is the right price for a feature and too high for a wrong default value. When the price is too high the process gets skipped altogether, and then nothing is checked. This skill is the short path: one approval before the code, one before the pull request, and the same standards in between.

What it keeps:

- The ask rule.
- The glossary and the ADRs. The change follows them.
- A test before the fix.
- A worktree, never the developer's checkout.
- The independent checks in `deliver` before the pull request: against the spec, and a review of the code.
- The findings log, so `retro` can learn from small changes too.

What it drops: the question rounds in `refine`, the refactor analysis in `strategic-design`, the plan, and the build subagents. You read the code and build the change yourself. The other skills hand that work to subagents because it fills a context. A quick fix doesn't, and if it starts to, it isn't one.

## The ask rule

No assumptions, and no decisions on the developer's behalf. Reading code and tickets, running tests and writing `spec.md` need no permission. Once the spec is approved, neither do creating the worktree and writing the test and the change the spec describes.

Everything else is a question: something unexpected happens, a test fails for the wrong reason, a test you didn't touch goes red, the build or a tool doesn't work, or the change needs something the spec doesn't describe. Say what you found (with `file:line` or the actual output), the options, and what you recommend. Then wait.

Never do these to get past a problem: weaken, change, skip or disable a test, try another approach than the approved one, or widen the scope. The `implement` skill owns the full rule ("The ask rule"), and it holds here.

In a quick fix most questions mean the same thing: this is not a quick fix. See "When it stops being quick".

## What counts as a quick fix

All of these must hold. Check them in step 2, and keep checking while you build.

- **The change is known.** You can point at the lines that are wrong and say what they should be. For a bug, the cause is known, not guessed. A cause the `investigate` skill proved counts.
- **It is small and local.** One repo. One place, or the same small edit in a few places. A diff the developer reads in a minute: as a guide, a few dozen lines at most, tests not counted.
- **Nothing needs deciding.** Reading the code leaves no open question about what it should do. One point read back for confirmation is fine. A list of questions is `refine`'s job.
- **The code already has the right shape.** No refactor first, and no new abstraction.
- **The language holds.** The change needs no new glossary term, changes no term's meaning and breaks no recorded rule.
- **The decisions hold.** It follows the accepted ADRs for the area, and makes no decision that deserves an ADR of its own (the `adr` skill, "What gets an ADR").
- **Nobody else has to adapt.** No migration, no change to an API contract, a message format or stored data, no new dependency, no feature flag. Whatever calls or consumes the changed code behaves as before, apart from the fix itself.
- **Nothing changes in how it runs.** It trusts no new input, changes nothing about who may do what, adds no query or call on a busy path, and is deployed and reverted as plain code. These are the points `refine` checks as non-functional requirements (its step 3), and for a quick fix every one of them comes out as "no change".
- **Existing tests keep their expected results.** If a test asserts the behavior you are about to change, somebody decided that behavior once. Changing it is a real question.

## When it stops being quick

If one of those points fails, at any time, stop. Tell the developer which point failed and what you found, with `file:line`, and recommend the skill that fits: `investigate` when the cause turned out not to be known, `implement` for everything else. The developer decides. Don't carry on quietly, and don't switch skills quietly either.

Nothing is thrown away when the work moves to `implement`:

- Set `spec.md` back to `Status: draft` and add what you found under a **Why this is not a quick fix** heading. `refine` continues from that file.
- Leave the worktree as it is, and say what is in it: the branch, any commits, any uncommitted changes. `implement` uses the same worktree.

## Where things live

`spec.md` and the worktree are in the work's folder: `work/<key-or-slug>/` in a home repo, otherwise `.implement/<key-or-slug>/` at the root of the repo. The `refine` skill owns the rule ("Where the documents live"): how the folder is named and kept out of git, and the status line the spec starts with. A quick fix has no `plan.md`.

The folder also holds `findings.md`, the log of what went wrong along the way. Add an entry when a question stops the work, with the answer it got, and when the developer corrects something. The `retro` skill owns the format ("The findings log"). Appending to it needs no permission.

If the folder already holds a spec or a plan from `implement`, this work is already in the full workflow. Say so and ask, instead of starting a quick fix beside it.

## 1. Gather the request

Take free text as given, and fetch a ticket the way `refine` does in its step 1: the description, the acceptance criteria and every comment. Don't work from a title alone. If the work's folder has an `investigation.md`, read it; its cause and reproduction are where this fix starts.

## 2. Read the code and check that it is a quick fix

Read it yourself:

- The lines to change, what calls them, and the tests that cover them.
- The glossary entries for the terms the change touches, and the names the code uses for them. `refine` says where the glossary is ("The shared language").
- The ADRs for the area. `adr` says where they are.
- The repo's coding standards, `CLAUDE.md` or `AGENTS.md`.
- The test layer the new test belongs in, and the exact command that runs it.

Check that the code you read is the code the work will start from, the way `refine` does at the end of its step 2. The fix is built in a worktree cut from the remote's default branch, not in this checkout.

If you have opened more than a handful of files and still can't say exactly what the change is, it is not a quick fix.

Then go through "What counts as a quick fix", point by point. For a bug, state it as: given X, expected Y, actual Z.

## 3. Write the short spec and get it approved

Write `spec.md`, and post it in the chat as well. It starts with the status line, then a line that says `Kind: quick fix`, then:

- **Goal:** one sentence.
- **Type:** change or bug. For a bug: given X, expected Y, actual Z.
- **Today:** what the code does, with `file:line`, and the commit it was read at.
- **After:** what it does instead.
- **Acceptance criteria:** usually one to three. Each one must be checkable by a test.
- **Out of scope:** what a reader might expect to be fixed along the way but isn't.
- **Language:** the glossary terms the change touches, each with the words not to use for it. All of them exist already.
- **Change:** the lines to change and what they become. The test: what it asserts, its layer and the command that runs it. If no test fits (a typo in a comment, a value no test can reach), say why instead of inventing one. The branch name and the branch it starts from, the default branch unless the developer says otherwise. One commit.

Like every spec, it has no assumptions section. If there is one point to confirm, ask it together with the spec.

Wait for an explicit approval, then set the status line. That approval covers the worktree, the test and the change as the spec describes them, and nothing beyond it.

## 4. Build it

Create the worktree the way `implement` says ("Work in a worktree"): where it goes, how it is set up, and the check of its starting point. Where that section says the plan, read the spec's Change section. Write the worktree's path into `spec.md` under a **Worktree** heading. That is not a change to the spec and leaves its status as it is.

Then build it yourself, test first:

1. **Red.** Write the test and run it. It must fail for the reason the spec gives. For a bug this is the reproduction. If it passes, or fails for another reason, the cause is not what the spec says: stop, and see "When it stops being quick". Never ship a speculative fix.
2. **Green.** Write the least code that makes it pass. Match the surrounding code and reuse existing helpers.
3. **Tidy.** Only the code you just wrote, with the tests green.

The rules for the loop in `implement` (3.4) hold here: a test is never edited, skipped or disabled to get to green, names use the agreed terms, the code follows the repo's coding standards, no dependency is added, and nothing outside the spec is touched. Debt you notice next to the fix goes in the report, not in the diff.

Run the test layers the change touches, the build, and the linter or type checker, in the worktree. Show the output of any failure and ask what to do about it. Don't report success on anything you didn't run.

Commit on the branch, never on the default branch.

## 5. Deliver

Run the `deliver` skill without waiting to be asked. It has two subagents with a fresh context look at the diff, one that checks it against the spec and one that reviews the code. It reports their verdicts, describes the change so the developer can approve the code, and opens the pull request once they do.

Don't do those checks yourself, and don't skip them because the diff is small. Small diffs get waved through, and that is how they break things. If a verdict leads to more work and the work is still a quick fix, do it under the same rules and let `deliver` check again.

Review comments and failing checks on the pull request go through the `revise` skill. It makes its fixes under the rules of this skill for as long as the work is still a quick fix.

## Report

Keep it short:

- The pull request and the verdicts from `deliver`.
- The test that proves the fix, with `file:line`. For a bug: whether it reproduced.
- What changed, by file.
- Anything unverified, and anything you noticed next to the fix and left alone.
