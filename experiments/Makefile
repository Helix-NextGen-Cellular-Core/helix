#### Variables ####

ifndef ROOT_DIR
$(error ROOT_DIR is not set)
endif

ifndef CORE_CLUSTER_VERSION
$(error CORE_CLUSTER_VERSION is not set)
endif

ifndef CORE_5GC_TYPE
$(error CORE_5GC_TYPE is not set)
endif

export GNBSIM_TYPE ?= cluster-1node-16pods--sctpnodelay-gap1ms-withMsgChannels

export EXPERIMENT_TYPE ?= e2e-latency/REG/REG-1ues-100events-10ms-parallel-1gnbsim

export LOGS_PREFIX ?= default
export HELIX_DIR = $(ROOT_DIR)
export HOSTS_INI ?= $(HELIX_DIR)/hosts.ini

export PLATFORM_ROOT_DIR ?= $(HELIX_DIR)/deps/platform

#### a. Provision experiment ####

run-experiment:
	cd $(PLATFORM_ROOT_DIR) && \
	CORE_CLUSTER_VERSION=$(CORE_CLUSTER_VERSION) \
	CORE_5GC_TYPE=$(CORE_5GC_TYPE) \
	GNBSIM_TYPE=$(GNBSIM_TYPE) \
	EXPERIMENT_TYPE=$(EXPERIMENT_TYPE) \
	LOGS_PREFIX=$(LOGS_PREFIX) \
	ROOT_DIR=$(ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/experiments/$(EXPERIMENT_TYPE)/vars.yml" \
	GNBSIM_HOSTS_INI_FILE=$(HOSTS_INI) \
	make platform-simulator-start

collect-experiment:
	cd $(PLATFORM_ROOT_DIR) && \
	CORE_CLUSTER_VERSION=$(CORE_CLUSTER_VERSION) \
	CORE_5GC_TYPE=$(CORE_5GC_TYPE) \
	GNBSIM_TYPE=$(GNBSIM_TYPE) \
	EXPERIMENT_TYPE=$(EXPERIMENT_TYPE) \
	LOGS_PREFIX=$(LOGS_PREFIX) \
	ROOT_DIR=$(ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/experiments/$(EXPERIMENT_TYPE)/vars.yml" \
	GNBSIM_HOSTS_INI_FILE=$(HOSTS_INI) \
	make platform-collector-collect

#### b. Provision prometheus ####
install-prometheus:
	cd $(PLATFORM_ROOT_DIR) && \
	CORE_CLUSTER_VERSION=$(CORE_CLUSTER_VERSION) \
	CORE_5GC_TYPE=$(CORE_5GC_TYPE) \
	GNBSIM_TYPE=$(GNBSIM_TYPE) \
	EXPERIMENT_TYPE=$(EXPERIMENT_TYPE) \
	LOGS_PREFIX=$(LOGS_PREFIX) \
	ROOT_DIR=$(ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/experiments/$(EXPERIMENT_TYPE)/vars.yml" \
	GNBSIM_HOSTS_INI_FILE=$(HOSTS_INI) \
	make platform-5g-sys-install-prometheus