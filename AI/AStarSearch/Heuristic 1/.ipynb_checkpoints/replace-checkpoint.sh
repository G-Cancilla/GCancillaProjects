#!/bin/bash

# Directory containing your input files
input_directory="/home/jovyan/Intro To Ai/OLA1/Heuristic 1"

for i in {0..99}; do
    input_file="$input_directory/a-star-1-$i.txt"
    
    if [ -f "$input_file" ]; then
        # Use sed to replace "Branching factor: " with "b = "
        sed -i 's/Branching factor: /b = /g' "$input_file"
        echo "Modified $input_file"
    fi
done