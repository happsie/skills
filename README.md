# skills

Skills library for Claude Code, packaged as a plugin marketplace.

## Install

```
/plugin marketplace add happsie/skills
/plugin install happsie@happsie-skills
```

Update later with `/plugin marketplace update happsie-skills`.

## Workflow

How the skills fit together. `implement` runs `refine`, `strategic-design`, the build and `deliver` in order, and each of them also works on its own.

![Workflow flowchart](docs/workflow.svg)

## Add a skill

Skills live in `plugins/happsie/skills/`. Create `plugins/happsie/skills/<name>/SKILL.md` with `name` and `description` frontmatter. It shows up as `happsie:<name>`. Add it to `docs/workflow.dot` and regenerate the flowchart (see `CLAUDE.md`).

## Add a plugin

Create `plugins/<plugin>/.claude-plugin/plugin.json` and list it in `.claude-plugin/marketplace.json`.

## Develop locally

```
claude plugin validate .
/plugin marketplace add /path/to/this/repo
```
