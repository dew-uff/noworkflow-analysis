# Beyond Python: the glue pipeline case study (noWorkflow 2 paper)

This folder holds the case study of the section "Beyond Python" of the
noWorkflow 2 paper: the same credit card fraud problem as the running
example, with a Python script as the glue between an R script and a C
program. The Python script never changes; between trials, the R script and
then the C program are edited, and noWorkflow shows what changed in the
code it launched and how the outputs changed.

## Files

| File | Role |
|------|------|
| `fraud_pipeline.py` | The wrapper, the script of every `now run`: it prepares the data with pandas (`prepared.csv`), then launches `Rscript model.R`, compiles `metrics.c` with `cc` and runs the binary. |
| `model.R` | Logistic regression in base R (no packages): reads `prepared.csv`, writes the predictions to `pred.csv`. |
| `metrics.c` | Precision, recall and F1 of the predictions, written to `out.txt`. |
| `patch_2_threshold.patch` | Change of trial **1.1.2**: the threshold of `model.R`, 0.5 to 0.3. |
| `patch_3_accuracy.patch` | Change of trial **1.1.3**: `metrics.c` also writes the accuracy. |
| `run.sh` | Driver: builds the three trials, writes the listings of the paper and restores the first trial; then, when R has the rdtLite package, runs a fourth trial in a project of its own. |
| `rdtlite/fraud_pipeline.py` | The wrapper of the fourth trial: the same pipeline with `model.R` run under rdtLite (`Rscript -e 'rdtLite::prov.run("model.R", prov.dir = ".")'`); it differs from `fraud_pipeline.py` in that line only. |

## Requirements

- **noWorkflow 2.2.0** or later (the `now` command), with **pandas**;
- **R 4** or later (`Rscript`; base R is enough);
- a C compiler (`cc`), `patch`, and **Graphviz** (`dot`) for the drawing of the dataflow;
- optional, for the fourth trial: the **rdtLite** package in R
  (`Rscript -e 'install.packages("rdtLite")'`); without it `run.sh` says so and skips that trial;
- the Kaggle **Credit Card Fraud Detection** dataset as `creditcard.csv`
  (<https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud>), the same file as the running example.

## How to run

```bash
# from this folder, with the dataset at the root of the package
CCF_DATASET=../creditcard.csv ./run.sh
```

`run.sh` copies the three source files and the dataset into a fresh `run/`
work directory, so the files here stay untouched, and runs everything
there. Before each trial it deletes the outputs of the pipeline
(`pred.csv`, `out.txt` and the `metrics` binary), so that each trial
writes them anew: a file that a process rewrites with the same content is
recorded as a read.

## Trial history reproduced

| Trial | What changed before it | Setting of the paper |
|-------|------------------------|----------------------|
| **1.1.1** | nothing: the baseline, threshold 0.5 | |
| **1.1.2** | `model.R`: threshold 0.5 to 0.3 | Python + R |
| **1.1.3** | `metrics.c`: it also writes the accuracy | Python + an arbitrary (compiled) language |
| **2.0.0** (backup) | `now restore 1.1.1` | |
| **1.1.1** of `run/rdtlite/` | the baseline in a project of its own, `model.R` run under rdtLite | Python + R, with R's own provenance |

The tags stay at 1.1.x because the Python script and its command line are
the same in the three trials; the changes are seen through the programs
the script launches. The final `now restore 1.1.1` puts `model.R` and
`metrics.c` back as the first trial read them and removes the outputs the
trials created; since those outputs differ from the last trial, it first
saves the state of the project as the backup trial 2.0.0.

The fourth trial runs in `run/rdtlite/`, a project of its own, so the
history above stays as it is. rdtLite writes the provenance of `model.R`
to `prov_model/prov.json`, a PROV-JSON document; its command line names
neither `model.R` nor the files the script reads and writes, but the
document does, and noWorkflow records them as file accesses of the launch
of `Rscript`.

## Listings

`run.sh` writes the outputs that the paper shows to `run/listings/`:

| File | Command |
|------|---------|
| `show-1.1.1-f.txt` | `now show 1.1.1 -f`: the nine file accesses of the baseline, those of the launched programs included |
| `diff-1.1.1-1.1.2-f-content.txt` | `now diff 1.1.1 1.1.2 -f --content`: the edit of `model.R` and its effect on `pred.csv` and `out.txt` (Python + R) |
| `diff-1.1.2-1.1.3-f-m.txt` | `now diff 1.1.2 1.1.3 -f -m`: `metrics.c` edited and the `metrics` binary replaced as a module (arbitrary language) |
| `dataflow-1.1.3-activation.dot`, `.pdf` | `now export dataflow 1.1.3 -m activation`: each launch connected to the files it read and wrote |
| `show-rdtlite-1.1.1-f.txt` | `now show 1.1.1 -f` in `run/rdtlite/`: `model.R`, `prepared.csv` and `pred.csv` as accesses of the `Rscript` launch, taken from rdtLite's document, next to `prov_model/prov.json` and the copies rdtLite keeps (Python + R, with R's own provenance) |

Timestamps, hashes of the binaries, paths and the versions of R and of the
compiler depend on the machine. With the Kaggle dataset, R 4.6.1 and Apple
clang 21, the baseline writes `precision=0.8736`, `recall=0.6786` and
`F1=0.7638`; trial 1.1.2, `0.8125`, `0.6964` and `0.7500`; trial 1.1.3
adds `accuracy=0.9991`.

## The same files elsewhere

The case study lives in three places, each with its own purpose: the paper
(what it states noWorkflow records), this folder (the files that rebuild the
history) and the tests of noWorkflow
(`src/noworkflow/tests/e2e/corpus/beyond_python/` in
[gems-uff/noworkflow](https://github.com/gems-uff/noworkflow), which also
ships them as `Examples/glue_pipeline/`). The seven files above are byte for
byte the same here and in noWorkflow (the code hash of `fraud_pipeline.py`
that the listings print is the SHA-1 of its bytes); a change to the case
study in one place is carried to the other two.
