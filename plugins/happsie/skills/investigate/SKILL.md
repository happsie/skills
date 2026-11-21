---
name: investigate
description: Find the cause of a problem when nobody knows it yet. Pins down the symptom, collects evidence, tests hypotheses one at a time, and ends with either a proven cause and a way to reproduce it, or an honest account of what was ruled out. Never fixes anything. If the problem has no ticket yet, it ends by drafting one through ticket-creator. Use when the user says "investigate this", "why is this happening", "why is this slow", "this fails sometimes", "it's flaky", "I can't reproduce this", "find the root cause", "debug this", "what is going on with X", or when the implement skill can't get a bug to reproduce. Not for bugs with a known cause; those go straight to implement.
---

# Investigate

A fix for a guessed cause is worse than no fix: the real problem stays, and now something else has changed too. This skill finds the cause and proves it. Fixing is a separate step, done with the `implement` skill once the cause is known.

This skill changes nothing that lasts. It may add logging, write throwaway scripts and run experiments locally, and it reverts all of it before finishing. It commits nothing. The only file it leaves behind is `investigation.md`.

## The ask rule

No assumptions. Ask the developer when the symptom is unclear, when you need access you don't have, and before any experiment that could affect something shared: writing data, restarting a service, putting load on an environment other people use. Reading code, logs, metrics and data, and experimenting on your own machine, need no permission.

A cause is never assumed either. Until it is proven it is a hypothesis, and it is called that in everything you write.

## Where the notes live

Notes go in `investigation.md`, in the same folder the other skills use for this work: `work/<key-or-slug>/` in a home repo (the current directory's `CLAUDE.md` says it is one), otherwise `.implement/<key-or-slug>/` at the root of the repo, kept out of git through `.git/info/exclude`. If the file already exists, read it and continue from there.

Update it as you go, not at the end. An investigation often outlasts a session, and what has been ruled out is the most expensive thing to lose.

## 1. Pin down the symptom

Write down, and ask for what is missing:

- **Expected and actual.** What should happen, and what happens instead. Exact error text, numbers and timings, not "it's broken" or "it's slow".
- **Where and who.** Which environment, which users, accounts or data. Everyone, or some?
- **When.** Since when, how often, at what times. Always, or sometimes?
- **What it was like before.** Did it ever work? What is the last time it is known to have worked?

Separate what someone observed from what someone concluded. "The export times out" is an observation. "The database is slow" is a conclusion, and may be wrong.

## 2. Collect evidence before theories

Look first. A theory formed early decides what you look at afterwards.

- Logs, traces and metrics around the times it happened. Compare a failing case with a working one.
- What changed near the time it started: commits, deploys, config, dependencies, data volume, traffic, infrastructure.
- The code path from the entry point down, read as it is, not as it is supposed to work.
- Earlier tickets and incidents with the same symptom.

Try to reproduce it, on the smallest setup that shows it. Note exactly what you did and what came out, also when it doesn't reproduce: that is evidence too.

Build a timeline of what is known. The differences between working and failing cases (time, user, data, version, environment) are where the cause is.

## 3. List hypotheses

Write down every explanation that fits the evidence, not only the first one. For each:

- What else would be true if this were the cause.
- What would be true if it were not.
- The cheapest test that tells the two apart.

An explanation that no test could contradict is not a hypothesis yet; sharpen it. Order the list by how likely each is and how cheap it is to test. A cheap test of an unlikely cause often goes before an expensive test of a likely one.

Post the list before testing. The developer often knows something that removes half of it.

## 4. Test one thing at a time

- Change one thing per experiment. Two changes at once tell you nothing about either.
- Say what result you expect before you run it. A result you didn't predict is information; don't explain it away.
- Record each result in `investigation.md` as **confirmed**, **ruled out** or **inconclusive**, with the output that shows it.
- When there is no good hypothesis, cut the problem in half instead of thinking harder: `git bisect` between a working and a failing version, half the input, half the components switched off.
- For something that happens only sometimes, don't run it until it happens to pass or fail. Find what differs between the runs: timing, order, shared state, data, load.

When the list runs out, go back to step 2 for more evidence rather than inventing less likely stories. If two rounds bring nothing new, stop and tell the developer where things stand and what access or information would help.

## 5. Prove it

A cause is proven when both of these hold:

- You can make the problem appear and disappear on demand by controlling that one thing.
- It explains every part of the symptom from step 1, including the when and the who. If it explains the error but not why it started last Tuesday, there is more to find.

When the problem can't be reproduced at all, the bar is evidence that shows the cause directly, such as a log line or a trace of it happening. Say that this is the basis.

A story that merely fits is not proof. If that is all there is, report it as the leading hypothesis and say what would confirm it.

## 6. Clean up and report

Revert every temporary change: logging, scripts, config, local data. Check with `git status` that the working tree is as you found it.

Finish `investigation.md` and post it in the chat:

- **Symptom:** from step 1.
- **Cause:** what it is, with `file:line` and the evidence. Or **Not found**, with the leading hypotheses and what would confirm each.
- **How to reproduce:** exact steps, or why it can't be done.
- **Ruled out:** each hypothesis that was tested and what disproved it.
- **Open questions:** what is still unexplained.
- **Next step:** a recommendation. Usually to fix it with `implement`, which starts from the reproduction as its failing test. Sometimes that the cause lies outside the code, or that it isn't worth fixing.

## 7. Get it into the tracker

Findings that live only in a chat and a local file are lost to everyone else.

- **No ticket exists for the problem:** run the `ticket-creator` skill with `investigation.md` as input. It drafts the ticket and creates it once the developer approves. Do this also when the cause wasn't found, so what was ruled out isn't investigated twice. Skip it only if the developer says no ticket is needed.
- **A ticket exists:** draft a short comment with the cause, how to reproduce it and the recommended next step, and ask before posting it.

Don't start on the fix. The developer decides what happens next.
