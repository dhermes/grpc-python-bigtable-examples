BREW_PREFIX=$(shell brew --prefix)
LD_LIBRARY_PATH=$(BREW_PREFIX)/lib
PYTHONPATH=gcloud-python-bigtable

help:
	@echo 'Makefile for Python BigTable sample                                       '
	@echo '                                                                          '
	@echo '   make install                Install the Python dependencies            '
	@echo '   make run_cluster            Run example for Cluster Admin API          '
	@echo '   make run_table              Run example for Table Admin API            '
	@echo '                                                                          '
	@echo 'NOTE: Append USE_APP_DEFAULT=True to the end of your make command to      '
	@echo '      switch from a service account to a user account (via the application'
	@echo '      default credentials).                                               '

install:
	[ -d gcloud-python-bigtable ] || git clone https://github.com/dhermes/gcloud-python-bigtable
	cd gcloud-python-bigtable && git pull origin master

run_cluster: install
	python grpc_list_clusters.py

run_table: install
	python grpc_list_tables.py

.PHONY: install run_cluster run_table
