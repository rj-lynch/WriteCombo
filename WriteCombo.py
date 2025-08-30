import itertools
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import csv

# 1. Select DFMEA Excel file
def select_dfmea_files():
    """
    Open a file dialog to select one or more DFMEA Excel files and return their file paths as a list.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = list(filedialog.askopenfilenames(
        title="Select DFMEA Excel Files", 
        filetypes=[("Excel files", "*.xlsx *.xls")]))
    return file_paths

# 2. Find header indices
def find_header_indices(file_path):
    """
    Scan the first 20 rows of the Excel file to find the row and column indices for
    the '*Potential Cause(s)/Mechanism(s) of Failure' and 'RPN' headers.
    Returns a tuple: (header_row, cause_col_idx, rpn_col_idx).
    """
    preview = pd.read_excel(file_path, engine='openpyxl', header=None, nrows=20)
    cause_col_idx = rpn_col_idx = header_row = None
    rpn_found = False
    for i, row in preview.iterrows():
        for j, val in enumerate(row):
            val_str = str(val).replace('\n', '').replace(' ', '').lower() # Remove spaces, newlines and case
            if val_str == "*potentialcause(s)/mechanism(s)offailure":
                cause_col_idx, header_row = j, i
            if not rpn_found and (val_str == "r.p.n." or val_str == "rpn"):
                rpn_col_idx = j
                rpn_found = True
    header = (header_row, cause_col_idx, rpn_col_idx)
    return header

# 3 Create dictionary of failure causes and RPNs
def create_dict_dfmea_failure_causes(file_path, header):
    """
    Create a dictionary mapping failure causes to their RPN values from the Excel file,
    using the provided header indices. Returns a dict {cause: rpn}.
    """
    if header[0] is None or header[1] is None or header[2] is None:
        print(f"Error: Required columns not found in any of the first 20 rows.")
        return {}
        # Read the data, skipping rows before the header
    df = pd.read_excel(file_path, engine='openpyxl', header=None, skiprows=header[0]+1)
    failure_causes = {}
    for _, row in df.iterrows():
        cause = row[header[1]]
        rpn = row[header[2]]
        if pd.isna(cause) or pd.isna(rpn):
            continue
        failure_causes[cause] = rpn
    return failure_causes
    
# 4. Create combinations of failure causes
def create_combinations(failure_causes):
    """
    Generate all combinations of predefined test cases and failure causes.
    Returns an iterator of ((case, case_weight), (cause, rpn)) tuples.
    """
    cases = {"Boundary": 0.2, "Robust": 0.3, "State": 0.1, "Error": 0.4}
    combos = itertools.product(cases.items(),failure_causes.items())
    return combos

# 5. Calculate index and generate test specification
def calculate_index(combos):
    """
    Calculate an index for each test case/failure cause combination and generate
    a sorted test specification list. Returns a list of (index, test_case) tuples.
    """
    test_spec = []
    for combo in combos:
        index = (combo[0][1] * combo[1][1])
        test_case = (f"{combo[0][0]}-{combo[1][0]}")
        test_spec.append((index, test_case))
    test_spec.sort(reverse=True, key=lambda x: x[0])
    return test_spec

# 6. Write test specification to CSV file
def write_test_spec_to_csv(test_spec):
    """
    Write the test specification (index and test case) to a CSV file named 'test_specification.csv'.
    """
    with open('test_specification.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Test Case'])
        for row in test_spec:
            writer.writerow(row)
    print("Test specification written to test_specification.csv")

# Main execution
if __name__ == "__main__":
    file_paths = select_dfmea_files()
    all_failure_causes = {}
    for file_path in file_paths:
        header = find_header_indices(file_path)
        failure_causes = create_dict_dfmea_failure_causes(file_path, header)
        all_failure_causes.update(failure_causes)
    if not all_failure_causes:
        print("No failure causes found. Exiting.")
    else:
        combos = create_combinations(all_failure_causes)
        test_spec = calculate_index(combos)
        write_test_spec_to_csv(test_spec)