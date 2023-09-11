test:
	# TODO: tests
	mkdir -p tests
	pytest tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y .

run: quality_checks
	python main.py
