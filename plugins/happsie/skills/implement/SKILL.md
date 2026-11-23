---
name: implement
description: Implement a feature, task, bug fix or ticket end to end. Refines the request into a spec the developer approves, does a strategic design pass that decides whether to refactor first, builds with test-driven development, then has the result checked against the spec by an independent subagent and opens the pull request. Never assumes; every open decision or unexpected problem goes to the developer as a question. Use whenever the user asks to implement, build, code, fix, start or pick up something (e.g. "implement PROJ-123", "start on this ticket", "build this feature", "fix this bug", "let's do this one"), or gives a bare ticket key with intent to work on it. Input is free text or a ticket key from any tracker (Jira, GitHub, Linear, ...). Not for planning-only or review-only requests. A small, local change with nothing to decide can go through quick-fix instead.
---

# Implement

Four phases, each ending in something the developer has approved:

1. **Refine**: agree on what to build. Ends with an approved spec.
2. **Strategic design**: decide what shape the code should have, and refactor first if that makes it healthier. Ends with an approved plan and a finished refactor.
3. **Build**: test-driven, following the plan.
4. **Deliver**: an independent check against the spec, then the pull request.

Don't skip or reorder phases, however small or well defined the task looks. A small task makes each phase short, not optional.

There is one shorter path, and taking it is not your call. A small, local change with nothing to decide can go through the `quick-fix` skill instead. If the task looks like one, say so once before phase 1 and let the developer choose. Unless they choose it, run all four phases.

## The ask rule

This applies to every phase and overrides everything else in this skill.

**No assumptions, and no decisions on the developer's behalf.** Stop and ask when:

- A decision isn't covered by the approved spec or the approved plan.
- Something unexpected happens: a test fails for the wrong reason, a test you didn't touch goes red, the build breaks, the code behaves differently than the plan says, a tool or environment doesn't work.
- You want to deviate from the plan, however slightly.
- The spec or plan turns out to be wrong or incomplete.

What needs no permission: reading code and tickets, running tests and builds, creating the worktree the approved plan names, writing the tests and code that the plan already describes, and keeping `spec.md` and `plan.md` up to date.

When you ask, state what you found (with `file:line` or the actual output), the options, and what you recommend. Then wait. Don't try a workaround while waiting, and don't carry on with other work that depends on the answer.

Never do these to get past a problem: weaken or change a test, skip or disable a test, retry with a different approach than the plan's, widen the scope, or guess at what the developer meant.

A subagent can't ask the developer, so it asks you: it stops and returns the question, and you pass it on. Never answer for the developer. See 3.4.

## Keep the context small

An agent with a full context gets worse at everything: it forgets the rules, loses track of the plan and stops noticing its own mistakes. On a large codebase one ticket fills a context several times over, so this skill keeps the heavy work out of the main thread.

- **You hold the spec, the plan and the reports.** Reading through code and writing code is done by subagents, which start with a clean context and hand back a short report. `refine` reads the code this way, `strategic-design` maps the change and carries out the refactor this way, the build in phase 3 runs one subagent per feature step, and `deliver` checks the result in another. Open code yourself only to check a specific claim or to answer a specific question.
- **The files carry the state.** `spec.md` and `plan.md` hold everything the next phase needs, so nothing is lost when a session ends. When the spec is approved, and again when the plan is approved and the refactor is done, tell the developer that this is a good point to clear the context or start a new session, and that running `implement` on the same work picks it up from the files.
- **This costs more tokens in total**, since every subagent reads its part of the code from scratch. That is the price of a context that stays sharp to the end.

## Where the documents live

The spec and the plan are files, so they survive a long session and can be picked up in a new one. They are in the work's folder: `work/<key-or-slug>/` in a home repo, otherwise `.implement/<key-or-slug>/` at the root of the repo being worked on. The `refine` skill owns the rule ("Where the documents live"): how the folder is named and kept out of git, and the status line each file starts with. Only the developer's explicit approval sets a file to approved, and any later change sets it back to draft until it is approved again.

Writing and updating these two files needs no permission. Don't commit them unless asked.

`plan.md` also records progress: `strategic-design` ticks off each refactor step when it is done, and the build does the same for each feature step once it is committed. That is not a change to the plan and leaves its status as it is.

When starting, look for an existing folder for this work. If `spec.md` or `plan.md` is already approved, tell the developer what you found, including which steps are ticked off, and ask whether to resume from there or start over.

If the developer's answer to a question changes the spec or the plan, update the file and get it approved again before going on.

## Work in a worktree

All code for a piece of work is written in a git worktree made for it, never in the developer's checkout. The checkout stays as the developer left it: they can keep working there, switch branches or start a second piece of work while this one builds, and no agent touches their uncommitted changes.

There is one worktree per piece of work, for each repo it changes, and every step uses it. It is not one per subagent: the steps build on each other, so they all work on the same branch in the same place. If the agent tool can give a subagent a worktree of its own, don't use that.

