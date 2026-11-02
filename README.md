# Credit card fraud ML pipeline (noWorkflow 2 paper)

This repository materializes the **iterative ML pipeline** that serves as the
running example of the noWorkflow 2 paper, *The Conception and Evolution of
noWorkflow* (Information Systems): the script of the paper's first figure, the
patches that turn it into the versions of its trial history, the driver that
rebuilds that history, the scripts of the paper's usefulness and user-effort
evaluations, and the case study of its "Beyond Python" section.

The idea is a **single evolving script** (`credit_card_fraud.py`) plus a set of
**patches** that turn it into the successive code versions of the trial history.
Input-only variations are obtained by passing a different CLI argument, and the
backup trial is obtained with a restore.

## Files

| File | Role |
|------|------|
| `credit_card_fraud.py` | Baseline script (trial **1.1.1**): PCA=3, RandomForest, undersampling, ROC-AUC/F1. Identical to the paper's Figure `code:creditcardfraudTrial1`. |
| `preprocessing.py` | Local module introduced by trial **6.1.1** (`prepare()` reads the dataset and writes a prepared/intermediate copy). |
| `patch_2_pca.patch` | v1 → v2: PCA components `3 → 10`. |
| `patch_3_gradientboosting.patch` | v2 → v3: `RandomForestClassifier → GradientBoostingClassifier`. |
| `patch_4_keyerror.patch` | v3 → v4: typo `df['Class'] → df['Clas']` (raises `KeyError`, fails the trial). |
| `patch_5_scaler.patch` | v2 → v5: add `StandardScaler` before PCA (branch from 2.1.1). |
| `patch_6_localmodule.patch` | v2 → v6: refactor loading into local module `preprocessing.py` and cache an intermediate `prepared.csv` (branch from 2.1.1). |
| `run_trials.sh` | Driver that reproduces the whole trial history with `now run` / `now restore`. |
| `provenance_challenge_6_with_noworkflow.py` | The script that answers query Q6 of the First Provenance Challenge with noWorkflow's library (the usefulness evaluation); run it inside the `run/` directory the driver leaves. |
| `credit_card_fraud_mlflow.py` | Same pipeline instrumented with **MLflow** (manual `log_param`/`log_metric`/`log_artifact`) — for the effort comparison. |
| `credit_card_fraud_prov.py` | Same pipeline instrumented with **manual W3C PROV** (`prov` library) — for the effort comparison. |
| `generate_prov_graph.py` | Draws a PROV-N document as a PNG (`python generate_prov_graph.py provenance.provn`), to look at what the manual PROV variant records. |
| `requirements-effort.txt` | The pinned versions of MLflow and `prov` for the two instrumented variants (see Effort comparison). |

## Requirements

