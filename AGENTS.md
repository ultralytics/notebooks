# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

This repository (AGPL-3.0) holds the Ultralytics YOLO tutorial notebooks for Colab, Kaggle, and SageMaker Studio Lab, covering training, inference, export, and vision tasks. It is content only — there is no Python package to build or publish.

## Core Principles (CRITICAL)

**Less is more. The simplest solution is the best solution.** The action hierarchy for every change: **Delete > Replace > Add**.

1. **Solve at the owner**: Put behavior in the code path that owns or observes it. For fixes, never guard a symptom with a staleness check, initialization flag, skip-first-call branch, or `try/except` around broken logic; relocate the trigger and delete the wrong path. For features, extend the existing owner rather than creating a parallel abstraction.
2. **Search and reuse first**: Search the whole repository before creating a feature, component, helper, workflow, or utility. Reuse or adapt what exists, consolidate in-scope duplication in the shared owner, and delete duplicate paths. Three similar lines beat a helper nobody else calls.
3. **Delete and modify existing code before creating new code**: Bugfixes are net-negative by default unless deletion and relocation are demonstrably impossible. A new file must first prove it cannot fit cleanly in an existing owner.
4. **Keep scope minimal**: Implement only the simplest complete solution. Avoid impossible-state handling, speculative flags, compatibility shims, policy scaffolding, and unrelated cleanup. Tests are out of scope by default — rely on existing coverage and focused validation; only an uncovered, high-risk regression path justifies minimal new test code.
5. **Ship zero-regression, production-ready changes**: Understand what you remove instead of retaining broken code as insurance. Remove unused imports, functions, types, files, and comments; run relevant cleanup checks; and thoroughly debug and validate the changed owner. Do not break existing features or workflows unless the PR intentionally removes them with evidence.

**Review gate:** for every addition, the reviewer decides whether deleting or changing existing code would have fixed the problem instead — if it would, that is a blocking finding. A missing or thin PR description is never itself a finding.

NEVER push to `main`. NEVER force push. Always start work in a new git worktree (`git worktree add`) on a feature branch and open a PR — never edit the primary checkout directly, it may hold in-flight work.

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Review the full diff in-session against the Core Principles, performance, and the review gate above, then batch the fixes into one commit and push. After each round of bot or human commits, pull and resume the same reviewer on `<last-reviewed-sha>..HEAD` plus anything that delta could have invalidated. Repeat until the local head matches the live head.
3. Hand off or merge only on a clean final pass: one cold full-diff review returning LGTM with no findings, on a head that is still live at merge time.
4. Never fight other commits: Ultralytics Actions pushes auto-format and header commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never reset or revert commits you did not author.
5. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands

```bash
uv venv && uv pip install ultralytics pytest "shapely>=2.0.0"           # install (as CI does; never bare pip install)
pytest -m "not slow" tests/test_notebooks.py --maxfail=1 -p no:warnings # fast smoke tests (CI PR job)
pytest -m "slow" tests/test_notebooks.py --maxfail=1 -p no:warnings     # SAM tests (scheduled CI only)
pytest tests/test_notebooks.py::test_export_val_results                 # run one test
python3 docs/update-readme-table.py                                     # regenerate README tables (needs pyyaml, run from repo root)
```

- CI (`.github/workflows/ci.yml`) runs on `ubuntu-latest` with Python 3.14 via `ultralytics/actions/setup-uv@main` — a single Python version, no matrix, no coverage tooling; PRs run only the fast `notebook-smoke` job.
- There is no local lint config (no pyproject/ruff/prettier files); formatting is applied in PRs by the Ultralytics Actions bot (`.github/workflows/format.yml`: Ruff, docformatter, Prettier, codespell).

## Architecture

This is a content repository of 19 tutorial Jupyter notebooks (`notebooks/`) for Ultralytics YOLO — there is no Python package, no build, and no release/publish process (the repo's only GitHub release, v0.0.0, exists solely to host demo videos and images, including the demo video used by tests).

- The notebook tables in `README.md` and `README.zh-CN.md` (between `TABLE_START`/`TABLE_END` markers) are generated from `docs/notebooks-data.yml` by `docs/update-readme-table.py`; never edit them by hand — edit the YAML and regenerate.
- `.github/workflows/table.yml` triggers on any push touching that YAML or script (no branch filter) and commits both regenerated README tables to the pushed branch as `UltralyticsAssistant`.
- `tests/test_notebooks.py` smoke-tests notebook scenarios by calling the `ultralytics` API directly (Solutions classes, val-export, SAM); it does not execute the `.ipynb` files.
- The `notebook-sam` CI job runs only on the daily schedule (cron 08:00 UTC, gated by `github.event_name == 'schedule'`); PR runs execute only the fast job.

## Conventions

- Python and YAML files start with the `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` header — Ultralytics Actions adds these automatically; don't add or revert them manually.
- All tests hit the live network: they download model weights, demo videos from GitHub releases, `ultralytics.com` assets, and the `coco8` dataset; downloaded `*.pt` weights land in the repo root and are gitignored.
- `pytest.ini` defines the only custom marker, `slow`, reserved for heavyweight tests that run on scheduled CI only.
- There is no version-bump or release process; changes ship by merging to `main`.
