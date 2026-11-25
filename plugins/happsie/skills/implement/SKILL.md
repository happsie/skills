---
name: implement
description: Implement a feature, task, bug fix or ticket end to end. Refines the request into a spec the developer approves, does a strategic design pass that decides whether to refactor first, builds with test-driven development, then has independent subagents check the result against the spec and review the code, and opens the pull request once the developer has approved the code. Never assumes; every open decision or unexpected problem goes to the developer as a question. Use whenever the user asks to implement, build, code, fix, start or pick up something (e.g. "implement PROJ-123", "start on this ticket", "build this feature", "fix this bug", "let's do this one"), or gives a bare ticket key with intent to work on it. Input is free text or a ticket key from any tracker (Jira, GitHub, Linear, ...). Not for planning-only or review-only requests. A small, local change with nothing to decide can go through quick-fix instead.
---

# Implement

Four phases, each ending in something the developer has approved:

1. **Refine**: agree on what to build. Ends with an approved spec.
2. **Strategic design**: decide what shape the code should have, and refactor first if that makes it healthier. Ends with an approved plan and a finished refactor.
3. **Build**: test-driven, following the plan.
4. **Deliver**: an independent check against the spec and an independent code review, a description of the change to approve the code from, then the pull request.

Don't skip or reorder phases, however small or well defined the task looks. A small task makes each phase short, not optional.

There is one shorter path, and taking it is not your call. A small, local change with nothing to decide can go through the `quick-fix` skill instead. If the task looks like one, say so once before phase 1 and let the developer choose. Unless they choose it, run all four phases.

## The ask rule

This applies to every phase and overrides everything else in this skill.

**No assumptions, and no decisions on the developer's behalf.** Stop and ask when:

- A decision isn't covered by the approved spec or the approved plan.
- Something unexpected happens: a test fails for the wrong reason, a test you didn't touch goes red, the build breaks, the code behaves differently than the plan says, a tool or environment doesn't work.
- You want to deviate from the plan, however slightly.
- The work seems to need a dependency the plan doesn't name: a new package, service or tool, or a new major version of one.
- The spec or plan turns out to be wrong or incomplete.

What needs no permission: reading code and tickets, running tests and builds, creating the worktree the approved plan names, writing the tests and code that the plan already describes, and keeping `spec.md` and `plan.md` up to date.

When you ask, state what you found (with `file:line` or the actual output), the options, and what you recommend. Then wait. Don't try a workaround while waiting, and don't carry on with other work that depends on the answer.

Never do these to get past a problem: weaken or change a test, skip or disable a test, retry with a different approach than the plan's, widen the scope, or guess at what the developer meant.

A subagent can't ask the developer, so it asks you: it stops and returns the question, and you pass it on. Never answer for the developer. See 3.4.

## Keep the context small

An agent with a full context gets worse at everything: it forgets the rules, loses track of the plan and stops noticing its own mistakes. On a large codebase one ticket fills a context several times over, so this skill keeps the heavy work out of the main thread.

- **You hold the spec, the plan and the reports.** Reading through code and writing code is done by subagents, which start with a clean context and hand back a short report. `refine` reads the code this way, `strategic-design` maps the change and carries out the refactor this way, the build in phase 3 runs one subagent per feature step, and `deliver` checks the result in another. Open code yourself only to check a specific claim or to answer a specific question.
- **The files carry the state.** `spec.md` and `plan.md` hold everything the next phase needs, so nothing is lost when a session ends, and the context can be cleared between phases. "Clear the context" below says when to recommend that and what to tell the developer.
- **This costs more tokens in total**, since every subagent reads its part of the code from scratch. That is the price of a context that stays sharp to the end.

## Clear the context

Subagents keep the heavy work out of your context, and it still fills: with the questions and the answers, the reports, and everything you opened to check them. Only the developer can clear it. Your part is to say when, to make sure nothing is lost by it, and to hand over the line that picks the work up again. A developer who is only told "you may want to clear the context" has to work out what to type afterwards, and usually doesn't clear.

When to recommend it:

- **At the points where the files hold everything.** The spec is approved and `refine` has finished with the glossary and the ticket. The plan is approved, its decisions are recorded and the refactor is done. The build is verified (3.5). The pull request is open. Say it in a line or two when you report that point, then go on with the next phase unless the developer takes it. The next phase starts from the files either way.
- **When the context shows that it is full.** The host has compacted or summarized the conversation. Several feature steps, or more than one round of checks, have gone through this thread since it was last cleared. You had to open the spec or the plan again to recall what it says. The developer points out something you forgot, or a rule you stopped following. Then finish what is in flight, stop at the next safe point, and recommend it before starting anything new. Wait for the answer. An agent with a full context is the one that drops the rules, so carrying on is the developer's call and not yours.

