$(PYTHON)# Likelihood Estimator Makefile
# Used for generic management tasks
#
# standard variables  -------------------------------------------------------

VENV_DIR=venv
PYTHON=python3
ACTIVATE_VENV=source $(VENV_DIR)/bin/activate

PLATFORM= $(shell uname)

# targets -------------------------------------------------------------------

# ------------------------
# SETUP and CLEANUP targets
#

$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE_VENV) && pip3 install -r requirements.txt

git-hooks:
	pre-commit install

setup: $(VENV_DIR) git-hooks

clean:
ifeq ($(PLATFORM),Linux)
	find . -name "*.pyc" | xargs -r rm -rf
	find . -name "*test.html" | xargs  -r rm -rf
else
	find . -name "*.pyc" | xargs rm -rf
	find . -name "*test.html" | xargs rm -rf
endif

cleanall: clean
	rm -rf $(VENV_DIR)

# ------------------------
# TEST AND ANALYSIS targets
#

test: setup
	rm -rf tests/temp/*
	$(ACTIVATE_VENV)  && coverage run --source $(SRC_DIR) -m unittest discover
	$(ACTIVATE_VENV)  && coverage report  --omit '*/venv/*,*test_*,*/lib/*' --fail-under=5 -m --skip-covered
	$(ACTIVATE_VENV) && coverage html --omit '*/venv/*,*test_*'

