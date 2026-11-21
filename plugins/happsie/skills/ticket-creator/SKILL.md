---
name: ticket-creator
description: Write one ticket and create it in the user's tracker. The ticket is non-technical and readable by anyone on the team, yet precise enough for an agent to build from, with the sections Description, Why, Acceptance criteria, Scenarios and Out of scope. Finds related tickets and sets up links (blocks, is blocked by, relates to, parent or epic) when the tracker supports it. Use when the user asks to "create a ticket", "write a ticket for this", "make a Jira issue", "open an issue for this", "file a bug", "turn this brief into a ticket", or wants an existing ticket description rewritten in this format. Input is free text, the conversation so far, or an approved brief from the refine skill. Works with any tracker (Jira, GitHub, Linear, ...). For more than one ticket, use ticket-orchestrator.
---

# Ticket creator

A ticket is read many times: by the person who prioritizes it, the developer or agent who builds it, the tester who checks it, and whoever wonders a year later why it was done. This skill writes one ticket that all of them can understand, shows the draft, and creates it in the tracker once the user has approved it.

Nothing is written to the tracker before that approval.

## The ask rule

No assumptions. If the request doesn't say why the work matters, what done looks like, or where the ticket belongs, ask. Never fill a gap with what seems likely. Reading the tracker, the code and project docs needs no permission.

## Plain language

The ticket describes what the user or the business gets, in the words they would use themselves. It does not describe how to build it.

- No file paths, class names, endpoints, table names or library names. They are wrong by the time someone picks the ticket up, and they shut out every non-developer reader.
- Use the domain's own terms. If the project has a glossary, follow it.
- Write in the language the project's existing tickets use.
- Short sentences. No filler, no selling.

If the work is technical by nature (an upgrade, a migration, a cleanup), still say it in terms of what it gives: what gets faster, safer, cheaper or possible afterwards. Name the technical thing once, in plain words, and leave the details out.

## 1. Gather

- **Free text or conversation.** Take it as given. Read any ticket, document or thread it points at.
- **A brief from `refine`** (`brief.md`, see the `refine` skill for where it lives). It must be approved. Use it only when the work has no ticket yet. If the brief was refined from an existing ticket, say so and ask whether to update that ticket's description instead of creating a new one.

A brief is written for developers. Carry over the goal, the target behavior, the acceptance criteria and what is out of scope, and translate them into plain language. Leave the file references and technical decisions behind.

Then look in the tracker:

- Search for tickets about the same thing. If one looks like a duplicate, show it and ask before going on.
- Find related tickets: work this one depends on, work that waits for this one, and a parent or epic it belongs under.
- Read a few recent tickets in the project to see which issue types, labels and language are in use.

## 2. Ask

Ask for whatever is still missing, in one numbered list, with your recommended answer for each. Typical gaps:

- Why it matters, and for whom.
- What is deliberately not part of it.
- Project, issue type and parent or epic, when they can't be read from the request or the tracker.
- Whether a related ticket you found really blocks this one or is just related.

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

## 4. Get it approved

Post the draft in the chat, together with:

- Where it goes: tracker, project, issue type, parent or epic.
- The links you will create, each with its direction: "is blocked by ABC-12", "relates to ABC-40".

Wait for an explicit approval. If the user changes something, update the draft and ask again.

## 5. Create and link

Create the ticket with whatever is available: a tracker MCP server, a CLI such as `gh issue create`, or another skill built for that tracker. Format the description for the tracker:

- **GitHub, GitLab, Linear, Jira Cloud:** Markdown. Checkboxes as `- [ ]`, scenarios in a `gherkin` code block.
- **Jira Server / Data Center:** wiki markup. Headings as `h2.`, criteria as a `*` bullet list since there are no checkboxes, scenarios in a `{code}` block.
- **Anything else:** look at how an existing ticket is formatted and match it.

Set only the fields that were approved. Leave assignee, sprint, priority and estimate alone unless the user asked for them.

Then create the links. Check the direction of each one before sending it: "A blocks B" and "B blocks A" are easy to swap, and trackers name the two ends differently. If the tracker has no link type for a relation, mention the other ticket's key under the relevant section of the description instead.

If there is no way to reach the tracker, say so and give the finished ticket as text to paste in.

## Report

The ticket key and URL, and the links that were created. If a link or field couldn't be set, say which and why.
