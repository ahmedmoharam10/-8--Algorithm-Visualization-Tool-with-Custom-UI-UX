def hanoi4(n, peg_source, peg_intermediate1, peg_intermediate2, peg_dest):
    if n == 0:
        return 0

    if n == 1:
        print('{} --> {}'.format(peg_source,peg_dest))
        return 1

    if n == 2:
        print('{} --> {}'.format(peg_source, peg_intermediate1))
        print('{} --> {}'.format(peg_source, peg_dest))
        print('{} --> {}'.format(peg_intermediate1, peg_dest))
        return 3

    total_moves = 0
    total_moves += hanoi4(n - 2, peg_source, peg_intermediate2, peg_dest, peg_intermediate1)
    print('{} --> {}'.format(peg_source,peg_intermediate2))
    print('{} --> {}'.format(peg_source, peg_dest))
    print('{} --> {}'.format(peg_intermediate2, peg_dest))
    total_moves += 3
    total_moves += hanoi4(n - 2, peg_intermediate1, peg_source, peg_intermediate2, peg_dest)
    return total_moves

while True:
    try:
        num_disks = int(input("Enter the number of disks (non-negative integer): "))
        if num_disks < 0:
            print("Please enter a non-negative integer.")
            continue
        break
    except ValueError:
        print("Invalid input. Enter a valid integer.")

print(f'\n4-peg Tower of Hanoi solution for {num_disks} disks:')
result = hanoi4(num_disks, 'A', 'B', 'C', 'D')
print(f'\nTotal number of moves: {result}')