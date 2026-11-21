# Home repo

This is a home repo. It contains no product code. Work from here across the repos listed below; do not ask the user to change directory.

## Repos

| Repo | Path | Purpose | Stack |
|------|------|---------|-------|
| <name> | <absolute path> | <one line> | <stack> |

### <name>

- Path: `<absolute path>`
- Agent instructions: `<path to CLAUDE.md / AGENTS.md, or "none">`
- Glossary: `<path in repo, or repos/<name>/glossary.md>`
- ADRs: `<path in repo, or repos/<name>/adr/>`
- Coding standards: `<path in repo, or repos/<name>/coding-standards.md>`
- Build and test: `<commands>`
- Talks to: <other repos in this index it calls or depends on, and how>

## Working in a repo from here

- Before touching a repo, read its agent instructions and its coding standards from the paths above. They are not loaded automatically from here.
- Use absolute paths and `git -C <path>`. Do not `cd` into repos.
- Each repo has its own branches, commits and PRs. A cross-repo change is one branch per repo with the same name.
- Follow the target repo's conventions, not this repo's.

## Where knowledge lives

Lookup order for a term, decision or convention:

1. The repo's own docs.
2. `repos/<repo>/` in this repo, for doc types the repo does not have.
3. `docs/` in this repo, for things that span repos.

Where to write something new:

- It concerns one repo and that repo has the doc type: write it in the repo.
- It concerns one repo and that repo lacks the doc type: write it in `repos/<repo>/`. Do not add glossary, ADR or standards files to a repo that has none; other teams own those repos.
- It spans two or more repos: write it in `docs/` here. Shared terms go in `docs/glossary.md`, cross-repo decisions in `docs/adr/`, shared conventions in `docs/coding-standards.md`.

Never copy single-repo content into `docs/`. If a repo-level doc and a shared doc disagree, the repo-level doc wins for that repo; flag the conflict.

Files in `repos/` marked "Inferred" were generated from code. Treat them as a good guess and correct them when you learn better.

## Work in progress

Briefs and plans for work done from here live in `work/<ticket-key-or-slug>/` as `brief.md` and `plan.md`, also when the code changes land in other repos. The `refine`, `strategic-design` and `implement` skills write and read them there.

## Adding a repo

Run the `home-repo` skill again with the new repo path.
