# Contributing to Tajweed Recitation Coach

Thank you for contributing! This document explains how to report issues, propose changes, and submit code so maintainers can review and merge reliably.

## Table of Contents
- How to contribute
- Development setup
- Branching & PR workflow
- Commit message guidelines
- Tests & linters
- Code review checklist
- Reporting issues
- Code of Conduct

## How to contribute
- Found a bug? Open an issue with steps to reproduce, expected vs actual behavior, and logs/screenshots.
- Want to add a feature or fix? Open an issue first to discuss scope unless it's a trivial typo or docs fix.
- Fork the repo, create a branch from `main`, implement your change, and open a pull request (PR).

## Development setup
1. Clone the project:

   git clone https://github.com/<your-fork>/Tajweedcoach.git
   cd Tajweedcoach

2. Backend (Docker):

   cd backend
   docker compose up -d

   # Optional: run locally without Docker
   python -m venv .venv
   .\\.venv\\Scripts\\Activate.ps1   # PowerShell
   pip install -r requirements.txt
   uvicorn app.main:app --reload

3. Frontend:

   cd frontend
   npm install
   npm run dev

## Branching & PR workflow
- Branch name format: `type/short-description`, e.g. `feature/add-audio-widget`, `fix/api-timeout`.
- Rebase or merge `main` before opening the PR to keep history clean.
- Every PR should target the `main` branch unless the issue specifies otherwise.
- Include a clear description, screenshots (if UI), and link to the issue.
- Add tests for new features or bug fixes where applicable.

## Commit message guidelines
- Use simple, descriptive messages. Prefer Conventional Commits style:

  feat: add verse-selection component
  fix: properly handle empty audio uploads
  docs: clarify README setup steps

- Keep body text wrapped at ~72 chars and reference issues: `Refs #123` or `Closes #123`.

## Tests & linters
- Backend tests (if present): run from `backend/` with pytest:

  cd backend
  pytest

- Frontend tests (if present): run from `frontend/`:

  cd frontend
  npm test

- Linters / formatters:
  - Python: black, isort, flake8 (run from `backend`)
  - JavaScript: eslint, prettier (run from `frontend`)

Run formatters before committing. CI will also run linters and tests on PRs.

## Code review checklist (for contributors & reviewers)
- Code is well-tested and passes CI.
- Changes are documented (README or /docs) when user-visible.
- No sensitive data or secrets are committed.
- Performance impact considered for audio/ML paths.
- New dependencies are justified and licensed appropriately.

## Reporting issues
When opening an issue, include:
- Short descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Node/Python versions)
- Logs or screenshots

## Code of Conduct
Be respectful. This project follows a Contributor Covenant-style Code of Conduct. If a CODE_OF_CONDUCT.md is not present, maintain respectful and constructive collaboration.

## Need help?
If unsure where to start, open an issue labeled `good first issue` or ask in the issue thread — maintainers will help steer the work.

---

Thank you for helping improve Tajweed Recitation Coach!
