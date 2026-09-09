# Contributing to CodePilot

## 1. Git Workflow & Branching
- Develop new features on dedicated branches: `feature/<feature-name>`
- Ensure all commits follow conventional commit format:
  - `feat(scope): ...`
  - `fix(scope): ...`
  - `docs(scope): ...`
  - `test(scope): ...`

---

## 2. Automated Quality Gates
Before creating a PR, verify all tests pass:
```bash
python -m unittest discover tests -p "*.py"
```
Ensure zero test failures and no security or memory regressions.
