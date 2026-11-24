---
name: strategic-design
description: Strategic programming step between agreed requirements and writing the feature. Takes an approved spec, maps the code changes the feature needs, and asks whether the code would be healthier if it were refactored first so the feature becomes a small, obvious change. Proposes a preparatory refactor (or says none is needed), gets it approved, and carries it out without changing behavior or the expected results of existing tests. Decisions the plan makes that deserve an ADR are recorded once the plan is approved. Use when the user asks "should we refactor first", "do a strategic analysis", "design this before we build it", "prep refactor for this feature", "make the change easy first", or as the second phase of the implement skill. Not for agreeing on what to build (refine), and not for cleanup that no feature needs.
---

# Strategic design

Tactical programming gets the feature working in the code as it stands and leaves the design a little worse each time. Strategic programming asks first what shape the code should have for this feature to fit well, and gets it into that shape before building. Make the change easy, then make the easy change.

This skill answers one question: **with this feature in it, would the code be healthier if we refactored first?** It then produces a plan the developer approves, and carries out the refactor part of it.

It needs an approved spec (goal, target behavior, acceptance criteria). Read it from `spec.md`. If there isn't one, or its status is still draft, run the `refine` skill first.

## The ask rule

No assumptions. Stop and ask the developer when:

- A decision isn't covered by the spec or the approved plan.
- Something unexpected happens: a test fails, the code behaves differently than the plan says, a step doesn't work.
- You want to do something the plan doesn't describe, however small.

Reading code, running tests and carrying out steps the approved plan already describes need no permission. When you ask, say what you found, the options, and what you recommend.

A subagent can't ask the developer, so it asks you: it stops and returns the question, and you pass it on. Never answer for the developer.

## Where the documents live

The spec and the plan are files, so they survive a long session and can be picked up in a new one. They are in the work's folder: `work/<key-or-slug>/` in a home repo, otherwise `.implement/<key-or-slug>/` at the root of the repo being worked on. The `refine` skill owns the rule ("Where the documents live"): how the folder is named and kept out of git, and the status line each file starts with. Only the developer's explicit approval sets a file to approved, and any later change sets it back to draft until it is approved again.

Writing and updating these two files needs no permission. Don't commit them unless asked.

During the refactor, `plan.md` also records progress: tick off each refactor step when it is done. That is not a change to the plan and leaves its status as it is.

If a `plan.md` already exists for this work, read it and continue from there instead of starting over. An approved plan is not written again, and a ticked step is done.

## 1. Map the tactical change

Work out what the feature would look like if it were built straight into the code as it is today. List every place that would change, with `file:line`, and what would change there. This is the baseline the refactor is judged against. Don't write any of it.

Have read-only subagents trace the code and return the places with `file:line`, the way `refine` reads code in its step 2, so your context is kept for the judgment in steps 2 and 3. Give them the spec and the area to cover, not your idea of the design. Then open the places they point to yourself. Whether code is the wrong shape is judged by reading it, not from a report about it.

## 2. Judge the health of that change

Look at the tactical version and at the code around it. Signs that the code is the wrong shape for this feature:

- The same edit is needed in several places.
- It adds another branch to a conditional or type switch that already has several.
- A function or class picks up one more responsibility, or one more parameter or flag that only some callers use.
- The new behavior can't be tested without heavy setup or mocking.
- New code has to reach through layers, or copy knowledge that lives somewhere else.
- A name or abstraction stops being true once the feature exists.
- The code names a thing differently than the spec's Language section does: `customer` in the code where the agreed term is "account holder". Every such name is a place where the next reader has to translate.
- This is the second or third variant of something handled ad hoc each time.
- The code to change is hard enough to follow that the change itself is risky.

If you don't understand why the code is built the way it is, ask before judging it. Check ADRs and `git log` first.

## 3. Decide: refactor first, or not

For each problem found in step 2, ask what shape of code would make the feature a small, local change. Typical moves: extract a function or class, split a responsibility, move logic to the data it uses, introduce an interface so variants plug in, replace a conditional with polymorphism, add a seam that makes the code testable.

Rules for the proposal:

