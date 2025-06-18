Script to find all combinations of failure causes identified in DFMEA
function combinationsTable = createCombinationTable(variableValues, variableNamesString)
% Generates all combinations of string variables and creates a table.
% Takes a string to specify variable names.
variableValues = { ["Clear", "Windy", "Rainy","Snowy"], ["Icy", "Wet", "Loose","Dry"], ["5%","10%","20%"], ["Oversensitive","Undersensitive","Normal"], ["Worn", "Normal"],["Unladen","Max GVM distributed", "Max GVM at rear","Max GVM at front"],[ "Normal", "Worn"], ["Critical", "Normal"],["Correct", "Wrong Tires", "Wrong  Brakes"]};
variableNamesString = 'Weather,Road Condition,Slope,Sensitivity,Tire Condition,Load,Brake Condition,Battery,Tire/Brake Status';
numVariables = length(variableValues);
numCombinations = prod(cellfun(@length, variableValues));

% Pre-allocate a cell array to store string combinations
combinations = cell(numCombinations, numVariables);

% Generate combinations (unchanged from previous versions)
k = 1;
indices = ones(1, numVariables);
while k <= numCombinations
    for j = 1:numVariables
        combinations{k, j} = variableValues{j}{indices(j)};
    end
    
    indices(end) = indices(end) + 1;
    for j = numVariables:-1:1
        if indices(j) > length(variableValues{j})
            indices(j) = 1;
            if j > 1
                indices(j-1) = indices(j-1) + 1;
            end
        end
    end
    k = k + 1;
end

% Parse variable names from the input string
variableNames = strsplit(variableNamesString, ','); %splits by comma
variableNames = strtrim(variableNames); %removes leading/trailing spaces


% Check for errors in the number of variable names
if length(variableNames) ~= numVariables
    error('Number of variable names in the string must match the number of variables in variableValues.');
end

% Create a table
combinationsTable = array2table(combinations, 'VariableNames', variableNames);

% Example usage:
disp(combinationsTable(1:min(100, height(combinationsTable)),:));

end