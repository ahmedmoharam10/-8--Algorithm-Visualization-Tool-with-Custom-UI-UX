from collections import deque

def bfs_algorithm():
    # Pegs are 0-indexed: 0=Source, 1=Intermediate1, 2=Intermediate2, 3=Destination
    initial_state = [[8, 7, 6, 5, 4, 3, 2, 1], [], [], []]
    desired_state = [[], [], [], [8, 7, 6, 5, 4, 3, 2, 1]]

    visited = set()
    queue = deque()
    queue.append((initial_state, []))

    while queue:
        current_state, moves = queue.popleft()
        state = tuple(tuple(peg) for peg in current_state)

        if state in visited:
            continue
        visited.add(state)

        if current_state == desired_state:
            return moves

        for src in range(4): #(0 to 3)
            if not current_state[src]:
                continue
            top_disk = current_state[src][-1]

            for dest in range(4):
                if src == dest:
                    continue 

                if current_state[dest] and current_state[dest][-1] <= top_disk:
                    continue

                new_state = [list(peg) for peg in current_state]
                new_state[dest].append(new_state[src].pop())

                new_moves = moves + [(src, dest, top_disk)]
                queue.append((new_state, new_moves))

    return None

solution_moves = bfs_algorithm()

if solution_moves:
    peg_names = {
        0: "A",
        1: "B",
        2: "C",
        3: "D"
    }
    print(f"\n4-peg Tower of Hanoi solution for 8 disks:")
    for i, (src, dest, disk) in enumerate(solution_moves, 1):
        print(f"Move {i}: {peg_names[src]} --> {peg_names[dest]}")

    print(f"\nOptimal number of moves: {len(solution_moves)}")