- **Where.** `worktrees/<repo_name>/` inside the work's folder, next to `spec.md` and `plan.md`. Outside a home repo `.implement/` is already kept out of git. In a home repo, add `work/*/worktrees/` to the home repo's `.git/info/exclude`.
- **When.** Right before the first file is written on the branch: a glossary change or an ADR that lives in the repo, the refactor in `strategic-design`, or the build when there is none of those. Never before the plan is approved.
- **How.** Fetch, then `git worktree add` at that path with the branch name and the starting point from the plan's Git section. If the branch already exists, add the worktree for that branch instead of creating it. If the branch is checked out somewhere else, or the worktree can't be created, ask. If the work came over from `quick-fix`, its worktree is already there and `spec.md` names it: use it, and ask what to do with unfinished changes in it.
- **Set it up.** A new worktree holds the tracked files and nothing else: no installed dependencies, no build output, no local files that git ignores. Run the repo's install or build step. If the tests need an untracked local file from the checkout, such as an `.env`, copy it over and tell the developer which files you copied.
- **Check the starting point.** The spec and the plan were written from the developer's checkout, and the worktree is cut from the remote. Those can be different code. The spec names the commit it was read at: list the files the spec and the plan refer to that differ between that commit and the worktree (`git diff --name-only <that commit> HEAD -- <files>`). If any do, stop and ask, since the spec's Today and the plan's steps may no longer hold. Then run the plan's test commands once, before the first change. They must be green here. A green run in the checkout says nothing about this code. If they are red, stop and ask.
- **Write the glossary change.** If the spec's Language section has new or changed terms and the glossary is a tracked file in the repo, `refine` left the file alone so the checkout stays untouched. Write the entries in the worktree now, the way `refine` describes in its step 6, and commit them where the plan says.
- **Write it down.** Put each repo's worktree path in `plan.md` under a **Worktrees** heading. Like ticking off steps, this leaves the plan's status as it is.

From then on the worktree is the repo path for everything: it is what subagents are given, and where you run tests and check their reports. The checkout is only read.

When resuming, use the worktree `plan.md` lists. If it is gone but the branch is still there, add it again.

The worktree stays after the pull request is opened, since review comments get fixed there. Never remove it yourself; `deliver` tells the developer how.

## Phase 1: Refine

Run the `refine` skill on the input. It gathers the request, reads the code, asks its questions and ends with an approved `spec.md`. The spec's Language section holds the agreed terms and rules, and `refine` writes them to the glossary. The later phases follow them.

Don't go on without an explicit approval of the spec.

## Phase 2: Strategic design

Run the `strategic-design` skill with the approved spec. It maps the changes the feature needs and the test layers the repo has, judges whether a preparatory refactor would leave the code healthier, gets the plan approved, records the plan's decisions as ADRs through the `adr` skill, and carries out any approved refactor. It never changes behavior or what existing tests expect.

Don't go on until the plan is approved, any refactor is finished, and every test is green.

## Phase 3: Build with TDD

Work test-first. Every test should pin down behavior someone relies on. A test that exists only to raise coverage costs maintenance and adds nothing.

You run this phase and subagents do the building, one feature step each (3.4). If phase 2 wrote nothing to the branch, the worktree doesn't exist yet: create it first ("Work in a worktree"), and run everything below in it. Steps 3.1 to 3.3 prepare what they need.

### 3.1 Check the test layers

`strategic-design` mapped the test layers and wrote them into `plan.md` under **Test commands**: unit, integration, BDD (`.feature` files and their step definitions), end to end, each with its exact command and what it needs to run. Every build subagent works from that list, and so does a session that resumes later.

Check that it covers every layer this work needs. For BDD, read the existing feature files and step definitions for the area so you can reuse them.

If a layer the work needs is missing from the list or can't run locally, ask before going on. Adding a command to the list is not a change to the plan and leaves its status as it is.

### 3.2 Bugs: reproduce first

For a bug, don't touch production code until a test reproduces it.

1. State the bug as: given X, expected Y, actual Z.
2. Write a test that asserts the expected behavior, in the layer closest to where the bug shows.
3. Run it. It must fail for the reason the bug describes. A compile error or a setup failure doesn't count.
4. If it passes, or you can't reproduce the bug, stop and ask. Report what you tried and the plausible explanations. Never ship a speculative fix. Finding an unknown cause is the job of the `investigate` skill.

That test is the first red of the loop in 3.4.

### 3.3 Choose the scenarios

Derive scenarios from the spec's acceptance criteria and the real edge cases on the code path: boundaries, empty or missing data, error responses, permissions, concurrency where it matters. Each rule in the spec's Language section that the work touches is a scenario too, unless a test already pins it. A rule nothing tests gets broken by the next change. For each, check:

- Would this test fail if the behavior broke?
- Would anyone care if it broke?
- Is it already covered, at this layer or another?

Drop what fails those checks: getters and setters, framework behavior, tests that only verify a mock was called, near-duplicates. If a step needs no new test (config, a pure rename), say so instead of inventing one.

Put each scenario in the right layer:

