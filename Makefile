BREW_PREFIX=$(shell brew --prefix)
LD_PATH=$(BREW_PREFIX)/lib

help:
	@echo 'Makefile for Python BigTable sample                           '
	@echo '                                                              '
	@echo '   make run_table              Run example for Table Admin API'

run_table:
	LD_LIBRARY_PATH=$(LD_PATH) python grpc_list_tables.py

.PHONY: run_table
