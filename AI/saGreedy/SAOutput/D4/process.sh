#!/bin/bash

# Output file
output_file="SA-4-100-output.txt"

# Remove the output file if it already exists
rm -f "$output_file"

# Loop through files
for i in {0..99}
do
    filename="SA-4-100-$i.txt"
    
    # Check if the file exists
    if [ -f "$filename" ]; then
        # Get the last line of the file (excluding empty lines)
        last_line=$(sed -e '/^$/d' "$filename" | tail -n 1)
        
        # Append the last line to the output file with a corresponding number in parentheses
        echo -e "$last_line\t($i)" >> "$output_file"
    fi
done
