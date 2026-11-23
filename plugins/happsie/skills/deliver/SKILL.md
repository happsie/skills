---
name: deliver
description: Close out finished work. Has two independent subagents with a fresh context look at the diff, one that checks it against the approved spec, criterion by criterion, and one that reviews the code for bugs and departures from the repo's coding standards. Then describes the change for the developer to approve the code from (how it changed, what happens when it is deployed, whether it can be reverted), opens the pull request with a description built from the spec and links it on the ticket. Use when the user says "deliver this", "ship it", "open the PR", "create a pull request", "wrap this up", "are we done", "check this against the spec", "did we build what we agreed", or when the build in the implement or quick-fix skill has finished. Works with any code host and tracker (GitHub, GitLab, Jira, Linear, ...). Not for work that is still being built, not for reviewing a pull request someone else opened, and not for review comments or failing checks on a pull request that is already open (revise).
---

# Deliver

Whoever built the change is the worst judge of whether it is done. They know what they meant to build, so they read the diff and see that. This skill has someone else look: two subagents that have never seen this conversation.

- **The spec check** gets the approved spec and the code, and checks that what was agreed is what got built.
- **The code review** reads the code the way a reviewer would. Code can meet every criterion and still be wrong: an error that is swallowed, a copy of a helper that already exists, a query inside a loop.

Then the developer gets a description of the change to approve the code from, and the pull request is opened and linked on the ticket.

## The ask rule

No assumptions. The verdicts go to the developer as they came back. What to do about a criterion that isn't met or a finding from the review is their decision, and nothing is pushed or posted before they approve it.

## 1. Find the contract and the change

- **The contract.** `spec.md` for this work, and `plan.md` if there is one. They live in `work/<key-or-slug>/` in a home repo, otherwise in `.implement/<key-or-slug>/` at the root of the repo. The spec must be approved. A spec that says `Kind: quick fix` comes from the `quick-fix` skill: it is short, there is no plan, and its Change section describes the approved change. If there is no spec but there is a ticket, its acceptance criteria are the contract; tell the developer that is what will be checked. If there is neither, ask what the work should be checked against. Don't write the criteria yourself from what was built.
- **The change.** The branch, the branch it will merge into, and every repo involved. If `plan.md` lists worktrees, or `spec.md` does for a quick fix, the work is there (`implement` and `quick-fix` build in them): read, run and push from the worktrees, not from the developer's checkout. Everything must be committed. If there are uncommitted changes, or the work sits on the default branch, stop and ask.
- **The standards.** Where the repo keeps its coding standards (`CONTRIBUTING.md`, `docs/coding-standards*`, `docs/conventions*`, `STYLEGUIDE*`), its `CLAUDE.md` or `AGENTS.md`, and its ADRs. In a home repo the home `CLAUDE.md` says where each repo's are. Note the paths and leave the reading to the code review. If the repo has none, the review compares the change with the code around it.

## 2. Check in two fresh subagents

Both checks are done by new subagents, never by you, and never by a fork of this conversation, since a fork inherits everything you know.

- Start each with a clean context. They are two subagents, not one with both jobs: an agent that is handed a checklist and a hunt does the checklist.
- Run them on the strongest model available. Set the model explicitly if the default for subagents is a smaller or faster one. This is the last check before other people spend time on the change; it is not the place to save tokens.
- They are read-only and change no file.
- Start them at the same time. The spec check runs the tests, the build and the linter. The code review doesn't, so two runs never collide in the same worktree.

Give each only what it needs to find things, and nothing about what you think of them:

- The path to `spec.md` and `plan.md`, or the ticket key and how to fetch it.
- The repo paths (the worktrees, when the work has them), the branch and the base branch.
- For the code review, the paths from "The standards" in step 1.
- Its instructions below.

Do not tell either of them what was built, how, which criteria you believe are met, what was hard, or what the tests showed. Do not paste your report or a summary of the work. An agent that is handed a conclusion tends to return it.

### The spec check

Instructions for the subagent, to pass on as they are:

