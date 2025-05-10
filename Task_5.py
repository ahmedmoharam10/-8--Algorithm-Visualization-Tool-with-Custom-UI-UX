def solve_switch_puzzle(total_switches):
    # Start with all switches ON (1 = ON, 0 = OFF)
    switches = [1] * total_switches
    steps = [(0, switches.copy())]  # Step 0: initial state (0 means no switch flipped)

    def flip_switch(index):
        """
        Flip the switch at the given index while obeying these rules:
        - The immediate right switch must be ON
        - All switches further to the right must be OFF
        """
        if index < total_switches - 1:
            # Ensure the switch to the right is ON
            if switches[index + 1] == 0:
                flip_switch(index + 1)
            # Ensure all switches beyond that are OFF
            for j in range(index + 2, total_switches):
                if switches[j] == 1:
                    flip_switch(j)
            # If the conditions are still not met, retry this switch
            if switches[index + 1] == 0 or any(switches[j] for j in range(index + 2, total_switches)):
                flip_switch(index)
                return

        # Flip this switch
        switches[index] ^= 1  # 1 → 0 or 0 → 1
        steps.append((index + 1, switches.copy()))  # Record step (1-based switch number)

    def turn_off_switches(start, end):
        """
        Recursively turn OFF all switches in the range from start to end (inclusive).
        """
        if start > end:
            return

        if start == end:
            if switches[start] == 1:
                flip_switch(start)
            return

        mid = (start + end) // 2

        # First handle the right half to satisfy flipping conditions
        turn_off_switches(start, mid)
        turn_off_switches(mid + 1, end)

        # After recursion, ensure left half switches are OFF
        for i in range(start, mid + 1):
            if switches[i] == 1:
                flip_switch(i)

    # Start the divide-and-conquer toggle process
    turn_off_switches(0, total_switches - 1)

    return steps


# ----- Input and Output -----

num_switches = int(input("Enter number of switches: "))
solution_steps = solve_switch_puzzle(num_switches)

# Display each step
for i, (switch_num, state) in enumerate(solution_steps):
    state_str = " ".join("1" if s else "0" for s in state)
    if i == 0:
        print(f"Step {i}: Initial state         →    {state_str}")
    elif i > 0 and i < 10:
        print(f"Step {i}: Flipped switch {switch_num:<2}     →    {state_str}")
    else:
        print(f"Step {i}: Flipped switch {switch_num:<2}    →    {state_str}")

# Show total number of moves (excluding the initial state)
print(f"Minimum number of moves: {len(solution_steps) - 1}")
