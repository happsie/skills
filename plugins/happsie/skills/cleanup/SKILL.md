---
name: cleanup
description: Remove what a finished piece of work left behind on the developer's machine, which is the git worktrees it was built in and its local branches. Checks first that every pull request is merged, or that the developer says the work is dropped, shows anything that would be lost, and removes nothing before the developer has approved the list. Keeps the work's folder with the spec, the plan and the findings. Use when the user says "clean up", "clean up PROJ-123", "remove the worktrees", "delete the old branches", "this is merged, tidy up", "we dropped this one", "what work is still lying around", or when a pull request built with implement or quick-fix has been merged. Works on one piece of work, or on every finished one. Not for learning from the work (retro), not for work that is still in review (revise), and not for tidying code.
---

# Cleanup

A piece of work leaves things behind on the developer's machine: a worktree per repo with its installed dependencies, a local branch, copied files such as an `.env`, and the work's folder. No other skill removes them, because each one still needs them: review comments are fixed in the worktree, and the lessons are read from the folder. Left alone, that becomes gigabytes of worktrees and a branch list nobody can read.

This skill removes the worktrees and the branches once the work is finished. It changes no code and it keeps the documents.

## The ask rule

No assumptions. Nothing is removed before the developer has approved the list of what goes, and nothing that holds work that exists nowhere else is removed without it being shown first. Whether the work is finished is checked, not taken on trust. Reading the work's folder, the repos and the pull requests needs no permission.

Never use `--force`, `git branch -D` or a deletion on the remote to get past something. Each of those is a question.

## 1. Find the work

- **One piece of work.** Its folder is `work/<key-or-slug>/` in a home repo, otherwise `.implement/<key-or-slug>/` at the root of the repo (`refine`, "Where the documents live").
- **No work named.** List every work folder, and say for each one whether its pull requests are merged, open or missing. Propose the finished ones, and leave the rest alone.

For each piece of work, collect:

- The worktrees: the paths under the Worktrees heading in `plan.md`, or in `spec.md` for a quick fix, and anything else under the folder's `worktrees/`. Compare with `git worktree list` in each repo.
- The branches those worktrees are on.
- The pull requests: the Pull requests heading `deliver` wrote in `plan.md` or `spec.md`. If it is missing, look the branch up on the code host.

## 2. Check that it is finished

Work is finished when every pull request is merged, or when the developer says it is dropped. Check each pull request on the code host with whatever is available: `gh`, `glab`, a code host MCP server. If the code host can't be reached, say so and ask.

If a pull request is still open, leave everything for that work as it is and say so. Review comments get fixed in that worktree.

Work with no pull request is either not delivered yet or dropped. Don't decide which. Ask.

## 3. Look for what would be lost

For each worktree:

- Uncommitted changes (`git status --short`), and ignored files that are not build output or installed dependencies.
- Commits the pull request doesn't have: compare the branch's head with the pull request's head commit on the code host. For dropped work, commits that are on no remote.

Either one is work that exists nowhere else. Show it and ask what to do with it.

## 4. Propose and get approval

Post what you will remove and what you will keep, and wait for an explicit approval:

- **Worktrees:** each path, removed with `git worktree remove <path>`, then `git worktree prune`. Files that were copied in when the worktree was set up go with it.
- **Local branches:** each one, deleted with `git branch -d`. That refuses a branch git doesn't see as merged, which is what a squash or a rebase merge looks like. Then show that the pull request is merged and ask before `git branch -D`. The branch of dropped work is not merged at all: ask whether to delete it or keep it.
- **Remote branches:** only when they are still there and the developer asks. Most code hosts delete them on merge, and a dropped branch may be someone else's starting point.
- **The work's folder:** kept. `spec.md`, `plan.md`, `investigation.md` and `findings.md` are small, and the `retro` skill reads them, also later and across several pieces of work. Remove it only if the developer asks.

Two kinds of worktree are not the work's own:

- One the `retro` skill made for lessons (`<repo_name>-retro`) belongs to a pull request of its own. Remove it when that one is merged, and leave it until then.
- One left by an investigation that was never finished (`<repo_name>-investigate`) holds only experiments. List it and ask.

If `findings.md` has no Retro section, say that no retro has been run on this work. It can still be run afterwards, since it reads the folder and not the worktree.

## 5. Remove

Remove what was approved, in the order above. If a command refuses, stop and show what it said. Don't reach for a stronger one.

Then note the date beside each path under Worktrees in `plan.md` or `spec.md`, so a later session doesn't look for a worktree that is gone. That leaves the file's status as it is.

## Report

- What was removed: each worktree and each branch.
- What was kept and why: the folder, an open pull request, anything the developer chose to keep.
- Work that was left alone because it isn't finished.
