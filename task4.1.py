def brute_force(boxes, steps, results, history):
    # Base case: If no box has more than 1 penny, we add the current path to results
    if all(x < 2 for x in boxes):
        results.append((history[:], steps))  # Store the path and number of steps
        return

    # Try moving coins from every box
    for i in range(len(boxes) - 1):  # -1 to avoid index error (no "next box" after last)
        if boxes[i] >= 2:  # If the current box has 2 or more pennies
            new_state = boxes[:]  # Create a new state (copy of current boxes)
            new_state[i] -= 2  # Move 2 pennies from the current box
            new_state[i + 1] += 1  # Add 1 penny to the next box

            # Recursively explore the new state
            brute_force(new_state, steps + 1, results, history + [new_state])


def run_Pmachine_brute_force(n):
    boxes = [0] * (n + 1)  # Create a list of boxes
    boxes[0] = n  # Put all pennies in the first box
    results = []  # To store all possible results
    brute_force(boxes, 0, results, [boxes[:]])  # Start brute-force exploration
    return results


def min_boxes_used(final_results):
    # Find the minimum number of boxes used across all paths
    min_boxes = float('inf')
    for path, _ in final_results:
        # Count how many boxes have at least 1 penny
        non_empty_boxes = sum(1 for box in path[-1] if box > 0)
        min_boxes = min(min_boxes, non_empty_boxes)
    return min_boxes


def main():
    while True:
        try:
            n = int(input("How many pennies do you want to drop into the machine? "))
            if n < 0:
                print("Please enter a non-negative number.")
            else:
                break
        except ValueError:
            print("Please enter a valid whole number.")

    results = run_Pmachine_brute_force(n)

    print(f"\n--- Brute-force results for {n} pennies ---")
    for idx, (path, steps) in enumerate(results):
        print(f"\nResult {idx + 1} (Steps: {steps}):")
        for step_num, state in enumerate(path):
            print(f"  Step {step_num}: {state}")

    # Calculate the minimum number of boxes used across all paths
    min_boxes = min_boxes_used(results)
    print(f"\nMinimum number of boxes used: {min_boxes}")

    print(f"\nTotal unique paths explored: {len(results)}")


if __name__ == "__main__":
    main()
