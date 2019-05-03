$(PYTHON)# Likelihood Estimator Makefile
# Used for generic management tasks
#
# standard variables  -------------------------------------------------------

VENV_DIR=venv
PYTHON=python3
ACTIVATE_VENV=source $(VENV_DIR)/bin/activate
PLATFORM= $(shell uname)
SRC_DIR = imbh/

# targets -------------------------------------------------------------------

# ------------------------
# SETUP and CLEANUP targets
#

$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE_VENV) && pip3 install -r requirements.txt

git-hooks:
	#pre-commit install

setup: $(VENV_DIR) git-hooks

clean:
ifeq ($(PLATFORM),Linux)
	find . -name "*.pyc" | xargs -r rm -rf
	find . -name "*test.html" | xargs  -r rm -rf
else
	find . -name "*.pyc" | xargs rm -rf
	find . -name "*test.html" | xargs rm -rf
endif
	rm -rf $(SRC_DIR)tests/temp/*

cleanall: clean
	rm -rf $(VENV_DIR)

# ------------------------
# TEST AND ANALYSIS targets
#

test: setup
	rm -rf $(SRC_DIR)tests/temp/*
	mkdir -p $(SRC_DIR)tests/temp/
	$(ACTIVATE_VENV)  && cd $(SRC_DIR) && coverage run --source . -m unittest discover
	$(ACTIVATE_VENV)  && cd $(SRC_DIR) && coverage report  --omit '*/venv/*,*test_*,*/lib/*' --fail-under=5 -m --skip-covered
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && coverage html --omit '*/venv/*,*test_*'

##

create_dag: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) create_dag.py --jobs 200 --sub_fname "inj_imbh_pe.sub" --dag_fname "dag_creation/inj_imbh_pe.dag"

generate_parameter_h5: setup
	$(ACTIVATE_VENV) &&  cd $(SRC_DIR) && $(PYTHON) create_imbh_parameter_h5.py --number_of_injections 200 --prior_file injection_parameter_generator/imbh_injection_generation.prior --out_dir injection_parameter_generator/

run_pe_test: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) run_imbh_pe.py -f injection_parameter_generator/injection_data.h5 -i 1 -p imbh_pe_calculator/imbh_pe.prior -o tests/pe_test


results: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) summarise_pe_results.py -r tests/pe_test -i injection_parameter_generator/injection_data.h5

results_cit: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) summarise_pe_results.py -r /home/avi.vajpeyi/projects/imbh_pe_out -i injection_parameter_generator/injection_data.h5
