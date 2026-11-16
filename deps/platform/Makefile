#### Variables ####

# TODO: fix this ...
export CORE_CLUSTER_VERSION ?= ''
export CORE_5GC_TYPE ?= ''
export GNBSIM_TYPE ?= ''
export EXPERIMENT_TYPE ?= ''
export LOGS_PREFIX ?= default

export ROOT_DIR ?= $(PWD)
export PLATFORM_ROOT_DIR ?= $(ROOT_DIR)
export C5GC_ROOT_DIR ?= $(PLATFORM_ROOT_DIR)/deps/5gc
export GNBSIM_ROOT_DIR ?= $(PLATFORM_ROOT_DIR)/deps/gnbsim

export ANSIBLE_NAME ?= ansible-platform
export ANSIBLE_CONFIG ?= $(PLATFORM_ROOT_DIR)/ansible.cfg

export C5GC_HOSTS_INI_FILE ?= $(PLATFORM_ROOT_DIR)/5gc-hosts.ini
export GNBSIM_HOSTS_INI_FILE ?= $(PLATFORM_ROOT_DIR)/gnbsim-hosts.ini

export EXTRA_VARS ?= "@$(PLATFORM_ROOT_DIR)/vars/main.yml"

#### Start Ansible docker ####

ansible:
	export ANSIBLE_NAME=$(ANSIBLE_NAME); \
	sh $(GNBSIM_ROOT_DIR)/scripts/ansible ssh-agent bash

#### Provisioning platform ####

platform-install: platform-5gc-install platform-gnbsim-install
platform-uninstall: platform-gnbsim-uninstall platform-5gc-uninstall 

#### Provisioning 5gc ####

platform-5gc-install:
	cd $(C5GC_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	C5GC_ROOT_DIR=$(C5GC_ROOT_DIR) \
	EXTRA_VARS=$(EXTRA_VARS) \
	HOSTS_INI_FILE=$(C5GC_HOSTS_INI_FILE) \
	make 5gc-install

platform-5gc-uninstall:
	cd $(C5GC_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	C5GC_ROOT_DIR=$(C5GC_ROOT_DIR) \
	EXTRA_VARS=$(EXTRA_VARS) \
	HOSTS_INI_FILE=$(C5GC_HOSTS_INI_FILE) \
	make 5gc-uninstall

#### Provisioning gnbsim ####
# NOTE: run `make platform-gnbsim-docker-install` once to install the docker runtime

platform-gnbsim-install:
	cd $(GNBSIM_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	GNBSIM_ROOT_DIR=$(GNBSIM_ROOT_DIR) \
	EXTRA_VARS=$(EXTRA_VARS) \
	HOSTS_INI_FILE=$(GNBSIM_HOSTS_INI_FILE) \
	make gnbsim-install

platform-gnbsim-uninstall:
	cd $(GNBSIM_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	GNBSIM_ROOT_DIR=$(GNBSIM_ROOT_DIR) \
	EXTRA_VARS=$(EXTRA_VARS) \
	HOSTS_INI_FILE=$(GNBSIM_HOSTS_INI_FILE) \
	make gnbsim-uninstall

#### a. Debugging ####

platform-pingall:
	cd $(C5GC_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	C5GC_ROOT_DIR=$(C5GC_ROOT_DIR) \
	EXTRA_VARS=$(EXTRA_VARS) \
	HOSTS_INI_FILE=$(C5GC_HOSTS_INI_FILE) \
	make 5gc-pingall

	cd $(GNBSIM_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	GNBSIM_ROOT_DIR=$(GNBSIM_ROOT_DIR) \
	EXTRA_VARS=$(EXTRA_VARS) \
	HOSTS_INI_FILE=$(GNBSIM_HOSTS_INI_FILE) \
	make gnbsim-pingall

#### b. Provision simulator ####
platform-simulator-start:
	ansible-playbook -i $(GNBSIM_HOSTS_INI_FILE) $(PLATFORM_ROOT_DIR)/simulator.yml --tags start \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS) \
		--extra-vars "{ 'collector': { 'storage': { 'logs_prefix': '$(LOGS_PREFIX)' } } }" \
		--extra-vars "{ 'PLATFORM_PARAMS': { 'CORE_CLUSTER_VERSION': $(CORE_CLUSTER_VERSION), 'CORE_5GC_TYPE': $(CORE_5GC_TYPE), \
									         'GNBSIM_TYPE': $(GNBSIM_TYPE), 'EXPERIMENT_TYPE': $(EXPERIMENT_TYPE)} }"

#### b. Provision collector ####
platform-collector-collect:
	ansible-playbook -i $(GNBSIM_HOSTS_INI_FILE) $(PLATFORM_ROOT_DIR)/collector.yml --tags collect \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS) \
		--extra-vars "{ 'collector': { 'storage': { 'logs_prefix': '$(LOGS_PREFIX)' } } }" \
		--extra-vars "{ 'PLATFORM_PARAMS': { 'CORE_CLUSTER_VERSION': $(CORE_CLUSTER_VERSION), 'CORE_5GC_TYPE': $(CORE_5GC_TYPE), \
									         'GNBSIM_TYPE': $(GNBSIM_TYPE), 'EXPERIMENT_TYPE': $(EXPERIMENT_TYPE)} }"

#### b. Provision prometheus ####
platform-5g-sys-install-prometheus:
	ansible-playbook -i $(GNBSIM_HOSTS_INI_FILE) $(PLATFORM_ROOT_DIR)/5g-sys.yml --tags install_sys \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS) \
		--extra-vars "{ 'PLATFORM_PARAMS': { 'CORE_CLUSTER_VERSION': $(CORE_CLUSTER_VERSION), 'CORE_5GC_TYPE': $(CORE_5GC_TYPE), \
									         'GNBSIM_TYPE': $(GNBSIM_TYPE), 'EXPERIMENT_TYPE': $(EXPERIMENT_TYPE)} }"
