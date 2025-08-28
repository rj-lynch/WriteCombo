from WriteCombo import select_dfmea_files, create_dict_dfmea_failure_causes
import pytest
import pandas as pd
import os

def test_select_dfmea_file(mocker):
    expected_paths = ['C:/path/to/my_file.xlsx', 'D:/another/path/second.xls']
    mock_ask = mocker.patch('WriteCombo.filedialog.askopenfilenames', return_value=tuple(expected_paths))
    mock_tk = mocker.patch('WriteCombo.tk.Tk')
    mock_tk.return_value.withdraw = mocker.Mock()

    result = select_dfmea_files()

    assert result == expected_paths
    mock_ask.assert_called_once_with(
        title="Select DFMEA Excel Files",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    mock_tk.assert_called_once()
    mock_tk.return_value.withdraw.assert_called_once()

def test_select_feature_file_cancelled(mocker):
    mock_ask = mocker.patch('WriteCombo.filedialog.askopenfilenames', return_value=())
    mock_tk = mocker.patch('WriteCombo.tk.Tk')
    mock_tk.return_value.withdraw = mocker.Mock()

    result = select_dfmea_files()

    assert result == []
    mock_ask.assert_called_once_with(
        title="Select DFMEA Excel Files",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    mock_tk.assert_called_once()
    mock_tk.return_value.withdraw.assert_called_once()

def test_create_dict_dfmea_failure_causes(tmp_path):
    # Create temp data for Excel
    df = pd.DataFrame({
        '*Potential Cause(s)/ Mechanism(s) of Failure': ['Cause 1', 'Cause 2', 'Cause 3', 'Cause 4', 'Cause 5', 'Cause 6', 'Cause 7', 'Cause 8', 'Cause 9'],
        'RPN': [5, 3, 5, 8, 5, 3, 8, 8, 8]
    })
    file_path = tmp_path / "temp_dfmea.xlsx"
    df.to_excel(file_path, index=False)

    # Call the function to test
    result = create_dict_dfmea_failure_causes(str(file_path))

    # Build expected dict as function returns
    expected = {'Cause 1': 5, 'Cause 2': 3, 'Cause 3': 5, 'Cause 4': 8, 'Cause 5': 5, 'Cause 6': 3,'Cause 7': 8, 'Cause 8': 8, 'Cause 9': 8}

    assert result == expected