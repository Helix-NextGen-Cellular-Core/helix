# SD-Core Helm chart (sd-core 0.12.6)

The Helix core is installed from `sd-core-0.12.6.tgz` in this directory (see `chart_ref` in `core/5gc/*/vars.yml`).
The chart's original repository, `https://charts.aetherproject.org`, is offline, so the chart is shipped here.

It was reassembled from the published upstream sources at the exact versions the original `sd-core` 0.12.6 depended on.
**The one difference from the original:** `bess-upf` 0.1.3 (Nov 2022) replaces 0.1.0 (Oct 2022), which is not available anywhere.
The UPF is deployed for N4 (PFCP) signalling, and Helix does not modify it.

| Chart | Version | Source | sha256 |
|---|---|---|---|
| sd-core (umbrella) | 0.12.6 | [omec-project/sdcore-helm-charts](https://github.com/omec-project/sdcore-helm-charts) `1fe7e5f` (`sdcore-helm-charts/`), `bess-upf` dependency set to 0.1.3 | `9ed1df5f7b172758cfba65f204cc9d4f1f62b560627dcf3d734bce3f8cfcc18c` |
| 5g-control-plane | 0.8.12 | same repo, `6f36517` | `a8322f7593518490b973d5c43be84471f8a03c2b513f41647a533592b8f3252a` |
| ↳ mongodb (Bitnami) | 13.6.4 | official release `https://charts.bitnami.com/bitnami/mongodb-13.6.4.tgz` | `236df2a75a8166898d35ba4d104b0220b63b2ccd1de9790fab404fe431f5b040` (matches Bitnami's index) |
| ↳ kafka (Bitnami) | 20.0.4 | official release `https://charts.bitnami.com/bitnami/kafka-20.0.4.tgz` | `6dca1bb19e4d298b1d0d857195f990b5b1373a3040054acea818ff2ebc94c7ad` (matches Bitnami's index) |
| omec-control-plane | 0.12.0 | same repo, `e208e45` | `affa7af47e2e99cf294f30e7687eedf24e0434604cf70e65a9deeccd78e75f42` |
| ↳ cassandra (incubator) | 0.13.1 | official release `https://charts.helm.sh/incubator/packages/cassandra-0.13.1.tgz` | `1fce06a65e30d323627461eea535626500dd1118dca0946a598dd80c75313415` (matches the incubator index) |
| omec-sub-provision | 0.6.0 | same repo, `e208e45` | `28c311ae8b62a15bfa9682a0c5174fccc31d36a60a71e4749a85daa77cf1233a` |
| 5g-ran-sim | 0.6.5 | same repo, `22556c7` | `00162cd71fe4d739ca5a9274d682440bc4f36022e493fe8efcc46e637b5c06ec` |
| bess-upf (alias `omec-user-plane`) | 0.1.3 | same repo, `dc68664` (unchanged import of the Nov 2022 chart) | `fbbd96597a769b6a86b05edbf15263d2dd20dd1ef54ea40df6193c305a8e9329` |

The ONF subcharts were packaged with Helm v3.11.3 from the git trees at the listed commits, without modification.
4G components (`omec-control-plane`), `5g-ran-sim` and Kafka are included because the umbrella chart requires them; they are disabled in the Helix values.

All charts are licensed under Apache-2.0 by their authors (Open Networking Foundation, Bitnami, Helm incubator).
