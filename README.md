# Credit card fraud ML pipeline (noWorkflow 2 paper)

This folder materializes the **iterative ML pipeline** that serves as the running
example of the noWorkflow 2 paper. It is the concrete
artifact behind Figure 1 in the paper.

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
| `credit_card_fraud_mlflow.py` | Same pipeline instrumented with **MLflow** (manual `log_param`/`log_metric`/`log_artifact`) — for the effort comparison. |
| `credit_card_fraud_prov.py` | Same pipeline instrumented with **manual W3C PROV** (`prov` library) — for the effort comparison. |

## Requirements

These scripts **cannot run in the paper-writing environment** (it lacks the ML
libraries and the dataset). Run them in the execution environment (e.g. the
`noworkflow-analysis` repo), which needs:

- **noWorkflow 2** (the `now` command);
- Python packages: `scikit-learn`, `imbalanced-learn`, `pandas`;
- the Kaggle **Credit Card Fraud Detection** dataset as `creditcard.csv`
  (<https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud>).

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

### Applying a single patch manually

```bash
patch -p1 < patch_2_pca.patch        # turns v1 into v2
patch -R -p1 < patch_2_pca.patch     # reverts it
```
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

