WriteCombo

This script generates all possible combinations of failure causes for a DFMEA (Design Failure Mode and Effects Analysis) scenario, calculates a "Complexity-Probability Index" for each combination, and exports the results to a CSV file.

Features
Generates all combinations of categorical variables (e.g., weather, road condition, slope, etc.).
Calculates a risk score for each combination based on provided complexity and probability values.
Outputs the results as a Pandas DataFrame and saves them to test_combinations.csv.
How It Works
Define Variables: Lists of possible values for each failure cause are defined in variable_values.
Define Names: The names of each variable are provided as a comma-separated string in variable_names_string.
Define Complexity & Probability: For each variable value, a tuple of (complexity, probability) is provided in complexity_probabilities.
Generate Combinations: The script uses itertools.product to generate all possible combinations.
Calculate Index: For each combination, the script multiplies the complexity and probability values across all variables to compute the "Complexity-Probability Index".
Export: The resulting table is saved as test_combinations.csv.
Usage
Ensure you have Python 3 and the required dependencies installed:

Run the script:

The output file test_combinations.csv will be created in the same directory.

Example Output
The script prints the first few rows of the generated table:

Customization
To use different variables or risk scoring, modify the variable_values, variable_names_string, and complexity_probabilities lists at the top of the script.

For questions or improvements, please open an issue or pull request.
