import math

# Function used to display the coins in a triangle format
def print_triangle(rows):
    max_width = len(' '.join(['🟡'] * len(rows[-1]["coins"]))) if rows else 0
    for row in rows:
        row_str = ' '.join(['🟡' for _ in row["coins"]])
        print(f"{row_str:^{max_width}} (Row {row['row_num']} - {row['type']})")


# Helper function to update types (Top, Middle, Bottom)
def update_row_types(rows):
    for idx, row in enumerate(rows):
        if idx == 0:
            row["type"] = "Top"
        elif idx == len(rows) - 1:
            row["type"] = "Bottom"
        else:
            row["type"] = "Middle"

# Helper function to print middle rows (for debugging)
def print_middle_rows(rows):
    print("\n🔵 Current Middle Rows:")
    for row in rows:
        if row["type"] == "Middle":
            print(f"Row {row['row_num']}: {row['coins']}")

# Main function to invert the triangle
def invert_coin_triangle():
    n = int(input("Enter number of rows (n ≥ 1): "))

    if n == 1:
        print("Already inverted (0 moves needed)")
        return 0

    T_n = n * (n + 1) // 2  # Total number of coins
    if n > 6:
        M_n = math.floor((T_n/ 3)+1)  # Expected moves (rounded down)
    else:
         M_n = math.floor(T_n/ 3)

    # Initialize triangle
    coins = list(range(1, T_n + 1))
    rows = []
    start = 0
    for i in range(1, n + 1):
        row_coins = coins[start:start + i]
        row_type = "Top" if i == 1 else ("Bottom" if i == n else "Middle")
        rows.append({"row_num": i, "coins": row_coins, "type": row_type})
        start += i

    # Save original sizes to compute target inverted structure
    original_row_sizes = {row["row_num"]: len(row["coins"]) for row in rows}
    target_sizes = {}

    original_order = list(original_row_sizes.values())
    inverted_order = original_order[::-1]

    # Map: current row number ➝ corresponding inverted size
    for idx, row in enumerate(rows):
        target_sizes[row["row_num"]] = inverted_order[idx]

    print("\nInitial triangle:")
    print_triangle(rows)

    move_count = 0
    target_first_row_size = n  # After inversion, top row should have n coins

    while True:
        if not rows:
            break

        if move_count == 0:
            # First move: slide top coin to bottom and shift remaining coins upwards
            print(f"\nMove {move_count + 1}: Slide top coin to bottom and shift remaining coins upwards")
            top_coin = rows[0]["coins"].pop(0)

            if not rows[0]["coins"]:
                empty_row = rows.pop(0)
            else:
                empty_row = None

            for row in rows:
                row["row_num"] -= 1

            if empty_row:
                empty_row["coins"] = [top_coin]
                empty_row["row_num"] = rows[-1]["row_num"] + 1 if rows else 1
                rows.append(empty_row)
            else:
                new_row_num = rows[-1]["row_num"] + 1 if rows else 1
                rows.append({"row_num": new_row_num, "coins": [top_coin], "type": "Bottom"})

            update_row_types(rows)
            print_triangle(rows)
            move_count += 1

        else:
            if len(rows[0]["coins"]) < target_first_row_size:
                print(f"\nMove {move_count + 1}: Slide coin from bottom-upper row to top row")
                coin_to_move = rows[-2]["coins"].pop(-1)
                rows[0]["coins"].append(coin_to_move)

                if not rows[-2]["coins"]:
                    rows.pop(-2)

                update_row_types(rows)
                print_triangle(rows)
                move_count += 1
            else:
                break

    print("\n🔧 Adjusting all rows to match target inverted structure...")

    while True:
        changed = False
        for row in rows:
            current_size = len(row["coins"])
            expected_size = target_sizes[row["row_num"]]

            if current_size < expected_size:
                # Find a donor row with excess coins
                donor = next((r for r in rows if len(r["coins"]) > target_sizes[r["row_num"]]), None)
                if donor:
                    coin_to_move = donor["coins"].pop()
                    row["coins"].append(coin_to_move)
                    move_count += 1
                    changed = True
                    update_row_types(rows)
                    print(f"\nMoved coin: Row {donor['row_num']} ➔ Row {row['row_num']}")
                    print_triangle(rows)
                    break

        if not changed:
            break

    print(f"\n✅ Total real moves made: {move_count}")
    print(f"🔸 Expected moves (Tn/3): {M_n}")

if __name__ == "__main__":
    invert_coin_triangle()