- **BDD**, if the repo has BDD tests for the area and the scenario is business-visible behavior. Use the existing style and reuse step definitions.
- **Integration**, for behavior that depends on persistence, messaging, HTTP contracts or wiring.
- **Unit**, for logic: branching, calculations, validation, mapping.

Don't push everything into unit tests because they are easiest, and don't repeat one scenario in every layer.

Post the list, one line per scenario with its layer, the acceptance criterion or rule it covers and the feature step it belongs to. Wait for a go-ahead before any of them is written.

To find the edge cases and what is already covered, use the code facts `refine` collected and the `file:line` references in the plan. If that isn't enough, send a read-only subagent to look, as `refine` does, instead of reading the code path yourself.

### 3.4 The loop

Build the feature steps from the plan in order, each one in a new subagent with a clean context. Never use a fork of this conversation, and never reuse the subagent that built an earlier step: the point is that each step starts without the history of the others. One at a time, never in parallel. The steps build on each other and share one branch and one worktree.

Give the subagent:

- The paths to `spec.md` and `plan.md`, and which feature step is its own. It reads the whole of both, and builds only its step.
- The scenarios for that step from 3.3, each with its layer.
- The worktree paths and the branch. It works only in the worktree, on that branch, and never in the developer's checkout or on the default branch.
- The rest of this section, from "Work outside-in" to the end of the report list, passed on as it is.

Don't tell it how you would build the step or what you expect it to run into. The plan says what to build.

Work outside-in: when a BDD or integration scenario applies, write it first as the outer red, then drive the code with unit tests inside it.

For each scenario:

1. **Red.** Write the test. Run it. Confirm it fails for the expected reason.
2. **Green.** Write the least production code that makes it pass. Match the surrounding code and reuse existing helpers.
3. **Refactor.** Tidy the code you just wrote, with tests green. Rerun.

The refactor step here covers only code written in this phase. Anything larger belongs in phase 2: stop and ask.

Rules for the loop:

- A test that fails for an unexpected reason, or a test you didn't write going red, stops the work. Ask.
- So does a build that breaks, and a tool or an environment that doesn't work. Don't work around it.
- Never edit a test to get it green, and never skip, disable or delete one. If you believe a test is wrong, stop and ask.
- Build the step the way the plan describes it. If that way doesn't work, don't try another one. Ask.
- Existing tests keep their expected results unless the spec says that behavior changes. If one has to change and the spec doesn't cover it, ask.
- Name things with the terms in the spec's Language section: types, functions, fields, tests, scenario text and anything a user reads. Never use a word the spec says not to use, and don't coin a synonym. If the code needs a domain concept that has no agreed term, stop and ask.
- Stay inside the spec and the plan. No speculative abstractions, no unrelated cleanup.

Commit where the plan says to, on the branch, never on the default branch.

If you hit anything the rules above say to ask about, stop there. Leave the working tree as it is, don't try a workaround, and report back with the question: what you found (with `file:line` or the actual output), the options, and what you recommend. You will get the answer and carry on from where you stopped.

When the step is done, run the test layers it touched and report:

- Each scenario, with the test's `file:line`, the failure it showed when red and the result when green.
- What changed, by file.
- The commits made.
- The test commands run and their results, with the output of any failure.
- Anything you couldn't run or verify, and anything you noticed that a later step or the developer should know.

When a subagent comes back:

- **With a question:** post it to the developer as it came, and wait. Don't answer it yourself, even when the answer looks obvious from the spec; if it were covered there, the subagent would not have had to ask. Then send the answer to the same subagent so it continues with what it already knows. If it can't be continued, start a new one with the step, the question, the answer and a note that the working tree holds unfinished work from the first attempt.
- **With a report:** check it before going on. The step's commits exist, the working tree is clean, and the tests it names pass when you run them. A report is a claim until then. If something doesn't hold, that is something unexpected: stop and ask.

If an answer changes the spec or the plan, update the file and get it approved again before the next step starts. If the answer is a decision that deserves an ADR, it goes under the plan's Decisions and is recorded the way `strategic-design` does it, once the plan is approved again.

Tick the step off in `plan.md`, tell the developer in a line or two what was built, and start the next one.

### 3.5 Verify

When every step is ticked off, run every affected test layer, the build, and the linter or type checker yourself, in the worktree. Show the output of any failure, and ask what to do about it. If something can't be run, say exactly what is unverified. Don't report success on anything you didn't run.

## Phase 4: Deliver

When the build is verified and committed, run the `deliver` skill without waiting to be asked. It has a subagent with a fresh context check the diff against the spec, reports the verdict, and opens the pull request once the developer approves it.

Don't do that check yourself and don't skip it because the tests are green. If the verdict leads to more work, do it under the rules of phase 3, in a new build subagent that gets the finding as its step, and let `deliver` check again.

## Report

Keep it short:

- The pull request and the verdict from `deliver`.
- For a bug: whether it reproduced, and the test that proves the fix.
- Scenarios covered, and in which layer.
- What was refactored first, and what was built, by file.
- Each question that came up along the way and the answer given.
- The ADRs written.
- Anything unverified or left open.
