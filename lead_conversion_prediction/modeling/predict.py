"""Model inference - loads best model and makes predictions."""
from pathlib import Path
import pandas as pd
import typer
import joblib
from loguru import logger
from lead_conversion_prediction.config import MODELS_DIR, TEST_X_PATH, TEST_Y_PATH

app = typer.Typer()


@app.command()
def main(
    model_path: Path = MODELS_DIR / "lead_model_xgboost.pkl",
    features_path: Path = TEST_X_PATH,
    labels_path: Path = TEST_Y_PATH,
):
    """Perform inference using the best model."""
    logger.info("Starting model inference...")
    
    # Load the XGBoost model
    model = joblib.load(model_path)
    logger.info(f"Loaded model from {model_path}")
    
    # Load test data
    X = pd.read_csv(features_path)
    y = pd.read_csv(labels_path)
    logger.info(f"Loaded test data: {len(X)} samples")
    
    # Make predictions on first 5 rows
    predictions = model.predict(X.head(5))
    actual = y.head(5)
    
    # Print results in the expected format
    # Print results in the expected format
    print(predictions, "   lead_indicator")
    print(actual.to_string(header=False))

    # Validation Logic
    expected_predictions = "[0 1 0 1 0]"
    expected_actual = """0  0.0
1  1.0
2  0.0
3  1.0
4  0.0"""

    actual_predictions_str = str(predictions)
    actual_actual_str = actual.to_string(header=False)

    import sys
    
    if actual_predictions_str.strip() != expected_predictions.strip():
        logger.error("Validation Failed: Predictions do not match expected output.")
        print(f"EXPECTED PREDICTIONS:\n{expected_predictions}")
        print(f"ACTUAL PREDICTIONS:\n{actual_predictions_str}")
        sys.exit(1)

    if actual_actual_str.strip() != expected_actual.strip():
        logger.error("Validation Failed: Actual values do not match expected output.")
        print(f"EXPECTED ACTUAL:\n{expected_actual}")
        print(f"ACTUAL ACTUAL:\n{actual_actual_str}")
        sys.exit(1)
    
    logger.success("Inference complete!")


if __name__ == "__main__":
    app()
