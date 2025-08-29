WriteCombo

This script processes DFMEA (Design Failure Mode and Effects Analysis) Excel files, extracts failure causes and their RPN (Risk Priority Number) values, generates all possible test case combinations, calculates a test index for each, and exports the results to a CSV file.

Features
- Selects one or more DFMEA Excel files via a file dialog.
- Automatically detects the header row and the columns for failure cause and RPN, even if their position varies.
- Builds a dictionary mapping each unique failure cause to its RPN.
- Generates all combinations of test case types and failure causes.
- Calculates a test index for each combination (case weight × RPN).
- Outputs the results to 'test_specification.csv'.

How It Works
1. **File Selection:** The script prompts you to select one or more Excel files containing DFMEA data.
2. **Header Detection:** It scans the first 20 rows of each file to find the header row and the columns for failure cause and RPN, robust to line breaks and whitespace.
3. **Dictionary Creation:** For each file, it creates a dictionary mapping each failure cause to its RPN value.
4. **Combination Generation:** It creates all combinations of predefined test case types and the extracted failure causes.
5. **Index Calculation:** For each combination, it multiplies the test case weight by the RPN to compute a test index.
6. **Export:** The results are saved as 'test_specification.csv' in the same directory.

Usage
1. Ensure you have Python 3 and the required dependencies installed (pandas, openpyxl).
2. Run the script:
	```
	python WriteCombo.py
	```
3. Select the desired DFMEA Excel files when prompted.
4. The output file 'test_specification.csv' will be created in the same directory.

Customization
- To change the test case types or their weights, edit the `cases` dictionary in the `create_combinations` function.
- The script is robust to different header row positions and column orders in your Excel files.

For questions or improvements, please open an issue or pull request.