- **A pattern must earn its place.** Name a design pattern only when it removes a concrete problem from step 2. Never introduce one for its own sake or for features that might come later.
- **"No refactor needed" is a valid answer**, and often the right one. If the tactical change is already small and clean, say so and move on.
- **Stay inside the feature's path.** Refactor only code the feature touches. Report other debt you notice as a note; don't act on it.
- **Use the agreed language.** Every class, function, field, endpoint, table and message the plan adds or renames is named with the terms in the spec's Language section, never with a word the spec says not to use. Renaming existing code to the agreed term is a refactor step like any other, inside the feature's path only. If the design needs a domain concept that has no agreed term, stop and ask. The answer goes into the spec, which then needs approval again.
- **Match the codebase.** Use the patterns and conventions the project already uses before bringing in new ones.
- **Follow the recorded decisions.** An accepted ADR for the area holds. If the design you want goes against one, stop and ask. Either the design changes or the ADR is superseded, and the developer says which. An ADR with status `Inferred` was read out of the code and binds nothing yet. If the design relies on one or goes against one, ask whether it holds; the `adr` skill records the answer ("Confirming an inferred ADR").
- **A new dependency is a decision.** Use what the repo already has first. If the design needs a package, a service or a tool the repo doesn't use yet, or a new major version of one, it goes under Decisions with what it is for and why nothing already in the repo does the job. Check that a package with exactly that name exists in the registry and is the one you mean; a name that only sounds right is how the wrong package gets installed. The build adds no dependency the plan doesn't name.
- **Weigh the cost.** A refactor that is larger or riskier than the feature needs a strong reason.

## 4. Check the safety net

Map the test layers first, whether or not there is a refactor. Find which layers the repo has: unit, integration, BDD (`.feature` files and their step definitions), end to end. Note the exact command that runs each, and what it needs: Docker, a database, a local environment. The refactor, the build and the final check all run from this list, and so does a session that resumes later. If a layer this work needs can't run locally, ask.

A refactor is only safe if tests pin the current behavior.

- Find the tests that cover the code to be refactored and run them. They must be green before anything changes. If any are red, stop and ask.
- Where coverage is missing or thin, plan characterization tests: tests that pin what the code does today, written and green before the refactor starts. They record current behavior, including behavior that looks wrong. Report anything that looks wrong; don't fix it.

These runs are in the developer's checkout, since the worktree doesn't exist before the plan is approved. They show whether there is a safety net. The baseline that counts is run again in the worktree before the first change (`implement`, "Work in a worktree").

## 5. Present the plan and get it approved

Write `plan.md` next to the spec with the sections below, and post it in the chat as well:

- **Tactical version:** the changes from step 1, and what they cost the design.
- **Recommendation:** refactor first, or no refactor, with the reason in a sentence or two.
- **Refactor steps:** ordered, small, each one leaving the tests green. Empty if none.
- **Characterization tests:** which ones to add first, and what they pin.
- **Test commands:** the test layers from step 4, each with the exact command that runs it and what it needs.
- **Names:** the domain names the plan adds or renames, each with the term from the spec it stands for. Existing names on the feature's path that keep a word the spec says not to use are listed too, with the reason they stay.
- **Feature steps:** how the feature gets built once the code has its new shape. Ordered, each one tied to acceptance criteria from the spec. Every non-functional requirement in the spec that asks for something belongs to a step too, including the ones no test can check, such as a log line or the way back after a deploy. In `implement`, each step is built by a subagent that starts with nothing but the spec, the plan and that step, so write every step for a reader who hasn't seen this conversation: the files and symbols it touches with `file:line`, what exists when it starts, what must be true when it is done, and what it leaves for later steps. Make each step small enough to build and test in one sitting, and leave the tests green at the end of it.
- **Decisions:** the decisions in this plan that deserve an ADR, judged by the `adr` skill's "What gets an ADR", including any from the spec's Decisions section. Each one states the context, the decision, the alternatives that lost and why, the consequences, and the ADR it supersedes if there is one. Most plans have none; say so instead of inventing one. If you don't know why an alternative lost, that is a question for the developer, not something to fill in.
- **Risks and open questions.**
- **Git:** branch name, the branch it starts from (the default branch unless the spec or the developer says otherwise), and where the commits fall. Refactor commits and feature commits are always separate. If the spec has new or changed terms that go into the glossary, and the glossary is a tracked file in the repo, writing them gets its own commit on the branch. So do ADRs written to a tracked folder in the repo.

