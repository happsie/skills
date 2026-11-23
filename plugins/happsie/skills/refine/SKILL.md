---
name: refine
description: Refine a feature request, task or ticket into a brief the developer has approved, before any code is written. Reads the ticket and the code it touches, cross-checks them, and asks the questions whose answers change what gets built, even when the request looks well defined. Also agrees on the domain terms and rules the work depends on and records them in the project's glossary. Use when the user asks to "refine this", "refine PROJ-123", "let's align on this ticket", "what's unclear about this feature", "grill me on this", or as the first phase of the implement skill. Input is free text or a ticket key from any tracker (Jira, GitHub, Linear, ...). Writes the brief to a file and updates the glossary; it never changes code.
---

# Refine

Building the wrong thing is the most expensive mistake. This skill pins down what to build and ends with a brief the developer has explicitly approved. That brief is the contract every later step works from.

This skill never edits code, creates branches or writes to the tracker. The only files it writes are the brief and, once the brief is approved, the glossary.

## The ask rule

No assumptions. If something is unclear, contradictory or missing, ask the developer. Never pick an interpretation yourself, and never fill a gap with what seems likely. Reading code, reading the ticket and running read-only commands need no permission. Deciding what the feature should do always does.

## Where the documents live

The brief and the plan are files, so they survive a long session and can be picked up in a new one. Each piece of work gets a folder named after the ticket key, or a short slug for free text:

- **In a home repo** (the current directory's `CLAUDE.md` says it is a home repo, as set up by the `home-repo` skill): `work/<key-or-slug>/` in the home repo. This holds even when the code changes land in other repos.
- **Anywhere else:** `.implement/<key-or-slug>/` at the root of the repo being worked on. Keep it out of git by adding `.implement/` to `.git/info/exclude`. Don't edit the repo's `.gitignore` for this.

The folder holds `brief.md` (written by `refine`) and `plan.md` (written by `strategic-design`). Each starts with a status line: `Status: draft`, or `Status: approved <YYYY-MM-DD>` once the developer has approved it. Only the developer's explicit approval sets it to approved. Any later change sets it back to draft until approved again.

Writing and updating these two files needs no permission. Don't commit them unless asked.

## The shared language

The request, the brief, the tickets and the code should use the same word for the same thing. When they don't, people agree on a sentence and mean different things by it, and the code ends up with three names for one concept. So the project's glossary is treated the way domain-driven design treats its ubiquitous language: terms and the rules about them are proposed, agreed with the developer, written down, and from then on followed by every later step.

A glossary entry holds a term and the agreements about it:

```markdown
## <Term>

<What it means, in one or two sentences.>

- **Also called:** <other words for it in code, tickets or speech>
- **Rules:** <what always holds for it, one per line: "A published recipe has at least one ingredient.">
- **Context:** <the repo, module or team where it means this. Leave out if it means this everywhere.>
- **Status:** agreed <YYYY-MM-DD> | inferred
```

- **Also called** lists the words to stop using. New briefs, tickets, code and tests use the term itself.
- **Rules** are the agreements: statements about the term that hold no matter which feature is being built. A rule is not an acceptance criterion. A criterion is done when the work is done; a rule keeps holding afterwards.
- **Status** says how far to trust the entry. `agreed` means a person approved it. `inferred` means it was read out of code or tickets and nobody has confirmed it. Follow agreed entries. Treat inferred ones as a good guess, and get the ones this work relies on confirmed.

One term has one meaning within a context. If two repos or modules use the same word for different things, that is two entries, each with its context. Don't bend them into one definition. Write down both, and how one translates into the other where they meet.

Where the glossary is:

- **In a home repo:** the home `CLAUDE.md` says where each repo's glossary is and where terms shared between repos go. Follow it.
- **Anywhere else:** the repo's own glossary (`GLOSSARY.md`, `docs/glossary*`, or a glossary section in the README or docs). If it uses another format, keep that format and fit the same information into it.
- **If there is none:** ask in step 4 whether to create `docs/glossary.md`. If the developer says no, the agreed language lives only in the brief.

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
- The glossary entries for the area, and the names the code uses for the same things.
- Other project docs that define rules: ADRs, coding standards, `CLAUDE.md`, `AGENTS.md`.

## 3. Cross-check the request against the code

This is where the real questions come from:

- Requirements the code contradicts, or that assume something the code doesn't do.
- Cases the request ignores but the code must handle: empty or missing data, data that predates the change, error responses, permissions, other user types or settings.
- Consumers whose behavior would change or break.
- Hidden scope: migrations, feature flags, API contract changes, translations, docs.
- Acceptance criteria too vague to write a test against.
- A proposed solution that is worse than an obvious alternative. Say so.

Then cross-check the language. Collect the domain terms the request uses and the names the code uses for the same things, and compare both with the glossary. Skip generic technical words. Look for:

- A term the work depends on that the glossary doesn't have.
- A term that the request, the code and the glossary use differently.
- Two words for one thing, or one word for two things.
- A rule in the glossary that the request breaks.
- A rule the request takes for granted that isn't written down. "Only the owner can close an account", hidden inside an acceptance criterion, is a rule.
- Inferred entries this work relies on.

Classify the work as a **feature/change** or a **bug/inconsistency** (wrong output, crash, two code paths disagreeing). For a bug, the expected behavior is what you ask about.

## 4. Ask

Always run at least one round, even when the request looks complete. A well-defined ticket still gets its key points read back for confirmation: the ones that cost the most if you understood them wrong.

Post one numbered list. Each question states:

- What you found, with a `file:line` reference or a quote from the ticket.
- The options.
- Your recommended answer and why.

A language question is a proposal: the term, its meaning, its rules and the words it replaces, written as the glossary entry would read. Never settle a term or a rule yourself, and never let a request that breaks an agreed rule pass quietly. Either the request changes or the rule does, and the developer says which.

Don't ask what the ticket or the code already answers. Push back when an answer conflicts with the code or the ticket. Keep going round by round until no open question would change what gets built.

## 5. Write the brief and get it approved

Write `brief.md` with the sections below, and post it in the chat as well:

- **Goal:** one sentence.
- **Type:** feature/change or bug.
- **Today:** current behavior, with file references.
- **After:** target behavior.
- **Acceptance criteria:** concrete, testable statements. Each one must be checkable by a test.
- **Out of scope:** what will not be touched.
- **Language:** the terms this work depends on, each with its meaning, its rules and the words not to use for it, marked new, changed or existing. The rest of the brief uses these terms and no other words for the same things.
- **Decisions:** each question from step 4 with the answer the developer gave.

The brief has no assumptions section. Anything you would have put there is a question for step 4.

Wait for an explicit approval. If the developer changes something, update the file and ask again. The brief is approved only when they say so; then set its status line and tell them the path.

## 6. Update the glossary

Once the brief is approved, write its new and changed terms into the glossary with status `agreed` and today's date. Approving the brief approves these entries, so nothing goes into the glossary before that. If the brief changes later and is approved again, bring the glossary in line with it.

Don't commit the change. Tell the developer which glossary files changed. When the glossary is a tracked file in the repo being worked on, the change belongs on the work's branch, and `strategic-design` plans a commit for it.