A safe point is one where nothing lives only in the conversation: no subagent has a step half done, no question is waiting for an answer, no file is waiting for approval, and the worktree has no uncommitted changes. Never recommend a clear in the middle of one of those. Get the answer or finish the step first.

Before you recommend it, make the files carry what you know. The status lines are right, the finished steps are ticked off, the worktree paths, the scenarios that got their go-ahead and the notes from finished steps are in `plan.md`, and `findings.md` has every question and correction so far. If the next session needs something that has no place in those files, this is not a safe point yet.

What to tell the developer:

- That this is a good point to clear the context, or that it is needed, with the sign you saw.
- What is saved and where: the work's folder, and how far the work has come.
- How: `/clear` in Claude Code, or a new session. Either way from the same directory as now, the repo or the home repo, and not from the worktree.
- The prompt to paste afterwards, in a code block so it can be copied. It names the skill, the work's key or slug, the folder, and where to pick up:

  ```
  Continue PROJ-123 with the implement skill. The files are in .implement/PROJ-123/. The spec and the plan are approved, and feature steps 1 to 3 are ticked off. Pick up at feature step 4.
  ```

The prompt points at the files. It doesn't carry the state. If you are adding facts to it that the next session would need, write them to the files instead: the prompt is gone after the next clear, and the files are not.

Recommend a clear, not a summary of the conversation (`/compact` in Claude Code). A summary keeps a blurred copy of everything, including what no longer matters. The files are exact.

### Pick up from the files

A new context knows nothing about the work. The prompt says where to look, and that is all to take from it. Where the work stands is read from the files and the repo, because those are what was left behind on purpose, and a prompt can be out of date or mistyped.

1. **Read the work's folder.** `spec.md`, `plan.md` and `findings.md`, in full. Not the code: subagents read that.
2. **Check that the files and the repo agree.** The worktrees `plan.md` lists exist, are on the plan's branch and have no uncommitted changes. Every ticked step has its commits, and the branch has no commits past the last ticked step. If a worktree is gone and the branch is still there, add it again. Anything else that doesn't fit, or a prompt that says something the files don't, is something unexpected: say what you found and ask.
3. **Find the place.** Take the first row that fits:

   | The files say | Pick up at |
   |---|---|
   | No `spec.md`, or its status is draft | Phase 1. `refine` continues from the draft. |
   | The spec is approved. No `plan.md`, or its status is draft | Phase 2. `strategic-design` continues from the draft. |
   | The plan is approved. A decision has no ADR yet, or a refactor step is not ticked | Phase 2, at step 6 or 7 of `strategic-design`, with the first thing that is open. |
   | The refactor is done. `plan.md` has no Scenarios | Phase 3, from 3.1. |
   | The scenarios are there. A feature step is not ticked | 3.4, at the first step that is not ticked. |
   | Every step is ticked. `plan.md` lists no pull request | 3.5. Run the verification again, since a new context has not seen it pass. Then phase 4. |
   | `plan.md` lists a pull request | Not this skill. `revise` for review comments and failing checks, `retro` and `cleanup` once it is merged. |

4. **Say it, then go on.** Tell the developer in a few lines what the files say and where you pick up. Don't redo what is approved: an approved spec is not asked about again, an approved plan is not designed again, and the scenarios in `plan.md` have their go-ahead.

The other skills follow this rule when they run on their own, each with its own files and its own prompt.

## Where the documents live

The spec and the plan are files, so they survive a long session and can be picked up in a new one. They are in the work's folder: `work/<key-or-slug>/` in a home repo, otherwise `.implement/<key-or-slug>/` at the root of the repo being worked on. The `refine` skill owns the rule ("Where the documents live"): how the folder is named and kept out of git, and the status line each file starts with. Only the developer's explicit approval sets a file to approved, and any later change sets it back to draft until it is approved again.

Writing and updating these two files needs no permission. Don't commit them unless asked.

`plan.md` also records progress: `strategic-design` ticks off each refactor step when it is done, and the build does the same for each feature step once it is committed. That is not a change to the plan and leaves its status as it is. The same goes for the other things that are written there as the work goes on: the worktree paths ("Work in a worktree"), the scenarios the developer gave a go-ahead for (3.3), the notes finished steps leave for later ones (3.4), and the pull requests once `deliver` has opened them.

When starting, look for an existing folder for this work. If `spec.md` or `plan.md` is already approved, tell the developer what you found, including which steps are ticked off, and ask whether to resume from there or start over. If they came with the prompt from "Clear the context", they have answered that already. Either way, resuming is done the way "Pick up from the files" describes.

If the developer's answer to a question changes the spec or the plan, update the file and get it approved again before going on. A spec that changed may no longer match its ticket, so bring the ticket in line the way `refine` does in its step 7.

