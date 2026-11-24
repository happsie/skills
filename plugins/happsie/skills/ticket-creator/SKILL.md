---
name: ticket-creator
description: Write exactly one ticket and create it in the user's tracker, after the user has approved the draft. For two or more tickets, use ticket-orchestrator instead, never this skill in a loop. The ticket is non-technical, with the sections Description, Why, Acceptance criteria, Scenarios and Out of scope, and gets links to related tickets. Use for every request to create a ticket, also a rushed "just create it", since creating one directly skips the draft and the approval. Triggers: "create a ticket", "write a ticket for this", "make a Jira issue", "open an issue", "file a bug", "turn this spec into a ticket", or to rewrite an existing ticket in this format. Works with any tracker (Jira, GitHub, Linear, ...).
---

# Ticket creator

A ticket is read many times: by the person who prioritizes it, the developer or agent who builds it, the tester who checks it, and whoever wonders a year later why it was done. This skill writes one ticket that all of them can understand, shows the draft, and creates it in the tracker once the user has approved it.

Nothing is written to the tracker before that approval.

## One ticket only

Count the tickets the request will end in before doing anything else. If it is two or more (a list of things to file, a document or spec with several pieces of work, an epic with stories, "tickets" in the plural), stop and run the `ticket-orchestrator` skill. Open it and follow it; its name alone doesn't tell you what it asks for. Don't run this skill once per ticket: tickets written one at a time overlap, leave gaps and get their links wrong, and the user never sees the set as a whole.

The one exception is when `ticket-orchestrator` sent you here to read the ticket format. Then steps 3 and 5 apply to each ticket, and the orchestrator handles the rest.

## The ask rule

No assumptions. If the request doesn't say why the work matters, what done looks like, or where the ticket belongs, ask. Never fill a gap with what seems likely. Reading the tracker, the code and project docs needs no permission.

## Plain language

The ticket describes what the user or the business gets, in the words they would use themselves. It does not describe how to build it.

- No file paths, class names, endpoints, table names or library names. They are wrong by the time someone picks the ticket up, and they shut out every non-developer reader.
- Use the domain's own terms. If the project has a glossary, follow it exactly: its terms, never a word it lists under "Also called", and nothing that goes against a rule it records. The `refine` skill describes where the glossary is and what an entry holds. A ticket that calls one thing by two names gets built as two things.
- Write in the language the project's existing tickets use.
- Short sentences. No filler, no selling.

If the work is technical by nature (an upgrade, a migration, a cleanup), still say it in terms of what it gives: what gets faster, safer, cheaper or possible afterwards. Name the technical thing once, in plain words, and leave the details out.

## 1. Gather

- **Free text or conversation.** Take it as given. Read any ticket, document or thread it points at.
- **A spec from `refine`** (`spec.md`, see the `refine` skill for where it lives). It must be approved. Use it only when the work has no ticket yet. If the spec was refined from an existing ticket, say so and ask whether to update that ticket's description instead of creating a new one.
- **Findings from `investigate`** (`investigation.md`). The ticket is usually a bug. The symptom becomes the Description, with how to see it in the steps a user would take. The cause goes in as one plain sentence; if it wasn't found, say that and what has been ruled out. The acceptance criteria describe the correct behavior, not the fix.

- **Ready-made ticket drafts** in a document, an artifact or the conversation. They are input like any other, not finished tickets. Rewrite each into the template and the plain language below, however complete it looks. If something in a draft doesn't fit the template, ask where it goes; don't keep the draft's format to make room for it.

Specs and findings are written for developers. From a spec, carry over the goal, the target behavior, the acceptance criteria and what is out of scope, and translate them into plain language. Keep the terms from its Language section as they are; they are already the domain's words. Leave the file references and technical detail behind in both cases.

Read the glossary entries for the area, if the project has a glossary.

Then look in the tracker:

- Search for tickets about the same thing. If one looks like a duplicate, show it and ask before going on.
- Find related tickets: work this one depends on, work that waits for this one, and a parent or epic it belongs under.
- Read a few recent tickets in the project to see which issue types, labels and language are in use. That is all they decide. They are not a model for the format or the level of technical detail: a project full of technical tickets still gets this template in plain language. If the user wants the project's existing style instead, that is their call, so ask; don't choose it for them.

## 2. Ask

Ask for whatever is still missing, in one numbered list, with your recommended answer for each. Typical gaps:

- Why it matters, and for whom.
- What is deliberately not part of it.
- Project, issue type and parent or epic, when they can't be read from the request or the tracker.
- Whether a related ticket you found really blocks this one or is just related.
- A term the ticket needs that the glossary doesn't have, or that the request uses in another sense than the glossary. Propose the entry as `refine` does: the term, its meaning, its rules. The same goes for a request that breaks a recorded rule: ask whether the request or the rule changes.

