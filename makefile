format:
	poetry run black .
start-db:
	docker-compose up -d
stop-db:
	docker-compose down
start-app:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000
test:
	poetry run pytest tests -v