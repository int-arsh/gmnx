SHELL := /usr/bin/env bash

# Python and Docker settings
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
DOCKER_IMAGE := test-gmnx
DOCKER_TAG := latest

# Test settings
TEST_DIR := tests
COVERAGE_DIR := htmlcov

.PHONY: help test test-unit test-docker test-all clean install-deps build test-coverage

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install-deps: ## Install Python dependencies
	@if [ ! -d "$(VENV)" ]; then python3 -m venv $(VENV); fi
	$(PIP) install -r requirements.txt

build: ## Build Docker image for testing
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

test-unit: ## Run unit tests only
	$(PYTHON) -m pytest $(TEST_DIR)/test_ask.py -v

test-docker: build ## Run Docker container tests
	$(PYTHON) -m pytest $(TEST_DIR)/test_docker.py -v

test: ## Run all tests
	$(PYTHON) -m pytest $(TEST_DIR)/ -v

test-coverage: ## Run tests with coverage report
	$(PYTHON) -m pytest $(TEST_DIR)/ --cov=. --cov-report=html --cov-report=term
	@echo "Coverage report generated in $(COVERAGE_DIR)/index.html"

test-all: test test-coverage ## Run all tests with coverage

clean: ## Clean up test artifacts
	rm -rf $(COVERAGE_DIR)
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .coverage
	docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG) 2>/dev/null || true

# Quick test commands for development
quick-test: ## Quick test without Docker (unit tests only)
	$(PYTHON) -m pytest $(TEST_DIR)/test_ask.py -v --tb=short

lint: ## Run basic linting
	$(PYTHON) -m flake8 ask.py tests/ --max-line-length=100 --ignore=E501,W503

format: ## Format code with black
	$(PYTHON) -m black ask.py tests/ --line-length=100
