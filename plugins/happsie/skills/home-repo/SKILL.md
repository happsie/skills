---
name: home-repo
description: Set up or extend a home repo - a personal local repo a developer works from across many repos. It holds a CLAUDE.md index of the other repos (paths, purpose, where their docs live), shared cross-repo glossary, ADRs and coding standards, and a repos/<repo> folder with seeded docs for repos that lack their own. Use when the user asks to "set up a home repo", "create a home repo", "init my home repo", "add a repo to the home repo", or wants one place to work from across several repos without changing directory.
---

# Home repo

A home repo is a personal, local repo the developer sits in while working across many other repos. It never contains the other repos' code. It contains:

- `CLAUDE.md`: an index of the other repos (absolute paths, purpose, where their docs live) and the rules for working across them.
- `docs/glossary.md`, `docs/adr/`, `docs/coding-standards.md`: shared docs, only for things that span two or more repos.
- `repos/<repo_name>/`: glossary, ADRs and coding standards for repos that do not have their own. Other teams work in those repos with their own conventions, so we keep these docs here instead of adding files to their repos.
- `work/<key-or-slug>/`: the brief and plan for each piece of work done from here, written by the `refine`, `strategic-design` and `implement` skills.
- `.claude/settings.json`: the repos listed as additional directories, so Claude can read and edit them from here.

Repo-level docs always win. If a repo has its own glossary, ADRs or coding standards, those are used and written to. `repos/<repo_name>/` only fills the gaps, per doc type. The home `docs/` folder is never a place for single-repo content.

The skill is safe to re-run. Use the same steps to add repos later.

## 1. Collect inputs

- **Home directory.** Default is the current directory. It must not be inside one of the repos it indexes. If the current directory is itself a code repo, stop and ask where the home repo should live.
- **Repos.** Use the paths the user gave. If they gave none, ask. If they point at a parent folder, list the git repos directly under it and let them pick.

Resolve every repo to an absolute path. The repo name is the directory basename; if two collide, ask for a name.

On a re-run, read the existing `CLAUDE.md` index first and treat repos already listed as known.

## 2. Scan each repo

Read only; never write to the indexed repos. With more than three repos, scan them in parallel with subagents, one per repo, each returning the facts below.

For each repo find:

- **Purpose and stack**: README, build files (`pom.xml`, `build.gradle*`, `go.mod`, `package.json`, ...), top-level layout.
- **Agent instructions**: `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.cursor/rules`, `.github/copilot-instructions.md`.
- **Glossary**: `GLOSSARY.md`, `docs/glossary*`, `doc/glossary*`, a glossary or ubiquitous-language section in the README or docs.
- **ADRs**: `docs/adr`, `doc/adr`, `adr`, `docs/decisions`, `docs/architecture/decisions`, any folder of numbered decision files.
- **Coding standards**: `CONTRIBUTING.md`, `docs/coding-standards*`, `docs/conventions*`, `STYLEGUIDE*`, or a substantial conventions section in `CLAUDE.md`/`AGENTS.md`.

Linter and formatter config alone does not count as coding standards, but it is input for seeding them.

Record for each of the three doc types either the path inside the repo, or "missing".

## 3. Scaffold the home repo

Create what is missing. Never overwrite existing content; merge into it.

- `CLAUDE.md` from `assets/home-claude-template.md`. Fill in one index row and one detail section per repo. On a re-run, only add or update the rows for new or changed repos and leave the user's edits alone.
- `docs/glossary.md`, `docs/coding-standards.md`, `docs/adr/README.md` (from `assets/adr-README.md`) and `docs/adr/0000-template.md` (from `assets/adr-template.md`) from `assets/`. These start empty apart from the header. Do not invent cross-repo content. Only add an entry if the scan found something that clearly spans repos (the same term used in several repos, a shared protocol), and say so in the summary.
- `.claude/settings.json` with every repo path in `permissions.additionalDirectories`. Merge with existing settings.
- `git init` if the home directory is not a git repo, so the docs have history. Do not commit unless asked.

## 4. Seed `repos/<repo_name>/`

For each repo, for each doc type marked missing, write a seeded draft:

- `repos/<repo_name>/glossary.md`: domain terms from entity and type names, package names, API resources, README. Term, one-line meaning, where it appears. Skip generic technical words.
- `repos/<repo_name>/coding-standards.md`: what the code actually does. Language and framework versions, formatter and linter config, package layout, naming, error handling, test layers and naming, build and test commands. State observed conventions, not general best practice.
- `repos/<repo_name>/adr/NNNN-<slug>.md`: one file per significant decision that is visible in the code (framework, persistence, messaging, API style, module structure), using `assets/adr-template.md` with status `Inferred`. Three to six is normal. The context section should say what the code shows; do not make up the original reasoning.

Start every seeded file with:

```
> Inferred from the code on <YYYY-MM-DD>. Not verified by the owning team.
```

Do not create a `repos/` file for a doc type the repo already has. If a doc type has nothing worth writing, skip the file and note it in the summary instead of writing filler.

On a re-run, if a repo now has its own version of a doc that also exists in `repos/<repo_name>/`, do not delete the `repos/` copy. Update the index to point at the repo's own doc and tell the user which `repos/` files are now superseded, so they can move anything useful across.

## 5. Report

Summarise briefly: repos indexed, which docs each repo has itself versus in `repos/`, anything superseded, and anything that needs the user's attention. Remind them to restart Claude Code in the home repo and accept the workspace trust dialog; `additionalDirectories` is ignored until the home repo is trusted.
