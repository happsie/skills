---
name: refine
description: Refine a feature request, task or ticket into a spec the developer has approved, before any code is written. Reads the ticket and the code it touches, cross-checks them, and asks the developer about everything it would otherwise decide itself, even when the answer looks obvious or the request looks well defined. Also agrees on the domain terms and rules the work depends on and records them in the project's glossary. Use when the user asks to "refine this", "refine PROJ-123", "let's align on this ticket", "what's unclear about this feature", "grill me on this", or as the first phase of the implement skill. Input is free text or a ticket key from any tracker (Jira, GitHub, Linear, ...). Writes the spec to a file and updates the glossary; it never changes code. Not for finding the cause of a problem (investigate), and not for writing the ticket itself (ticket-creator).
---

# Refine

Building the wrong thing is the most expensive mistake. This skill pins down what to build and ends with a spec the developer has explicitly approved. That spec is the contract every later step works from.

This skill never edits code, creates branches or writes to the tracker. The only files it writes are the spec and, once the spec is approved, the glossary.

## The ask rule

No assumptions. If something is unclear, contradictory or missing, ask the developer. Never pick an interpretation yourself, and never fill a gap with what seems likely. Reading code, reading the ticket, fetching from the remote and running read-only commands need no permission. Deciding what the feature should do always does.

## Where the documents live

The spec and the plan are files, so they survive a long session and can be picked up in a new one. Each piece of work gets a folder named after the ticket key, or a short slug for free text:

