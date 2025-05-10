from collections import deque

rows, columns = 4,3

starting_position = {
    'B':[(0, 0), (0, 1), (0, 2)],
    'W':[(3, 0), (3, 1), (3, 2)]
}

ending_position = {
    'B':[(3, 0), (3, 1), (3, 2)],
    'W':[(0, 0), (0, 1), (0, 2)]
}

knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]

def state_key(white, black):
    return tuple(sorted(white)) + tuple(sorted(black))

def position_is_valid(position, occupied):
    r, c = position
    return 0 <= r < rows and 0 <= c < columns and position not in occupied

def minimum_moves(starting_position, ending_position):
    queue = deque()
    visited = set()

    start = (tuple(starting_position['W']), tuple(starting_position['B']))
    goal = (tuple(ending_position['W']), tuple(ending_position['B']))

    queue.append((start, []))
    visited.add(state_key(*start))

    while queue:
        (w_pos, b_pos), path = queue.popleft()
        if (sorted(w_pos), sorted(b_pos)) == (sorted(goal[0]), sorted(goal[1])):
            return path

        for i, knight in enumerate(w_pos):
            for row, column in knight_moves:
                new_pos = (knight[0] + row, knight[1] + column)
                if position_is_valid(new_pos, w_pos + b_pos):
                    new_w_pos = list(w_pos)
                    new_w_pos[i] = new_pos
                    state = (tuple(new_w_pos), b_pos)
                    key = state_key(*state)
                    if key not in visited:
                        visited.add(key)
                        queue.append((state, path + [(f'W{i+1}', knight, new_pos)]))

        for i, knight in enumerate(b_pos):
            for row, column in knight_moves:
                new_pos = (knight[0] + row, knight[1] + column)
                if position_is_valid(new_pos, w_pos + b_pos):
                    new_b_pos = list(b_pos)
                    new_b_pos[i] = new_pos
                    state = (w_pos, tuple(new_b_pos))
                    key = state_key(*state)
                    if key not in visited:
                        visited.add(key)
                        queue.append((state, path + [(f'B{i+1}', knight, new_pos)]))

    return None

solution = minimum_moves(starting_position, ending_position)

if solution:
    for step in solution:
        print(f"Move {step[0]} from {step[1]} to {step[2]}")
    print(f"\nTotal moves: {len(solution)}")