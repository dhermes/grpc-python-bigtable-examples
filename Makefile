BREW_PREFIX=$(shell brew --prefix)
LD_LIBRARY_PATH=$(BREW_PREFIX)/lib
export LD_LIBRARY_PATH
PYTHONPATH=gcloud-python-bigtable
ifneq ($(VERBOSE),)
	GRPC_TRACE=surface,batch
	export GRPC_TRACE
endif

help:
	@echo 'Makefile for Python BigTable sample                                       '
	@echo '                                                                          '
	@echo '   make _install_core           Install core gRPC library                 '
	@echo '   make _install_grpc_py        Install Python gRPC library               '
	@echo '   make _python_deps            Install the Python dependencies           '
	@echo '   make list_clusters           Use Cluster Admin API to list clusters    '
	@echo '   make list_zones              Use Cluster Admin API to list zones       '
	@echo '   make list_zones_low_level    Same as `list_zones`, using low-level API '
	@echo '   make list_tables             Use Table Admin API to list tables        '
	@echo '                                                                          '
	@echo 'NOTE: Append USE_APP_DEFAULT=True to the end of your make command to      '
	@echo '      switch from a service account to a user account (via the application'
	@echo '      default credentials).                                               '
	@echo '                                                                          '
	@echo 'NOTE: Append VERBOSE=True to the end of your make command to log more     '
	@echo '      output from your examples.                                          '

_install_core:
	curl -fsSL https://goo.gl/getgrpc | bash

_install_grpc_py:
	CFLAGS=-I$(BREW_PREFIX)/include LDFLAGS=-L$(BREW_PREFIX)/lib pip install --upgrade grpcio

_python_deps:
	[ -d gcloud-python-bigtable ] || git clone https://github.com/dhermes/gcloud-python-bigtable
	cd gcloud-python-bigtable && git pull origin master

list_clusters: _python_deps
	python grpc_list_clusters.py

list_zones: _python_deps
	python grpc_list_zones.py

list_zones_low_level: _python_deps
	python grpc_low_level_list_zones.py

list_tables: _python_deps
	python grpc_list_tables.py

.PHONY: _install_core _install_grpc_py _python_deps list_clusters list_zones_low_level list_tables
