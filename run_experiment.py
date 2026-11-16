#!/usr/bin/env python3
"""Run Helix experiments.

Each run drives load from gnbsim against the core that `make start-platform`
brought up, then collects logs to the storage node under
<helix_logs_dir>/<logs-prefix>/<experiment>/<core>/<gnbsim>/<cluster>/<timestamp>/.

Use --reset-core for measurements: it reinstalls the core before every run.

Run inside the Ansible container (`make start-ansible`).

Examples:
  ./run_experiment.py --list
  ./run_experiment.py --core helix-1pod --exp e2e-latency/REG/REG-1ues-100events-10ms-parallel-1gnbsim
  ./run_experiment.py --core helix-1pod helix-2pods helix-4pods --suite e2e --repeat 3 --reset-core
  ./run_experiment.py --core helix-4pods --exp 'e2e-latency/SR/*' --dry-run
"""

import argparse
import fnmatch
import os
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_CLUSTER = "cluster-1node"
DEFAULT_GNBSIM = "cluster-1node-16pods--sctpnodelay-gap1ms-withMsgChannels"

# Named experiment sets (glob patterns relative to experiments/).
SUITES = {
    "e2e": ["e2e-latency/*/*"],
    "failure": ["failure/*/*"],
    "autoscaling": ["autoscaling/*/*"],
    "realtrace": ["realtrace/*/*"],
}


def list_dirs(base, depth):
    """Relative paths of directories exactly `depth` levels below base."""
    out = []
    for dirpath, dirnames, _ in os.walk(base):
        rel = os.path.relpath(dirpath, base)
        level = 0 if rel == "." else rel.count(os.sep) + 1
        if level == depth:
            out.append(rel)
            dirnames[:] = []
    return sorted(out)


def available():
    return {
        "core": list_dirs(os.path.join(ROOT_DIR, "core", "5gc"), 1),
        "gnbsim": list_dirs(os.path.join(ROOT_DIR, "gnbsim"), 1),
        "cluster": list_dirs(os.path.join(ROOT_DIR, "core", "k8s"), 1),
        "exp": list_dirs(os.path.join(ROOT_DIR, "experiments"), 3),
    }


def resolve_experiments(patterns, all_exps):
    selected = []
    for pat in patterns:
        matches = [e for e in all_exps if fnmatch.fnmatch(e, pat.strip("/"))]
        if not matches:
            sys.exit(f"error: no experiment matches '{pat}' (see --list)")
        selected += [m for m in matches if m not in selected]
    return selected


def check(kind, names, avail):
    for n in names:
        if n not in avail[kind]:
            sys.exit(f"error: unknown {kind} '{n}' (available: {', '.join(avail[kind])})")


def make(target, env, dry_run):
    print(f"+ make {target}  [{env['CORE_5GC_TYPE']} | {env['GNBSIM_TYPE']} | {env['EXPERIMENT_TYPE']}]", flush=True)
    if dry_run:
        return
    rc = subprocess.run(["make", target], cwd=ROOT_DIR, env=env).returncode
    if rc != 0:
        sys.exit(f"error: 'make {target}' failed with exit code {rc}")


def main():
    avail = available()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--core", nargs="+", default=["helix-1pod"], help="core profile(s) under core/5gc/")
    p.add_argument("--gnbsim", default=DEFAULT_GNBSIM, help="gnbsim profile under gnbsim/")
    p.add_argument("--cluster", default=DEFAULT_CLUSTER, help="cluster profile under core/k8s/")
    p.add_argument("--exp", nargs="+", default=[], help="experiment path(s) under experiments/, globs allowed")
    p.add_argument("--suite", choices=sorted(SUITES), action="append", default=[], help="named experiment set")
    p.add_argument("--repeat", type=int, default=1, help="runs per (core, experiment)")
    p.add_argument("--logs-prefix", default="default", help="sub-directory under helix_logs_dir for this campaign")
    p.add_argument("--reset-core", action="store_true", help="reinstall the core before each run")
    p.add_argument("--reset-gnbsim", action="store_true", help="reinstall gnbsim before each run")
    p.add_argument("--dry-run", action="store_true", help="print what would run")
    p.add_argument("--list", action="store_true", help="list available profiles and experiments")
    args = p.parse_args()

    if args.list:
        for kind in ("core", "gnbsim", "cluster"):
            print(f"{kind}:\n  " + "\n  ".join(avail[kind]))
        print("suites:\n  " + "\n  ".join(f"{k}: {' '.join(v)}" for k, v in sorted(SUITES.items())))
        print("experiments:\n  " + "\n  ".join(avail["exp"]))
        return

    patterns = args.exp + [pat for s in args.suite for pat in SUITES[s]]
    if not patterns:
        p.error("give --exp and/or --suite (see --list)")
    experiments = resolve_experiments(patterns, avail["exp"])
    check("core", args.core, avail)
    check("gnbsim", [args.gnbsim], avail)
    check("cluster", [args.cluster], avail)

    total = len(args.core) * len(experiments) * args.repeat
    print(f"{total} run(s): {len(args.core)} core(s) x {len(experiments)} experiment(s) x {args.repeat} repeat(s)")

    n = 0
    for core in args.core:
        base_env = dict(os.environ,
                        ROOT_DIR=ROOT_DIR,
                        CORE_CLUSTER_VERSION=args.cluster,
                        CORE_5GC_TYPE=core,
                        GNBSIM_TYPE=args.gnbsim,
                        LOGS_PREFIX=args.logs_prefix)
        for exp in experiments:
            env = dict(base_env, EXPERIMENT_TYPE=exp)
            for _ in range(args.repeat):
                n += 1
                print(f"=== run {n}/{total}")
                if args.reset_core:
                    make("resetcore", env, args.dry_run)
                if args.reset_gnbsim:
                    make("resetgnbsim", env, args.dry_run)
                make("start-experiment", env, args.dry_run)


if __name__ == "__main__":
    main()
