---
name: implement
description: Implement a feature, task, bug fix or ticket end to end. Refines the request into a brief the developer approves, does a strategic design pass that decides whether to refactor first, builds with test-driven development, then has the result checked against the brief by an independent subagent and opens the pull request. Never assumes; every open decision or unexpected problem goes to the developer as a question. Use whenever the user asks to implement, build, code, fix, start or pick up something (e.g. "implement PROJ-123", "start on this ticket", "build this feature", "fix this bug", "let's do this one"), or gives a bare ticket key with intent to work on it. Input is free text or a ticket key from any tracker (Jira, GitHub, Linear, ...). Not for planning-only or review-only requests.
---

# Implement

Four phases, each ending in something the developer has approved:

1. **Refine**: agree on what to build. Ends with an approved brief.
2. **Strategic design**: decide what shape the code should have, and refactor first if that makes it healthier. Ends with an approved plan and a finished refactor.
3. **Build**: test-driven, following the plan.
4. **Deliver**: an independent check against the brief, then the pull request.

Don't skip or reorder phases, however small or well defined the task looks. A small task makes each phase short, not optional.

## The ask rule

This applies to every phase and overrides everything else in this skill.

**No assumptions, and no decisions on the developer's behalf.** Stop and ask when:

- A decision isn't covered by the approved brief or the approved plan.
- Something unexpected happens: a test fails for the wrong reason, a test you didn't touch goes red, the build breaks, the code behaves differently than the plan says, a tool or environment doesn't work.
- You want to deviate from the plan, however slightly.
- The brief or plan turns out to be wrong or incomplete.

What needs no permission: reading code and tickets, running tests and builds, writing the tests and code that the approved plan already describes, and keeping `brief.md` and `plan.md` up to date.

When you ask, state what you found (with `file:line` or the actual output), the options, and what you recommend. Then wait. Don't try a workaround while waiting, and don't carry on with other work that depends on the answer.

Never do these to get past a problem: weaken or change a test, skip or disable a test, retry with a different approach than the plan's, widen the scope, or guess at what the developer meant.

## Where the documents live

The brief and the plan are files, so they survive a long session and can be picked up in a new one. Each piece of work gets a folder named after the ticket key, or a short slug for free text:

- **In a home repo** (the current directory's `CLAUDE.md` says it is a home repo, as set up by the `home-repo` skill): `work/<key-or-slug>/` in the home repo. This holds even when the code changes land in other repos.
- **Anywhere else:** `.implement/<key-or-slug>/` at the root of the repo being worked on. Keep it out of git by adding `.implement/` to `.git/info/exclude`. Don't edit the repo's `.gitignore` for this.

The folder holds `brief.md` (written by `refine`) and `plan.md` (written by `strategic-design`). Each starts with a status line: `Status: draft`, or `Status: approved <YYYY-MM-DD>` once the developer has approved it. Only the developer's explicit approval sets it to approved. Any later change sets it back to draft until approved again.

Writing and updating these two files needs no permission. Don't commit them unless asked.

When starting, look for an existing folder for this work. If `brief.md` or `plan.md` is already approved, tell the developer what you found and ask whether to resume from there or start over.

If the developer's answer to a question changes the brief or the plan, update the file and get it approved again before going on.

## Phase 1: Refine

Run the `refine` skill on the input. It gathers the request, reads the code, asks its questions and ends with an approved `brief.md`.

Don't go on without an explicit approval of the brief.

## Phase 2: Strategic design

Run the `strategic-design` skill with the approved brief. It maps the changes the feature needs, judges whether a preparatory refactor would leave the code healthier, gets the plan approved and carries out any approved refactor. It never changes behavior or what existing tests expect.

Don't go on until the plan is approved, any refactor is finished, and every test is green.

## Phase 3: Build with TDD

Work test-first. Every test should pin down behavior someone relies on. A test that exists only to raise coverage costs maintenance and adds nothing.

### 3.1 Map the test layers

Find which test layers the repo has and how each runs: unit, integration, BDD (`.feature` files and their step definitions), end to end. Note the exact command for each, and whether it needs Docker, a database or a local environment. For BDD, read the existing feature files and step definitions for the area so you can reuse them.

If a layer the work needs can't run locally, ask before going on.

### 3.2 Bugs: reproduce first

For a bug, don't touch production code until a test reproduces it.

1. State the bug as: given X, expected Y, actual Z.
2. Write a test that asserts the expected behavior, in the layer closest to where the bug shows.
3. Run it. It must fail for the reason the bug describes. A compile error or a setup failure doesn't count.
4. If it passes, or you can't reproduce the bug, stop and ask. Report what you tried and the plausible explanations. Never ship a speculative fix. Finding an unknown cause is the job of the `investigate` skill.

That test is the first red of the loop in 3.4.

### 3.3 Choose the scenarios

Derive scenarios from the brief's acceptance criteria and the real edge cases on the code path: boundaries, empty or missing data, error responses, permissions, concurrency where it matters. For each, check:

- Would this test fail if the behavior broke?
- Would anyone care if it broke?
- Is it already covered, at this layer or another?

Drop what fails those checks: getters and setters, framework behavior, tests that only verify a mock was called, near-duplicates. If a step needs no new test (config, a pure rename), say so instead of inventing one.

Put each scenario in the right layer:

- **BDD**, if the repo has BDD tests for the area and the scenario is business-visible behavior. Use the existing style and reuse step definitions.
- **Integration**, for behavior that depends on persistence, messaging, HTTP contracts or wiring.
- **Unit**, for logic: branching, calculations, validation, mapping.

Don't push everything into unit tests because they are easiest, and don't repeat one scenario in every layer.

Post the list, one line per scenario with its layer and the acceptance criterion it covers. Wait for a go-ahead before writing any of them.

### 3.4 The loop

Follow the feature steps from the plan, in order. Work outside-in: when a BDD or integration scenario applies, write it first as the outer red, then drive the code with unit tests inside it.

For each scenario:

1. **Red.** Write the test. Run it. Confirm it fails for the expected reason.
2. **Green.** Write the least production code that makes it pass. Match the surrounding code and reuse existing helpers.
3. **Refactor.** Tidy the code you just wrote, with tests green. Rerun.

The refactor step here covers only code written in this phase. Anything larger belongs in phase 2: stop and ask.

Rules for the loop:

- A test that fails for an unexpected reason, or a test you didn't write going red, stops the work. Ask.
- Never edit a test to get it green. If you believe a test is wrong, stop and ask.
- Existing tests keep their expected results unless the brief says that behavior changes. If one has to change and the brief doesn't cover it, ask.
- Stay inside the brief and the plan. No speculative abstractions, no unrelated cleanup.

Commit where the plan says to, on the branch, never on the default branch.

### 3.5 Verify

Run every affected test layer, the build, and the linter or type checker. Show the output of any failure, and ask what to do about it. If something can't be run, say exactly what is unverified. Don't report success on anything you didn't run.

## Phase 4: Deliver

When the build is verified and committed, run the `deliver` skill without waiting to be asked. It has a subagent with a fresh context check the diff against the brief, reports the verdict, and opens the pull request once the developer approves it.

Don't do that check yourself and don't skip it because the tests are green. If the verdict leads to more work, do it under the rules of phase 3 and let `deliver` check again.

## Report

Keep it short:

- The pull request and the verdict from `deliver`.

- For a bug: whether it reproduced, and the test that proves the fix.
- Scenarios covered, and in which layer.
- What was refactored first, and what was built, by file.
- Each question that came up along the way and the answer given.
- Anything unverified or left open.
