---
description: Configure Bash permission levels for development workflows
argument-hint: [level]
---

Configure Bash tool permissions in the project's `.claude/settings.json` based on the user's chosen security level. This command helps quickly set up permissions on a new machine.

## Permission Levels

### Level 1 - readonly (只读浏览)

Suitable for: code review, reading code, browsing repos. No modifications allowed.

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git show:*)",
      "Bash(git branch --list:*)",
      "Bash(git branch -a:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(ls:*)",
      "Bash(wc:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(which:*)",
      "Bash(echo:*)"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

### Level 2 - localdev (本地开发)

Suitable for: daily development, refactoring, testing. All git operations are local-only (no push). This is the recommended level for most development workflows.

Includes everything in Level 1, plus:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git show:*)",
      "Bash(git branch:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git checkout:*)",
      "Bash(git switch:*)",
      "Bash(git merge:*)",
      "Bash(git rebase:*)",
      "Bash(git stash:*)",
      "Bash(git worktree:*)",
      "Bash(git tag:*)",
      "Bash(cd:*)",
      "Bash(mkdir:*)",
      "Bash(cp:*)",
      "Bash(mv:*)",
      "Bash(touch:*)",
      "Bash(chmod:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(ls:*)",
      "Bash(wc:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(which:*)",
      "Bash(echo:*)",
      "Bash(uv:*)",
      "Bash(pip:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(pytest:*)",
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(node:*)",
      "Bash(cargo:*)",
      "Bash(make:*)",
      "Bash(cmake:*)",
      "Bash(go:*)",
      "Bash(rustc:*)",
      "Bash(gcc:*)",
      "Bash(g++:*)",
      "Bash(javac:*)",
      "Bash(java:*)",
      "Bash(sort:*)",
      "Bash(uniq:*)",
      "Bash(sed:*)",
      "Bash(awk:*)",
      "Bash(cut:*)",
      "Bash(tr:*)",
      "Bash(tee:*)",
      "Bash(diff:*)",
      "Bash(tar:*)",
      "Bash(unzip:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(jq:*)"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

### Level 3 - fulldev (完整开发)

Suitable for: trusted environments, CI/CD integration, full autonomy. Includes remote git operations and broader system access. Use with caution.

Includes everything in Level 2, plus remote git and broader tools:

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(gh:*)",
      "Bash(cd:*)",
      "Bash(mkdir:*)",
      "Bash(cp:*)",
      "Bash(mv:*)",
      "Bash(touch:*)",
      "Bash(chmod:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(ls:*)",
      "Bash(wc:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(which:*)",
      "Bash(echo:*)",
      "Bash(uv:*)",
      "Bash(pip:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(pytest:*)",
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(node:*)",
      "Bash(cargo:*)",
      "Bash(make:*)",
      "Bash(cmake:*)",
      "Bash(go:*)",
      "Bash(rustc:*)",
      "Bash(gcc:*)",
      "Bash(g++:*)",
      "Bash(javac:*)",
      "Bash(java:*)",
      "Bash(sort:*)",
      "Bash(uniq:*)",
      "Bash(sed:*)",
      "Bash(awk:*)",
      "Bash(cut:*)",
      "Bash(tr:*)",
      "Bash(tee:*)",
      "Bash(diff:*)",
      "Bash(tar:*)",
      "Bash(unzip:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(jq:*)",
      "Bash(docker:*)",
      "Bash(docker-compose:*)",
      "Bash(kubectl:*)",
      "Bash(ssh:*)",
      "Bash(scp:*)",
      "Bash(rsync:*)",
      "WebSearch",
      "WebFetch"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

## Behavior

1. If the user provides a level argument (e.g., `/setup-permissions localdev`), apply that level directly.
2. If no argument, present the three levels with a brief comparison table and ask the user to choose.
3. After the user chooses, write the permissions to the **project-level** settings file at `.claude/settings.json` in the current working directory.
4. Preserve any existing non-permission settings (like `enabledPlugins`) in the file.
5. Show a summary of what was configured and what commands are now auto-allowed vs still require confirmation.

## Comparison Table (for display when no argument given)

| Capability | Level 1 (readonly) | Level 2 (localdev) | Level 3 (fulldev) |
|---|:---:|:---:|:---:|
| git read (status/log/diff) | auto | auto | auto |
| git local write (add/commit/merge) | confirm | auto | auto |
| git remote (push/pull/fetch) | confirm | confirm | auto |
| git destructive (reset --hard, -D) | confirm | confirm | confirm |
| Build tools (uv/npm/make/cargo) | confirm | auto | auto |
| Test runners (pytest/jest) | confirm | auto | auto |
| File operations (mkdir/cp/mv) | confirm | auto | auto |
| Docker/K8s | confirm | confirm | auto |
| SSH/SCP | confirm | confirm | auto |
| rm -rf / dangerous ops | confirm | confirm | confirm |

Note: `confirm` means the user will be prompted. `auto` means auto-allowed. Destructive operations like `rm -rf`, `git reset --hard`, `git push --force` always require confirmation regardless of level — they are intentionally excluded from all levels.

## Important

- Never add `rm` to any auto-allow list
- Never add `git reset --hard` or `git push --force` to auto-allow
- Never add `git branch -D` (force delete) — only `git branch -d` (safe delete) is allowed in Level 2+
- Level 3 uses `Bash(git:*)` which covers all git commands including push, but destructive flags still get caught by Claude's built-in safety checks
