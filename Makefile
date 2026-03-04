include .env

.PHONY: tests

migrate:
	docker-compose run -it --rm api uv run alembic revision --autogenerate && make migrateup

migrateup:
	docker-compose run -it --rm api uv run alembic upgrade head

up:
	docker-compose up -d --build && make logs

logs:
	docker-compose logs -f --tail=10000 api

down:
	docker compose down -v

stop:
	docker compose stop api

start:
	docker-compose start api && make logs

restart:
	docker-compose restart api && make logs

tests:
	docker compose exec -it api uv run pytest -v

db:
	docker compose exec -it postgres psql -h localhost -U ${DB_USER} -d ${DB_NAME}

ps:
	docker-compose ps -a