The folder also holds `findings.md`, the log of what went wrong along the way. Add an entry every time a question stops the work, with the answer it got, and every time the developer corrects something that was built or proposed. Write it when it happens; by the end of the work nobody remembers it. The `retro` skill owns the format ("The findings log") and turns the log into lessons once the work is merged. Appending to it needs no permission.

## Work in a worktree

All code for a piece of work is written in a git worktree made for it, never in the developer's checkout. The checkout stays as the developer left it: they can keep working there, switch branches or start a second piece of work while this one builds, and no agent touches their uncommitted changes.

There is one worktree per piece of work, for each repo it changes, and every step uses it. It is not one per subagent: the steps build on each other, so they all work on the same branch in the same place. If the agent tool can give a subagent a worktree of its own, don't use that.

- **Where.** `worktrees/<repo_name>/` inside the work's folder, next to `spec.md` and `plan.md`. Outside a home repo `.implement/` is already kept out of git. In a home repo, add `work/*/worktrees/` to the home repo's `.git/info/exclude`.
- **When.** Right before the first file is written on the branch: a glossary change or an ADR that lives in the repo, the refactor in `strategic-design`, or the build when there is none of those. Never before the plan is approved.
- **How.** Fetch, then `git worktree add` at that path with the branch name and the starting point from the plan's Git section. If the branch already exists, add the worktree for that branch instead of creating it. If the branch is checked out somewhere else, or the worktree can't be created, ask. If the work came over from `quick-fix`, its worktree is already there and `spec.md` names it: use it, and ask what to do with unfinished changes in it.
- **Set it up.** A new worktree holds the tracked files and nothing else: no installed dependencies, no build output, no local files that git ignores. Run the repo's install or build step. If the tests need an untracked local file from the checkout, such as an `.env`, copy it over and tell the developer which files you copied.
- **Check the starting point.** The spec and the plan were written from the developer's checkout, and the worktree is cut from the remote. Those can be different code. The spec names the commit it was read at: list the files the spec and the plan refer to that differ between that commit and the worktree (`git diff --name-only <that commit> HEAD -- <files>`). If any do, stop and ask, since the spec's Today and the plan's steps may no longer hold. Then run the plan's test commands once, before the first change. They must be green here. A green run in the checkout says nothing about this code. If they are red, stop and ask.
- **Write the glossary change.** If the spec's Language section has new or changed terms that go into the glossary, and the glossary is a tracked file in the repo, `refine` left the file alone so the checkout stays untouched. Write the entries in the worktree now, the way `refine` describes in its step 6, and commit them where the plan says.
- **Write it down.** Put each repo's worktree path in `plan.md` under a **Worktrees** heading. Like ticking off steps, this leaves the plan's status as it is.

From then on the worktree is the repo path for everything: it is what subagents are given, and where you run tests and check their reports. The checkout is only read.

When resuming, use the worktree `plan.md` lists. If it is gone but the branch is still there, add it again.

The worktree stays after the pull request is opened, since review comments get fixed there. Never remove it on your own. The `cleanup` skill removes it, with the developer's approval, once the work is merged or dropped.

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

For a bug, don't touch production code until a test reproduces it. If the `investigate` skill found the cause, its way to reproduce the bug is in `investigation.md` and in the spec's Today, and the test starts from it.

1. State the bug as: given X, expected Y, actual Z.
2. Write a test that asserts the expected behavior, in the layer closest to where the bug shows.
3. Run it. It must fail for the reason the bug describes. A compile error or a setup failure doesn't count.
4. If it passes, or you can't reproduce the bug, stop and ask. Report what you tried and the plausible explanations. Never ship a speculative fix. Finding an unknown cause is the job of the `investigate` skill.

That test is the first red of the loop in 3.4.

### 3.3 Choose the scenarios

Derive scenarios from the spec's acceptance criteria and the real edge cases on the code path: boundaries, empty or missing data, error responses, permissions, concurrency where it matters. Each rule in the spec's Language section that the work touches is a scenario too, unless a test already pins it. A rule nothing tests gets broken by the next change. So is each non-functional requirement a test can check: the input that must be refused, the user who isn't allowed, the dependency that answers with an error. For each, check:

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

Then write the list into `plan.md` under a **Scenarios** heading, grouped by feature step. Until it is there, the go-ahead exists only in the conversation, and the list is gone the first time the context is cleared. Like ticking off steps, this leaves the plan's status as it is. When resuming, the scenarios in `plan.md` already have their go-ahead, so don't choose them again. A change to the list later is asked about the same way and written there too.

To find the edge cases and what is already covered, use the code facts `refine` collected and the `file:line` references in the plan. If that isn't enough, send a read-only subagent to look, as `refine` does, instead of reading the code path yourself.

### 3.4 The loop

