.PHONY: usage
usage:
	@grep '^[^#[:space:]].*:' Makefile | grep -v '^\.PHONY:' | cut -d: -f1

.PHONY: test coverage docs build
test:
	tox

coverage:
	tox -e coverage
	open htmlcov/index.html

docs:
	tox -e docs

build:
	python -m build

clean:
	python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python3 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('pytest_cache')]"
	rm -rdf ./build
	rm -rdf ./dist
	rm -rdf ./docs/build
	rm -rdf ./htmlcov
	rm -rdf .mypy_cache
	rm -rdf .pytest_cache
	rm -rdf .coverage
	rm -rdf pypipedrive_client.egg-info

.PHONY: testpypi
testpypi:
	python -m build
	twine check dist/*
	twine upload -r testpypi dist/* --verbose

.PHONY: pypi
pypi:
	python -m build
	twine check dist/*
	twine upload dist/*