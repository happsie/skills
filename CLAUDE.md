# skills

A Claude Code plugin marketplace. The `happsie` plugin holds general purpose skills that take work from idea to pull request.

## Layout

- `.claude-plugin/marketplace.json`: the marketplace, lists every plugin.
- `plugins/happsie/.claude-plugin/plugin.json`: plugin name and version.
- `plugins/happsie/skills/<name>/SKILL.md`: one skill per folder, with extra files in `assets/` when needed.
- `plugins/happsie/evals/<case>/`: one eval case per folder, with `prompt.md` and `graders/*.md`. Results land in `evals/results/`, which is ignored.
- `docs/workflow.py`: generates the workflow flowchart. `docs/workflow.svg` is its output and is shown in the README.

## Keep the workflow flowchart up to date

The flowchart in the README must always match the skills. Update `docs/workflow.py` and regenerate the picture in the same change whenever:

- a skill is added, removed or renamed
- a skill starts or stops handing off to another skill
- a skill's input, output file (`spec.md`, `plan.md`, `investigation.md`, `findings.md`, an ADR) or approval step changes
- the one-line summary of a skill in the chart is no longer true

Regenerate (plain Python, no dependencies):

```
python3 docs/workflow.py
```

Never edit `docs/workflow.svg` by hand. Look at the rendered picture before finishing (`rsvg-convert docs/workflow.svg -o /tmp/workflow.png`) and check that no text overlaps or runs outside its box; positions are set by hand in the script. Keep the three starting points: an idea with no ticket, a ticket or task that goes straight to `implement` (or to `quick-fix` when the change is small), and a problem with an unknown cause. Keep the three steps after the pull request as well: `revise` for review comments and failing checks, and `retro` and `cleanup` once it is merged. Don't replace it with Mermaid.

## Writing skills

- Frontmatter needs `name` (same as the folder) and `description`. The description decides when the skill triggers, so say what it does, list the phrases a user would say, and say what it is not for.
- Skills are tracker and code host agnostic (Jira, GitHub, Linear, ...). No company-specific tools or names.
- Every skill that makes decisions has an "ask rule" section: no assumptions, and nothing is written to a tracker or pushed before the user approves.
- Refer to other skills by name in backticks, and reuse them instead of copying their rules. When a skill that others depend on changes (`refine`, `implement`, `ticket-creator`, `deliver`), read the skills that call it and fix what no longer fits.
- The spec and the plan live in one folder per piece of work. `refine` owns the rule ("Where the documents live"); the other skills name the two paths in a sentence and point to it. The same rule says that a folder named with a slug takes the ticket key once the work gets a ticket; `ticket-creator` does the rename.
- The ticket says what the spec says. `refine` owns the rule ("Bring the ticket in line"): when an approved spec differs from its ticket, the developer chooses between an update, a comment or leaving it, and `ticket-creator` writes it ("An existing ticket"). `implement` does it again when the spec changes, and `deliver` checks it one last time.
- The glossary is the agreed domain language. `refine` owns the entry format and the rules for proposing and recording terms ("The shared language"); `strategic-design`, `implement`, `quick-fix`, `deliver` and `ticket-creator` enforce it. `home-repo/assets/glossary.md` repeats the entry format for seeding, so change both together.
- ADRs keep the decisions and the reasons for them. `adr` owns what gets one, the file format and where they live ("What gets an ADR"); `strategic-design` lists them in the plan and records them once it is approved, and `refine`, `quick-fix` and `deliver` check the work against them. An ADR seeded as `Inferred` binds nothing until the developer confirms it; `refine` and `strategic-design` ask when work relies on one, and `adr` records the answer ("Confirming an inferred ADR"). `home-repo/assets/adr-template.md` repeats the template for seeding, so change both together.
- Keep the main context small. Skills hand the heavy reading and building to subagents with a clean context (`refine` for code reading, `strategic-design` for mapping the change and for the refactor, `implement` for each feature step, `investigate` for digging, `deliver` for the check), and the main thread holds the spec, the plan and the reports. `implement` owns the rule ("Keep the context small"). A subagent can't ask the user, so it returns its question to the main thread, which passes it on unanswered.
- The files carry the state, so the context can be cleared. `implement` owns the rule ("Clear the context"): the points where a clear is always offered, the signs that one is needed, what a safe point is, the prompt the developer is given to paste into the new session, and how that session finds its place from the files ("Pick up from the files"). `refine`, `strategic-design`, `investigate`, `deliver` and `revise` follow it when they run on their own. Whatever a skill gets approved in the chat, or learns that a later step needs, has to end up in a file (`plan.md` holds the scenarios, the notes from the build, the worktrees and the pull requests), or a clear loses it.
- Code is written in one git worktree per piece of work, shared by every step, so the developer's checkout is left alone. `implement` owns the rule ("Work in a worktree"); `strategic-design`, `quick-fix` and `deliver` follow it. Not one worktree per subagent: the steps run in order on one branch. Nothing is written in the checkout, and that includes a glossary that is a tracked file in the repo. `investigate` experiments in a throwaway worktree of its own, at the commit the problem shows on, and removes it when it is done. The work's worktrees and branches are removed by `cleanup` once the work is merged or dropped, never by the skills before it. `cleanup` keeps the work's folder, since `retro` reads it.
- `quick-fix` is the short path for a small, local change. It drops the question rounds, the plan and the subagents, and keeps every standard: the ask rule, the glossary, the ADRs, test first, the coding standards, the worktree, the findings log and the checks in `deliver`. It owns the list of what counts as a quick fix ("What counts as a quick fix") and hands over to `implement` when a point on it fails. A standard added to `implement` belongs in `quick-fix` too.
- `deliver` owns the two independent checks (the spec check and the code review, each in its own fresh subagent) and the description of the change the developer approves the code from ("Describe the change"). `implement`, `quick-fix` and `revise` run `deliver` instead of checking the work themselves.
- The non-functional requirements (security, performance, failure, observability, rollout and rollback, dependencies) are cross-checked in `refine`, which owns the list (its step 3) and the spec section. `strategic-design` puts them in the plan's steps, `quick-fix` requires every one to be "no change" and says so in its short spec, and `deliver` checks them.
- The rules don't end at the pull request. `revise` handles review comments and failing checks: it sorts them with the developer, makes the fixes under the rules of the skill that built the work (`implement` or `quick-fix`) and sends the result back through `deliver`. Work that changes several repos has one pull request per repo, and `deliver`, `revise`, `retro` and `cleanup` handle them as a set.
- `findings.md` is the log of what went wrong in a piece of work. `retro` owns the format and who writes to it ("The findings log"); `deliver`, `implement`, `quick-fix` and `revise` append to it. `retro` turns it into lessons and puts each one where it is enforced: a check a machine runs, the coding standards, the glossary (through `refine`'s rules), an ADR (through `adr`) or the repo's agent instructions.
- Write in plain, direct English and explain why a rule exists. Match the tone of the existing skills.

## Before finishing a change

- Run `claude plugin validate .`.
- When a ticket skill changed, run its evals, on Sonnet and never on Fable. `--ablation none` makes the "skill fired" graders count, and `--no-publish` keeps the report local:

  ```
  claude plugin eval plugins/happsie --model sonnet --ablation none --no-publish
  ```

  The runs have no tracker, so the evals check routing, the template and that the reply stops for approval. They can't catch a real create call. A failure worth fixing in a skill gets a case here.
- Bump `version` in `plugins/happsie/.claude-plugin/plugin.json` when a skill is added or its behavior changes. Installed plugins only update when the version changes.
- Update the README if install steps, layout or the workflow changed.
