# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

## Core Principles (CRITICAL)

Respecting these principles is critical for every PR.

**Less is more. The simplest solution is the best solution.**

The action hierarchy for every change: **Delete > Replace > Add**. The best code change is a deletion. The second best is modifying what exists. Adding new code is the last resort.

1. **Minimal**: The simplest solution that works. Do not over-engineer, over-abstract, or add code just in case. Three similar lines beat a premature abstraction. Avoid error handling for impossible states, feature flags, compatibility shims, or policy scaffolding unless they are truly required.
2. **Solve at the source**: Do not hack fixes. Solve problems at their root. If something is broken, fix or remove the broken thing. Never patch over a broken abstraction, add workarounds, or add synchronization code for state that should not be duplicated.
3. **Delete ruthlessly**: When replacing code, delete what it replaced. Remove unused imports, functions, types, files, and commented-out code. Git preserves history. Run the repo's relevant dead-code or cleanup check when available.
4. **Replace > Add**: Modify existing code over adding new code. Edit existing files, extend existing components or functions with minimal parameters, and reuse existing utilities. If creating a new file, first prove it cannot fit cleanly in an existing file.
5. **Check existing**: Search the entire repo before creating anything new. If a feature, component, helper, responder, workflow, or utility already solves a similar problem, reuse or adapt it and delete the duplicate path.
6. **Deduplicate**: Do not duplicate existing code when updating the repo. Consolidate or refactor duplicates you find when it is in scope and low risk.
7. **Zero Regression**: Do not break existing features or workflows unless the PR intentionally removes them with evidence.
8. **Production ready**: All changes must be thoroughly debugged, validated, and production ready.

**When fixing bugs, ask: "What can I delete?" before "What can I replace?" before "What should I add?"**

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Launch an independent adversarial review agent with cold context (just the PR diff and this file) to hunt for bugs, regressions, and Core Principles violations — use the Codex CLI, one fresh `codex exec` run per round. Fix, push, and repeat until a fresh run reports LGTM.
3. Never fight other commits: Ultralytics Actions pushes auto-format and header commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never force-push, reset, or revert commits you did not author.
4. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands

```bash
uv venv && uv pip install ultralytics pytest "shapely>=2.0.0"           # install (as CI does; never bare pip install)
pytest -m "not slow" tests/test_notebooks.py --maxfail=1 -p no:warnings # fast smoke tests (CI PR job)
pytest -m "slow" tests/test_notebooks.py --maxfail=1 -p no:warnings     # SAM tests (scheduled CI only)
pytest tests/test_notebooks.py::test_export_val_results                 # run one test
python3 docs/update-readme-table.py                                     # regenerate README.md table (needs pyyaml, run from repo root)
```

- CI (`.github/workflows/ci.yml`) runs on `ubuntu-latest` with Python 3.14 via `ultralytics/actions/setup-uv@main` — a single Python version, no matrix, no coverage tooling; PRs run only the fast `notebook-smoke` job.
- There is no local lint config (no pyproject/ruff/prettier files); formatting is applied in PRs by the Ultralytics Actions bot (`.github/workflows/format.yml`: Ruff, docformatter, Prettier, codespell).

## Architecture

This is a content repository of 19 tutorial Jupyter notebooks (`notebooks/`) for Ultralytics YOLO — there is no Python package, no build, and no release/publish process (the repo's only GitHub release, v0.0.0, exists solely to host demo videos and images, including the demo video used by tests).

- The notebook table in `README.md` (between `TABLE_START`/`TABLE_END` markers) is generated from `docs/notebooks-data.yml` by `docs/update-readme-table.py`; never edit the table by hand — edit the YAML and regenerate.
- `.github/workflows/table.yml` triggers on any push touching that YAML or script (no branch filter) and commits the regenerated `README.md` to the pushed branch as `UltralyticsAssistant`.
- `README.zh-CN.md` is a manual mirror of `README.md`: `table.yml` does not touch it, so its table (kept in English) must be synced by hand whenever the table changes.
- `tests/test_notebooks.py` smoke-tests notebook scenarios by calling the `ultralytics` API directly (Solutions classes, val-export, SAM); it does not execute the `.ipynb` files.
- The `notebook-sam` CI job runs only on the daily schedule (cron 08:00 UTC, gated by `github.event_name == 'schedule'`); PR runs execute only the fast job.

## Conventions

- Python and YAML files start with the `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` header — Ultralytics Actions adds these automatically; don't add or revert them manually.
- All tests hit the live network: they download model weights, demo videos from GitHub releases, `ultralytics.com` assets, and the `coco8` dataset; downloaded `*.pt` weights land in the repo root and are gitignored.
- `pytest.ini` defines the only custom marker, `slow`, reserved for heavyweight tests that run on scheduled CI only.
- There is no version-bump or release process; changes ship by merging to `main`.
