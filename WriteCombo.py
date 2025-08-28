import itertools
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import csv

# 1. Select DFMEA Excel file
def select_dfmea_files():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = list(filedialog.askopenfilenames(
        title="Select DFMEA Excel Files", 
        filetypes=[("Excel files", "*.xlsx *.xls")]))
    return file_paths

# 2. Read DFMEA Excel file and find failure causes
def create_dict_dfmea_failure_causes(file_path):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        cause_col = "*Potential Cause(s)/ Mechanism(s) of Failure"
        rpn_col = "RPN"
        if cause_col not in df.columns or rpn_col not in df.columns:
            print(f"Error: Required columns not found in header.")
            return {}
        result = {}
        for cause, rpn in zip(df[cause_col], df[rpn_col]):
            result[cause] = rpn
        return result
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}