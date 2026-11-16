#### Variables ####

export ROOT_DIR ?= $(CURDIR)
export ANSIBLE_NAME ?= ansible-helix
# testbed inventory (copy hosts.ini.example)
export HOSTS_INI ?= $(ROOT_DIR)/hosts.ini

# folder name under core/k8s/
export CORE_CLUSTER_VERSION ?= cluster-1node
# folder name under core/5gc/
export CORE_5GC_TYPE ?= helix-1pod
# folder name under gnbsim/
export GNBSIM_TYPE ?= cluster-1node-16pods--sctpnodelay-gap1ms-withMsgChannels
# folder path under experiments/
export EXPERIMENT_TYPE ?= e2e-latency/REG/REG-1ues-100events-10ms-parallel-1gnbsim

## Provision k8s/5gc ##
include core/Makefile

## Provision gnbsim ##
include gnbsim/Makefile

## Provision ansible ##
start-ansible:
	cd core; ANSIBLE_NAME=$(ANSIBLE_NAME) make ansible 

## Provision platform
start-platform: start-k8s-router start-5gc start-gnbsim
stop-platform: stop-gnbsim stop-5gc stop-k8s-router 

resetcore: 
# 	# sleep 10.0;
	$(MAKE) stop-5gc;
	# sleep 10.0;
	$(MAKE) start-5gc;

resetgnbsim:
	$(MAKE) stop-gnbsim;
	$(MAKE) start-gnbsim;

## Provision experiment ##
include experiments/Makefile

start-experiment: run-experiment collect-experiment

## Inventory check ##
start-k8s-router stop-k8s-router start-5gc stop-5gc start-gnbsim stop-gnbsim \
gnbsim-docker-install run-experiment collect-experiment pingall: | $(HOSTS_INI)

$(HOSTS_INI):
	@echo "error: $(HOSTS_INI) not found; run: cp hosts.ini.example hosts.ini and edit it" >&2; exit 1

aether-install-prometheus: install-prometheus

pingall:
	cd $(PLATFORM_ROOT_DIR) && \
	CORE_CLUSTER_VERSION=$(CORE_CLUSTER_VERSION) \
	CORE_5GC_TYPE=$(CORE_5GC_TYPE) \
	GNBSIM_TYPE=$(GNBSIM_TYPE) \
	EXPERIMENT_TYPE=$(EXPERIMENT_TYPE) \
	ROOT_DIR=$(ROOT_DIR) \
	EXTRA_VARS="@$(HELIX_DIR)/experiments/$(EXPERIMENT_TYPE)/vars.yml" \
	GNBSIM_HOSTS_INI_FILE=$(HOSTS_INI) \
	C5GC_HOSTS_INI_FILE=$(HOSTS_INI) \
	HOSTS_INI_FILE=$(HOSTS_INI) \
	make platform-pingall
