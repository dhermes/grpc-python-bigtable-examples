BREW_PREFIX=$(shell brew --prefix)
LD_PATH=$(BREW_PREFIX)/lib

help:
	@echo 'Makefile for Python BigTable sample                           '
	@echo '                                                              '
	@echo '   make install                Install the Python dependencies'
	@echo '   make run_table              Run example for Table Admin API'

install:
	[ -d gcloud-python-bigtable ] || git clone https://github.com/dhermes/gcloud-python-bigtable
	cd gcloud-python-bigtable && git pull origin master

run_table: install
	PYTHONPATH=gcloud-python-bigtable LD_LIBRARY_PATH=$(LD_PATH) python grpc_list_tables.py

.PHONY: run_table
