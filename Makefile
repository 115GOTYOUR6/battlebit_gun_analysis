SHELL := /bin/bash
TEST_DIRS = ./tests ./modeling_tools/tests

run_all_tests :
	for dir in $(TEST_DIRS); do \
	 	echo ; \
		echo "Running tests in $$dir"; \
		python3 -m unittest discover -s $$dir -p "test*.py"; \
		if [ $$? -ne 0 ]; then \
			echo "Error. Make sure the python venv is active before"; \
			echo "running this makefile."; \
		fi \
	done