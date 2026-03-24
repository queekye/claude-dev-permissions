# claude-dev-permissions

A Claude Code plugin that provides quick-setup permission levels for development workflows.

## Install

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/claude-dev-permissions.git ~/.claude/plugins/claude-dev-permissions

# Or install via Claude Code
/install-plugin ~/.claude/plugins/claude-dev-permissions
```

## Usage

```
/setup-permissions              # Interactive: shows comparison table, asks you to choose
/setup-permissions readonly     # Level 1: read-only browsing
/setup-permissions localdev     # Level 2: local development (recommended)
/setup-permissions fulldev      # Level 3: full development with remote ops
```

## Permission Levels

| Capability | readonly | localdev | fulldev |
|---|:---:|:---:|:---:|
| git read (status/log/diff) | auto | auto | auto |
| git local write (add/commit/merge) | confirm | **auto** | auto |
| git remote (push/pull/fetch) | confirm | confirm | **auto** |
| Build tools (uv/npm/make/cargo) | confirm | **auto** | auto |
| Test runners (pytest) | confirm | **auto** | auto |
| File ops (mkdir/cp/mv) | confirm | **auto** | auto |
| Docker/SSH | confirm | confirm | **auto** |
| Destructive ops (rm/reset --hard) | confirm | confirm | confirm |

**Destructive operations always require confirmation**, regardless of level.

## How it works

The command writes permission rules to your project's `.claude/settings.json`. Existing non-permission settings (like `enabledPlugins`) are preserved.