Wait for an explicit approval. The developer may take the refactor, reject it, or cut it down. Update the file and confirm again after any change, then set its status line once approved. If they reject the refactor, the feature steps follow the tactical version.

## 6. Record the decisions

Only after approval, and only if the plan has entries under Decisions. A decision that is written down only in `plan.md` is gone when the work is done, and the plan is not kept in git.

Write each one as an ADR with the `adr` skill. It says where ADRs live and what the file looks like. The plan's approval covers the text, so don't ask again unless the ADR would say something the plan doesn't.

If the ADR folder is a tracked part of a repo this work changes, the ADRs belong on the work's branch: create the worktree first ("Work in a worktree" in `implement`), write them there and commit them where the plan says. Otherwise write them where they live and don't commit.

A decision that comes up later, during the refactor or the build, goes the same way: into the plan's Decisions section, approved with the plan, then recorded.

## 7. Carry out the refactor

Only after approval, and only if the plan has refactor steps. Work on the plan's branch in a git worktree made for this work, never in the developer's checkout and never on the default branch. The `implement` skill says where the worktree goes and how it is set up ("Work in a worktree"). Follow it here too, also when this skill runs on its own.

Subagents with a clean context do the work, and you keep the plan and their reports. A refactor reads and rewrites a lot of code, and doing it yourself fills your context before the feature is even started. One subagent adds the characterization tests. Then the refactor steps go out in order, one subagent at a time, never in parallel. Steps that reshape the same code can go to one subagent; start a new one when the work moves to another part of the code. Never use a fork of this conversation.

Give the subagent:

- The paths to `spec.md` and `plan.md`, and which steps are its own. It reads the whole of both, and does only its steps.
- The worktree paths and the branch. They work only in the worktree. The commands that run the tests are in the plan under Test commands.
- The rest of this section, from the numbered steps to the end of the report list, passed on as it is.

The work:

1. Add the characterization tests. Run them. They must pass against the unchanged code.
2. Take one refactor step. Run the tests. Green means go on to the next step.
3. Commit where the plan says to.

Hard rules:

- **No behavior change.** A refactor changes structure only. No feature code in this phase.
- **Never change what an existing test expects.** Assertions, expected values and test data stay exactly as they are. That includes the characterization tests once they are written.
- **Mechanical test edits are allowed**, and only these: imports, renamed or moved symbols, and setup or wiring that moved code makes necessary. List every such edit in the report.
- **Never delete, skip or disable a test.**
- **A red test stops the work.** If a test can't stay green without changing what it asserts, either the refactor changed behavior or the test is tied to the old structure. Don't decide which. Stop and ask.
- **So does a build that breaks, and a tool or an environment that doesn't work.** Don't work around it.
- **Don't go past the plan.** If the refactor turns out to need more than was approved, stop and ask.

If you hit anything these rules say to stop or ask about, stop there. Leave the working tree as it is, don't try a workaround, and report back with the question: what you found (with `file:line` or the actual output), the options, and what you recommend. You will get the answer and carry on from where you stopped.

When your steps are done, report:

- What changed for each step, by file.
- Test results before and after, with the commands run and the output of any failure.
- Every mechanical test edit, with `file:line`.
- The commits made.
- Anything about the feature steps that no longer holds now that the code has its new shape, and debt noticed outside the feature's path.

When a subagent comes back:

- **With a question:** post it to the developer as it came, and wait. Don't answer it yourself. Then send the answer to the same subagent so it continues with what it already knows. If it can't be continued, start a new one with the steps, the question, the answer and a note that the working tree holds unfinished work from the first attempt.
- **With a report:** check it before going on. The commits exist, the working tree is clean, the tests pass when you run them, and the diff changes no assertion, expected value or test data in an existing test. A report is a claim until then. If something doesn't hold, stop and ask.

Tick the steps off in `plan.md` and send out the next ones.

## 8. Hand off

Report:

- The ADRs written, with their paths.
- What was refactored, and where.
- Test results before and after.
- Every mechanical test edit made.
- The feature steps, updated in `plan.md` if the refactor changed anything about them. A changed plan needs approval again.
- Debt noticed outside the feature's path.

An approved plan with its refactor done is a point where the files hold everything. When this skill runs on its own, say that this is a good time to clear the context, and give the prompt that continues the work with `implement`. That skill owns the rule ("Clear the context"), and says it itself when this skill runs as its second phase.
