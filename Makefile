.PHONY: setup dev test lint seed migrate

setup:
	python -m pip install -e .[dev]

dev:
	docker compose up --build

test:
	pytest -q

lint:
	ruff check .

seed:
	python scripts/seed_data.py

migrate:
	alembic upgrade head
