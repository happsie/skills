# skills

A Claude Code plugin marketplace. The `happsie` plugin holds general purpose skills that take work from idea to pull request.

## Layout

- `.claude-plugin/marketplace.json`: the marketplace, lists every plugin.
- `plugins/happsie/.claude-plugin/plugin.json`: plugin name and version.
- `plugins/happsie/skills/<name>/SKILL.md`: one skill per folder, with extra files in `assets/` when needed.
- `docs/workflow.dot`: source of the workflow flowchart. `docs/workflow.svg` is generated from it and shown in the README.

## Keep the workflow flowchart up to date

The flowchart in the README must always match the skills. Update `docs/workflow.dot` and regenerate the picture in the same change whenever:

- a skill is added, removed or renamed
- a skill starts or stops handing off to another skill
- a skill's input, output file (`brief.md`, `plan.md`, `investigation.md`) or approval step changes
- the one-line summary of a skill in the chart is no longer true

Regenerate with Graphviz (`brew install graphviz`):

```
dot -Tsvg docs/workflow.dot -o docs/workflow.svg
```

Never edit `docs/workflow.svg` by hand. Look at the rendered picture before finishing, and check that labels don't overlap. Don't replace it with Mermaid.

## Writing skills

- Frontmatter needs `name` (same as the folder) and `description`. The description decides when the skill triggers, so say what it does, list the phrases a user would say, and say what it is not for.
- Skills are tracker and code host agnostic (Jira, GitHub, Linear, ...). No company-specific tools or names.
- Every skill that makes decisions has an "ask rule" section: no assumptions, and nothing is written to a tracker or pushed before the user approves.
- Refer to other skills by name in backticks, and reuse them instead of copying their rules. When a skill that others depend on changes (`refine`, `ticket-creator`, `deliver`), read the skills that call it and fix what no longer fits.
- Write in plain, direct English and explain why a rule exists. Match the tone of the existing skills.

## Before finishing a change

- Run `claude plugin validate .`.
- Bump `version` in `plugins/happsie/.claude-plugin/plugin.json` when a skill is added or its behavior changes. Installed plugins only update when the version changes.
- Update the README if install steps, layout or the workflow changed.
