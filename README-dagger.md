# Dagger Pipeline

Containerized ML pipeline using [Dagger](https://dagger.io/).

## Requirements

- Dagger CLI v0.19+ (`curl -fsSL https://dl.dagger.io/dagger/install.sh | sh`)
- Docker running

## Usage

```bash
# Full pipeline: features -> train -> package
dagger call pipeline --source .

# Export model tarball locally
dagger call pipeline --source . export --path ./models.tar

# Run individual steps
dagger call prepare-data --source .  # feature engineering
dagger call train --source .         # model training
dagger call predict --source .       # inference
```

## How it works

The pipeline chains these steps:

1. `PrepareData` - runs `features.py` (imputation, scaling)
2. `Train` - runs `train.py` (XGBoost + LogReg)
3. `Package` - creates `models.tar`
4. `Upload` - returns the tarball

## Files

```
dagger/
├── main.go       # entry point
├── pipeline.go   # pipeline functions
└── .gitignore    # ignores generated code

dagger.json              # module config
requirements-dagger.txt  # minimal deps (no mlflow)
```

## Notes

- Uses `requirements-dagger.txt` to avoid slow mlflow install
- Pip packages are cached between runs
- Large dirs (venv, .git) are excluded via `+ignore` directive
