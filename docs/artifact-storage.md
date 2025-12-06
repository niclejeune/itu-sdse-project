# Artifact Storage Strategy

This project ensures reproducibility by versioning both data and model artifacts.

## Storage Locations

### Processed Data
- **Location**: `data/processed/`
- **Versioning**: Tracked by DVC.
- **Description**: Cleaned and feature-engineered datasets ready for training.

### Model Artifacts
- **Location**: `models/`
- **Versioning**: Tracked by DVC.
- **Description**: Serialized model files (e.g., `.pkl`, `.json`) and other artifacts like scalers.

### Metadata & Metrics
- **Location**: `mlruns/` (local) or Remote MLflow Server.
- **Tool**: [MLflow](https://mlflow.org/).
- **Description**: Experiment tracking, including parameters, metrics, and run metadata.

## Usage
Use the `lead_conversion_prediction.utils.storage` module to save and load artifacts. This ensures paths are consistent with the configuration.

```python
from lead_conversion_prediction.utils.storage import save_model, load_model

# Save a model
save_model(model, "model.pkl")

# Load a model
model = load_model("model.pkl")
```
