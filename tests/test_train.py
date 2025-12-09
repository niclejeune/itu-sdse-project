import pandas as pd
import pytest
from lead_conversion_prediction.modeling.train import create_dummy_cols

def test_create_dummy_cols_encoding():
    df = pd.DataFrame({"col": ["A", "B", "A"]})
    res = create_dummy_cols(df, "col")
    assert "col_B" in res.columns
    assert "col_A" not in res.columns
    assert res.iloc[0]["col_B"] == 0
    assert res.iloc[1]["col_B"] == 1

def test_create_dummy_cols_drops_original():
    df = pd.DataFrame({"col": ["A", "B"], "other": [1, 2]})
    res = create_dummy_cols(df, "col")
    assert "col" not in res.columns
    assert "other" in res.columns
