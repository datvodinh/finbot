install:
	@echo "🚀 Install dependencies using Poetry"
	@cd apps/agent poetry install  && cd ../..
	@echo "🚀 Install Playwright"
	@playwright install

update:
	@echo "🚀 Update dependencies using Poetry"
	@cd apps/agent && poetry update && cd ../..

export: ## Export requirements.txt file
	@echo "🚀 Exporting requirements.txt file"
	@cd apps/agent && poetry export --without-hashes -f requirements.txt --output requirements.txt
	@cd ../..

run: ## Run the application
	@python apps/agent/src/main.py

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := run