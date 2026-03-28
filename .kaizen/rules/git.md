# Git Rules

## Commit Format

```
<type>: <short description>

[optional body]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code change that doesn't fix a bug or add a feature
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat: add agentic workflow pipeline
fix: correct vector search query in retrieval_pipeline.py
docs: update fine-tuning SKILL.md with Colab instructions
```

## Branch Strategy

- `main` — production-ready code
- `feat/<feature-name>` — feature development
- `fix/<issue>` — bug fixes
- `docs/<topic>` — documentation

```
git checkout -b feat/my-feature
git commit -m "feat: description"
git push origin feat/my-feature
# Open PR → review → merge to main
```

## Never Do

- `git push --force` to main
- Commit secrets, API keys, or credentials
- Commit generated files (node_modules, __pycache__, .next, *.pyc)
- Merge directly to main without PR review

## Required Before Commit

- [ ] Tests pass locally
- [ ] Code formatted (ruff / prettier)
- [ ] No lint errors
- [ ] Committed to feature branch (not main directly)
