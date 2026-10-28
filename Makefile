.PHONY: setup analisis test lint
setup:
	uv sync
analisis:
	uv run python scripts/analisis.py
test:
	uv run pytest -q
lint:
	uv run ruff check . && uv run ruff format --check .
