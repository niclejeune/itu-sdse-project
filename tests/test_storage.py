import os
import pytest
from unittest.mock import patch
from lead_conversion_prediction.utils.storage import save_model, load_model, save_data

class DummyModel:
    def __init__(self, val):
        self.val = val

def test_save_model_creates_file(tmp_path):
    model = DummyModel(1)
    filename = "test_model.pkl"
    path = save_model(model, filename, model_dir=tmp_path)
    assert os.path.exists(path)
    assert path == str(tmp_path / filename)

def test_save_model_creates_directory(tmp_path):
    model = DummyModel(1)
    new_dir = tmp_path / "subdir"
    filename = "test_model.pkl"
    path = save_model(model, filename, model_dir=new_dir)
    assert os.path.exists(new_dir)
    assert os.path.exists(path)

@patch("lead_conversion_prediction.utils.storage.get_model_path")
def test_load_model_returns_object(mock_path, tmp_path):
    model = DummyModel(42)
    filename = "test_model_load.pkl"
    full_path = tmp_path / filename
    
    import joblib
    joblib.dump(model, full_path)
    
    mock_path.return_value = str(full_path)
    loaded = load_model(filename)
    assert loaded.val == 42

@patch("lead_conversion_prediction.utils.storage.get_model_path")
def test_load_model_raises_file_not_found(mock_path, tmp_path):
    mock_path.return_value = str(tmp_path / "nonexistent.pkl")
    with pytest.raises(FileNotFoundError):
        load_model("nonexistent.pkl")

def test_save_data_csv(tmp_path):
    import pandas as pd
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    filename = "test_data.csv"
    
    with patch("lead_conversion_prediction.utils.storage.get_processed_data_path") as mock_path:
        full_path = str(tmp_path / filename)
        mock_path.return_value = full_path
        
        saved_path = save_data(df, filename)
        
        assert saved_path == full_path
        assert os.path.exists(full_path)
        pd.testing.assert_frame_equal(df, pd.read_csv(full_path))
