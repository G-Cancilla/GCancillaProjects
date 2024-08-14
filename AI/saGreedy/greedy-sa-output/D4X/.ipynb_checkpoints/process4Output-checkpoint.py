output_file = "Conclusion-4-100.txt"
greedy_file = "greedy4_100_output.txt"
sa_file = "SA-4-100-output.txt"

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

        # Extract the numbers before the seed
        greedy_value = float(greedy_values[-2])  # The second-to-last value
        sa_value = float(sa_values[-2])  # The second-to-last value
        difference = abs(greedy_value - sa_value)

        if greedy_value > sa_value:
            winner = 'Winner: G'
            g_wins += 1
        elif sa_value > greedy_value:
            winner = 'Winner: SA'
            sa_wins += 1
        else:
            winner = 'Winner: ='
            ties += 1

        conclusion = f'G: {greedy_value}, SA: {sa_value}, diff: {difference}, {winner}'

        with open(output_file, 'a') as f_out:
            f_out.write(conclusion + '\n')

# Print the counts at the end
with open(output_file, 'a') as f_out:
    f_out.write(f"SA wins: {sa_wins}, G wins: {g_wins}, Ties: {ties}\n")