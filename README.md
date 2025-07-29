# Install Dependencies
```bash
# create virtual environment
python3 -m venv .venv

# activate virtual environment
source .venv/bin/activate

#install uv
pip install uv

# install dependencies
uv sync --frozen
```

# Run locally
```bash
# run mcp forge gateway
./start_gateway

# run mcp weather server
python -m server

# run langgraph agent
python -m agent
```


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

