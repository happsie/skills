---
name: deliver
description: Close out finished work. Has an independent subagent with a fresh context check the diff against the approved spec, one acceptance criterion at a time, then opens the pull request with a description built from the spec and links it on the ticket. Use when the user says "deliver this", "ship it", "open the PR", "create a pull request", "wrap this up", "are we done", "check this against the spec", "did we build what we agreed", or when the build phase of the implement skill has finished. Works with any code host and tracker (GitHub, GitLab, Jira, Linear, ...).
---

# Deliver

Whoever built the change is the worst judge of whether it is done. They know what they meant to build, so they read the diff and see that. This skill has someone else check it: a subagent that has never seen this conversation and gets only the approved spec and the code. Then it opens the pull request and tells the ticket.

## The ask rule

No assumptions. The verdict goes to the developer as it came back. What to do about a criterion that isn't met is their decision, and nothing is pushed or posted before they approve it.

## 1. Find the contract and the change

- **The contract.** `spec.md` for this work, and `plan.md` if there is one. They live in `work/<key-or-slug>/` in a home repo, otherwise in `.implement/<key-or-slug>/` at the root of the repo. The spec must be approved. If there is no spec but there is a ticket, its acceptance criteria are the contract; tell the developer that is what will be checked. If there is neither, ask what the work should be checked against. Don't write the criteria yourself from what was built.
- **The change.** The branch, the branch it will merge into, and every repo involved. If `plan.md` lists worktrees (the `implement` skill builds in them), the work is there: read, run and push from the worktrees, not from the developer's checkout. Everything must be committed. If there are uncommitted changes, or the work sits on the default branch, stop and ask.

## 2. Verify in a fresh subagent

The check is done by a new subagent, never by you, and never by a fork of this conversation, since a fork inherits everything you know.

- Start it with a clean context.
- Run it on the strongest model available. Set the model explicitly if the default for subagents is a smaller or faster one. This is the last check before other people spend time on the change; it is not the place to save tokens.
- It is read-only: it may run tests and builds, but changes no file.

Give it only what it needs to find things, and nothing about what you think of them:

- The path to `spec.md` and `plan.md`, or the ticket key and how to fetch it.
- The repo paths (the worktrees, when the work has them), the branch and the base branch.
- The instructions below.

Do not tell it what was built, how, which criteria you believe are met, what was hard, or what the tests showed. Do not paste your report or a summary of the work. An agent that is handed a conclusion tends to return it.

Instructions for the subagent, to pass on as they are:

> You are checking finished work against what was agreed. You have not seen how it was built, and that is the point. Trust only what you read and run yourself. Change no files.
>
> 1. Read the spec: goal, target behavior, acceptance criteria, out of scope, language, decisions. Read the plan if there is one; it describes an approved refactor and the build steps.
> 2. Read the full diff between the base branch and the branch, and enough of the surrounding code to understand it. Follow each changed path from its entry point.
> 3. For each acceptance criterion, look for two things: the code that makes it true, and a test that would fail if it stopped being true. Read the test and judge whether it really checks the criterion, not just whether it exists or has a matching name.
> 4. Run the tests, the build and the linter or type checker. Report what you ran and the result. If something can't be run, say so.
> 5. Look for what the spec didn't ask for: changes that trace to no criterion and no step in the plan, anything listed as out of scope that was touched anyway, and existing tests whose expected results were changed, weakened, skipped or removed.
> 6. Look for what the spec implies but the diff misses: the cases named under target behavior and decisions, callers and consumers of what changed, data that predates the change.
> 7. If the plan has a Decisions section, check that each decision has its ADR, and that the diff does what the ADR says.
> 8. If the spec has a Language section, check the diff against it. Names the diff adds or changes (types, functions, fields, endpoints, tests, text a user reads) must use the agreed terms: not a word the spec says not to use, and not a new synonym. For each rule listed there that the change touches, look for the code that keeps it true and a test that would fail if it broke.
>
> Report:
> - One line per acceptance criterion: **met**, **not met** or **can't tell**, with `file:line` for the code and for the test, and one sentence of reasoning. "Met" needs both the code and a test that proves it. If you are unsure, it is "can't tell", with what would settle it.
> - Language: every name that departs from the agreed terms, with `file:line`, and every rule that is broken or that no test pins.
> - Decisions: every one in the plan with no ADR, and every place the diff goes against an ADR, with `file:line`.
> - Changes outside the spec and the plan.
> - Test, build and lint results, with the output of any failure.
> - Anything else that would make you hesitate to merge this.
>
> Don't soften the verdict and don't suggest fixes. Say what you found.

## 3. Report the verdict

Post the subagent's verdict to the developer as it came back: every criterion with its status and evidence, the language and decision findings, and every other finding. Don't summarize away a finding, reword it into something milder, or drop one because you know the explanation. If you disagree with a finding, show it anyway and say why you disagree; the developer decides.

If everything is met and nothing else was found, go on to step 4.

Otherwise stop and ask what to do with each open point: fix it, accept it as is, or change the spec. Fixes follow the `implement` skill's rules, and a changed spec needs approval again. After any change to the code, run step 2 again with a **new** subagent. Don't send the old one back to re-check; it now has a history with this change.

## 4. Open the pull request

Write the description from the spec, not from the commit log:

- What changes and why, in a few sentences.
- The acceptance criteria, each with the verdict it got.
- The ADRs this work added or superseded, if any.
- How it was verified: what was run, and anything that couldn't be.
- Anything the developer accepted as is in step 3, stated plainly.
- A reference to the ticket.

Follow the repo's pull request template and title conventions if it has them. Leave file-by-file walkthroughs out; the diff shows that.

Post the title and description in the chat, with the branch and the target it will merge into. Wait for an explicit approval. Then push the branch and open the pull request with whatever is available: `gh`, `glab`, a code host MCP server.

## 5. Tell the ticket

If the work has a ticket, link the pull request on it, with a link field if the tracker has one, otherwise a short comment. Don't move the ticket to another status, reassign it or tick off its criteria unless the developer asks.

## Report

The pull request URL, the verdict in one line (for example "5 of 5 criteria met, lint clean"), and anything accepted as is or left unverified.

If the work has worktrees, list them and say that `git worktree remove <path>` removes each one once the pull request is merged. Don't remove them yourself: review comments get fixed there.
