# claude-dev-permissions

Explicit, reviewable permission profiles for Claude Code projects. These are
workflow defaults, not a sandbox or a guarantee about arbitrary shell code.

## Load the plugin

Install Python 3.8+ and Claude Code, then load the local plugin folder:

```bash
git clone https://github.com/queekye/claude-dev-permissions.git
claude --plugin-dir ./claude-dev-permissions
```

In that session, run `/dev-permissions:setup-permissions readonly`, `localdev`,
or `fulldev`. Without an argument, the command asks which profile to apply.
Local folder loading is documented in [Claude Code plugins](https://code.claude.com/docs/en/plugins).
No marketplace or account credential is bundled with this project.

You can apply a profile directly without invoking an AI:

```bash
# From the project to configure, replace the script path.
python /path/to/claude-dev-permissions/scripts/configure_permissions.py readonly --project .
# The first command previews only. Add --apply to write settings.
python /path/to/claude-dev-permissions/scripts/configure_permissions.py readonly --project . --apply
```

## Profiles

| Capability | readonly | localdev | fulldev |
|---|---|---|---|
| Native review (Read/Grep/Glob) | allowed | allowed | allowed |
| Native file edits | denied | allowed in project paths | allowed in project paths |
| Bash | denied | selected commands | selected commands |
| Git add/commit; trusted tests/build scripts | denied | allowed | allowed |
| Git fetch/pull | denied | ask | allowed |
| Git push; reset/clean/rebase/checkout/branch/tag/worktree/config/remote | denied | ask | ask |
| Python/shell interpreters, Docker, SSH and arbitrary commands | denied | no blanket allow | no blanket allow |
| Starting permission mode | dontAsk | default (manual) | default (manual) |

The JSON files in `profiles/` are authoritative. `readonly` disables Bash
completely; shell commands described as read-only can invoke helpers or write
files. Development profiles require trusted repositories: tests, package
scripts and git hooks can run arbitrary code, write data, or contact a network.
`localdev` does not enforce offline operation.

Ask rules take priority over allow rules for matching conventional command
text. There is no broad git, interpreter, or shell allow. This cannot guarantee
a prompt for every destructive action: an allowed script can perform one
internally, and `git -C ... push`, aliases, full paths, or custom wrappers differ
from `git push ...`. For filesystem/network enforcement use
[Claude Code sandboxing](https://code.claude.com/docs/en/sandboxing) or an isolated
container. Review [Claude Code permissions](https://code.claude.com/docs/en/permissions)
for rule syntax, priority and the limitations of command matching.

## Existing settings and scope

The script replaces the entire project `permissions` object, including old
broad allow rules and `additionalDirectories`; other top-level settings are
preserved. Malformed JSON or a symlinked destination is rejected without
overwriting it; Windows junction/reparse destinations are also rejected.
It previews unless `--apply` is present. It does not back up or
commit configuration; make a private backup if previous permissions are needed.

Review `/permissions` after applying a profile. Other settings, current mode,
hooks, mods and MCP tools can change effective behavior; this project does not
remove or audit them. Project allow rules require workspace trust. Restart if
needed to use the new default mode. Do not enable bypass mode or grant another
execution tool and assume readonly still fences the whole environment. Managed
restrictions may block an intended allow. Global and local user settings are
not modified by the script.

After applying readonly, Claude cannot run the configuration script through
Bash to switch profiles. Run it yourself in a terminal, or change settings
through Claude Code's permission UI; the plugin must not work around its deny
rules to change them.

## Verification

```bash
python -m unittest discover -s tests -v
```

Tests cover profile invariants, permission replacement, setting preservation,
dry runs, invalid input and unsafe destinations. They do not exercise an
authenticated Claude session or reimplement its shell parser. See
[HANDOFF.md](HANDOFF.md) for current state and next checks.

MIT license for this repository's code and documentation. Claude Code is a
separate product; documentation links do not imply endorsement.
