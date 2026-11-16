# Helix: A Flexible and Scalable NextGen Cellular Core

Helix is a scalable, cloud-native 5G core designed to improve control-plane performance while preserving the flexibility of the 3GPP Service-Based Architecture (SBA).
It scales network functions independently through UE-aware load balancing, distributed state management, and per-UE state caching, and it recovers from network-function failures while keeping per-UE state consistent.

This repository is the **testbed**: it deploys Kubernetes, the Helix core and the gnbsim load generator with Ansible, runs experiments and collects their logs.

| Repository | Contents |
|---|---|
| `helix` (this repo) | Testbed, core and gnbsim profiles, experiments |
| [`amf`](https://github.com/Helix-NextGen-Cellular-Core/amf), [`smf`](https://github.com/Helix-NextGen-Cellular-Core/smf), [`sctplb`](https://github.com/Helix-NextGen-Cellular-Core/sctplb), [`nrf`](https://github.com/Helix-NextGen-Cellular-Core/nrf), [`udm`](https://github.com/Helix-NextGen-Cellular-Core/udm), [`udr`](https://github.com/Helix-NextGen-Cellular-Core/udr), [`ausf`](https://github.com/Helix-NextGen-Cellular-Core/ausf), [`pcf`](https://github.com/Helix-NextGen-Cellular-Core/pcf), [`nssf`](https://github.com/Helix-NextGen-Cellular-Core/nssf) | Helix network functions (based on [OMEC / SD-Core](https://github.com/omec-project)) |
| [`gnbsim`](https://github.com/Helix-NextGen-Cellular-Core/gnbsim) | Load generator (branch `realtrace` for real-trace workloads) |
| [`util`](https://github.com/Helix-NextGen-Cellular-Core/util), [`nas`](https://github.com/Helix-NextGen-Cellular-Core/nas), [`mongodblibrary`](https://github.com/Helix-NextGen-Cellular-Core/mongodblibrary) | Libraries used by the network functions |

## Contents
1. [Overview](#1-overview)
2. [Requirements](#2-requirements)
3. [Setup and first run](#3-setup-and-first-run)
4. [Running the experiments](#4-running-the-experiments)
5. [Results](#5-results)
6. [Configuration](#6-configuration)
7. [Repository layout](#7-repository-layout)

## 1. Overview

```
 control machine                core node                        gnbsim node            storage node
 ┌──────────────────┐   SSH     ┌────────────────────────────┐   N2/SCTP   ┌───────────────┐       ┌──────────────┐
 │ Ansible container│──────────▶│ RKE2 Kubernetes            │◀────────────│ gnbsim        │       │ experiment   │
 │ (make, run_      │           │  └─ Helix core (Helm):     │   N3/GTP-U  │ containers    │──logs▶│ logs         │
 │  experiment.py)  │──────────▶│     SCTP-LB, AMF, SMF, UDM,│◀────────────│ (Docker,      │       │              │
 └──────────────────┘           │     UDR, PCF, ..., UPF,    │             │  macvlan)     │       │              │
                                │     MongoDB, Redis         │             └───────────────┘       └──────────────┘
                                └────────────────────────────┘
```

| Folder | Selects |
|---|---|
| `core/5gc/<profile>` | Helix core: pods per network function, Helm values |
| `gnbsim/<profile>` | Load generator: gnbsim image, number of containers |
| `experiments/<family>/<procedure>/<name>` | Workload: UEs, procedure, events, rate |
| `core/k8s/<profile>` | Kubernetes (RKE2) settings |

`make start-platform` installs Kubernetes, the core and the gnbsim containers; `run_experiment.py` runs experiments and collects their logs.

## 2. Requirements

| Machine | Tested with |
|---|---|
| Core node | 60 vCPU (Xeon Gold 6530), 62 GB RAM, Ubuntu 22.04 (`helix-4pods` needs about 64 vCPU / 48 GB) |
| gnbsim node (+ log storage) | 16 vCPU, 15 GB RAM, Ubuntu 22.04 (256 UEs) |
| Control machine | any Linux with Docker, `make`, `git` (can be one of the nodes) |

- Use dedicated machines: the playbooks install RKE2 and Docker, flush iptables rules, and change sysctls, routes and macvlan interfaces.
- Every node: Ubuntu, internet access (container images from `ghcr.io`; RKE2, kubectl, Helm and Docker from their official download sites), SSH from the control machine as a user with passwordless `sudo`, a CPU with AVX (MongoDB).
- **Data-plane NIC:** the core and gnbsim nodes need a NIC with the same name on both (`helix_data_iface`), with IPv4 addresses in one subnet on the same L2 segment. Example for the core node (`/etc/netplan/60-helix-data.yaml`, then `sudo netplan apply`; use `10.10.0.2/24` on the gnbsim node):
  ```yaml
  network:
    version: 2
    ethernets:
      enp1s0np0:            # your helix_data_iface
        dhcp4: false
        addresses: [10.10.0.1/24]
  ```
- The testbed uses `10.42.0.0/16`, `10.43.0.0/16`, `172.20.0.0/16`, `172.250.0.0/16`, `192.168.250.0/24` and `192.168.252.0/24`; they must not overlap your networks.
- On the control machine, load an SSH key that logs into every node: `eval $(ssh-agent) && ssh-add`.

## 3. Setup and first run

```bash
git clone https://github.com/Helix-NextGen-Cellular-Core/helix.git
cd helix
cp hosts.ini.example hosts.ini      # node IPs, SSH user, data NIC, log directory
make start-ansible                  # opens the Ansible control container
```

Inside the container:
```bash
make pingall                        # Ansible reaches every node
make gnbsim-docker-install          # once per gnbsim node
make start-platform                 # Kubernetes, Helix core (helix-1pod), gnbsim containers
./run_experiment.py --core helix-1pod --reset-core --exp e2e-latency/REG/REG-1ues-100events-10ms-parallel-1gnbsim
```

Without an interactive shell, prefix commands with `deps/platform/scripts/ansible`, e.g. `deps/platform/scripts/ansible make pingall`. Put environment variables before the prefix (`EXPERIMENT_MAX_WAIT=200 deps/platform/scripts/ansible ./run_experiment.py …`); the launcher passes `EXPERIMENT_MAX_WAIT`, `HELIX_IMAGES` and `GNBSIM_IMAGE` into the container. Only one launcher container runs at a time (it is named `ansible`).

Check: on the core node `kubectl -n omec get pods` lists 17 pods, all `Running` (amf, ausf, init-net, metricfunc, mongodb-0, mongodb-arbiter-0, nrf, nssf, pcf, redis, sctplb, simapp, smf, udm, udr, upf-0 `5/5`, webui); on the gnbsim node `docker ps` lists 16 `gnbsim-<n>` containers.

Ansible prints `FAILED - RETRYING` while it waits for gnbsim, and a few `fatal: … ...ignoring` lines (`pkill` after each run, `rke2-uninstall.sh` on the gnbsim node); these are expected. A step failed only if `PLAY RECAP` shows `failed=` above 0 or the command exits non-zero.
Tear down with `make stop-platform`.

## 4. Running the experiments

`./run_experiment.py --list` shows profiles and experiments; `--dry-run` prints what would run.
Always pass `--reset-core` (reinstalls the core before every run).

Run times on our testbed: `make start-platform` ~4.5 min; one E2E run ~3–4 min including the core reset (the E2E sweep below is 198 runs, ~12 h); autoscaling ~11 min; each failure run ~5.5 min; the real-trace suite ~13 min plus ~3 min for each `make resetgnbsim`.

**E2E latency** (registration, PDU session, service request; 1–256 UEs; 1, 2 and 4 pods per NF):
```bash
./run_experiment.py --core helix-1pod helix-2pods helix-4pods --suite e2e --repeat 3 --reset-core --logs-prefix e2e
```

**Autoscaling** (256 UEs arriving one per second; Kubernetes HPAs scale the NFs):
```bash
EXPERIMENT_MAX_WAIT=200 ./run_experiment.py --core helix-autoscaling --reset-core \
  --exp autoscaling/SR/SR-256ues-30000events-10ms-parallel-autoscaling-16gnbsim-startImsiDelay1
```
gnbsim is stopped after `EXPERIMENT_MAX_WAIT` seconds, so its summary shows no passed UEs; judge the run by the service-request counts (§5) and by the AMF/SMF replica counts (`kubectl -n omec get hpa`), which go from 1 to 5.

**Failure** (1 UE, 10,000 service requests; the SMF serving the UE is deleted during the run):
```bash
./run_experiment.py --core helix-failure-2smf --reset-core --exp failure/SR/SR-1ues-10000events-10ms-parallel-1gnbsim &
# on the core node, ~30 s after the output shows "TASK [simulator : async start gnbsims]":
IP=$(kubectl -n omec logs upf-0 -c pfcp-agent | grep -oE 'F-SEID IPv4=[0-9.]+' | tail -1 | cut -d= -f2)
SMF=$(kubectl -n omec get po --no-headers -o custom-columns=NAME:.metadata.name,IP:.status.podIP | awk -v ip=$IP '/^smf/ && $2==ip {print $1}')
kubectl -n omec delete pod $SMF
```
Use `helix-failure-1smf` for the single-SMF case. Expected: all 10,000 service requests pass; one request right after the delete takes ~3 s (2 SMFs) or ~6 s (1 SMF).

**Real traces** (256 UEs; delays from operator traces). The trace files `ECM_IDLE-L_SRV_REQ.csv` and `ECM_CONNECTED-L_S1_CONN_REL.csv` are available on request (open an issue in this repository); put them in `realTraces/`, then:
```bash
make resetgnbsim GNBSIM_TYPE=cluster-1node-10pods--sctpnodelay-gap1ms-realtrace
./run_experiment.py --core helix-4pods --gnbsim cluster-1node-10pods--sctpnodelay-gap1ms-realtrace --suite realtrace --reset-core
make resetgnbsim                    # back to the default gnbsim profile
```

**Experiment names** describe the workload: `SR-256ues-100events-10ms-parallel-X6gnbsim` = service requests, 256 UEs, 100 events per UE 10 ms apart, all UEs in parallel, 16 gnbsim containers ("X6" = 16). Each folder has `vars.yml` (containers, UEs, first IMSI, autoscaling settings) and `gnbsim.yaml` (the gnbsim profile).

## 5. Results

Each run is collected on the storage node (`--logs-prefix` defaults to `default`); run the commands below there:
```
<helix_logs_dir>/<logs-prefix>/<experiment>/<core profile>/<gnbsim profile>/<cluster profile>/<timestamp>/
├── gnbsim-logs/<gnbsim node>/    one log per gnbsim container (folder = the node's name in hosts.ini)
└── corelogs/                  logs of every Helix pod, Pods.log, Helm values
```

gnbsim logs one line per procedure: `[LOG][E2E],imsi-…,<start s>,<end s>,<start ns>,<end ns>,<latency ms>,<hh:mm:ss>,<procedure>,<pass|fail>`.
```bash
grep -rh '^\[LOG\]\[E2E\]' <run dir>/gnbsim-logs | awk -F, '{print $9, $10}' | sort | uniq -c        # pass/fail per procedure
grep -rh '^\[LOG\]\[E2E\]' <run dir>/gnbsim-logs | awk -F, '$10=="pass"{print $9, $7}' | sort -k1,1 -k2n \
  | awk '{n[$1]++; v[$1,n[$1]]=$2} END{for(p in n){k=int(n[p]*0.95); if(k<1)k=1; printf "%-40s n %6d  median %5d ms  p95 %5d ms\n", p, n[p], v[p,int((n[p]+1)/2)], v[p,k]}}'   # latency per procedure
```

## 6. Configuration

**`hosts.ini`**: `[master_nodes]` / `[aether_nodes]` (core node), `[worker_nodes]` (optional extra Kubernetes nodes), `[gnbsim_nodes]`, `[storage_nodes]`; `helix_core_ip` (core node's data-NIC address), `helix_data_iface`, `helix_logs_dir`.

**Core profiles** (`core/5gc/`; Helm values in `core/values/`):

| Profile | Pods per NF |
|---|---|
| `helix-1pod` | 1 |
| `helix-2pods` | AMF, SMF, UDM, UDR, PCF: 2 |
| `helix-4pods` | AMF, SMF, UDM, UDR, PCF: 4 |
| `helix-autoscaling` | 1, scaled by HPA |
| `helix-failure-1smf`, `helix-failure-2smf` | 1 or 2 SMFs |

**gnbsim profiles** (`gnbsim/`): `cluster-1node-16pods--sctpnodelay-gap1ms-withMsgChannels` (default) and `cluster-1node-10pods--sctpnodelay-gap1ms-realtrace` (real traces). Both start 16 containers; the "10pods" in the real-trace name is historical.

**Images** (release `v1.0.0`, built from the repositories above):

| Image | Used by |
|---|---|
| `ghcr.io/helix-nextgen-cellular-core/{amf,smf,sctplb,nrf,udm,udr,ausf,pcf,nssf}:v1.0.0` | all core profiles |
| `ghcr.io/helix-nextgen-cellular-core/gnbsim:v1.0.0` | default gnbsim profile |
| `ghcr.io/helix-nextgen-cellular-core/gnbsim-realtrace:v1.0.0` | real-trace gnbsim profile |

To use other images: `GNBSIM_IMAGE=<image>` overrides the gnbsim profile's image, and `HELIX_IMAGES=<name>` overlays `core/values/images/<name>.yaml` (Helm values with `5g-control-plane.images.tags`; see `example.yaml`) on the core's values. Set them for `make start-platform`, `make resetcore` / `resetgnbsim` and `run_experiment.py --reset-core`.

Long runs: gnbsim processes still running after `EXPERIMENT_MAX_WAIT` seconds (default 500) are stopped.

## 7. Repository layout

```
├── Makefile               start-ansible, pingall, gnbsim-docker-install, start-platform, resetcore, resetgnbsim, stop-platform
├── run_experiment.py      experiment runner (--help)
├── hosts.ini.example      testbed inventory template
├── redis.yml              Redis for the Helix AMF/SMF state
├── core/                  k8s/ and 5gc/ profiles, values/ (Helm values), charts/ (SD-Core chart 0.12.6)
├── gnbsim/                load-generator profiles
├── experiments/           e2e-latency, autoscaling, failure, realtrace
├── templates/rke2/        RKE2 node configuration
├── deps/platform/         Ansible playbooks and roles
└── *.sh                   helpers for the autoscaling experiments
```

Licensed under the Apache License 2.0 (see `LICENSE`). Parts of the Ansible roles and the Helm values come from the [Aether / SD-Core](https://github.com/omec-project) projects (Apache-2.0).
