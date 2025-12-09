import pandas as pd
import numpy as np
import pytest
from lead_conversion_prediction.dataset import describe_numeric_col

def test_describe_numeric_col_stats():
    s = pd.Series([1, 2, 3, 4, 5])
    res = describe_numeric_col(s)
    assert res["Count"] == 5
    assert res["Mean"] == 3.0
    assert res["Min"] == 1
    assert res["Max"] == 5

def test_describe_numeric_col_handling_nans():
    s = pd.Series([1, 2, np.nan])
    res = describe_numeric_col(s)
    assert res["Count"] == 2
