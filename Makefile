PROJECT_NAME = airflow_tiktok
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs

ENV = --env-file .env

AIRFLOW_COMPOSE = docker_compose/airflow.yml
POSTGRES_COMPOSE = docker_compose/postgres.yml
MONGO_COMPOSE = docker_compose/mongo.yml

POSTGRES_CONTAINER = airflow_postgres
MONGO_CONTAINER = airflow_mongo
AIRFLOW_CONTAINER = airflow_webserver

COMPOSE_ALL = -f $(POSTGRES_COMPOSE) -f $(MONGO_COMPOSE) -f $(AIRFLOW_COMPOSE)

.PHONY: up
up:
	@echo "Starting all containers..."
	$(DC) $(ENV) -f $(AIRFLOW_COMPOSE) up -d
	@echo "All containers are up!"

.PHONY: up-postgres
up-postgres:
	@echo "Starting PostgreSQL..."
	$(DC) $(ENV) -f $(POSTGRES_COMPOSE) up -d

.PHONY: up-mongo
up-mongo:
	@echo "Starting MongoDB..."
	$(DC) $(ENV) -f $(MONGO_COMPOSE) up -d

.PHONY: down
down:
	@echo "Stopping all containers..."
	$(DC) $(ENV) -f $(POSTGRES_COMPOSE) down
	$(DC) $(ENV) -f $(MONGO_COMPOSE) down
	$(DC) $(ENV) -f $(AIRFLOW_COMPOSE) down
	@echo "Containers stopped."

.PHONY: logs-postgres
logs-postgres:
	@echo "Showing PostgreSQL logs..."
	$(LOGS) -f $(POSTGRES_CONTAINER)

.PHONY: logs-mongo
logs-mongo:
	@echo "Showing MongoDB logs..."
	$(LOGS) -f $(MONGO_CONTAINER)

.PHONY: logs-airflow
logs-airflow:
	@echo "Showing Airflow logs..."
	$(LOGS) -f $(AIRFLOW_CONTAINER)

.PHONY: install
install:
	@echo "Installing all dependencies (runtime + dev)..."
	poetry install --with dev

.PHONY: shell
shell:
	@echo "Activating Poetry shell..."
	poetry shell

.PHONY: black
black:
	@echo "Running Black formatter (check mode)..."
	poetry run black --check .

.PHONY: black-fix
black-fix:
	@echo "Running Black formatter (fix mode)..."
	poetry run black .

.PHONY: flake8
flake8:
	@echo "Running Flake8..."
	poetry run flake8 .

.PHONY: isort
isort:
	@echo "Running isort (check)..."
	poetry run isort --check-only .

.PHONY: isort-fix
isort-fix:
	@echo "Fixing import order with isort..."
	poetry run isort .

.PHONY: lint
lint: black flake8 isort
	@echo "All linting checks passed!"

.PHONY: pre-commit
pre-commit: black flake8 isort
	@echo "Running pre-commit hooks..."
	poetry run pre-commit run --all-files