- **Python 3.12** and the environment in which every noWorkflow execution
  of the paper ran, the time measurements of its overhead evaluation and the
  trials whose listings and figures it shows alike. It is recorded, every
  version pinned, in the companion repository of the overhead experiments
  ([`paper-environment/`](https://github.com/dew-uff/noworkflow-overhead-experiments/tree/is-2026-r1/paper-environment)),
  and installs with one command:

  ```bash
  python3.12 -m venv venv && . venv/bin/activate
  pip install -r https://raw.githubusercontent.com/dew-uff/noworkflow-overhead-experiments/is-2026-r1/paper-environment/requirements.txt
  ```

  It pins **noWorkflow 2.2.0** (the `now` command), pandas 3.1.0 and the
  rest of the ML stack; the versions were resolved on Linux x86_64. What
  noWorkflow records depends on them: pandas 3.1, for one, reads the dataset
  in parallel, opening it seven times, and probes the cgroup files to count
  the processors, all of which `now show -f` lists as file accesses.
- the Kaggle **Credit Card Fraud Detection** dataset as `creditcard.csv`
  (<https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud>).

The case study in [`beyond-python/`](beyond-python/) also needs R, a C
compiler and Graphviz; its README lists them.

## Trial history reproduced

Tags follow noWorkflow's `X.Y.Z` scheme (X = code changed, Y = input changed,
Z = same code and input).

| Trial | Change | Tag | How |
|-------|--------|-----|-----|
| baseline | PCA=3, RandomForest, seed 42 | **1.1.1** | `now run credit_card_fraud.py` |
| re-execution | same code, same input | **1.1.2** | `now run credit_card_fraud.py` |
| re-execution | same code, same input | **1.1.3** | `now run credit_card_fraud.py` |
| input | seed 40 (CLI arg), same code | **1.2.1** | `now run credit_card_fraud.py 40` |
| code | PCA 3 → 10 | **2.1.1** | `patch_2_pca.patch` |
| input | seed 40, same code (v2) | **2.2.1** | `now run credit_card_fraud.py 40` |
| code | RandomForest → GradientBoosting | **3.1.1** | `patch_3_gradientboosting.patch` |
| code (fails) | `df['Clas']` typo → KeyError | **4.1.1** (red) | `patch_4_keyerror.patch` |
| branch | restore 2.1.1 + StandardScaler | **5.1.1** | `now restore 2.1.1` + `patch_5_scaler.patch` |
| branch | restore 2.1.1 + local module + intermediate file | **6.1.1** | `now restore -a 2.1.1` + `patch_6_localmodule.patch` |
| backup | edit + restore without running | **7.0.0** (yellow) | `now restore 5.1.1` |

> **Why `now restore -a 2.1.1` (and not a plain `now restore`) for the local-module branch:**
> that restore runs right after the *successful* trial 5.1.1, which wrote `out.txt`. A plain
> `now restore` compares the working tree against the head trial, sees `out.txt` changed, and
> creates an **unwanted backup trial** — shifting every later tag by one (6.1.1 → 7.1.1 and the
> intended backup 7.0.0 → 8.0.0). The `-a` (`--skip-access`) flag restores the script without
> comparing/restoring file accesses, avoiding that spurious backup. The earlier restore (after
> the *failed* 4.1.1) needs no `-a`, because that trial crashed before writing `out.txt`.

Resulting history:

```
1.1.1 ── 1.1.2 ── 1.1.3 ── 1.2.1 ── 2.1.1 ── 2.2.1 ── 3.1.1 ── 4.1.1 (KeyError, red)
                                       │
                                       ├── 5.1.1                (branch: + StandardScaler)
                                       └── 6.1.1 ── 7.0.0       (branch: + local module + intermediate; 7.0.0 = backup)
```
## How to run

```bash
# from this folder, in the execution environment
CCF_DATASET=/path/to/creditcard.csv ./run_trials.sh
```

The driver copies the baseline and the dataset into a fresh `run/` work directory
(so the canonical files here stay untouched), applies the patches in order, and
invokes `now run` / `now restore`. The KeyError trial (4.1.1) is expected to fail;
the script continues past it. Inspect the result with `now vis` (or `now list`).

The random forest has no seed, so the metrics that a trial with
`RandomForestClassifier` writes, and the outputs of `f1_score` that the
paper's query Q6 lists, may change from one run to the next; the history, the
code hashes and the file accesses do not.

### Applying a single patch manually

```bash
patch -p1 < patch_2_pca.patch        # turns v1 into v2
patch -R -p1 < patch_2_pca.patch     # reverts it
```
## Beyond Python case study

The folder [`beyond-python/`](beyond-python/) holds the case study of the
paper's section "Beyond Python": the same problem and dataset, with a
Python script as the glue between an R script and a C program, edited
across three trials. It has its own driver (`run.sh`) and README.

## Usefulness evaluation

The paper answers the queries of the First Provenance Challenge over the trial
history above with `now vis`, SQL, Prolog, pattern matching and the command
line; the one query that uses noWorkflow as a library, Q6, is the script
`provenance_challenge_6_with_noworkflow.py`, run inside the `run/` directory
the driver leaves (`cd run && python ../provenance_challenge_6_with_noworkflow.py`).

## Effort comparison

The same baseline pipeline is provided in three forms, so the paper can compare the
**user effort** required to obtain provenance. noWorkflow captures it automatically
(no code changes); MLflow and manual PROV require the user to add and maintain
annotations by hand.

| Approach | File | 
|----------|------|
| noWorkflow 2 | `credit_card_fraud.py` (run with `now run`)  |
| MLflow | `credit_card_fraud_mlflow.py` | 
| Manual W3C PROV | `credit_card_fraud_prov.py` | 

The two instrumented variants run no noWorkflow and the paper reports only
the instrumentation they require; they need MLflow and `prov` on top of the
environment above, pinned in `requirements-effort.txt`
(`pip install -r requirements-effort.txt`; `generate_prov_graph.py` draws
the PROV document with pydot, which `prov[dot]` brings).

