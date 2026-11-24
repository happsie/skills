---
name: adr
description: Record a decision as an ADR (architecture decision record) so the reason for it outlives the conversation it was made in. Writes one short file per decision with the context, the decision, the alternatives that lost and the consequences, in the project's ADR folder, and marks an older ADR as superseded when the new one replaces it. Also turns an ADR that was inferred from the code into an accepted one, once the developer confirms that the decision holds. Use when the user says "write an ADR", "record this decision", "add a decision record", "document why we chose X", "supersede ADR 7", "confirm this inferred ADR", or when the strategic-design skill has an approved plan with decisions to record. Not for making the decision, not for domain terms and rules (the glossary, through refine), and not for what a feature should do (the spec).
---

# ADR

Code shows what was decided. It doesn't show why, or what was turned down. Without that, the next person either undoes the decision without knowing what it protected, or doesn't dare touch it. An ADR is a short note that keeps the reason: one decision, written down when it is made, by the people who made it.

This skill records decisions. It never makes them, and it never changes code.

## The ask rule

No assumptions. The developer makes the decision and you write down what they decided.

- Never invent the reasoning. If you don't know why something was chosen, or what else was considered, ask.
- Nothing is written to the ADR folder before the developer has approved the text.
- An accepted ADR is not rewritten. When a decision changes, a new ADR supersedes the old one, so the history stays readable.

## What gets an ADR

A decision gets one when someone reading the code later would ask "why is it like this?" and the code can't answer. Signs:

- It was a choice between real alternatives, and the one that lost was reasonable.
- It is costly to reverse: persistence, messaging, an API contract, a module boundary, a new dependency.
- It sets a pattern or convention that later work is expected to follow.
- It goes against an existing ADR, or against how the codebase normally does things.

What doesn't get one:

- What the feature should do. That is the spec.
- What a domain term means, or a rule about it. That is the glossary, which `refine` keeps.
- Formatting, naming and other habits. Those are coding standards.
- A choice any developer on the project would make the same way, or one that is local and cheap to change.

Most pieces of work produce no ADR. If you are unsure whether a decision qualifies, ask instead of writing one to be safe. A folder full of trivial records is one nobody reads.

## Where ADRs live

- **In a home repo:** the home `CLAUDE.md` says where each repo's ADRs are and where decisions that span repos go. Follow it.
- **Anywhere else:** the repo's own ADR folder (`docs/adr`, `doc/adr`, `adr`, `docs/decisions`, `docs/architecture/decisions`, or any folder of numbered decision files). Keep its format, numbering and index as they are, and fit the same information into them.
- **If there is none:** ask whether to create `docs/adr/`. If the developer says no, nothing is written.

## The format

When the folder has no format of its own, use `assets/adr-template.md`:

- **Status:** `Accepted` once the developer has approved it. `Proposed` when they want it written down before it is settled, for example to take it to the team. `Superseded by NNNN` when a later ADR replaced it. `Inferred` is for records read out of code that nobody has confirmed; the `home-repo` skill seeds those, and this skill doesn't write them. It turns one into an accepted ADR once someone confirms it ("Confirming an inferred ADR").
- **Repos:** the repos affected. Leave the line out when the ADR lives in the only repo it concerns.
- **Context:** the situation that forced a choice, and the constraints that mattered. Facts, not the argument for the decision.
- **Decision:** what was decided, in a sentence or two, stated as what we do.
- **Alternatives:** what else was considered and why it lost. This is the part people come back for.
- **Consequences:** what gets easier, what gets harder, and what later work now has to do.

One decision per file, named `NNNN-short-title.md` with the next free number. Keep it under a page. An ADR that needs more is usually two decisions.

## 1. Gather the decision

The decision comes from the conversation, from the Decisions section of an approved `plan.md` (written by `strategic-design`), or from a spec.

- Read the ADRs already in the folder. Find any that the new decision contradicts, replaces or builds on.
- If the context refers to code, open it and check that it says what you are about to write.
- List what is missing: the reason, the alternatives, the consequences. Ask for those. Don't fill them in.

If the decision contradicts an accepted ADR, say so before writing anything. Either the decision changes, or the old ADR is superseded, and the developer says which.

## 2. Draft and get approval

Post the full text of the ADR in the chat, with the path it will get and any ADR it supersedes. Wait for an explicit approval.

When `strategic-design` calls this skill with an approved plan, that approval covers the decisions as the plan states them. Write them without asking again, and ask only when the ADR would say something the plan doesn't.

## 3. Write it

- Write the file with status `Accepted` and today's date, or `Proposed` if that is what the developer asked for.
- If the folder has an index (a README table or a list), add the row.
- When it supersedes an older ADR, set the old one's status to `Superseded by NNNN` and update its index row. Change nothing else in the old file.

Don't commit unless asked. When the ADR folder is a tracked part of a repo that a piece of work is changing, the ADR belongs on that work's branch: write it in the work's worktree, and `strategic-design` plans a commit for it.

## Confirming an inferred ADR

An ADR with status `Inferred` was read out of the code by the `home-repo` skill. It says what the code does. Nobody has said that the decision still holds, or why it was made, so it binds nobody, and it stays that way until someone asks. `refine` and `strategic-design` ask when a piece of work relies on one or goes against one, and the developer can ask at any time.

Show the ADR and ask two things:

- Does this decision hold, as something later work has to follow?
- Why was it made, and what was turned down? "Nobody knows any more" is an answer. Write that instead of a reason.

Then draft the result and get it approved as in step 2:

- **It holds.** Rewrite the file with what the developer said: fill in Alternatives, set the status to `Accepted` with today's date, and remove the "Inferred from the code" line at the top. An inferred ADR may be rewritten. The rule against rewriting protects accepted ones.
- **It doesn't hold.** It was an accident of the code, or the team has moved on. If something else was decided in its place, write that as a new ADR and mark this one `Superseded by NNNN`. If nothing was, delete the file and its index row: a record of a decision nobody made is worse than no record.
- **The developer can't say.** Leave it as `Inferred`, and say that the work goes on without it binding anything.

## Report

The path of each ADR written, its status, and any ADR it superseded.
