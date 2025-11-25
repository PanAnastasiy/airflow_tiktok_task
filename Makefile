PROJECT_NAME = airflow_tiktok
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs

ENV = --env-file .env

AIRFLOW_COMPOSE = docker_compose/airflow.yml
AIRFLOW_CONTAINER = airflow_webserver

.PHONY: up
up:
	@echo "Starting all containers..."
	$(DC) $(ENV) -f $(AIRFLOW_COMPOSE) up -d
	@echo "All containers are up!"

.PHONY: down
down:
	@echo "Stopping container..."
	$(DC) $(ENV) -f $(AIRFLOW_COMPOSE) down
	@echo "Containers stopped."

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
