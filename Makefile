PYTHON=python3

all:
	$(PYTHON) -m conspread

t: test
test:
	$(PYTHON) -m unittest discover -v


test_register:
	$(PYTHON) setup.py register -r https://testpypi.python.org/pypi
test_install:
	$(PYTHON) setup.py sdist upload -r https://testpypi.python.org/pypi
	$(PYTHON) -m pip install -U -i https://testpypi.python.org/pypi conspread

register:
	$(PYTHON) setup.py register
upload:
	$(PYTHON) setup.py sdist upload
install:
	$(PYTHON) -m pip install -U conspread
