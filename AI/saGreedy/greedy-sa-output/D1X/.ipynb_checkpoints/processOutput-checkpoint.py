output_file = "Conclusion-1-100.txt"
greedy_file = "greedy1_100_output.txt"
sa_file = "SA-1-100-output.txt"

# Initialize counters
sa_wins = 0
g_wins = 0
ties = 0

# Clear the output file if it exists
with open(output_file, 'w') as f:
    pass

# Open the input files
with open(greedy_file, 'r') as f_greedy, open(sa_file, 'r') as f_sa:
    for line_greedy, line_sa in zip(f_greedy, f_sa):
        greedy_values = line_greedy.split()
        sa_values = line_sa.split()
        
        greedy_y = float(greedy_values[1])
        sa_y = float(sa_values[1])
        difference = abs(greedy_y - sa_y)
        
        if greedy_y > sa_y:
            winner = 'Winner: G'
            g_wins += 1
        elif sa_y > greedy_y:
            winner = 'Winner: SA'
            sa_wins += 1
        else:
            winner = 'Winner: ='
            ties += 1

        conclusion = f'G: {greedy_y}, SA: {sa_y}, diff: {difference}, {winner}'

        with open(output_file, 'a') as f_out:
            f_out.write(conclusion + '\n')

# Print the counts at the end
with open(output_file, 'a') as f_out:
    f_out.write(f"SA wins: {sa_wins}, G wins: {g_wins}, Ties: {ties}\n")
