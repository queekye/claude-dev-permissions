---
description: Apply explicit project permission profiles with a preview
argument-hint: [readonly|localdev|fulldev]
---

Configure `.claude/settings.json` using checked-in profiles and the deterministic
script. Do not invent or merge additional permission rules.

1. Read `${CLAUDE_PLUGIN_ROOT}/README.md` for the profiles and limitations.
2. If `$ARGUMENTS` is empty, show the profile table and ask the user to choose.
   Never choose fulldev automatically. Accept only readonly/localdev/fulldev;
   reject any other argument.
3. Preview with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure_permissions.py" PROFILE --project .`.
   Use `python` instead when that is the available Python 3 interpreter.
4. If the user requested that profile, apply the same command plus `--apply`.
   This replaces the whole project permissions object and preserves other
   top-level settings. Do not change global or settings.local.json files.
5. Report profile/target path, ask the user to inspect `/permissions`, and
   explain that a restart may be needed for the new default mode.

Readonly denies Bash and native write tools and uses dontAsk for unapproved
calls. It provides native Read/Grep/Glob review, not automatic git inspection.
Localdev/fulldev use manual default mode, selected trusted development commands,
and ask rules for ordinary git push and risky git families. They do not
automatically allow every git, Python, shell, Docker or SSH invocation.

Trusted build/test scripts can execute arbitrary code and network operations.
Command-text rules are not a sandbox; never promise that every destructive
operation always prompts or that a profile overrides managed policy. Other
settings, hooks, mods and MCP tools still affect effective access. Link the
official documentation in README when explaining these limits.
