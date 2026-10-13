# Maintainer handoff

This is the maintained permission-profile project. The copy in the private
research-tools archive is historical; future changes belong here. The initial
readonly profile used acceptEdits, and fulldev broadly allowed git while
claiming destructive commands always prompt. Current profiles remove those
rules and replace the entire project permissions object deterministically.

Python 3.8+ is required; no Python dependencies. Claude Code is required only
to use the plugin. Load with `claude --plugin-dir /path/to/claude-dev-permissions`
and run `/dev-permissions:setup-permissions PROFILE`, or use the Python script
in README. No datasets, models or credentials are bundled or needed. Installing
Python and Claude Code are the only external resource requirements.

Run `python -m unittest discover -s tests -v`. Tests check configuration behavior
and profile invariants, not Claude's shell parser. The 2026-10-13 check used
official permission and plugin docs linked in README; it did not run an
authenticated Claude session. Trusted scripts, hooks, mods, settings scopes
and other execution tools affect effective access. Profiles are not a sandbox.

Next: test loading and actual prompts in a disposable authenticated Claude
workspace; record Claude version and settings sources. Review arbitrary code
execution/network capability before adding any auto-allowed command family.
Keep tests aligned with the authoritative JSON. Consider a marketplace only
after runtime acceptance. Preserve history with additive commits.

MIT, copyright Kang Chen. The initial repository has four authored plugin and
documentation files and one Kang Chen commit. No vendored implementation was
found. Added code/tests are authored for this repository. Anthropic docs are
referenced by URL, not copied; this project is not endorsed by Anthropic.