Don't ask what the request or the tracker already answers.

## 3. Draft

**Title:** what changes, in a few words, from the user's point of view. "Users can reset their password by email", not "Add password reset endpoint".

**Description:** what this is about, in a short paragraph. What is the situation today, and what will be different. For a bug: what happens, what should happen instead, and how to see it, in the steps a user would take.

**Why:** who needs this and what it gives them. This is what lets a reader judge priority and make the right call on a detail the ticket didn't cover.

**Acceptance criteria:** a checklist of what must be true when the work is done. One plain sentence per item, each one something a person can check by using the product. Cover the main outcome, the important exceptions and anything that must keep working as before.

**Scenarios:** concrete examples of the criteria, written as Given / When / Then with real values. A criterion says what must hold ("A team can't have more members than its plan allows"). A scenario shows it with an example ("Given a team with 5 members on a plan for 5, when an admin invites a sixth, then the invite is refused with a message that states the limit"). Write scenarios where an example removes doubt: rules, limits, exceptions, anything two people could read differently. Don't write one per criterion out of habit, and don't restate a criterion in other words. Leave the section out when no criterion needs an example, which is common for chores and technical work.

**Out of scope:** what a reader might expect to be included but isn't. Name the ticket that covers it, if there is one.

Template, shown here in Markdown:

````markdown
## Description
<what this is about, today and after>

## Why
<who needs it and what it gives them>

## Acceptance criteria
- [ ] <something a person can check>
- [ ] <...>

## Scenarios
```gherkin
Scenario: <short name>
  Given <starting situation>
  When <what the user does>
  Then <what they see>
```

## Out of scope
- <what is not included>
````

Keep each scenario to one behavior, in the words of the criteria. No UI element names, no technical steps.

The headings are fixed: these five, with these names, in this order. Scenarios is the only one that may be left out. Don't add a heading such as "Technical notes" or "Implementation" for what the plain-language rules keep out.

Before showing the draft, read it once more against the rules above: every heading is there, nothing in it names a file, class, endpoint, table or library, and every criterion can be checked by using the product.

## 4. Get it approved

Post the draft in the chat, together with:

- Where it goes: tracker, project, issue type, parent or epic.
- The links you will create, each with its direction: "is blocked by ABC-12", "relates to ABC-40".
- The glossary entries you will add or change, if step 2 settled any, and the file they go in.

Wait for an explicit approval. If the user changes something, update the draft and ask again.

Approval can only be given to a draft the user has seen, in full, in the chat. None of these are approval:

- The request itself. "Create a ticket for X" asks for this skill to run; it doesn't approve a text that didn't exist yet.
- Answers to the questions in step 2. They fill gaps in the draft; they don't approve it.
- "Just create it", "no need to check with me" or "I trust you", said before the draft exists. The user is trusting a text they haven't read. Show the draft anyway, keep the message short, and say that one word creates it.
- A permission mode that lets tool calls through without asking, or a user who seems to be in a hurry.

Handing the create call to a subagent doesn't change any of this.

If the last thing the user saw wasn't the exact text you are about to send to the tracker, you don't have approval. A ticket created without it has to be found, read and fixed or deleted by the user afterwards, which costs more than the wait.

## 5. Create and link

Create the ticket with whatever is available: a tracker MCP server, a CLI such as `gh issue create`, or another skill built for that tracker. Format the description for the tracker:

- **GitHub, GitLab, Linear, Jira Cloud:** Markdown. Checkboxes as `- [ ]`, scenarios in a `gherkin` code block.
- **Jira Server / Data Center:** wiki markup. Headings as `h2.`, criteria as a `*` bullet list since there are no checkboxes, scenarios in a `{code}` block.
- **Anything else:** look at how an existing ticket is formatted and match it.

Set only the fields that were approved. Leave assignee, sprint, priority and estimate alone unless the user asked for them.

Then create the links. Check the direction of each one before sending it: "A blocks B" and "B blocks A" are easy to swap, and trackers name the two ends differently. If the tracker has no link type for a relation, mention the other ticket's key under the relevant section of the description instead.

Write the approved glossary entries into the glossary with status `agreed` and today's date. Don't commit them. A ticket has no branch to put them on, so when the glossary is a tracked file in a repo, the change is left uncommitted in the developer's checkout. Say that in the report, so they can commit it or take it onto a branch, and it isn't found later as a change nobody remembers making.

If there is no way to reach the tracker, say so and give the finished ticket as text to paste in.

## Report

The ticket key and URL, the links that were created, and any glossary file that changed and is waiting to be committed. If a link or field couldn't be set, say which and why.
