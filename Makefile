$(PYTHON)# Likelihood Estimator Makefile
# Used for generic management tasks
#
# standard variables  -------------------------------------------------------

# make sure pip installs are going to venv/lib and not venv/lib64
# https://amoreopensource.wordpress.com/2018/05/25/problems-with-aws-linux-and-pip/

VENV_DIR=venv_bbmaster
PYTHON=python3
ACTIVATE_VENV=source $(VENV_DIR)/bin/activate
PLATFORM= $(shell uname)
SRC_DIR = imbh/
ifeq ($(PLATFORM),Linux)
	PYTHON=python3.6
endif

#results_dir = ../bilby_pipe_sub/outdir_imbh_injection_pe/result
results_dir = /home/avi.vajpeyi/public_html/bilby_pipe_imbh_results/result/
bilby_pipe_dir = bilby_pipe_sub

# targets -------------------------------------------------------------------

# ------------------------
# SETUP and CLEANUP targets
#

$(VENV_DIR):
	unset PYTHON_INSTALL_LAYOUT
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE_VENV) && pip install -r requirements.txt

git-hooks:
ifeq ($(PLATFORM),Linux)
	#pre-commit install
else
	pre-commit install
endif

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

create_dag: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) create_dag.py --jobs 200 --sub_fname "inj_imbh_pe.sub" --dag_fname "dag_creation/inj_imbh_pe.dag"

generate_parameter_h5: setup
	$(ACTIVATE_VENV) &&  cd $(SRC_DIR) && $(PYTHON) create_imbh_parameter_h5.py --number_of_injections 200 --prior_file injection_parameter_generator/imbh_injection_generation.prior --out_dir injection_parameter_generator/

run_pe_test: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) run_imbh_pe.py -f injection_parameter_generator/injection_data.h5 -i 1 -p imbh_pe_calculator/imbh_pe.prior -o tests/pe_test

results: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) summarise_pe_results.py -r tests/pe_test

results_cit: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) summarise_pe_results.py -r /home/avi.vajpeyi/public_html/imbh_pe_result_files/data/

results_summary: setup
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) summarise_pe_results.py -r $(results_dir)

make_injections: setup
	$(ACTIVATE_VENV) && cd $(bilby_pipe_dir) && bilby_pipe_create_injection_file create_injection.ini

run_pe: setup
	$(ACTIVATE_VENV) && cd $(bilby_pipe_dir) && bilby_pipe injection_pe.ini
