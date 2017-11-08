PYTHON=python3
PACKAGE=graffunc

all:
	$(PYTHON) -m $(PACKAGE)

t: test
test:
	pytest graffunc -v --ignore=venv/ --doctest-module

release:
	fullrelease
