# Contributing

Thank you for considering contributing to Forenlims. This document explains the preferred workflow, how to run checks and tests, and where to find templates and CI.

## Filing issues

- Use the issue templates in the repository. See the bug and feature templates:
  - [Bug template](.github/ISSUE_TEMPLATE/bug.yml)
  - [Feature template](.github/ISSUE_TEMPLATE/feature.yml)
- Provide a clear title, steps to reproduce (for bugs), and expected vs actual behavior.

## Pull request workflow

1. Fork the repository and create a topic branch named like `fix/short-description` or `feat/short-description`.
2. Make small, focused commits and write clear commit messages.
3. Ensure tests and linters pass locally (see Testing & Linters).
4. Open a pull request targeting `main`. Fill the PR template: [.github/pull_request_template.md](.github/pull_request_template.md).
5. A maintainer will review. Address review comments and push updates to the same branch.

## Testing & Linters

- Run Django tests:
  - python manage.py test — see [`manage.py`](manage.py)
- Linting and formatting:
  - Ruff: `poetry run ruff check .`
  - djLint: `poetry run djlint --check .`
- Convenience scripts defined in the project:
  - Lint-check: use the [`scripts.check.main`](scripts/check.py) entrypoint via the poetry script `lint-check` (see [pyproject.toml](pyproject.toml)).
  - Lint-fix: use the [`scripts.fix.main`](scripts/fix.py) entrypoint via the poetry script `lint-fix` (see [pyproject.toml](pyproject.toml)).
- Auto-fixers:
  - `poetry run ruff check --fix .`
  - `poetry run djlint --reformat .`
  - Or run `poetry run lint-fix` to execute the configured fixers.

## Pre-commit and CI

- We use pre-commit hooks configured in [.pre-commit-config.yaml](.pre-commit-config.yaml).
- GitHub Actions run tests and linters on push and PRs: [.github/workflows/DjangoCI.yaml](.github/workflows/DjangoCI.yaml).

## Development environment

- This project uses Poetry for dependency management. See [pyproject.toml](pyproject.toml).
- Python version is pinned in [.python-version](.python-version) (project uses Python 3.13).
- Use a virtual environment and `poetry install` to set up.

## Code style

- We follow rules configured in [pyproject.toml](pyproject.toml) (Ruff and djLint profiles). Please run linters before opening PRs.

## Commits & Pull Request checklist

- [ ] All tests pass locally and in CI.
- [ ] Linter checks passed.
- [ ] Documentation updated if necessary.
- [ ] PR description explains the change and motivation.

## License

- By contributing, you agree that your contributions will be licensed under the project's license: [LICENSE](LICENSE) (Apache License 2.0).

## Questions

If you're unsure about how to contribute or which design is preferred, open an issue or start a discussion.
