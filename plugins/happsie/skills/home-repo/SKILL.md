---
name: home-repo
description: Set up or extend a home repo - a personal local repo a developer works from across many repos. It holds a CLAUDE.md index of the other repos (paths, purpose, where their docs live), glossaries that hold the agreed domain terms and rules, shared ADRs and coding standards, and a repos/<repo> folder with seeded docs for repos that lack their own. Use when the user asks to "set up a home repo", "create a home repo", "init my home repo", "add a repo to the home repo", or wants one place to work from across several repos without changing directory. Not for work inside a single repo, and not for adding terms or decisions once it is set up (refine and adr do that).
---

# Home repo

A home repo is a personal, local repo the developer sits in while working across many other repos. It never contains the other repos' code. It contains:

- `CLAUDE.md`: an index of the other repos (absolute paths, purpose, where their docs live) and the rules for working across them.
- `docs/glossary.md`, `docs/adr/`, `docs/coding-standards.md`: shared docs, only for things that span two or more repos.
- `repos/<repo_name>/`: glossary, ADRs and coding standards for repos that do not have their own. Other teams work in those repos with their own conventions, so we keep these docs here instead of adding files to their repos.
- `work/<key-or-slug>/`: the spec and plan for each piece of work done from here, written by the `refine`, `strategic-design`, `implement` and `quick-fix` skills, and the git worktrees the code for that work is written in.
- `.claude/settings.json`: the repos listed as additional directories, so Claude can read and edit them from here.

The glossaries are the agreed domain language for the work done from here. The `refine` skill describes what an entry holds (term, meaning, other names, rules, context, status) and keeps them up to date as work is refined; this skill only sets them up and seeds them.

The same goes for ADRs. The `adr` skill says what gets one, what the file looks like and how one supersedes another, and writes them as decisions are made; this skill sets up the folders and seeds inferred ones.

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
- `docs/glossary.md`, `docs/coding-standards.md`, `docs/adr/README.md` (from `assets/adr-README.md`) and `docs/adr/0000-template.md` (from `assets/adr-template.md`) from `assets/`. These start empty apart from the header. Do not invent cross-repo content. Only add an entry if the scan found something that clearly spans repos (the same term used with the same meaning in several repos, a shared protocol), and say so in the summary. A word that two repos use for different things is not a shared term. Each repo's glossary keeps its own meaning, and the shared glossary gets one entry that says how the meanings differ and how one maps to the other where the repos talk.
- `.claude/settings.json` with every repo path in `permissions.additionalDirectories`. Merge with existing settings.
- `git init` if the home directory is not a git repo, so the docs have history. Do not commit unless asked.

## 4. Seed `repos/<repo_name>/`

For each repo, for each doc type marked missing, write a seeded draft:

- `repos/<repo_name>/glossary.md`, from `assets/glossary.md`: domain terms from entity and type names, package names, API resources, README. One entry per term in the format the asset shows, every one with status `inferred`. When the code has several names for one thing, pick the most used as the term and list the rest under "Also called". Write a rule only where the code enforces it (a validation, a constraint, a state check), and state what the code does. Skip generic technical words.
- `repos/<repo_name>/coding-standards.md`: what the code actually does. Language and framework versions, formatter and linter config, package layout, naming, error handling, test layers and naming, build and test commands. State observed conventions, not general best practice.
- `repos/<repo_name>/adr/NNNN-<slug>.md`: one file per significant decision that is visible in the code (framework, persistence, messaging, API style, module structure), using `assets/adr-template.md` with status `Inferred`. Three to six is normal. The context section should say what the code shows; do not make up the original reasoning, and leave out the Alternatives section, since the code doesn't show what was turned down.

Start every seeded coding standards and ADR file with:

```
> Inferred from the code on <YYYY-MM-DD>. Not verified by the owning team.
```

The glossary has no such banner. Its entries are agreed one at a time, so each carries its own status.

Do not create a `repos/` file for a doc type the repo already has. If a doc type has nothing worth writing, skip the file and note it in the summary instead of writing filler.

On a re-run, if a repo now has its own version of a doc that also exists in `repos/<repo_name>/`, do not delete the `repos/` copy. Update the index to point at the repo's own doc and tell the user which `repos/` files are now superseded, so they can move anything useful across.

## 5. Report

Summarise briefly: repos indexed, which docs each repo has itself versus in `repos/`, anything superseded, and anything that needs the user's attention. Remind them to restart Claude Code in the home repo and accept the workspace trust dialog; `additionalDirectories` is ignored until the home repo is trusted.
