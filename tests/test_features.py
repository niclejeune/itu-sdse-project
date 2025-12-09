import pandas as pd
import numpy as np
import pytest
from lead_conversion_prediction.features import impute_missing_values

def test_impute_missing_values_mean():
    s = pd.Series([1.0, 2.0, np.nan], dtype="float64")
    imputed = impute_missing_values(s, method="mean")
    assert imputed.isna().sum() == 0
    assert imputed[2] == 1.5

def test_impute_missing_values_median():
    s = pd.Series([1.0, 100.0, np.nan], dtype="float64")
    imputed = impute_missing_values(s, method="median")
    assert imputed[2] == 50.5 

def test_impute_missing_values_categorical_mode():
    s = pd.Series(["a", "a", "b", np.nan], dtype="object")
    imputed = impute_missing_values(s) 
    assert imputed[3] == "a"
