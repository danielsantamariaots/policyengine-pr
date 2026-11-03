all: install format test

install:
	pip install -e .[dev]

format:
	ruff format .
	ruff check .

test:
	python -m policyengine_core.scripts.policyengine_command test -c policyengine_pr policyengine_pr/tests
