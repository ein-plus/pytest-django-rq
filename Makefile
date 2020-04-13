SHELL = /bin/bash -o pipefail
PROD_REQ := requirements/prod.txt
TEST_REQ := requirements/test.txt
DEV_REQ := requirements/dev.txt
SETUP_PY := setup.py

.PHONY: all reqs test dev clean release

all: reqs test

clean:
	rm -rf build

build/pip-tools-installed:
	which pip-compile || pip install pip-tools
	mkdir build; touch $@

$(PROD_REQ): $(SETUP_PY) build/pip-tools-installed
	pip-compile -o $@ $<

$(TEST_REQ): $(TEST_REQ:.txt=.in) $(PROD_REQ) $(SETUP_PY) build/pip-tools-installed
	pip-compile $<

$(DEV_REQ): $(DEV_REQ:.txt=.in) $(TEST_REQ) $(SETUP_PY) build/pip-tools-installed
	pip-compile $<

reqs: $(PROD_REQ) $(TEST_REQ) $(DEV_REQ)

build/test-req-installed: $(TEST_REQ)
	pip install -r $<
	touch $@

build/dev-req-installed: reqs
	pip install -r $(PROD_REQ) $(TEST_REQ) $(DEV_REQ)
	pip install -e .
	touch $@

dev: build/dev-req-installed

test: build/test-req-installed
	pytest --log-level=DEBUG
	pytest --doctest-modules pytest_django_rq

release:
	python setup.py sdist bdist_wheel upload
