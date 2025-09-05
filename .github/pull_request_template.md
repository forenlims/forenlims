## Summary

Short description of the change and the motivation. Keep it concise.

## Type of change

- [ ] Bugfix
- [ ] New feature
- [ ] Documentation
- [ ] Refactor
- [ ] Tests
- [ ] CI / tooling

## Related issues

Closes: # (issue number)
Relates to: #

## Changes made

Describe the main changes at a glance (one or two bullets).

## How to test

Provide short, reproducible steps to verify the change locally:

- Install: `poetry install`
- Run tests: `poetry run python manage.py test`
- Lint: `poetry run ruff check .` and `poetry run djlint --check .`

Include commands and example inputs/outputs where useful.

## Checklist

- [ ] I have read the contributing guidelines and SECURITY.md
- [ ] Tests added/updated where applicable
- [ ] Linting and formatting checks pass locally
- [ ] No credentials or secrets included
- [ ] Commits are small and focused; branch is rebased onto main

## Release notes / CHANGELOG

If relevant, add a one-line entry for the changelog under "Unreleased" (e.g. "Added: ...", "Fixed: ...", "Breaking: ...").

## Breaking changes

Describe any breaking API/behavior changes here. If present, mark as a MAJOR bump in the changelog.

## Notes for reviewers

Anything the reviewer should pay special attention to (design decisions, performance impacts, known limitations).

> Security-sensitive changes: do NOT open a public PR. Follow SECURITY.md to report privately.
