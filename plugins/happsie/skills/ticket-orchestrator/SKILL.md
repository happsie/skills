---
name: ticket-orchestrator
description: Create two or more tickets as one connected set. Use whenever a request will end in more than one ticket, also when the tickets come from one document, spec, artifact or list, or already exist as drafts. Slices the work, maps dependencies, shows the outline and every draft for approval, then creates the tickets with parent or epic and blocks / relates-to links. Use for "create tickets for this", "create these tickets", "break this down into tickets", "split this epic into stories", "make an epic with stories", "turn this spec into tickets". Works with any tracker (Jira, GitHub, Linear, ...). For a single ticket, use ticket-creator.
---

# Ticket orchestrator

Several tickets created one at a time end up overlapping, leaving gaps, and pointing at each other in the wrong direction. This skill plans the set as a whole first, then creates it in an order where every link can be made.

Each ticket follows the `ticket-creator` skill: its sections, its plain-language rules and its tracker formatting. Open that skill and read it before drafting, every time; the template is there and not here, and tickets written from memory of it come out in another format. This skill adds what a set needs on top: slicing, connections and creation order.

Nothing is written to the tracker before the user has approved the set. There are two approvals, the outline in step 4 and the drafts in step 5, and both are needed however many tickets there are.

## The ask rule

No assumptions. How the work is sliced, what depends on what, and what is left out are the user's decisions. Recommend, then ask. Reading the tracker, the code and project docs needs no permission.

## 1. Understand the whole

Gather the request the way `ticket-creator` does: free text, the conversation, ready-made ticket drafts, or an approved spec from `refine`. Ready-made drafts are input, not finished tickets: they still go through the slicing below and get rewritten into the `ticket-creator` format. If the input is an existing epic or ticket to break down, read it with its children, links and comments.

Then look in the tracker for what already exists: tickets that cover part of this work, and tickets outside the set that it depends on or that wait for it. Existing tickets are reused and linked, not recreated.

Ask for what is missing: the goal of the whole, why it matters, what is out of scope, and where the tickets go (project, parent or epic, issue types).

## 2. Slice

Split the work into tickets where each one:

- **Delivers something a person can see or use when it is done.** Slice by outcome, not by layer. "Users can reset their password by email" is a ticket. "Backend for password reset" and "Frontend for password reset" are not: neither gives anyone anything alone, and neither can be described without technical terms.
- **Can be checked by itself**, with its own acceptance criteria.
- **Is small enough to finish in a few days.** If it isn't, look for a thinner first version and put the rest in a follow-up ticket.
- **Doesn't overlap with another.** Every criterion belongs to exactly one ticket.

Work that has no visible outcome but must happen first (a migration, a new integration) gets its own ticket, described by what it makes possible.

Don't split for the sake of it. If the work is one ticket, say so and hand over to `ticket-creator`.

Then check the set against the whole: together the tickets cover the goal, and nothing in them goes beyond it. Whatever was left out is listed as out of scope on the parent, or on the ticket where a reader would expect it.

## 3. Map the connections

- **Parent or epic.** Every ticket in the set hangs under one, unless the user says otherwise. Use an existing one if it fits; otherwise the set includes a new one. The parent's description follows the same format and describes the whole: its Why is the reason for all of it, and its acceptance criteria are the outcomes of the set, not a list of the child tickets.
- **Blocks / is blocked by.** Only where one ticket truly can't start or can't be finished before another is done. Fewer is better: every blocking link is work that can't run in parallel. If most tickets block each other in a chain, the slicing is probably by layer or step; go back to step 2.
- **Relates to.** For tickets that touch the same thing without depending on each other. Use sparingly.
- **Links out of the set**, to existing tickets found in step 1.

There must be no cycles. If A blocks B and B blocks A, they are one ticket or the split is wrong.

## 4. Get the outline approved

Before writing full descriptions, post the outline. Give each new ticket a temporary id (T1, T2, ...):

| Id | Type | Title | Delivers | Blocked by | Relates to |
|----|------|-------|----------|------------|------------|
| E1 | Epic | ... | ... | | |
| T1 | Story | ... | one line | | |
| T2 | Story | ... | one line | T1 | ABC-40 |

Add where the set goes (tracker, project, parent), what is out of scope for the whole, and any open question about the slicing with your recommendation.

Wait for an explicit approval. Changing the outline is cheap now and expensive after the tickets exist.

## 5. Draft every ticket

Write each ticket in the `ticket-creator` format. Across the set:

- Use the same word for the same thing in every ticket, and make it the glossary's word when the project has a glossary.
- Each ticket must make sense to someone who reads only that one. Repeat the little context that needs, and refer to the parent for the rest.
- Out of scope on one ticket names the ticket in the set that covers it ("Sharing a list is handled in T3").
- Refer to other new tickets by temporary id for now.

Post all drafts in the chat, each one in full, and wait for an explicit approval of the set. A summary, a table of titles or "the drafts follow the outline" is not the drafts. With many tickets, post them in batches rather than shortening them.

The rules for what counts as approval are the ones in `ticket-creator` ("Get it approved"): the original request, the answers to your questions and the approved outline are not approval of the drafts. The user approves the text that will be sent, after seeing it. If the user changes one ticket, check whether the change moves a criterion or a dependency in another, and show those changes too.

## 6. Create in order

1. The parent or epic, if it is new.
2. The tickets, blockers before the tickets they block. Keep a map from temporary id to real key as you go.
3. Replace every temporary id in the descriptions with the real key. Tickets created before the one they mention need an update afterwards.
4. The links, once all tickets exist. Check the direction of each one against the approved outline before sending it; "blocks" and "is blocked by" are easy to swap, and trackers name the two ends differently.

If a step fails, stop. Report what has been created with keys, what hasn't, and the error. Don't retry a create call without first checking the tracker for whether the ticket was made, or the set ends up with duplicates. Don't delete anything to clean up without asking.

Then read the set back from the tracker and compare it with the approved outline: every ticket exists under the right parent, every link is there and points the right way, and no temporary id is left in any description.

## Report

The outline table again, with real keys and URLs in place of temporary ids. List anything that couldn't be set and why.
