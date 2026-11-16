#### Variables ####

ifndef ROOT_DIR
$(error ROOT_DIR is not set)
endif

export GNBSIM_TYPE ?= cluster-1node-16pods--sctpnodelay-gap1ms-withMsgChannels

export HELIX_DIR = $(ROOT_DIR)
export HOSTS_INI ?= $(HELIX_DIR)/hosts.ini

export PLATFORM_ROOT_DIR ?= $(HELIX_DIR)/deps/platform
export GNBSIM_ROOT_DIR ?= $(PLATFORM_ROOT_DIR)/deps/gnbsim

#### a. Provision gnbsim ####

start-gnbsim:
	cd $(GNBSIM_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	GNBSIM_ROOT_DIR=$(GNBSIM_ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/gnbsim/$(GNBSIM_TYPE)/vars.yml" \
	HOSTS_INI_FILE=$(HOSTS_INI) \
	make gnbsim-install

stop-gnbsim:
	cd $(GNBSIM_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	GNBSIM_ROOT_DIR=$(GNBSIM_ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/gnbsim/$(GNBSIM_TYPE)/vars.yml" \
	HOSTS_INI_FILE=$(HOSTS_INI) \
	make gnbsim-uninstall

#### b. One-time: docker runtime on the gnbsim nodes ####

gnbsim-docker-install:
	cd $(GNBSIM_ROOT_DIR) && \
	ROOT_DIR=$(ROOT_DIR) \
	GNBSIM_ROOT_DIR=$(GNBSIM_ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/gnbsim/$(GNBSIM_TYPE)/vars.yml" \
	HOSTS_INI_FILE=$(HOSTS_INI) \
	make gnbsim-docker-install