> You are checking finished work against what was agreed. You have not seen how it was built, and that is the point. Trust only what you read and run yourself. Change no files.
>
> 1. Read the spec: goal, target behavior, acceptance criteria, non-functional requirements, out of scope, language, decisions. Read the plan if there is one; it describes an approved refactor and the build steps. A quick fix has no plan, and its spec has a Change section that describes the approved change instead.
> 2. Read the full diff between the base branch and the branch, and enough of the surrounding code to understand it. Follow each changed path from its entry point.
> 3. For each acceptance criterion, look for two things: the code that makes it true, and a test that would fail if it stopped being true. Read the test and judge whether it really checks the criterion, not just whether it exists or has a matching name.
> 4. If the spec has non-functional requirements, look for the code that meets each one that asks for something, and for a test where a test can check it. For each one marked "no change", check that the diff really changes nothing there.
> 5. Run the tests, the build and the linter or type checker. Report what you ran and the result. If something can't be run, say so.
> 6. Look for what the spec didn't ask for: changes that trace to no criterion and no step in the plan or the spec's Change section, anything listed as out of scope that was touched anyway, and existing tests whose expected results were changed, weakened, skipped or removed.
> 7. Look for what the spec implies but the diff misses: the cases named under target behavior and decisions, callers and consumers of what changed, data that predates the change.
> 8. If the plan has a Decisions section, check that each decision has its ADR, and that the diff does what the ADR says.
> 9. If the spec has a Language section, check the diff against it. Names the diff adds or changes (types, functions, fields, endpoints, tests, text a user reads) must use the agreed terms: not a word the spec says not to use, and not a new synonym. For each rule listed there that the change touches, look for the code that keeps it true and a test that would fail if it broke.
>
> Report:
> - One line per acceptance criterion: **met**, **not met** or **can't tell**, with `file:line` for the code and for the test, and one sentence of reasoning. "Met" needs both the code and a test that proves it. If you are unsure, it is "can't tell", with what would settle it.
> - One line per non-functional requirement, in the same way. One that no test can check is "met" on the code alone; say that it is.
> - Language: every name that departs from the agreed terms, with `file:line`, and every rule that is broken or that no test pins.
> - Decisions: every one in the plan with no ADR, and every place the diff goes against an ADR, with `file:line`.
> - Changes outside the spec and the plan.
> - Test, build and lint results, with the output of any failure.
> - Anything else that would make you hesitate to merge this.
>
> Don't soften the verdict and don't suggest fixes. Say what you found.

### The code review

Instructions for the subagent, to pass on as they are:

