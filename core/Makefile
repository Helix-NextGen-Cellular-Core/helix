#### Variables ####

ifndef ROOT_DIR
$(error ROOT_DIR is not set)
endif

export CORE_CLUSTER_VERSION ?= cluster-1node
export CORE_5GC_TYPE ?= helix-1pod

export HELIX_DIR = $(ROOT_DIR)
export HOSTS_INI ?= $(HELIX_DIR)/hosts.ini

export PLATFORM_ROOT_DIR ?= $(HELIX_DIR)/deps/platform
export C5GC_ROOT_DIR ?= $(PLATFORM_ROOT_DIR)/deps/5gc

export ANSIBLE_NAME ?= ansible-results

#### Start Ansible docker ####

ansible:
	ANSIBLE_NAME=$(ANSIBLE_NAME) ANSIBLE_MOUNT_DIR=$(HELIX_DIR) \
	bash $(PLATFORM_ROOT_DIR)/scripts/ansible bash

#### a. Provision k8s & router ####

start-k8s-router:
	cd $(C5GC_ROOT_DIR) && \
	ROOT_DIR=$(HELIX_DIR) \
	C5GC_ROOT_DIR=$(C5GC_ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/core/k8s/$(CORE_CLUSTER_VERSION)/vars.yml" \
	HOSTS_INI_FILE=$(HOSTS_INI) \
	make 5gc-k8s-router-install

stop-k8s-router:
	cd $(C5GC_ROOT_DIR) && \
	ROOT_DIR=$(HELIX_DIR) \
	C5GC_ROOT_DIR=$(C5GC_ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/core/k8s/$(CORE_CLUSTER_VERSION)/vars.yml" \
	HOSTS_INI_FILE=$(HOSTS_INI) \
	make 5gc-k8s-router-uninstall

#### a. Provision 5gc ####

start-5gc:
	cd $(C5GC_ROOT_DIR) && \
	ROOT_DIR=$(HELIX_DIR) \
	C5GC_ROOT_DIR=$(C5GC_ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/core/5gc/$(CORE_5GC_TYPE)/vars.yml" \
	HOSTS_INI_FILE=$(HOSTS_INI) \
	make 5gc-core-install

stop-5gc:
	cd $(C5GC_ROOT_DIR) && \
	ROOT_DIR=$(HELIX_DIR) \
	C5GC_ROOT_DIR=$(C5GC_ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/core/5gc/$(CORE_5GC_TYPE)/vars.yml" \
	HOSTS_INI_FILE=$(HOSTS_INI) \
	make 5gc-core-uninstall

reset-5gc: stop-5gc start-5gc
