# Data Sourcing Strategy

This project uses [DVC (Data Version Control)](https://dvc.org/) to manage large datasets and ensure reproducibility.

## Data Storage
Data is stored in a remote storage configured via DVC. The current remote is configured to pull data from a GitHub repository (acting as a DVC remote or external source).

## Directory Structure
The `data` directory is organized as follows:
- `data/raw`: Original, immutable data dump.
- `data/processed`: The final, canonical data sets for modeling.
- `data/interim`: Intermediate data that has been transformed.
- `data/external`: Data from third party sources.

## How to Fetch Data
To fetch the latest version of the data, run the following command in the project root:

```bash
dvc pull
```

This command will download the data files tracked by `.dvc` files into your local `data` directory.

## Configuration
Data paths and other configurations are managed in `config.yaml`. Avoid hardcoding paths in your scripts; instead, read them from this configuration file.