- **In a home repo** (the current directory's `CLAUDE.md` says it is a home repo, as set up by the `home-repo` skill): `work/<key-or-slug>/` in the home repo. This holds even when the code changes land in other repos.
- **Anywhere else:** `.implement/<key-or-slug>/` at the root of the repo being worked on. Keep it out of git by adding `.implement/` to `.git/info/exclude`. Don't edit the repo's `.gitignore` for this.

The folder holds `spec.md` (written by `refine`, or in a short form by `quick-fix`) and `plan.md` (written by `strategic-design`). Each starts with a status line: `Status: draft`, or `Status: approved <YYYY-MM-DD>` once the developer has approved it. Only the developer's explicit approval sets it to approved. Any later change sets it back to draft until approved again.

Writing and updating these two files needs no permission. Don't commit them unless asked.

The same folder holds `investigation.md` when `investigate` has run, and `findings.md`, the log of what the checks, the build and the reviewers found along the way. The `retro` skill owns that log ("The findings log").

Work that started as free text can get a ticket later: `investigate` ends by drafting one, and `ticket-creator` can turn a spec into one. The folder then takes the ticket key as its name. Otherwise the skill that picks the ticket up starts an empty folder beside the one that holds what is already known. `ticket-creator` renames it when it creates a ticket from a `spec.md` or an `investigation.md`. Git records where each worktree is, so if the folder holds worktrees, run `git worktree repair <new path>` in the repo for each one after the rename, and correct the paths written in `plan.md` or `spec.md`.

A ticket can also be created by hand. So before starting a new folder for a ticket key, look at the folders named with a slug. If one of them looks like the same work, ask whether it is, instead of starting a second folder.

## The shared language

The request, the spec, the tickets and the code should use the same word for the same thing. When they don't, people agree on a sentence and mean different things by it, and the code ends up with three names for one concept. So the project's glossary is treated the way domain-driven design treats its ubiquitous language: terms and the rules about them are proposed, agreed with the developer, written down, and from then on followed by every later step.

A glossary entry holds a term and the agreements about it:

```markdown
## <Term>

<What it means, in one or two sentences.>

- **Also called:** <other words for it in code, tickets or speech>
- **Rules:** <what always holds for it, one per line: "A published recipe has at least one ingredient.">
- **Context:** <the repo, module or team where it means this. Leave out if it means this everywhere.>
- **Status:** agreed <YYYY-MM-DD> | inferred
```

- **Also called** lists the words to stop using. New specs, tickets, code and tests use the term itself.
- **Rules** are the agreements: statements about the term that hold no matter which feature is being built. A rule is not an acceptance criterion. A criterion is done when the work is done; a rule keeps holding afterwards.
- **Status** says how far to trust the entry. `agreed` means a person approved it. `inferred` means it was read out of code or tickets and nobody has confirmed it. Follow agreed entries. Treat inferred ones as a good guess, and get the ones this work relies on confirmed.

Nothing goes into the glossary as `agreed` until the developer has said yes to two things about it: that the term should be in the glossary, and that the definition is correct. They are two questions, because the answers differ. A developer can agree that a word is needed and mean something else by it, and a definition can be right for a word that only matters in this one piece of work and has no place in a shared glossary. Ask both for every new term, with the entry written out as it would read, and take each term on its own. An approval of a spec or a ticket that happens to contain the entry answers neither question. A change to an existing entry is asked about the same way, with the old wording next to the new.

One term has one meaning within a context. If two repos or modules use the same word for different things, that is two entries, each with its context. Don't bend them into one definition. Write down both, and how one translates into the other where they meet.

Where the glossary is:

- **In a home repo:** the home `CLAUDE.md` says where each repo's glossary is and where terms shared between repos go. Follow it.
- **Anywhere else:** the repo's own glossary (`GLOSSARY.md`, `docs/glossary*`, or a glossary section in the README or docs). If it uses another format, keep that format and fit the same information into it.
- **If there is none:** ask in step 4 whether to create `docs/glossary.md`. If the developer says no, the agreed language lives only in the spec.

## 1. Gather the request

If a `spec.md` already exists for this work, read it and continue from there instead of starting over. A spec that says `Kind: quick fix` was handed over by the `quick-fix` skill and says why the work was not a quick fix. Treat it as the request plus what is known so far. It has not been through steps 2 to 4, so run them.

If the folder has an `investigation.md`, read it. The `investigate` skill wrote it, and it is where a fix starts: the symptom, the cause, how to reproduce it, what was ruled out and the commit all of that was found at. What it proved is known and is not asked about again. Carry the cause and the reproduction into the spec's Today, since the build reads the spec and not the investigation. What it calls a hypothesis is not known. If its cause is **Not found**, there is no fix to specify yet: say so and ask.

- **Free text.** Take it as given. If it points at a ticket, document or conversation you can reach, read that too.
- **Ticket key or URL.** Fetch it with whatever is available: a tracker MCP server, a CLI such as `gh issue view`, or another skill built for that tracker. Read the description, acceptance criteria and comments, then the parent or epic, sibling tickets, linked issues and any existing branches or PRs. Comments often overrule the description, so read them all.

If the ticket can't be fetched, say so and ask for the text. Don't work from a title alone.

## 2. Read the code the change touches

Have subagents do this reading, and keep your own context for the request, the questions and the spec. Following a code path through a large codebase fills the context long before the first question is asked, and an agent with a full context reasons worse about everything after it.

- Give each subagent one area to cover: an entry point and the path below it, the callers and consumers, or the glossary and project docs. Run them in parallel when there are several.
- Give it the request as it was written and the list below. Don't give it your reading of the request or what you expect it to find. An agent that is handed a conclusion tends to return it.
- Ask for facts, each with a `file:line` reference: what the code does today, what calls it, which tests cover it, which names it uses. No summaries without references, and no opinions on what to build.
- They are read-only.

A report is a map, not the evidence. Before you put a finding in a question or in the spec, open the lines it points to and check that they say what the report says. Read only those lines.

What to find: the entry points (endpoint, consumer, job, UI, CLI) and the path down to persistence, and the existing tests for that path. Look for:

- A similar feature that already exists, and how it was built.
- Everything that calls or consumes what will change: other modules, other services, the frontend, reports, exports.
- Recent `git log` on those files, for context or half-finished attempts.
- The glossary entries for the area, and the names the code uses for the same things.
- Other project docs that define rules: ADRs, coding standards, `CLAUDE.md`, `AGENTS.md`.

Then check that the code that was read is the code the work will start from. The work is not built in this checkout. It is built in a worktree cut from the branch the work starts from, normally the default branch as it is on the remote (`implement`, "Work in a worktree"). A checkout that is behind, on another branch or holds uncommitted changes shows other code, and a spec written against it is wrong from the first line. For each repo:

- Fetch, and note the commit the checkout is at and its branch.
- Compare the files your findings point to with the remote's default branch (`git diff --name-only <checkout commit> <remote default branch> -- <files>`), and check them for uncommitted changes (`git status --short -- <files>`).

If nothing differs, go on. If something does, ask now, before step 3: say which files differ, and ask whether the work starts from the default branch or from what the checkout has. Then read the differing files as they are at that starting point (`git show <ref>:<path>` reads a file without touching the checkout), so the findings describe the code the work will be built on.

## 3. Cross-check the request against the code

This is where the real questions come from:

- Requirements the code contradicts, or that assume something the code doesn't do.
- Cases the request ignores but the code must handle: empty or missing data, data that predates the change, error responses, permissions, other user types or settings.
- Consumers whose behavior would change or break.
- Hidden scope: migrations, feature flags, API contract changes, translations, docs.
- Acceptance criteria too vague to write a test against.
- A proposed solution that is worse than an obvious alternative. Say so.
- A request that goes against an accepted ADR. Either the request changes or the ADR is superseded, and the developer says which.
- An ADR with status `Inferred` that the request relies on or goes against. It was read out of the code and nobody has confirmed it, so it is a question: does the decision hold? The `adr` skill records the answer ("Confirming an inferred ADR").

Then cross-check what the request says nothing about: how the change behaves once it runs for real. Requests describe the behavior and leave this out, and what is never a requirement is never built or checked. For each point, find what the code on the path does today and whether the change moves it:

- **Security:** which input the change trusts and where it comes from, who may do the new thing and where that is enforced, and whether a secret or personal data ends up somewhere new: a log, a response, a message.
- **Performance:** how much data and how many calls it has to handle in production, not in the test data. A query per row, a list with no limit, a call on a path that runs for every request.
- **Failure:** what the user sees and what state the data is in when something it depends on is slow, down or answers with an error, and when the operation stops halfway or runs twice.
- **Observability:** how someone finds out that it stopped working, and what they would need to see to tell why: a log line, a metric, an alert.
- **Rollout and rollback:** what has to happen besides deploying the code (a migration, configuration, a flag, an order between repos), and whether reverting after a deploy brings the old behavior back. Data written in a new shape, messages already sent and a contract someone has started to use are not undone by a revert.
- **Dependencies:** whether it needs a package, a service or a tool the repo doesn't use yet. That is a decision, not a detail of the build.

For most work, most of these come out as "no change". Find that out by looking; don't assume it. The ones that apply are questions for step 4, and the ones that don't are read back there for confirmation.

Then cross-check the language. Collect the domain terms the request uses and the names the code uses for the same things, and compare both with the glossary. Skip generic technical words. Look for:

- A term the work depends on that the glossary doesn't have.
- A term that the request, the code and the glossary use differently.
- Two words for one thing, or one word for two things.
- A rule in the glossary that the request breaks.
- A rule the request takes for granted that isn't written down. "Only the owner can close an account", hidden inside an acceptance criterion, is a rule.
- Inferred entries this work relies on.

Classify the work as a **feature/change** or a **bug/inconsistency** (wrong output, crash, two code paths disagreeing). For a bug, the expected behavior is what you ask about.

## 4. Ask

The questions are there to align you and the developer, not only to fill gaps. Ask about everything you would otherwise decide yourself, also when the answer looks obvious. An obvious answer takes the developer a few seconds to confirm. A guess that looked obvious and was wrong is found after the code is written.

Always run at least one round, even when the request looks complete. What goes to the developer:

- Every open point from step 3.
- Everything you inferred instead of read: your reading of a vague sentence, a case the request doesn't mention, a default, what you would leave out of scope. If neither the ticket nor the code says it in so many words, it is a question, with your reading as the recommended answer.
- The key points of a well-defined ticket, read back for confirmation: the ones that cost the most if you understood them wrong.
- The non-functional points that came out as "no change", read back together in one question so the developer can object.

Each question states:

- What you found, with a `file:line` reference or a quote from the ticket.
- The options.
- Your recommended answer and why.

When the host has a tool for asking the user questions with options to pick from (`AskUserQuestion` in Claude Code), use it. The developer answers with a click, which keeps many questions cheap. Such a tool has room for a short question and its options only, so first post what you found in the chat, numbered and with the references, then ask with the tool: one question per point, the recommended option first, in as many calls as its limits need. Without such a tool, post one numbered list.

A language question is a proposal: the term, its meaning, its rules and the words it replaces, written as the glossary entry would read. For a new term, ask the two questions from "The shared language", one term at a time: should it be added to the glossary, and is this definition correct. Post the full entry in the chat first, since the question tool has no room for it. If the developer corrects the definition, show the corrected entry and ask again until they say it is right. If they don't want the term in the glossary, it is still agreed for this work and stays in the spec only. Never settle a term or a rule yourself, and never let a request that breaks an agreed rule pass quietly. Either the request changes or the rule does, and the developer says which.

Don't ask what the ticket or the code already says in so many words. Push back when an answer conflicts with the code or the ticket. Keep going round by round until nothing is left that you would have to decide yourself.

## 5. Write the spec and get it approved

Write `spec.md` with the sections below, and post it in the chat as well:

- **Goal:** one sentence.
- **Type:** feature/change or bug.
- **Today:** current behavior, with file references, and the commit and branch the code was read at.
- **After:** target behavior.
- **Acceptance criteria:** concrete, testable statements. Each one must be checkable by a test.
- **Non-functional requirements:** one line each for security, performance, failure, observability, rollout and rollback, and dependencies, from the cross-check in step 3: what is required, or "no change" with the reason in a few words. Whatever a test can check is written as an acceptance criterion as well, so it is built test-first and checked like the rest.
- **Out of scope:** what will not be touched.
- **Language:** the terms this work depends on, each with its meaning, its rules and the words not to use for it, marked new, changed or existing. A new term also says whether the developer wanted it in the glossary or only in this spec. The rest of the spec uses these terms and no other words for the same things.
- **Decisions:** each question from step 4 with the answer the developer gave. `strategic-design` picks up the ones that deserve an ADR and records them with the plan.

The spec has no assumptions section. Anything you would have put there is a question for step 4.

Wait for an explicit approval. If the developer changes something, update the file and ask again. The spec is approved only when they say so; then set its status line and tell them the path.

## 6. Update the glossary

Once the spec is approved, the new and changed terms the developer confirmed in step 4 go into the glossary with status `agreed` and today's date. Both answers are needed: the developer said yes to adding the term and said the definition is correct. Approving the spec doesn't replace either answer, so a term that got into the spec without them is asked about now, before it is written. A term the developer kept out of the glossary is not written. Nothing goes into the glossary before the spec is approved. If the spec changes later and is approved again, bring the glossary in line with it, and ask again about any entry whose wording changed.

Where they are written depends on where the glossary is:

- **Outside the code this work changes**, such as `repos/<repo>/glossary.md` or `docs/glossary.md` in a home repo: write them now. Don't commit. Tell the developer which files changed.
- **A tracked file in a repo this work changes:** don't write it in the developer's checkout. The change belongs on the work's branch, and an edit left uncommitted in the checkout has to be moved there and undone here later. The approved spec holds the entries until the work's worktree exists. They are written there and get a commit of their own (`implement`, "Work in a worktree"; `strategic-design` plans the commit). Once the worktree exists, later glossary changes are written in it too.

When this skill runs on its own and no build follows, there is no branch for the second case. Tell the developer that the terms are agreed in the spec and not yet in the glossary file, and write them to the checkout only if they ask.

## 7. Bring the ticket in line

Only when the work came from a ticket. The questions in step 4 usually change what the ticket says: a criterion got sharper, a case was added, something moved out of scope. The spec is a local file that is not in git, so the ticket is the only place the rest of the team sees what was agreed. A ticket that still says the old thing misleads the tester, the reviewer and whoever plans from it.

Compare the approved spec with the ticket on what a reader of the ticket relies on: the goal, the acceptance criteria, what is out of scope, and the decisions that change what a user gets. File references and how it will be built don't count. The ticket never had them.

If nothing differs, say so. If something does, list the differences and ask what to do with the ticket: update its description, add a comment that says what changed, or leave it. That is the developer's call, since the ticket may belong to someone else. This skill doesn't write to the tracker. An update or a comment goes through `ticket-creator` ("An existing ticket"), which puts it in plain language, shows the text and waits for approval before it writes.

When an approved spec changes later and is approved again, do this again.

## When it is done

Tell the developer the path of the spec, which glossary files changed, and what happened with the ticket.

An approved spec is a point where the files hold everything. When this skill runs on its own, say that this is a good time to clear the context, and give the prompt that continues the work with `strategic-design` or `implement`. The `implement` skill owns the rule ("Clear the context"), and says it itself when this skill runs as its first phase.
