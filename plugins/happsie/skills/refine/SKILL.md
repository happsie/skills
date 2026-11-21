---
name: refine
description: Refine a feature request, task or ticket into a brief the developer has approved, before any code is written. Reads the ticket and the code it touches, cross-checks them, and asks the questions whose answers change what gets built, even when the request looks well defined. Use when the user asks to "refine this", "refine PROJ-123", "let's align on this ticket", "what's unclear about this feature", "grill me on this", or as the first phase of the implement skill. Input is free text or a ticket key from any tracker (Jira, GitHub, Linear, ...). Writes the brief to a file; it never changes code.
---

# Refine

Building the wrong thing is the most expensive mistake. This skill pins down what to build and ends with a brief the developer has explicitly approved. That brief is the contract every later step works from.

This skill never edits code, creates branches or writes to the tracker. The only file it writes is the brief.

## The ask rule

No assumptions. If something is unclear, contradictory or missing, ask the developer. Never pick an interpretation yourself, and never fill a gap with what seems likely. Reading code, reading the ticket and running read-only commands need no permission. Deciding what the feature should do always does.

## Where the documents live

The brief and the plan are files, so they survive a long session and can be picked up in a new one. Each piece of work gets a folder named after the ticket key, or a short slug for free text:

- **In a home repo** (the current directory's `CLAUDE.md` says it is a home repo, as set up by the `home-repo` skill): `work/<key-or-slug>/` in the home repo. This holds even when the code changes land in other repos.
- **Anywhere else:** `.implement/<key-or-slug>/` at the root of the repo being worked on. Keep it out of git by adding `.implement/` to `.git/info/exclude`. Don't edit the repo's `.gitignore` for this.

The folder holds `brief.md` (written by `refine`) and `plan.md` (written by `strategic-design`). Each starts with a status line: `Status: draft`, or `Status: approved <YYYY-MM-DD>` once the developer has approved it. Only the developer's explicit approval sets it to approved. Any later change sets it back to draft until approved again.

Writing and updating these two files needs no permission. Don't commit them unless asked.

## 1. Gather the request

If a `brief.md` already exists for this work, read it and continue from there instead of starting over.

- **Free text.** Take it as given. If it points at a ticket, document or conversation you can reach, read that too.
- **Ticket key or URL.** Fetch it with whatever is available: a tracker MCP server, a CLI such as `gh issue view`, or another skill built for that tracker. Read the description, acceptance criteria and comments, then the parent or epic, sibling tickets, linked issues and any existing branches or PRs. Comments often overrule the description, so read them all.

If the ticket can't be fetched, say so and ask for the text. Don't work from a title alone.

## 2. Read the code the change touches

Find the entry points (endpoint, consumer, job, UI, CLI) and follow the path down to persistence. Read the existing tests for that path. Look for:

- A similar feature that already exists, and how it was built.
- Everything that calls or consumes what will change: other modules, other services, the frontend, reports, exports.
- Recent `git log` on those files, for context or half-finished attempts.
- Project docs that define terms or rules: glossary, ADRs, coding standards, `CLAUDE.md`, `AGENTS.md`.

## 3. Cross-check the request against the code

This is where the real questions come from:

- Requirements the code contradicts, or that assume something the code doesn't do.
- Cases the request ignores but the code must handle: empty or missing data, data that predates the change, error responses, permissions, other user types or settings.
- Consumers whose behavior would change or break.
- Hidden scope: migrations, feature flags, API contract changes, translations, docs.
- Acceptance criteria too vague to write a test against.
- Terms used differently in the request and in the code.
- A proposed solution that is worse than an obvious alternative. Say so.

Classify the work as a **feature/change** or a **bug/inconsistency** (wrong output, crash, two code paths disagreeing). For a bug, the expected behavior is what you ask about.

## 4. Ask

Always run at least one round, even when the request looks complete. A well-defined ticket still gets its key points read back for confirmation: the ones that cost the most if you understood them wrong.

Post one numbered list. Each question states:

- What you found, with a `file:line` reference or a quote from the ticket.
- The options.
- Your recommended answer and why.

Don't ask what the ticket or the code already answers. Push back when an answer conflicts with the code or the ticket. Keep going round by round until no open question would change what gets built.

## 5. Write the brief and get it approved

Write `brief.md` with the sections below, and post it in the chat as well:

- **Goal:** one sentence.
- **Type:** feature/change or bug.
- **Today:** current behavior, with file references.
- **After:** target behavior.
- **Acceptance criteria:** concrete, testable statements. Each one must be checkable by a test.
- **Out of scope:** what will not be touched.
- **Decisions:** each question from step 4 with the answer the developer gave.

The brief has no assumptions section. Anything you would have put there is a question for step 4.

Wait for an explicit approval. If the developer changes something, update the file and ask again. The brief is approved only when they say so; then set its status line and tell them the path.
