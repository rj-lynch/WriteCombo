from WriteCombo import (
    select_dfmea_files, 
    create_dict_dfmea_failure_causes, 
    create_combinations, 
    calculate_index, 
    write_test_spec_to_csv,
    find_header_indices
)
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

def test_find_header_indices(tmp_path):
    # Create a DataFrame with headers not in the first row
    data = [
        [None, None, None],
        [None, None, None],
        ['*Potential Cause(s)/ Mechanism(s) of Failure', None, 'R.P.N.'],
        ['Cause 1', None, 5],
        ['Cause 2', None, 3],
    ]
    file_path = tmp_path / "header_test.xlsx"
    pd.DataFrame(data).to_excel(file_path, index=False, header=False)
    header_row, cause_col_idx, rpn_col_idx = find_header_indices(str(file_path))
    assert header_row == 2
    assert cause_col_idx == 0
    assert rpn_col_idx == 2

def test_create_dict_dfmea_failure_causes(tmp_path):
    # Create temp data for Excel
    df = pd.DataFrame({
        '*Potential Cause(s)/ Mechanism(s) of Failure': ['Cause 1', 'Cause 2', 'Cause 3', 'Cause 4', 'Cause 5', 'Cause 6', 'Cause 7', 'Cause 8', 'Cause 9'],
        'R.P.N.': [5, 3, 5, 8, 5, 3, 8, 8, 8]
    })
    file_path = tmp_path / "temp_dfmea.xlsx"
    df.to_excel(file_path, index=False)

    # Find header indices using the new helper
    header_row, cause_col_idx, rpn_col_idx = find_header_indices(str(file_path))
    header = (header_row, cause_col_idx, rpn_col_idx)
    # Call the function to test with new signature
    result = create_dict_dfmea_failure_causes(str(file_path), header)

    # Build expected dict as function returns
    expected = {'Cause 1': 5, 'Cause 2': 3, 'Cause 3': 5, 'Cause 4': 8, 'Cause 5': 5, 'Cause 6': 3,'Cause 7': 8, 'Cause 8': 8, 'Cause 9': 8}

    assert result == expected

def test_create_combinations():
    failure_causes = {'Cause 1': 5, 'Cause 2': 3, 'Cause 3': 5}
    result = create_combinations(failure_causes)

    expected = [
        (('Boundary', 0.2), ('Cause 1', 5)),
        (('Boundary', 0.2), ('Cause 2', 3)),
        (('Boundary', 0.2), ('Cause 3', 5)),
        (('Robust', 0.3), ('Cause 1', 5)),
        (('Robust', 0.3), ('Cause 2', 3)),
        (('Robust', 0.3), ('Cause 3', 5)),
        (('State', 0.1), ('Cause 1', 5)),
        (('State', 0.1), ('Cause 2', 3)),
        (('State', 0.1), ('Cause 3', 5)),
        (('Error', 0.4), ('Cause 1', 5)),
        (('Error', 0.4), ('Cause 2', 3)),
        (('Error', 0.4), ('Cause 3', 5))
    ]

    assert list(result) == expected

def test_calculate_index():
    failure_causes = {'Cause 1': 5, 'Cause 2': 3, 'Cause 3': 5}
    combos = create_combinations(failure_causes)
    result = calculate_index(combos)

    expected = [
        (2.0, 'Error-Cause 1'),
        (2.0, 'Error-Cause 3'),
        (1.5, 'Robust-Cause 1'),
        (1.5, 'Robust-Cause 3'),
        (1.2, 'Error-Cause 2'),
        (1.0, 'Boundary-Cause 1'),
        (1.0, 'Boundary-Cause 3'),
        (0.9, 'Robust-Cause 2'),
        (0.6, 'Boundary-Cause 2'),
        (0.5, 'State-Cause 1'),
        (0.5, 'State-Cause 3'),
        (0.3, 'State-Cause 2')
    ]

    # Compare floats with tolerance using pytest.approx
    for (res_val, res_str), (exp_val, exp_str) in zip(result, expected):
        assert res_str == exp_str
        assert res_val == pytest.approx(exp_val)
    
def test_write_test_spec_to_csv(tmp_path):
    test_spec = [
            (2.0, 'Error-Cause 1'),
            (1.5, 'Robust-Cause 1'),
            (1.0, 'Boundary-Cause 1')
    ]
    os.chdir(tmp_path)
    write_test_spec_to_csv(test_spec)
    file_path = tmp_path / "test_specification.csv"
    assert file_path.exists()
    with open(file_path, 'r') as f:
        lines = f.readlines()
    assert lines[0].strip() == 'Index,Test Case'
    assert lines[1].strip() == '2.0,Error-Cause 1'
    assert lines[2].strip() == '1.5,Robust-Cause 1'
    assert lines[3].strip() == '1.0,Boundary-Cause 1'
    assert len(lines) == 4