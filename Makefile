.PHONY: setup analisis test lint datos
setup:
	uv sync
analisis:
	uv run python scripts/analisis.py
test:
	uv run pytest -q
lint:
	uv run ruff check . && uv run ruff format --check .
# Opcional: regenerar el CSV desde un parquet de boxscores propio
datos:
	uv run python scripts/extraer_partidos.py $(PARQUET) data/acb_partidos_2025_26.csv
