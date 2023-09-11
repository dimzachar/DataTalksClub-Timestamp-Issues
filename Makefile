test:
	# TODO: tests
	pytest tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y .

run: test quality_checks
	python main.py
