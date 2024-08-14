#!/bin/bash

# Directory containing your input files
input_directory="/home/jovyan/Intro To Ai/OLA1/Heuristic 2"

# Output file where consolidated data will be saved
output_file="consolidated_data.txt"

# Initialize variables to store values
v_values=""
n_values=""
d_values=""
branching_factor_values=""

# Loop through files from a-star-3-0.txt to a-star-3-99.txt
for i in {0..99}; do
    file="$input_directory/a-star-2-$i.txt"
    if [ -f "$file" ]; then
        while IFS= read -r line; do
            if [[ "$line" == "V="* ]]; then
                v_values+="${line#*=},"
            elif [[ "$line" == "N="* ]]; then
                n_values+="${line#*=},"
            elif [[ "$line" == "d="* ]]; then
                d_values+="${line#*=},"
            elif [[ "$line" == "Branching factor:"* ]]; then
                branching_factor_values+="${line#*:},"
            fi
        done < "$file"
    fi
done

# Remove trailing commas
v_values="${v_values%,}"
n_values="${n_values%,}"
d_values="${d_values%,}"
branching_factor_values="${branching_factor_values%,}"

# Write consolidated data to the output file
echo "V=$v_values" > "$output_file"
echo "N=$n_values" >> "$output_file"
echo "d=$d_values" >> "$output_file"
echo "Branching factor=$branching_factor_values" >> "$output_file"

echo "Consolidated data saved to $output_file"
