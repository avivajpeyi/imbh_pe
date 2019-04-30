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

cleanall: clean
	rm -rf $(VENV_DIR)

# ------------------------
# TEST AND ANALYSIS targets
#

test: setup
	rm -rf tests/temp/*
	rm -rf pe_test/
	$(ACTIVATE_VENV)  && coverage run --source . -m unittest discover
	$(ACTIVATE_VENV)  && coverage report  --omit '*/venv/*,*test_*,*/lib/*' --fail-under=5 -m --skip-covered
	$(ACTIVATE_VENV) && coverage html --omit '*/venv/*,*test_*'

##

create_dag: setup
	$(ACTIVATE_VENV) && python create_dag.py --jobs 200 --sub_fname "sub_imbh_pe.sub" --dag_fname "inj_imbh_pe.dag"

generate_parameter_h5: setup
	$(ACTIVATE_VENV) && python create_imbh_parameter_h5.py --number_of_injections 200 --prior_file imbh/injection_parameter_generator/imbh_injection_generation.prior --out_dir imbh/injection_parameter_generator

test_run: setup
	$(ACTIVATE_VENV) && python run_imbh_pe.py -f imbh/injection_parameter_generator/injection_data.h5 -i 1 -p /Users/Monash/Documents/projects/imbh_pe/imbh/imbh_pe_calculator/imbh_pe.prior -o ./pe_test
