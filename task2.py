def is_valid_move(board, from_idx, over_idx, to_idx):
    return (
        0 <= from_idx < len(board)
        and 0 <= over_idx < len(board)
        and 0 <= to_idx < len(board)
        and board[from_idx] == 'P'
        and board[over_idx] == 'P'
        and board[to_idx] == '_'
    )

def apply_move(board, from_idx, over_idx, to_idx):
    new_board = board[:]
    new_board[from_idx] = '_'
    new_board[over_idx] = '_'
    new_board[to_idx] = 'P'
    return new_board

def solve_all(board, path, solutions):
    if board.count('P') == 1:
        solutions.append((path + [board], board.index('P')))
        return

    for i in range(len(board)):
        # Right jump
        if is_valid_move(board, i, i + 1, i + 2):
            new_board = apply_move(board, i, i + 1, i + 2)
            solve_all(new_board, path + [board], solutions)

        # Left jump
        if is_valid_move(board, i, i - 1, i - 2):
            new_board = apply_move(board, i, i - 1, i - 2)
            solve_all(new_board, path + [board], solutions)

def analyze_all_initial_positions(n):
    results = {}
    all_solutions = {}

    for empty in range(n):
        board = ['P'] * n
        board[empty] = '_'
        solutions = []
        solve_all(board, [], solutions)
        
        if solutions:
            final_positions = list(set(sol[1] for sol in solutions))
            results[empty] = final_positions
            all_solutions[empty] = solutions
    return results, all_solutions

def display_board(board):
    return ' '.join(board)

def main():
    n = int(input("Enter an even number of cells (greater than 2): "))
    if n <= 2 or n % 2 != 0:
        print("Invalid input. Must be even and greater than 2.")
        return

    print(f"\nAnalyzing all initial positions for n = {n}...\n")
    results, all_solutions = analyze_all_initial_positions(n)

    if not results:
        print("No solvable initial positions found.")
    else:
        print("\nSummary of solvable positions and final peg locations:")
        for empty_pos, final_positions in sorted(results.items()):
            print(f"Initial empty at {empty_pos}: can end at {final_positions}")

        print("\nStep-by-step solutions for each valid starting position:")
        for empty_pos, solutions in sorted(all_solutions.items()):
            print(f"\nInitial empty at position {empty_pos}:")
            for idx, (path, final_pos) in enumerate(solutions, 1):
                print(f"  Solution {idx}: Final peg at {final_pos}")
                for step_num, board in enumerate(path + [['_']*n], 1):
                    print(f"    Step {step_num:2d}: {display_board(board)}")
                print()

        print("\nFinal summary:")
        print(f"Total solvable initial positions: {len(results)} / {n}")
        all_final_positions = sorted(set().union(*results.values()))
        print(f"All possible final positions: {all_final_positions}")

if __name__ == "__main__":
    main()
