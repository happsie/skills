# skills

A Claude Code plugin marketplace. The `happsie` plugin holds general purpose skills that take work from idea to pull request.

## Layout

- `.claude-plugin/marketplace.json`: the marketplace, lists every plugin.
- `plugins/happsie/.claude-plugin/plugin.json`: plugin name and version.
- `plugins/happsie/skills/<name>/SKILL.md`: one skill per folder, with extra files in `assets/` when needed.
- `docs/workflow.py`: generates the workflow flowchart. `docs/workflow.svg` is its output and is shown in the README.

## Keep the workflow flowchart up to date

The flowchart in the README must always match the skills. Update `docs/workflow.py` and regenerate the picture in the same change whenever:

- a skill is added, removed or renamed
- a skill starts or stops handing off to another skill
- a skill's input, output file (`spec.md`, `plan.md`, `investigation.md`) or approval step changes
- the one-line summary of a skill in the chart is no longer true

Regenerate (plain Python, no dependencies):

```
python3 docs/workflow.py
```

Never edit `docs/workflow.svg` by hand. Look at the rendered picture before finishing (`rsvg-convert docs/workflow.svg -o /tmp/workflow.png`) and check that no text overlaps or runs outside its box; positions are set by hand in the script. Keep the three starting points: an idea with no ticket, a ticket or task that goes straight to `implement`, and a problem with an unknown cause. Don't replace it with Mermaid.

## Writing skills

- Frontmatter needs `name` (same as the folder) and `description`. The description decides when the skill triggers, so say what it does, list the phrases a user would say, and say what it is not for.
- Skills are tracker and code host agnostic (Jira, GitHub, Linear, ...). No company-specific tools or names.
- Every skill that makes decisions has an "ask rule" section: no assumptions, and nothing is written to a tracker or pushed before the user approves.
- Refer to other skills by name in backticks, and reuse them instead of copying their rules. When a skill that others depend on changes (`refine`, `ticket-creator`, `deliver`), read the skills that call it and fix what no longer fits.
- The glossary is the agreed domain language. `refine` owns the entry format and the rules for proposing and recording terms ("The shared language"); `strategic-design`, `implement`, `deliver` and `ticket-creator` enforce it. `home-repo/assets/glossary.md` repeats the entry format for seeding, so change both together.
- Keep the main context small. Skills hand the heavy reading and building to subagents with a clean context (`refine` for code reading, `strategic-design` for mapping the change and for the refactor, `implement` for each feature step, `investigate` for digging, `deliver` for the check), and the main thread holds the spec, the plan and the reports. `implement` owns the rule ("Keep the context small"). A subagent can't ask the user, so it returns its question to the main thread, which passes it on unanswered.
- Write in plain, direct English and explain why a rule exists. Match the tone of the existing skills.

## Before finishing a change

- Run `claude plugin validate .`.
- Bump `version` in `plugins/happsie/.claude-plugin/plugin.json` when a skill is added or its behavior changes. Installed plugins only update when the version changes.
- Update the README if install steps, layout or the workflow changed.
