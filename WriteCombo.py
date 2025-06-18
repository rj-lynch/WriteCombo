import itertools
import pandas as pd

# Generates all combinations of variables and calculates complexity*probability score for each combination.
def create_combination_table(variable_values, variable_names_string, complexity_probabilities):
      
    # Parse variable names from the input string
    variable_names = [name.strip() for name in variable_names_string.split(',')]

    # Generate all combinations using itertools.product
    combinations = list(itertools.product(*variable_values))

    # Check if the lengths of variable_values and complexity_probabilities match
    if len(variable_values) != len(complexity_probabilities):
        raise ValueError("The number of variables in variable_values and complexity_probabilities must match.")

    # Check if the lengths of inner lists match
    for i in range(len(variable_values)):
        if len(variable_values[i]) != len(complexity_probabilities[i]):
            raise ValueError(f"The number of values for variable {variable_names[i]} in variable_values and complexity_probabilities must match.")

    # Calculate Risk Score for each combination
    risk_scores = []
    for combination_index, combination in enumerate(combinations):
        risk_score = 1  # Initialize with 1 for multiplicative accumulation
        for variable_index, value in enumerate(combination):
            # Find the index of the value in the corresponding variable's list
            value_index = variable_values[variable_index].index(value)

            # Multiply the complexity and probability and accumulate
            complexity, probability = complexity_probabilities[variable_index][value_index]
            risk_score *= (complexity * probability)

        risk_scores.append(risk_score)

    # Create a Pandas DataFrame
    combinations_df = pd.DataFrame(combinations, columns=variable_names)

    # Add the Risk Score column
    combinations_df['Complexity-Probability Index'] = risk_scores
    return combinations_df


# Failure causes from DFMEA
variable_values = [
    ["Clear", "Windy", "Rainy", "Snowy"],
    ["Icy", "Wet", "Loose", "Dry"],
    ["5%", "10%", "20%"],
    ["Oversensitive", "Undersensitive", "Normal"],
    ["Worn", "Normal"],
    ["Unladen", "Max GVM distributed", "Max GVM at rear", "Max GVM at front"],
    ["Normal", "Worn"],
    ["Critical", "Normal"]
]

# Categories for each failure cause
variable_names_string = 'Weather,Road Condition,Slope,Sensitivity,Tire Condition,Load,Brake Condition,Battery'

# Severity and occurence from DFMEA
complexity_probabilities = [
    [(1, 10), (10, 10), (10, 10), (10, 7)],  # Weather
    [(10, 9), (10, 8), (10, 7), (1, 10)],  # Road Condition
    [(1, 10), (10, 9), (10, 7)],  # Slope
    [(1, 8), (10, 8), (10, 10)],  # Sensitivity
    [(10, 10), (1, 9)],  # Tire Condition
    [(1, 10), (9, 10), (10, 9), (9, 9)],  # Load
    [(1, 9), (10, 10)],  # Brake Condition
    [(10, 9), (1, 10)]  # Battery
]


combinations_table = create_combination_table(variable_values, variable_names_string, complexity_probabilities)

# Print the first few rows of the table (optional)
print(combinations_table.head())

# Saves the table to a CSV file
combinations_table.to_csv("test_combinations.csv", index=False)