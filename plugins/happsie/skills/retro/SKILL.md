---
name: retro
description: Turn what went wrong in a piece of work into lessons that stop it from happening again. Reads the findings log (what the checks in deliver found, the questions that stopped the build, the developer's corrections, the review comments and failing checks), finds what would have caught each one earliest, and proposes a lesson for the place where it will be enforced, which is a check a machine runs, the coding standards, the glossary, an ADR or the repo's agent instructions. Writes nothing before the developer approves it. Use when the user says "retro", "run a retro", "retrospective", "what did we learn", "lessons learned", "why did this keep happening", "update the standards from this", "stop making this mistake", or when a pull request built with implement or quick-fix has been merged. Works on one piece of work or several. Not for finding the cause of a problem in the product (investigate), and not for checking work that isn't delivered yet (deliver).
---

# Retro

The glossary keeps the language and the ADRs keep the decisions. Without this skill nothing keeps the mistakes. A reviewer points out that errors are handled the wrong way, it is fixed, and the next piece of work handles them the wrong way again, because the fix is in the code and the reason is in a chat that is gone. This skill reads what went wrong, asks what would have caught it earliest, and writes that down where the next piece of work will meet it.

It changes no product code. It writes lessons, and only after the developer has approved each one.

## The ask rule

No assumptions. A lesson is a proposal until the developer approves it: the wording, and the file it goes in. Never write a rule because one finding suggests it, and never turn one person's review comment into a standard for the team without asking. Reading the log, the pull request, the code and the project docs needs no permission.

## The findings log

`findings.md` is the log of what went wrong in a piece of work. It is in the work's folder, next to `spec.md` and `plan.md`: `work/<key-or-slug>/` in a home repo, otherwise `.implement/<key-or-slug>/` at the root of the repo (`refine`, "Where the documents live"). It exists because the findings would otherwise be gone: they are fixed before the pull request, and the context they were found in is cleared.

One entry per finding:

```markdown
## <YYYY-MM-DD> <one line that says what was wrong>

- **Source:** spec check | code review | question during the build | developer correction | review comment | failing check
- **Found:** <what it was, with `file:line` or the output>
- **Outcome:** fixed in <commit> | accepted as is | spec changed | plan changed | answered | declined, <reason>
```

Who writes to it:

- `deliver`: every finding from the spec check and the code review, in every round.
- `implement` and `quick-fix`: every question that stopped the work, with the answer, and every time the developer corrects something that was built or proposed.
- `revise`: every review comment and every failing check.

Appending needs no permission, and the file is not committed. Entries are written when the thing happens, in plain words, and are not tidied afterwards. This skill adds a section of its own at the end (step 5) and changes nothing else in the file.

## 1. Gather what happened

One piece of work, or several. Patterns show better across several: the same finding in three logs is a lesson, and in one it may be an accident.

For each piece of work, read:

- `findings.md`.
- The Decisions section of `spec.md`, and Risks and open questions in `plan.md`.
- `investigation.md`, if there is one.
- The pull request, if it can be fetched: review comments and failed checks that are not in the log.

If there is no log, the work was not built with these skills or the log was lost. Work from the pull request and from what the developer tells you, and say that this is the basis.

Ask the developer what they would add. What annoyed them is often not in any file.

## 2. Find what would have caught it

For each finding, the question is not what was wrong, but what would have stopped it earliest:

- **The spec:** a question nobody asked, a criterion too vague to test, a case or a consumer that was missed.
- **The plan:** a step that left something out, a refactor that should have come first, a test layer that was missing.
- **A convention nobody wrote down:** the code was fine in general and wrong for this repo.
- **A term or a rule about it:** two names for one thing, or a rule that was broken because it isn't in the glossary.
- **A decision with no record:** something was undone or redone because nobody knew why it was the way it was.
- **A missing check:** something a linter, a type, a test or the pipeline could have refused.
- **The setup:** a tool, an environment or a command that didn't work the way the docs say.
- **A rule that exists and wasn't followed.** This is a different kind of finding. Writing the rule down a second time helps nothing. Ask why it wasn't seen: it is in a file nobody reads, it is too vague to act on, or it can only be kept by a machine.

Open the code and the docs to check each one. If you are about to say a convention is not written down, look for it first.

Then group them. Findings with the same cause are one lesson. Most findings are one-offs: a slip that the checks caught, as they are meant to. Say that they are, and leave them. A lesson is worth writing only when the same thing would happen again.

## 3. Choose where each lesson goes

Put it where it is enforced the hardest, and where the work that needs it will read it:

1. **A check a machine runs.** A lint rule, a type, a test, a step in the pipeline. A rule a machine checks can't be forgotten, so prefer this whenever the lesson can be expressed that way. It is a change to the code: draft a ticket for it with `ticket-creator`, or make it with `quick-fix` if the developer wants it now.
2. **The coding standards.** A convention for how code is written in this repo. `refine` and `quick-fix` read them, the build follows them and the code review in `deliver` checks against them. In a home repo, the home `CLAUDE.md` says where each repo's standards are and where shared ones go. Anywhere else, the repo's own (`CONTRIBUTING.md`, `docs/coding-standards*`, `docs/conventions*`, `STYLEGUIDE*`). If there are none, ask whether to create `docs/coding-standards.md`.
3. **The glossary.** A term, or a rule about one. Write the entry the way `refine` describes ("The shared language").
4. **An ADR.** A decision that should have been on record. The `adr` skill says what gets one and writes it.
5. **The repo's `CLAUDE.md` or `AGENTS.md`.** How to work in this repo: commands, setup, traps in the environment. Not conventions for the code; those are standards.
6. **The way of working.** A gap in the skills themselves: a question `refine` should ask, something the checks don't look for. An installed skill can't be changed from here. Report it to the developer in a form they can pass on to whoever owns the skills.

Write each lesson so that it can be followed and checked:

- One rule, and the reason for it in a sentence. A rule without its reason gets dropped the first time it is in the way.
- Specific. "Inject the clock; never read the system time in domain code" can be checked. "Be careful with time" can't.
- Stated as what to do. Add the wrong way only when it is the one people reach for.
- Not there already. If it is, the lesson is about why it wasn't followed (step 2).
- In line with the rest. If it goes against an existing standard or an accepted ADR, don't pick one. Show both and ask which holds.

A standards file that only grows stops being read. Where a new lesson sharpens an existing line, propose the edit to that line, not a new one below it.

## 4. Propose and get approval

Post one numbered list. For each lesson:

- The findings behind it: which work, which entries, with `file:line`.
- What would have caught it, from step 2.
- Where it goes, and why there.
- The exact text, as it will read in that file. For a ticket, the draft.

List the one-offs after it in a line each, so the developer can see what was left out and disagree.

Wait for an explicit approval. The developer takes, changes or drops each lesson. Approving one approves that text for that file, and nothing else.

## 5. Write the lessons

Where a lesson is written depends on where the file is:

- **Outside the code**, such as `repos/<repo>/coding-standards.md` or `docs/` in a home repo: write it now. Don't commit. Tell the developer which files changed.
- **A tracked file in a repo:** never in the developer's checkout. The change gets a worktree and a branch of its own, cut from the remote's default branch: `worktrees/<repo_name>-retro/` in the work's folder, set up the way `implement` describes ("Work in a worktree"). One commit. Post the pull request's title and description, and push and open it only after the developer approves. Don't put the lessons on the work's own branch: they are a separate change, and other people have a say in a shared standard.
- **A glossary entry or an ADR:** through `refine`'s rules and the `adr` skill, which say where those go.
- **A check a machine runs:** the ticket goes through `ticket-creator`, the change through `quick-fix`. Both ask for their own approval.

Then add a section at the end of each `findings.md` that was read, so the next retro doesn't propose the same thing:

```markdown
## Retro <YYYY-MM-DD>

- <lesson in one line> -> <file, ticket or pull request>
- One-offs, no lesson: <the entries, by their one-liners>
```

## Report

- Each lesson, where it was written, and any ticket or pull request opened for it.
- Lessons the developer dropped.
- Gaps in the way of working, worded so they can be passed on.
- The one-offs, in a line.
