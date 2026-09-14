# Contributing to AOE

Thank you for your interest in contributing to **AOE (Autonomous Outreach Engine)**! This document provides guidelines for contributing.

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** from `staging` for your changes:
   ```bash
   git checkout -b feature/your-feature-name staging
   ```
4. **Install dependencies**:
   ```bash
   cd job-agent
   python -m venv .venv
   .venv/Scripts/activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```

## Development Workflow

### Branch Strategy
| Branch | Purpose |
|---|---|
| `main` | Production-ready releases only |
| `staging` | Pre-production integration testing |
| `uat` | User acceptance testing & experiments |
| `feature/*` | New feature development |
| `fix/*` | Bug fixes |

### Commit Convention
Use [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add new job scraper adapter
fix: resolve email verification timeout
docs: update API endpoint documentation
refactor: simplify database connection pooling
test: add E2E tests for batch engine
chore: update dependencies
```

### Code Style
- **Python**: Follow PEP 8. Use [Ruff](https://docs.astral.sh/ruff/) for linting.
- **Frontend**: Tailwind CSS utility classes, vanilla JavaScript.
- **Commits**: Keep commits atomic and descriptive.

## Submitting Changes

1. Push your branch to your fork
2. Open a Pull Request against `staging` (never directly to `main`)
3. Fill out the PR template completely
4. Ensure CI passes
5. Wait for code review from a maintainer

## Reporting Issues

Use the [issue templates](https://github.com/lordpardonme/aoe/issues/new/choose) to report bugs or request features.

## Contributor License Assignment

AOE is distributed under a **Strict Proprietary & Source-Available License** (see [`LICENSE`](LICENSE)). By submitting a Pull Request, issue, or patch to this repository, you explicitly agree that:
1. Your contributions are licensed to and assigned to `@lordpardonme`.
2. Your contributions become subject to the terms of the project's proprietary license.
3. You retain no separate proprietary rights or claims to the codebase or its architecture.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Open a [Discussion](https://github.com/lordpardonme/aoe/discussions) or file an issue.
