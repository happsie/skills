# Home repo

This is a home repo. It contains no product code of its own. Work from here across the repos listed below; do not ask the user to change directory.

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

## Language

The glossaries are the agreed domain language. Read the entries for the area before writing a spec, a ticket or code.

- Use the glossary's term for a thing, in specs, tickets, code and tests. A word listed under "Also called" is not used in new work.
- The rules on an entry are agreements. Work that would break one stops until the developer says whether the work or the rule changes.
- Entries with status `agreed` were approved by a person. `inferred` ones were read out of the code: confirm the ones your work relies on.
- A term means one thing within a repo. When two repos use the same word differently, each keeps its own entry, and `docs/glossary.md` says how the two map to each other.
- New terms and rules are proposed to the developer, never just written down. The `refine` skill does this and updates the glossary once the spec is approved.

## Decisions

The ADRs record decisions and why they were made. Read the ones for the area before designing a change.

- An ADR with status `Accepted` holds. Work that would go against one stops until the developer says whether the work changes or the ADR is superseded.
- `Inferred` ones were read out of the code and nobody has confirmed the reasoning.
- New decisions are proposed to the developer, never just written down. The `strategic-design` skill lists them in the plan, and the `adr` skill writes them once approved.
- An accepted ADR is never rewritten. A new one supersedes it.

## Work in progress

Specs and plans for work done from here live in `work/<ticket-key-or-slug>/` as `spec.md` and `plan.md`, also when the code changes land in other repos. The `refine`, `strategic-design`, `implement` and `quick-fix` skills write and read them there.

The code for each piece of work is written in git worktrees of the repos it changes, in `work/<ticket-key-or-slug>/worktrees/<repo>/`, so the repos' own checkouts are left alone. They are kept out of this repo's git through `.git/info/exclude`.

## Adding a repo

Run the `home-repo` skill again with the new repo path.
