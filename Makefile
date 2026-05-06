.PHONY: install run-api run-frontend ingest test lint clean

install:
	pip install -r requirements.txt

run-api:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	streamlit run frontend/app.py

ingest:
	python -m ingestion.jobs.run_ingestion

test:
	python -m pytest tests/ -v

lint:
	ruff check app/ ingestion/ ml/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
