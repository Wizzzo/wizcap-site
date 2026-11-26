# Static site: no build. `make dev` serves it locally.
.PHONY: setup dev lint format test ci

setup:
	@python3 --version

dev:
	python3 -m http.server 8000

lint:
	@python3 tools/check_site.py

format:
	@true

test: lint

ci: lint