> You are reviewing a finished change before it becomes a pull request. You have not seen how it was built, and that is the point. Trust only what you read yourself. Change no files, and don't run the test suites, the build or the linter: another check is running them in the same place right now.
>
> That other check covers whether the acceptance criteria are met, so don't repeat it. Read the spec to know what the change is for. Your question is a different one: is this good code, and does it do what it means to do in every case, not only the ones someone wrote down?
>
> 1. Read the spec. Read the repo's coding standards, its `CLAUDE.md` or `AGENTS.md`, and the ADRs for the area, at the paths you were given.
> 2. Read the full diff between the base branch and the branch. For every function the diff touches, read the whole function, what calls it and what it calls. A diff read without the code around it hides most bugs.
> 3. Hunt for bugs. For each changed path, ask what happens with: empty, missing or malformed input; an error from something it calls (is it handled, passed on or swallowed); two requests at the same time; a retry or a second run; far more data than the tests use; a user who isn't allowed; data written before this change. Look for input that is trusted without a check, secrets or personal data that reach a log or a response, queries or calls inside a loop, resources that are never released, and a fallback or default that hides a failure instead of reporting it.
> 4. Look for departures from the standards, the ADRs and the way the code around the change does things. A new helper where one already exists: search before you accept anything new. Another way of handling errors, logging, configuration, naming or test setup than the repo's. A new dependency: check that the plan names it, that a package with exactly that name exists and is the one meant, and that nothing the repo already uses does the job. Code nothing calls, leftover debug output, commented-out code, a TODO. An abstraction, option or parameter that nothing in the spec needs.
> 5. Read the tests the diff adds as code too. Report a test that can't fail, one that asserts on a mock instead of on behavior, and one whose expected value repeats the implementation.
> 6. Work out what happens when this is deployed, and what happens if it is reverted after that. What has to be in place besides the new code: a migration, configuration, a secret, a flag and its default, a job, a deploy order between repos or services. What a revert would not undo: data migrated or written in a new shape, messages already sent, a contract another system has started to use, a cache. Say what the repo shows and what it doesn't; don't guess how it is deployed.
>
> Report:
> - **Findings**, the most serious first. Each one has `file:line`, what is wrong, and the input or situation that shows it. Mark each as a **bug** (behavior that is wrong, which you can describe concretely), a **departure** (name the standard, the ADR or the existing code it departs from, with `file:line`), or a **doubt** (it may be wrong and you can't settle it by reading; say what would settle it). Leave out taste: an opinion that no standard and no surrounding code backs is not a finding.
> - **How the code changed:** each part of the change in a line or two with `file:line`, in the order someone should read it.
> - **Where to look:** the few places that deserve a person's own eyes, the riskiest first, and why. The hardest logic, a choice the code makes that neither the spec nor the plan covers, anything that touches permissions, stored data or what other systems consume.
> - **Deploy:** what happens when this is deployed beyond new code running, with `file:line`. "Nothing beyond the code" is a valid answer.
> - **Revert:** whether reverting the change and deploying again brings the old behavior back, what it leaves behind, and what you couldn't tell from the repo.
>
> Don't soften a finding, and don't invent one to have something to report. If you found nothing, say so. Don't suggest fixes.

## 3. Report the verdicts

Post both verdicts to the developer as they came back: every criterion and requirement with its status and evidence, the language and decision findings, every finding from the code review with its mark, and everything else. Don't summarize away a finding, reword it into something milder, or drop one because you know the explanation. If you disagree with a finding, show it anyway and say why you disagree; the developer decides.

Add every finding to `findings.md` in the work's folder, and the developer's decision on it once they have made it. Do this for each round, also for findings that get fixed before the pull request: those are the ones nobody remembers afterwards. The `retro` skill owns the format ("The findings log") and turns the log into lessons later. Appending to it needs no permission.

If everything is met and the review found nothing, go on to step 4.

Otherwise stop and ask what to do with each open point: fix it, accept it as is, or change the spec. Fixes follow the rules of the skill that built the work, `implement` or `quick-fix`, and a changed spec needs approval again. After any change to the code, run step 2 again with **new** subagents, both of them. Don't send the old ones back to re-check; they now have a history with this change.

## 4. Describe the change

This is what the developer approves the code from. Until now they have approved a spec and a plan, which say what was meant. This says what was done, and what it will do once it is out.

Write it from the code review's report in the last round. A report is a claim: open the lines each statement points to before you repeat it. Keep it to a page. It is a guide to the diff, not a copy of it.

- **How the code changed.** In the order to read it, not file by file: what was refactored first, then each part of the feature, a line or two each with `file:line`.
- **Where to look.** The places that deserve the developer's own eyes, the riskiest first, and why each one is there.
- **When it is deployed.** What happens beyond new code running: migrations, new configuration or secrets, flags and their defaults, jobs, an order between repos or services, steps someone does by hand. If it is nothing, say "nothing beyond the code".
- **Can it be reverted.** Whether reverting the change and deploying again brings the old behavior back, and what a revert does not undo. If a plain revert is not enough, the way back.
- **Not verified.** What nobody ran or could tell, from both checks.

If the spec's non-functional requirements say how the change is rolled out and rolled back, say whether the code matches. If the repo doesn't show how it is deployed and the answer depends on it, ask. Don't fill in what a typical setup would do.

## 5. Open the pull request

Write the description from the spec, not from the commit log:

- What changes and why, in a few sentences.
- The acceptance criteria, each with the verdict it got.
- What happens when it is deployed and whether it can be reverted, from step 4.
- The ADRs this work added or superseded, if any.
- How it was verified: what was run, and anything that couldn't be.
- Anything the developer accepted as is in step 3, stated plainly.
- A reference to the ticket.

Follow the repo's pull request template and title conventions if it has them. Leave file-by-file walkthroughs out; the diff shows that.

Post the description of the change from step 4 in the chat, then the pull request's title and description, with the branch and the target it will merge into. If the work has a ticket, say also how the pull request will be linked on it in step 6: through a link field, or with a comment, and then show the comment's text. Wait for an explicit approval. It covers the code as step 4 describes it, the push, the pull request and that one link on the ticket. Then push the branch and open the pull request with whatever is available: `gh`, `glab`, a code host MCP server.

If the pull request is already open, the `revise` skill has sent the work back here after review. Show the commits to be pushed and what changes in the description instead, and after the approval push and update the pull request. Don't open a second one. The ticket already has its link, so step 6 is done.

## 6. Tell the ticket

If the work has a ticket, link the pull request on it the way step 5 showed: with a link field if the tracker has one, otherwise the short comment the developer approved. Write nothing else on the ticket. Don't move the ticket to another status, reassign it or tick off its criteria unless the developer asks.

## Report

The pull request URL, the verdicts in one line (for example "5 of 5 criteria met, review clean, lint clean"), and anything accepted as is or left unverified.

Say what comes after: review comments and failing checks on the pull request are handled with the `revise` skill, and once it is merged the `retro` skill turns `findings.md` into lessons.

If the work has worktrees, list them and say that `git worktree remove <path>` removes each one once the pull request is merged. Don't remove them yourself: review comments get fixed there.