Build the feature steps from the plan in order, each one in a new subagent with a clean context. Never use a fork of this conversation, and never reuse the subagent that built an earlier step: the point is that each step starts without the history of the others. One at a time, never in parallel. The steps build on each other and share one branch and one worktree.

Give the subagent:

- The paths to `spec.md` and `plan.md`, and which feature step is its own. It reads the whole of both, and builds only its step.
- The scenarios for that step, as `plan.md` lists them under Scenarios, each with its layer.
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
- Follow the repo's coding standards and its `CLAUDE.md` or `AGENTS.md`. Read them before you write; in a home repo the home `CLAUDE.md` says where each repo's are. Where they say nothing, do it the way the code around you does, and look for an existing helper before you write a new one.
- Add no dependency the plan doesn't name. If the step seems to need one, stop and ask.
- Stay inside the spec and the plan. No speculative abstractions, no unrelated cleanup.
- Keep it simple. Write the most straightforward code that passes the test: no layer, option, generic type or pattern that the step doesn't need today. Code that is clever or built for a future nobody asked for costs every reader after you.
- Don't comment code that explains itself. Write a comment only for what the code can't say: why it is done this way, or a trap the next reader would walk into. A comment that repeats the code goes stale and gets in the way. If the repo's standards ask for more, such as doc comments on a public API, follow them.

Commit where the plan says to, on the branch, never on the default branch. Keep the message short and about why the change is made: a subject line, and a line or two under it only when the reason isn't plain from the subject. Leave out how; the diff shows that. Follow the repo's commit conventions if it has them.

If you hit anything the rules above say to ask about, stop there. Leave the working tree as it is, don't try a workaround, and report back with the question: what you found (with `file:line` or the actual output), the options, and what you recommend. You will get the answer and carry on from where you stopped.

When the step is done, run the test layers it touched and report:

- Each scenario, with the test's `file:line`, the failure it showed when red and the result when green.
- What changed, by file.
- The commits made.
- The test commands run and their results, with the output of any failure.
- Anything you couldn't run or verify, and anything you noticed that a later step or the developer should know.

When a subagent comes back:

- **With a question:** post it to the developer as it came, and wait. Don't answer it yourself, even when the answer looks obvious from the spec; if it were covered there, the subagent would not have had to ask. Then send the answer to the same subagent so it continues with what it already knows. If it can't be continued, start a new one with the step, the question, the answer and a note that the working tree holds unfinished work from the first attempt. Add the question and its answer to `findings.md`.
- **With a report:** check it before going on. The step's commits exist, the working tree is clean, and the tests it names pass when you run them. A report is a claim until then. If something doesn't hold, that is something unexpected: stop and ask. If the report says something a later step should know, write it in `plan.md` under a **Notes from the build** heading, as the report said it and with the step it came from. The next subagent reads the plan and not this conversation, and so does a new context. A note leaves the plan's status as it is. If it means a later step no longer holds as written, that is a change to the plan: ask.

If an answer changes the spec or the plan, update the file and get it approved again before the next step starts. If the answer is a decision that deserves an ADR, it goes under the plan's Decisions and is recorded the way `strategic-design` does it, once the plan is approved again.

Tick the step off in `plan.md`, tell the developer in a line or two what was built, and start the next one. The gap between two steps is a safe point: if the context shows that it is full, recommend clearing it before the next step starts ("Clear the context").

### 3.5 Verify

When every step is ticked off, run every affected test layer, the build, and the linter or type checker yourself, in the worktree. Show the output of any failure, and ask what to do about it. If something can't be run, say exactly what is unverified. Don't report success on anything you didn't run.

A verified build is one of the points in "Clear the context". Say so with the prompt, then go on to phase 4.

## Phase 4: Deliver

When the build is verified and committed, run the `deliver` skill without waiting to be asked. It has two subagents with a fresh context look at the diff, one that checks it against the spec and one that reviews the code for bugs and departures from the repo's standards. It reports their verdicts, describes the change so the developer can approve the code, and opens the pull request once they do.

Don't do those checks yourself and don't skip them because the tests are green. If a verdict leads to more work, do it under the rules of phase 3, in a new build subagent that gets the finding as its step, and let `deliver` check again.

The work is not over when the pull request is open. Review comments and failing checks go through the `revise` skill, which keeps the fixes under these same rules. Once the pull request is merged, the `retro` skill turns `findings.md` into lessons for the next piece of work, and the `cleanup` skill removes the worktrees and the branches the work left behind.

## Report

Keep it short:

- The pull request and the verdicts from `deliver`.
- For a bug: whether it reproduced, and the test that proves the fix.
- Scenarios covered, and in which layer.
- What was refactored first, and what was built, by file.
- Each question that came up along the way and the answer given.
- The ADRs written.
- Anything unverified or left open.
