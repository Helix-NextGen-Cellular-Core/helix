#### Variables ####

export ROOT_DIR ?= $(PWD)
export C5GC_ROOT_DIR ?= $(ROOT_DIR)
export K8S_ROOT_DIR ?= $(C5GC_ROOT_DIR)/deps/k8s

export ANSIBLE_NAME ?= ansible-5gc
export ANSIBLE_CONFIG ?= $(K8S_ROOT_DIR)/ansible.cfg
export HOSTS_INI_FILE ?= $(C5GC_ROOT_DIR)/hosts.ini

export EXTRA_VARS ?= "@$(C5GC_ROOT_DIR)/vars/main.yml"

#### Provisioning k8s ####

include $(K8S_ROOT_DIR)/Makefile

#### a. Debugging ####

5gc-debug:
	ansible-playbook -i $(HOSTS_INI_FILE) $(C5GC_ROOT_DIR)/debug.yml \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS)

5gc-pingall:
	ansible-playbook -i $(HOSTS_INI_FILE) $(C5GC_ROOT_DIR)/pingall.yml \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS)

#### b. Provision router ####
5gc-router-install: 
	ansible-playbook -i $(HOSTS_INI_FILE) $(C5GC_ROOT_DIR)/router.yml --tags install \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS)
5gc-router-uninstall:
	ansible-playbook -i $(HOSTS_INI_FILE) $(C5GC_ROOT_DIR)/router.yml --tags uninstall \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS)

#### c. Provision core ####
5gc-core-install: 
	ansible-playbook -i $(HOSTS_INI_FILE) $(C5GC_ROOT_DIR)/core.yml --tags install \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS)
5gc-core-uninstall:
	ansible-playbook -i $(HOSTS_INI_FILE) $(C5GC_ROOT_DIR)/core.yml --tags uninstall \
		--extra-vars "ROOT_DIR=$(ROOT_DIR)" --extra-vars $(EXTRA_VARS)

#### d. Provision all ####
5gc-k8s-router-install: k8s-install 5gc-router-install
5gc-k8s-router-uninstall: 5gc-router-uninstall k8s-uninstall 

5gc-install: 5gc-k8s-router-install 5gc-core-install
5gc-uninstall: 5gc-core-uninstall 5gc-k8s-router-uninstall
