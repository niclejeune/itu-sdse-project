# Lead Conversion Prediction

Predicts whether a new user signup will convert to a paying customer, packaged as a reproducible MLOps project.

## Guarantees
- Reproducible models from versioned code + versioned data (DVC).
- Identical execution locally and in CI via a single Dagger runtime.
- Deterministic regression detection via fixed inference outputs.

## Why this exists
- Built for the ITU BDS MLOPS'25 assignment to turn a single exploratory notebook into a production-quality pipeline.
- Goal: give others a fast, portable way to rerun, inspect, and extend the model without guessing how the notebook worked.

## Design principles
- Parity first: the Dagger container is the single runtime for local development and CI.
- Immutable truth: `data/raw/raw_data.csv` comes from DVC and is never edited in place.
- Single source of config: `config.yaml` controls all data, model, and report paths.
- Unit testing: pytest covers data prep, feature engineering, storage helpers, and encoding; `predict.py` checks the expected inference output.
- Portable artifacts: models, scaler, and column list are saved in `models/` and can be packed into `models.tar` for transfer.

## How it works
Conceptually, this project is a deterministic data -> features -> model -> artifact compiler.
![Project Architecture](docs/project-architecture.png)

- Data flows from DVC-tracked `data/raw/` through cleaning (`lead_conversion_prediction.dataset`) into `data/interim/`, then through feature engineering (`lead_conversion_prediction.features`) into `data/processed/`.
- Training (`lead_conversion_prediction.modeling.train`) builds a tree-based XGBoost baseline plus a Logistic Regression variant, logs metrics to `reports/model_results.json`, and saves artifacts and the column manifest to `models/`.
- Inference (`lead_conversion_prediction.modeling.predict`) loads `models/lead_model_xgboost.pkl` and asserts the first five predictions on `data/processed/X_test.csv` match the reference output, catching regressions.
- The Dagger module (`dagger/pipeline.go`) wraps the flow in a Python 3.10 container, caches pip installs, and exposes discrete steps (`clean-data`, `prepare-data`, `train`, `predict`) plus a full `pipeline` that packages `models.tar`.

> *Design decision about default model choice*: The original notebook used `RandomizedSearchCV` for Logistic Regression without a fixed `random_state`, making results non-deterministic. To guarantee reproducibility, the pipeline defaults to the XGBoost model while still training and logging both variants.
The default is explicit (inference loads `models/lead_model_xgboost.pkl`), and both `RandomizedSearchCV` runs are now seeded with `random_state=42` to keep training repeatable.

## Run it (local with CI parity)
Prereqs: Python 3.10, Docker running, Dagger CLI, and DVC. Install Python deps once:

```bash
pip install -r requirements.txt
```

1) Pull the immutable raw data from the GitHub DVC remote:
```bash
dvc update data/raw/raw_data.csv.dvc
```
2) Preferred: run the end-to-end containerized pipeline and export the model bundle:
```bash
dagger call pipeline --source . export --path ./models.tar
```
Models are also written to `models/` inside the container and included in `models.tar`.
3) Run individual steps while iterating:
```bash
dagger call clean-data --source .
dagger call prepare-data --source .
dagger call train --source .
dagger call predict --source .
```
4) If Docker is unavailable, the same code paths run directly:
```bash
make data && make train && make predict
```
> Note: running without Docker skips the container isolation guarantees but exercises the exact same Python entry points used inside the Dagger pipeline.

## Automation
- `.github/workflows/main.yml` runs on every push and PR to `main`: DVC update, pytest, the Dagger pipeline, and uploads `models.tar`.
- A follow-up job uses `.github/actions/model-validator` to download the artifact and rerun `lead_conversion_prediction.modeling.predict`, catching any difference against the expected inference output.
- Pip caching and dependency isolation live inside the Dagger container, keeping CI runs aligned with local runs.

## Data and artifact management
- Raw data: `data/raw/raw_data.csv` tracked by DVC (`remote github`: https://github.com/Jeppe-T-K/itu-sdse-project-data).
- Interim: cleaned data and stats in `data/interim/` (`data_cleaned.csv`, `outlier_summary.csv`, `date_limits.json`, `columns_drift.json`).
- Processed: feature-complete datasets in `data/processed/` (including `X_test.csv` and `y_test.csv` for inference validation).
- Models: serialized models, scaler, and `columns_list.json` in `models/`; metrics in `reports/model_results.json`.

## Project layout (CCDS)
- `lead_conversion_prediction/`: versioned Python package so data prep, features, modeling, and utilities stay importable and testable.
- `data/`: raw, interim, processed, and external splits make lineage explicit and keep raw files immutable.
- `models/` and `reports/`: trained artifacts kept apart from evaluation outputs
- `dagger/`: containerized pipeline definition that enforces the single runtime used locally and in CI.
- `notebooks/`: exploratory analysis isolated from the production path.
- `tests/`: unit tests that validate transformation and storage contracts.

## Non-goals
- Online or batch serving
- Model monitoring or drift detection
- Hyperparameter optimization at scale

## Guide for safe extension
- Do not edit `data/raw/raw_data.csv` directly. Add new raw inputs through DVC and update `data/raw/raw_data.csv.dvc` if the source changes.
- Keep `lead_conversion_prediction.features` categorical columns and `bin_source` mapping in sync with any schema changes; rerun training to refresh `columns_list.json`.
- Inference validation expects the first five predictions on `data/processed/X_test.csv` to match `[0 1 0 1 0]`. If the reference data or model changes intentionally, update `lead_conversion_prediction.modeling.predict` and the CI validator together.
- When adding dependencies needed in the container, update both `requirements.txt` and `requirements-dagger.txt`.
- Always run `pytest` and `dagger call predict --source .` before shipping to make sure contracts and outputs still hold.
