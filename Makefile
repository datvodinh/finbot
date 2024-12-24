install:
	@echo "🚀 Install dependencies using Poetry"
	@poetry install
	@echo "🚀 Install Playwright"
	@playwright install
	
run: ## Run the application
	@python apps/agent/src/main.py

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := run