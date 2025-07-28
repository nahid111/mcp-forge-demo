# Code Quality

The project uses `ruff` for code formatting and linting:

```bash
# Format code
ruff format .

# Fix linting issues
ruff check . --fix

# Fix import sorting
ruff check . --select I --fix

# Fix unused imports
ruff check . --select I,F401 --fix
```