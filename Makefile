HERE = $(shell pwd)
BIN = $(HERE)/bin
PYTHON = $(BIN)/python
INSTALL = $(BIN)/pip install --no-deps
VTENV_OPTS ?= -p `which python2.7 | head -n 1`
VIRTUALENV = virtualenv-2.7

BUILD_DIRS = bin build include lib lib64 man share

.PHONY: all test coverage

all: build

$(PYTHON):
	$(VIRTUALENV) $(VTENV_OPTS) .

build: $(PYTHON)
	$(PYTHON) setup.py develop
	$(BIN)/pip install nose coverage

clean:
	rm -rf $(BUILD_DIRS)

test:
	$(BIN)/nosetests -sv henet/tests

coverage: build
	LONG=1 $(BIN)/nosetests -s -d -v --cover-html --cover-html-dir=html --with-coverage --cover-erase --cover-package henet henet/tests
