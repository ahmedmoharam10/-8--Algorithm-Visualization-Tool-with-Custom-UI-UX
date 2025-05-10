import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import math
from collections import deque
from tkinter import ttk


class TasksApp:
    def create_control_buttons(self):
        # Use ttk for better looking buttons
        tasks_frame = ttk.Frame(self.control_frame)
        tasks_frame.pack(side=tk.LEFT, padx=5)
       
        tasks = [
            ("Task 1", "Invert Triangle"),
            ("Task 2", "Peg Solitaire"),
            ("Task 3", "Knight Moves"),
            ("Task 4", "Penny Machine"),
            ("Task 5", "Security switches"),
            ("Task 6", "Tower of Hanoi"),
            ("Task 6.2", "4-Peg BFS Solution")
        ]
       
        # Configure button style
        style = ttk.Style()
        style.configure('Task.TButton',
                    font=('Arial', 9, 'bold'),
                    padding=6,
                    width=14)
       
        for i, (task, desc) in enumerate(tasks, 1):
            # Special handling for Task 6.2
            task_num = 6.2 if task == "Task 6.2" else i
            btn = ttk.Button(
                tasks_frame,
                text=f"{task}\n{desc}",
                command=lambda num=task_num: self.run_task(num),
                style='Task.TButton',
                width=14
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
           
       
        # Add separator
        ttk.Separator(self.control_frame, orient='vertical').pack(side=tk.LEFT, fill='y', padx=5)
       
        # Animation controls with better layout
        control_frame = ttk.Frame(self.control_frame)
        control_frame.pack(side=tk.LEFT, padx=5)
       
        # Control buttons in a grid
        self.start_btn = ttk.Button(control_frame, text="Start", command=self.start_animation)
        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self.pause_animation)
        self.step_btn = ttk.Button(control_frame, text="Step", command=self.step_animation)
       
        self.start_btn.grid(row=0, column=0, padx=2, pady=2, sticky='ew')
        self.pause_btn.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        self.step_btn.grid(row=0, column=2, padx=2, pady=2, sticky='ew')
       
        # Speed control with better label
        speed_frame = ttk.Frame(control_frame)
        speed_frame.grid(row=1, column=0, columnspan=3, pady=5, sticky='ew')
       
        ttk.Label(speed_frame, text="Animation Speed:").pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(
            speed_frame,
            from_=50,
            to=1000,
            command=self.set_speed
        )
        self.speed_scale.set(500)
        self.speed_scale.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
       
        # Clear button with warning color
        clear_btn = ttk.Button(
            control_frame,
            text="Clear All",
            command=self.clear_all
        )
        clear_btn.grid(row=0, column=3, rowspan=2, padx=5, sticky='ns')
           
    def __init__(self, root):
        self.root = root
        self.root.title("Analysis and Algorithms Tasks")
        self.root.geometry("1000x800")
        self.switch_states = []
        self.switch_steps = []
        self.current_switch_step = 0
       
        # Create main frames
        self.control_frame = tk.Frame(root)
        self.visualization_frame = tk.Frame(root, bg='white')
        self.output_frame = tk.Frame(root)
       
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.visualization_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
       
        # Create task buttons
        self.create_control_buttons()
       
        # Visualization canvas
        self.canvas = tk.Canvas(self.visualization_frame, bg='white', width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
       
        # Output area
        self.output_area = scrolledtext.ScrolledText(
            self.output_frame,
            wrap=tk.WORD,
            width=50,
            height=40,
            font=('Consolas', 10)
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)
       
        # Animation control
        self.animation_speed = 500  # milliseconds between steps
        self.animation_running = False
        self.pause_requested = False
        self.stop_requested = False
       
        # Redirect print statements
        import sys
        class PrintRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
               
            def write(self, string):
                self.text_widget.insert(tk.END, string)
                self.text_widget.see(tk.END)
               
            def flush(self):
                pass
               
        sys.stdout = PrintRedirector(self.output_area)
       
        # Visualization parameters
        self.coin_radius = 20
        self.row_spacing = 50
        self.start_x = 300
        self.start_y = 50
        self.coin_color = 'gold'
        self.highlight_color = 'red'
       
        # Data structures
        self.rows = []
        self.current_move = 0
        self.total_moves = 0
        self.target_sizes = {}
       
        # Task 2 variables
        self.peg_board = []
        self.peg_moves = []
        self.current_peg_step = 0
        self.peg_solutions = []
        self.peg_cell_size = 60
        self.peg_colors = {'P': 'blue', '_': 'white'}
        self.solution_displayed = False
        self.current_solution_index = 0
        self.all_solutions_flat = []
       
        # Task 3 variables
        self.knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
        self.knight_solution = []
        self.current_knight_step = 0
        self.knight_colors = {'W': 'white', 'B': 'black'}
       
        # Task 4 variables
        self.penny_boxes = []
        self.penny_history = []
        self.current_penny_step = 0
        self.all_penny_solutions = []
        self.current_penny_solution_index = 0
       
        # Task 6 variables
        self.hanoi_moves = []
        self.current_hanoi_step = 0
        self.hanoi_pegs = {'A': [], 'B': [], 'C': [], 'D': []}
        self.disk_colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00',
                           '#0000FF', '#4B0082', '#9400D3', '#FF1493']
   
    def set_speed(self, value):
        try:
            # Ensure the value is properly converted to an integer
            self.animation_speed = int(float(value))
        except (ValueError, TypeError):
            # Default to middle speed if conversion fails
            self.animation_speed = 500
   
    def clear_all(self):
        self.stop_animation()
        self.canvas.delete("all")
        self.output_area.delete(1.0, tk.END)
        self.rows = []
        self.current_move = 0
        self.total_moves = 0
        self.target_sizes = {}
        self.knight_solution = []
        self.current_knight_step = 0
        self.penny_boxes = []
        self.penny_history = []
        self.current_penny_step = 0
        self.hanoi_moves = []
        self.current_hanoi_step = 0
        self.hanoi_pegs = {'A': [], 'B': [], 'C': [], 'D': []}
        self.peg_board = []
        self.peg_moves = []
        self.current_peg_step = 0
        self.peg_solutions = []
        self.solution_displayed = False
        self.all_solutions_flat = []
        self.current_solution_index = 0
        self.all_penny_solutions = []
        self.current_penny_solution_index = 0
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED)
        self.step_btn.config(state=tk.DISABLED)
       
        # Remove navigation buttons if they exist
        if hasattr(self, 'nav_frame'):
            self.nav_frame.destroy()
        if hasattr(self, 'penny_nav_frame'):
            self.penny_nav_frame.destroy()
   
    def run_task(self, task_num):
        self.clear_all()
        print(f"=== Running Task {task_num} ===\n")
       
        if task_num == 1:
            self.prepare_task1()
        elif task_num == 2:
            self.prepare_task2()
        elif task_num == 3:
            self.prepare_task3()
        elif task_num == 4:
            self.prepare_task4()
        elif task_num == 5:
            self.prepare_task5()
        elif task_num == 6:
            self.prepare_task6()
        elif task_num == 6.2:  # Handle Task 6.2
            self.prepare_task6_part2()
        else:
            print(f"Task {task_num} functionality not implemented yet.")
   
    def prepare_task1(self):
        n = self.get_integer_input("Enter number of rows (n ≥ 1):")
        if n is None:
            return

        if n == 1:
            print("Already inverted (0 moves needed)")
            return

        T_n = n * (n + 1) // 2  # Total number of coins
        if n > 8:
            M_n = math.floor((T_n/3)+2)
        elif n > 6:
            M_n=math.floor((T_n/3)+1)  # Expected moves (rounded down)
        else:
            M_n = math.floor(T_n/3)
       
        # Initialize triangle data
        coins = list(range(1, T_n + 1))
        self.rows = []
        start = 0
        for i in range(1, n + 1):
            row_coins = coins[start:start + i]
            row_type = "Top" if i == 1 else ("Bottom" if i == n else "Middle")
            self.rows.append({"row_num": i, "coins": row_coins, "type": row_type})
            start += i

        # Save original sizes for inversion target
        original_row_sizes = {row["row_num"]: len(row["coins"]) for row in self.rows}
        self.target_sizes = {}
       
        original_order = list(original_row_sizes.values())
        inverted_order = original_order[::-1]
       
        for idx, row in enumerate(self.rows):
            self.target_sizes[row["row_num"]] = inverted_order[idx]

        print("\nInitial triangle:")
        self.visualize_triangle()
        self.start_btn.config(state=tk.NORMAL)
        self.step_btn.config(state=tk.NORMAL)
        self.total_moves = M_n  # Set expected total moves

        # Store the initial state for animation
        self.triangle_states = [self.rows.copy()]
   
    def prepare_task2(self):
        n = self.get_integer_input("Enter number of cells (even number > 2):", min_value=3)
        if n is None or n % 2 != 0:
            messagebox.showerror("Error", "Number must be even and greater than 2")
            return

        print("\nAnalyzing all initial positions...")
        results, all_solutions = self.analyze_all_initial_positions(n)
       
        # Find positions with no solutions
        all_positions = set(range(n))
        solvable_positions = set(results.keys())
        unsolvable_positions = all_positions - solvable_positions
       
        # Display summary of all positions
        print("\n=== Analysis Results ===")
        print(f"Total positions analyzed: {n}")
        print(f"Solvable positions: {len(solvable_positions)}")
        print(f"Unsolvable positions: {len(unsolvable_positions)}\n")
       
        if not all_solutions:
            print("No solutions found for any starting position!")
            return
       
        # Display solvable positions
        if solvable_positions:
            print("\nSolvable positions and their possible final peg locations:")
            for empty_pos, final_positions in results.items():
                print(f"  Initial empty at {empty_pos}: can end at {final_positions}")
       
        # Display unsolvable positions
        if unsolvable_positions:
            print("\nUnsolvable starting positions (no solutions exist):")
            print("  Positions:", sorted(unsolvable_positions))
       
        # Display detailed solutions for each valid starting position
        print("\n\nStep-by-step solutions for each valid starting position:")
        for empty_pos, solutions in all_solutions.items():
            print(f"\nInitial empty at position {empty_pos}:")
            for sol_num, (moves, final_pos) in enumerate(solutions[:3], 1):  # Limit to first 3 solutions
                print(f"  Solution {sol_num}: Final peg at {final_pos} (Total moves: {len(moves)-1})")
                for step, board in enumerate(moves, 1):  # Start counting from 0
                    print(f"    Step {step}/{len(moves)}: {' '.join(board)}")
       
        # Display final summary
        print("\n\n=== Final Summary ===")
        print(f"Total solvable initial positions: {len(results)} / {n}")
        if solvable_positions:
            all_final_positions = sorted({pos for positions in results.values() for pos in positions})
            print(f"All possible final positions: {all_final_positions}")
       
        # Flatten all solutions for navigation
        self.all_solutions_flat = []
        for empty_pos, solutions in all_solutions.items():
            for i, (moves, final_pos) in enumerate(solutions):
                self.all_solutions_flat.append({
                    'empty_pos': empty_pos,
                    'solution_num': i+1,
                    'moves': moves,
                    'final_pos': final_pos,
                    'total_steps': len(moves)
                })
       
        self.current_solution_index = 0
       
        # Create navigation buttons if we have solutions
        if self.all_solutions_flat:
            self.create_navigation_buttons()
            self.show_solution(0)
   
    def create_navigation_buttons(self):
        # Remove old navigation frame if it exists
        if hasattr(self, 'nav_frame'):
            self.nav_frame.destroy()
       
        # Create new navigation frame
        self.nav_frame = tk.Frame(self.control_frame)
        self.nav_frame.pack(side=tk.LEFT, padx=10)
       
        self.prev_btn = tk.Button(
            self.nav_frame,
            text="<< Previous",
            command=self.show_previous_solution,
            state=tk.DISABLED if self.current_solution_index <= 0 else tk.NORMAL
        )
        self.prev_btn.pack(side=tk.LEFT, padx=2)
       
        self.solution_label = tk.Label(
            self.nav_frame,
            text=f"Solution {self.current_solution_index+1} of {len(self.all_solutions_flat)}",
            width=20
        )
        self.solution_label.pack(side=tk.LEFT, padx=2)
       
        self.next_btn = tk.Button(
            self.nav_frame,
            text="Next >>",
            command=self.show_next_solution,
            state=tk.DISABLED if self.current_solution_index >= len(self.all_solutions_flat)-1 else tk.NORMAL
        )
        self.next_btn.pack(side=tk.LEFT, padx=2)
   
    def show_solution(self, index):
        if 0 <= index < len(self.all_solutions_flat):
            self.current_solution_index = index
            solution = self.all_solutions_flat[index]
            self.peg_moves = solution['moves']
            self.current_peg_step = 0  # Start at 0 (initial state)
           
            # Update navigation buttons state
            if hasattr(self, 'prev_btn'):
                self.prev_btn.config(state=tk.NORMAL if index > 0 else tk.DISABLED)
            if hasattr(self, 'next_btn'):
                self.next_btn.config(state=tk.NORMAL if index < len(self.all_solutions_flat)-1 else tk.DISABLED)
            if hasattr(self, 'solution_label'):
                self.solution_label.config(text=f"Solution {index+1} of {len(self.all_solutions_flat)}")
           
            # Show initial state as Step 1
            print("\n" + "="*50)
            print(f"Showing Solution {solution['solution_num']} for empty position {solution['empty_pos']}")
            print(f"Step 1/{len(self.peg_moves)}: {' '.join(self.peg_moves[0])}")
           
            self.peg_board = self.peg_moves[0]
            self.visualize_peg_board()
            self.start_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.NORMAL)
            self.total_moves = len(self.peg_moves)
   
    def show_next_solution(self):
        if self.current_solution_index < len(self.all_solutions_flat) - 1:
            self.current_solution_index += 1
            self.show_solution(self.current_solution_index)
   
    def show_previous_solution(self):
        if self.current_solution_index > 0:
            self.current_solution_index -= 1
            self.show_solution(self.current_solution_index)
   
    def create_penny_navigation_buttons(self):
        # Remove old navigation frame if it exists
        if hasattr(self, 'penny_nav_frame'):
            self.penny_nav_frame.destroy()
       
        # Create new navigation frame
        self.penny_nav_frame = tk.Frame(self.control_frame)
        self.penny_nav_frame.pack(side=tk.LEFT, padx=10)
       
        self.penny_prev_btn = tk.Button(
            self.penny_nav_frame,
            text="<< Previous",
            command=self.show_previous_penny_solution,
            state=tk.DISABLED if self.current_penny_solution_index <= 0 else tk.NORMAL
        )
        self.penny_prev_btn.pack(side=tk.LEFT, padx=2)
       
        self.penny_solution_label = tk.Label(
            self.penny_nav_frame,
            text=f"Solution {self.current_penny_solution_index+1} of {len(self.all_penny_solutions)}",
            width=20
        )
        self.penny_solution_label.pack(side=tk.LEFT, padx=2)
       
        self.penny_next_btn = tk.Button(
            self.penny_nav_frame,
            text="Next >>",
            command=self.show_next_penny_solution,
            state=tk.DISABLED if self.current_penny_solution_index >= len(self.all_penny_solutions)-1 else tk.NORMAL
        )
        self.penny_next_btn.pack(side=tk.LEFT, padx=2)
   
    def show_penny_solution(self, index):
        if 0 <= index < len(self.all_penny_solutions):
            self.current_penny_solution_index = index
            self.penny_history = self.all_penny_solutions[index]
            self.current_penny_step = 0
           
            # Update navigation buttons state
            if hasattr(self, 'penny_prev_btn'):
                self.penny_prev_btn.config(state=tk.NORMAL if index > 0 else tk.DISABLED)
            if hasattr(self, 'penny_next_btn'):
                self.penny_next_btn.config(state=tk.NORMAL if index < len(self.all_penny_solutions)-1 else tk.DISABLED)
            if hasattr(self, 'penny_solution_label'):
                self.penny_solution_label.config(text=f"Solution {index+1} of {len(self.all_penny_solutions)}")
           
            # Show initial state
            print("\n" + "="*50)
            print(f"Showing Penny Solution {index+1}")
            print(f"Step 1/{len(self.penny_history)}: {self.penny_history[0]}")
           
            self.visualize_penny_boxes()
            self.start_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.NORMAL)
            self.total_moves = len(self.penny_history) - 1
   
    def show_next_penny_solution(self):
        if self.current_penny_solution_index < len(self.all_penny_solutions) - 1:
            self.current_penny_solution_index += 1
            self.show_penny_solution(self.current_penny_solution_index)
   
    def show_previous_penny_solution(self):
        if self.current_penny_solution_index > 0:
            self.current_penny_solution_index -= 1
            self.show_penny_solution(self.current_penny_solution_index)
   
    def minimum_moves(self, initial_positions, target_positions):
        """Calculate minimum moves to transform initial knight positions to target positions using BFS."""
        # Knight movement directions (dx, dy)
        directions = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
       
        # Create a mapping from positions to knight IDs
        knight_id_map = {}
        for color in ['W', 'B']:
            for i, pos in enumerate(initial_positions[color]):
                knight_id_map[(color, pos)] = f"{color}{i+1}"
       
        # Convert positions to sets for easier comparison
        initial_state = {
            'W': set(initial_positions['W']),
            'B': set(initial_positions['B'])
        }
        target_state = {
            'W': set(target_positions['W']),
            'B': set(target_positions['B'])
        }
       
        # Check if already at target
        if initial_state == target_state:
            return []
       
        # BFS setup
        queue = deque()
        queue.append((initial_state, []))
        visited = set()
       
        # Helper function to create hashable state
        def state_to_tuple(state):
            return (frozenset(state['W']), frozenset(state['B']))
       
        visited.add(state_to_tuple(initial_state))
       
        while queue:
            current_state, path = queue.popleft()
           
            # Generate all possible next moves
            for color in ['W', 'B']:
                for knight_pos in list(current_state[color]):
                    for dx, dy in directions:
                        new_pos = (knight_pos[0] + dx, knight_pos[1] + dy)
                       
                        # Check if move is valid
                        if (0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 3 and
                            new_pos not in current_state['W'] and
                            new_pos not in current_state['B']):
                           
                            # Create new state
                            new_state = {
                                'W': set(current_state['W']),
                                'B': set(current_state['B'])
                            }
                            new_state[color].remove(knight_pos)
                            new_state[color].add(new_pos)
                           
                            # Get knight ID
                            knight_id = knight_id_map.get((color, knight_pos), f"{color}?")
                           
                            # Update ID mapping
                            knight_id_map[(color, new_pos)] = knight_id
                           
                            # Check if target reached
                            if new_state == target_state:
                                return path + [(knight_id, knight_pos, new_pos)]
                           
                            # Check if state already visited
                            state_tuple = state_to_tuple(new_state)
                            if state_tuple not in visited:
                                visited.add(state_tuple)
                                queue.append((new_state, path + [(knight_id, knight_pos, new_pos)]))
       
        return None  # No solution found
   
    def prepare_task3(self):
        # Default board setup for Task 3
        rows, columns = 4, 3
       
        self.initial_knight_positions = {
            'B': [(0, 0), (0, 1), (0, 2)],
            'W': [(3, 0), (3, 1), (3, 2)]
        }
       
        ending_position = {
            'B': [(3, 0), (3, 1), (3, 2)],
            'W': [(0, 0), (0, 1), (0, 2)]
        }
       
        print("Calculating solution for Task 3 (Knight Movement Problem)...")
        self.knight_solution = self.minimum_moves(self.initial_knight_positions, ending_position)
       
        if self.knight_solution:
            print("\nSolution found:")
            for step in self.knight_solution:
                print(f"Move {step[0]} from {step[1]} to {step[2]}")
            print(f"\nTotal moves: {len(self.knight_solution)}")
           
            # Reset counters
            self.current_knight_step = 0
            self.total_moves = len(self.knight_solution)
           
            # Visualize initial state
            self.visualize_knight_board(self.initial_knight_positions)
            self.start_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.NORMAL)
        else:
            print("No solution found!")
   
    def visualize_knight_board(self, positions):
        self.canvas.delete("all")
       
        # Draw title
        self.canvas.create_text(
            300, 20,
            text="Knight Movement Problem",
            font=('Arial', 16, 'bold')
        )
       
        # Draw board
        cell_size = 100
        for row in range(4):
            for col in range(3):
                x1 = 50 + col * cell_size
                y1 = 50 + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
               
                # Draw cell with alternating colors
                color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
               
                # Draw coordinates
                self.canvas.create_text(
                    x1 + 10, y1 + 10,
                    text=f"({row},{col})",
                    font=('Arial', 8),
                    anchor=tk.NW
                )
       
        # Draw knights with proper IDs
        for color, pos_list in positions.items():
            for i, (row, col) in enumerate(pos_list, 1):
                x = 50 + col * cell_size + cell_size // 2
                y = 50 + row * cell_size + cell_size // 2
               
                # Draw knight
                self.canvas.create_oval(
                    x - 30, y - 30,
                    x + 30, y + 30,
                    fill=self.knight_colors[color],
                    outline='black'
                )
               
                # Draw knight ID with appropriate text color
                text_color = 'black' if color == 'W' else 'white'
                self.canvas.create_text(
                    x, y,
                    text=f"{color}{i}",
                    font=('Arial', 12, 'bold'),
                    fill=text_color
                )
       
        # Draw move information
        if hasattr(self, 'current_knight_step') and hasattr(self, 'total_moves'):
            self.canvas.create_text(
                50, 20,
                text=f"Move: {self.current_knight_step}/{self.total_moves}",
                anchor=tk.W,
                font=('Arial', 12, 'bold')
            )
   
    def calculate_current_positions(self):
        # Reconstruct current positions based on moves made
        current_positions = {
            'W': [],
            'B': []
        }
       
        # Get the starting positions
        if not hasattr(self, 'initial_knight_positions'):
            return current_positions
       
        # Make a copy of initial positions
        from copy import deepcopy
        current_positions = deepcopy(self.initial_knight_positions)
       
        # Apply all moves up to current step
        for step in self.knight_solution[:self.current_knight_step]:
            knight_id, from_pos, to_pos = step
            color = knight_id[0]
           
            # Try to get the index, but handle the case where ID is generic (like "W?")
            try:
                index = int(knight_id[1:]) - 1
            except ValueError:
                # If we can't parse the number, find the first matching position
                for i, pos in enumerate(current_positions[color]):
                    if pos == from_pos:
                        index = i
                        break
                else:
                    # If we still can't find it, skip this move
                    continue
           
            # Remove from old position
            if from_pos in current_positions[color]:
                current_positions[color].remove(from_pos)
           
            # Add to new position
            current_positions[color].append(to_pos)
       
        return current_positions

    def prepare_task4(self):
        n = self.get_integer_input("How many pennies do you want to drop into the machine?")
        if n is None:
            return

        if n == 0:
            print("No pennies to process!")
            return

        print("\nRunning the penny machine (brute-force)...")
        results = self.run_Pmachine_brute_force(n)
        
        if not results:
            print("No solutions found!")
            return
        
        # Extract all solution paths
        self.all_penny_solutions = [path for (path, steps) in results]
        self.current_penny_solution_index = 0
        
        # Create navigation buttons
        self.create_penny_navigation_buttons()
        self.show_penny_solution(0)
    
    def prepare_task5(self):
        n = self.get_integer_input("Enter number of switches:")
        if n is None:
            return

        print("\nCalculating switch puzzle solution...")
        self.switch_steps = self.solve_switch_puzzle(n)
       
        if not self.switch_steps or len(self.switch_steps) == 0:
            print("No solution found or empty solution!")
            return
       
        # Reset current step to 0
        self.current_switch_step = 0
       
        print("\nInitial state:")
        self.visualize_switches()
        self.start_btn.config(state=tk.NORMAL)
        self.step_btn.config(state=tk.NORMAL)
        print(f"\nTotal steps calculated: {len(self.switch_steps)-1}")
   
    def prepare_task6(self):
        n = self.get_integer_input("Enter number of disks for 4-peg Tower of Hanoi (1-8 recommended):", min_value=0)
        if n is None:
            return

        print("\nCalculating moves for 4-peg Tower of Hanoi...")
        self.hanoi_moves = []
        total_moves = self.hanoi4(n, 'A', 'B', 'C', 'D', record_moves=True)
       
        print("\nInitial state:")
        self.hanoi_pegs = {'A': list(range(n, 0, -1)), 'B': [], 'C': [], 'D': []}
        self.visualize_hanoi()
        self.start_btn.config(state=tk.NORMAL)
        self.step_btn.config(state=tk.NORMAL)
        print(f"\nTotal moves calculated: {total_moves}")
   
    def prepare_task6_part2(self):
        print("\nCalculating BFS solution for 4-peg Tower of Hanoi with 8 disks...")
       
        # Run the BFS algorithm
        solution_moves = self.bfs_algorithm()
       
        if solution_moves:
            peg_names = {
                0: "A",
                1: "B",
                2: "C",
                3: "D"
            }
           
            # Print the solution
            print(f"\n4-peg Tower of Hanoi solution for 8 disks:")
            for i, (src, dest, disk) in enumerate(solution_moves, 1):
                print(f"Move {i}: {peg_names[src]} --> {peg_names[dest]} (Disk {disk})")
           
            print(f"\nOptimal number of moves: {len(solution_moves)}")
           
            # Prepare for visualization
            self.hanoi_moves = [(peg_names[src], peg_names[dest]) for src, dest, disk in solution_moves]
            self.hanoi_pegs = {'A': [8,7,6,5,4,3,2,1], 'B': [], 'C': [], 'D': []}
            self.current_hanoi_step = 0
            self.total_moves = len(self.hanoi_moves)
           
            # Visualize initial state
            self.visualize_hanoi()
            self.start_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.NORMAL)
        else:
            print("No solution found!")
   
    def bfs_algorithm(self):
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
   
    def hanoi4(self, n, peg_source, peg_intermediate1, peg_intermediate2, peg_dest, record_moves=False):
        if n == 0:
            return 0

        if n == 1:
            if record_moves:
                self.hanoi_moves.append((peg_source, peg_dest))
            return 1

        if n == 2:
            if record_moves:
                self.hanoi_moves.append((peg_source, peg_intermediate1))
                self.hanoi_moves.append((peg_source, peg_dest))
                self.hanoi_moves.append((peg_intermediate1, peg_dest))
            return 3

        total_moves = 0
        total_moves += self.hanoi4(n - 2, peg_source, peg_intermediate2, peg_dest, peg_intermediate1, record_moves)
        if record_moves:
            self.hanoi_moves.append((peg_source, peg_intermediate2))
            self.hanoi_moves.append((peg_source, peg_dest))
            self.hanoi_moves.append((peg_intermediate2, peg_dest))
        total_moves += 3
        total_moves += self.hanoi4(n - 2, peg_intermediate1, peg_source, peg_intermediate2, peg_dest, record_moves)
        return total_moves
   
    def run_Pmachine_brute_force(self, n):
        boxes = [0] * (n + 1)
        boxes[0] = n
        results = []
        self.brute_force(boxes, 0, results, [boxes[:]])
        return results

    def brute_force(self, boxes, steps, results, history):
        if all(x < 2 for x in boxes):
            results.append((history[:], steps))
            return

        for i in range(len(boxes) - 1):
            if boxes[i] >= 2:
                new_state = boxes[:]
                new_state[i] -= 2
                new_state[i + 1] += 1
                self.brute_force(new_state, steps + 1, results, history + [new_state])
    
    def visualize_penny_boxes(self):
            self.canvas.delete("all")
            if not self.penny_history:
                return
            
            current_state = self.penny_history[self.current_penny_step]
            box_width = 60
            box_height = 60
            start_x = 50
            start_y = 100
            max_boxes = len(current_state)
        
            # Draw title
            self.canvas.create_text(
                300, 30,
                text="Penny Machine",
                font=('Arial', 16, 'bold')
            )
        
            # Draw boxes
            for i in range(max_boxes):
                x1 = start_x + i * (box_width + 10)
                y1 = start_y
                x2 = x1 + box_width
                y2 = y1 + box_height
            
                # Draw box
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='#f0f0f0', outline='black')
            
                # Draw box number
                self.canvas.create_text(
                    x1 + box_width/2, y1 - 15,
                    text=f"Box {i}",
                    font=('Arial', 10)
                )
            
                # Draw pennies
                if current_state[i] > 0:
                    self.canvas.create_text(
                        x1 + box_width/2, y1 + box_height/2,
                        text=str(current_state[i]),
                        font=('Arial', 14, 'bold')
                    )
        
            # Draw move information
            self.canvas.create_text(
                50, 70,
                text=f"Step: {self.current_penny_step}/{self.total_moves}",
                anchor=tk.W,
                font=('Arial', 12, 'bold')
            )
   
    def visualize_switches(self):
        self.canvas.delete("all")
        if not self.switch_steps or len(self.switch_steps) == 0:
            # Show error message if no steps available
            self.canvas.create_text(
                300, 150,
                text="No switch steps available!",
                font=('Arial', 16),
                fill='red'
            )
            return
           
        # Make sure current step is within bounds
        if self.current_switch_step >= len(self.switch_steps):
            self.current_switch_step = len(self.switch_steps) - 1
        if self.current_switch_step < 0:
            self.current_switch_step = 0

        current_step = self.switch_steps[self.current_switch_step]
        switch_num, states = current_step
        n = len(states)
       
        # Rest of the visualization code remains the same...
        # Draw title
        self.canvas.create_text(
            300, 30,
            text="Switch Puzzle",
            font=('Arial', 16, 'bold')
        )
       
        # Draw switches
        switch_width = 40
        switch_height = 60
        start_x = 100
        start_y = 100
       
        for i in range(n):
            x = start_x + i * (switch_width + 10)
            y = start_y
           
            # Draw switch background
            self.canvas.create_rectangle(
                x, y,
                x + switch_width, y + switch_height,
                fill='#f0f0f0',
                outline='black'
            )
           
            # Draw switch state (ON/OFF)
            state = states[i]
            color = 'green' if state else 'red'
            self.canvas.create_oval(
                x + 5, y + 5 if state else y + switch_height - 25,
                x + switch_width - 5, y + 25 if state else y + switch_height - 5,
                fill=color,
                outline='black'
            )
           
            # Draw switch number
            self.canvas.create_text(
                x + switch_width/2, y + switch_height + 10,
                text=str(i+1),
                font=('Arial', 10)
            )
       
        # Draw move information
        self.canvas.create_text(
            50, 70,
            text=f"Step: {self.current_switch_step}/{len(self.switch_steps)-1}",
            anchor=tk.W,
            font=('Arial', 12, 'bold')
        )
       
        # Draw current action
        if self.current_switch_step > 0:
            action = f"Flipped switch {switch_num}"
            self.canvas.create_text(
                300, 70,
                text=action,
                font=('Arial', 12)
            )
   
    def solve_switch_puzzle(self, total_switches):
        # Start with all switches ON (1 = ON, 0 = OFF)
        switches = [1] * total_switches
        steps = [(0, switches.copy())]  # Step 0: initial state (0 means no switch flipped)

        if total_switches <= 0:
            return steps  # Return at least initial state

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
            steps.append((index + 1, switches.copy()))

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
        try:
            turn_off_switches(0, total_switches - 1)
        except Exception as e:
            print(f"Error solving switch puzzle: {e}")
            return steps  # Return whatever steps we have

        return steps
   
    def visualize_hanoi(self):
        self.canvas.delete("all")
       
        # Draw title
        self.canvas.create_text(
            300, 20,
            text="4-Peg Tower of Hanoi",
            font=('Arial', 16, 'bold')
        )

        # Draw pegs
        peg_positions = {'A': 100, 'B': 250, 'C': 400, 'D': 550}
        peg_height = 400
        peg_width = 20
        base_y = 500
       
        for peg, x in peg_positions.items():
            # Draw peg
            self.canvas.create_rectangle(
                x - peg_width//2, base_y - peg_height,
                x + peg_width//2, base_y,
                fill='brown',
                outline='black'
            )
           
            # Draw peg label
            self.canvas.create_text(
                x, base_y + 20,
                text=peg,
                font=('Arial', 12, 'bold')
            )
           
            # Draw disks
            disks = self.hanoi_pegs[peg]
            disk_height = 20
            max_disk_width = 100
            min_disk_width = 30
           
            for i, disk in enumerate(disks):
                disk_width = min_disk_width + (max_disk_width - min_disk_width) * disk / len(self.disk_colors)
                y = base_y - (i * disk_height)
               
                # Use modulo to cycle through colors
                color_index = (disk - 1) % len(self.disk_colors)
               
                # Draw disk with a tag that includes its peg and disk number
                disk_tag = f"disk_{peg}_{disk}"
                self.canvas.create_rectangle(
                    x - disk_width//2, y - disk_height,
                    x + disk_width//2, y,
                    fill=self.disk_colors[color_index],
                    outline='black',
                    tags=disk_tag
                )
               
                # Draw disk number with the same tag
                self.canvas.create_text(
                    x, y - disk_height//2,
                    text=str(disk),
                    font=('Arial', 10),
                    tags=disk_tag
                )
       
        # Draw move information
        self.canvas.create_text(
            50, 50,
            text=f"Move: {self.current_hanoi_step}/{len(self.hanoi_moves)}",
            anchor=tk.W,
            font=('Arial', 12, 'bold')
        )
   
    def visualize_peg_board(self):
        self.canvas.delete("all")
        if not self.peg_board:
            return
           
        n = len(self.peg_board)
        start_x = 100
        start_y = 100
       
        # Draw title
        self.canvas.create_text(
            300, 30,
            text="Peg Solitaire",
            font=('Arial', 16, 'bold')
        )
       
        # Draw board
        for i in range(n):
            x = start_x + i * self.peg_cell_size
            y = start_y
           
            # Draw cell
            self.canvas.create_rectangle(
                x, y,
                x + self.peg_cell_size, y + self.peg_cell_size,
                fill='lightgray',
                outline='black'
            )
           
            # Draw peg or empty
            if i < len(self.peg_board):
                state = self.peg_board[i]
                self.canvas.create_oval(
                    x + 5, y + 5,
                    x + self.peg_cell_size - 5, y + self.peg_cell_size - 5,
                    fill=self.peg_colors[state],
                    outline='black'
                )
       
        total_steps = len(self.peg_moves) if self.peg_moves else 0
        current_step = min(self.current_peg_step + 1, total_steps)  # 1-based
        self.canvas.create_text(
            50, 70,
            text=f"Move: {current_step}/{total_steps}",
            anchor=tk.W,
            font=('Arial', 12, 'bold')
        )
   
    def visualize_triangle(self):
        self.canvas.delete("all")
        if not self.rows:
            return
           
        # Draw title and move counter at the top
        self.canvas.create_text(
            300, 20,
            text="Triangle Inversion",
            font=('Arial', 16, 'bold')
        )
       
        self.canvas.create_text(
            50, 50,
            text=f"Move: {self.current_move}/{self.total_moves}",
            anchor=tk.W,
            font=('Arial', 12, 'bold')
        )
       
        # Draw the triangle
        start_y = 80  # Start lower to leave space for title and move counter
        for i, row in enumerate(self.rows):
            num_coins = len(row["coins"])
            y = start_y + i * self.row_spacing
            row_width = num_coins * (self.coin_radius * 2)
           
            # Draw row label
            self.canvas.create_text(
                30, y,
                text=f"Row {row['row_num']} ({row['type']})",
                anchor=tk.W,
                font=('Arial', 10)
            )
           
            # Draw coins
            for j in range(num_coins):
                x = self.start_x - row_width/2 + j * (self.coin_radius * 2) + self.coin_radius
                self.canvas.create_oval(
                    x - self.coin_radius, y - self.coin_radius,
                    x + self.coin_radius, y + self.coin_radius,
                    fill=self.coin_color,
                    outline='black'
                )
                self.canvas.create_text(
                    x, y,
                    text=str(row["coins"][j]),
                    font=('Arial', 10)
                )
   
    def animate_coin_move(self, from_row_idx, from_coin_idx, to_row_idx, to_coin_idx, callback):
        if not self.rows or from_row_idx >= len(self.rows) or to_row_idx >= len(self.rows):
            callback()
            return
       
        from_row = self.rows[from_row_idx]
        to_row = self.rows[to_row_idx]
       
        if from_coin_idx >= len(from_row["coins"]) or to_coin_idx > len(to_row["coins"]):
            callback()
            return
       
        # Get coin information
        coin_value = from_row["coins"][from_coin_idx]
       
        # Calculate positions
        from_y = self.start_y + from_row_idx * self.row_spacing
        from_num_coins = len(from_row["coins"])
        from_row_width = from_num_coins * (self.coin_radius * 2)
        from_x = self.start_x - from_row_width/2 + from_coin_idx * (self.coin_radius * 2) + self.coin_radius
       
        to_y = self.start_y + to_row_idx * self.row_spacing
        to_num_coins = len(to_row["coins"])
        to_row_width = (to_num_coins + 1) * (self.coin_radius * 2)  # +1 for the new coin
        to_x = self.start_x - to_row_width/2 + to_coin_idx * (self.coin_radius * 2) + self.coin_radius
       
        # Create a temporary coin for animation
        coin = self.canvas.create_oval(
            from_x - self.coin_radius, from_y - self.coin_radius,
            from_x + self.coin_radius, from_y + self.coin_radius,
            fill=self.highlight_color,
            outline='black'
        )
        coin_text = self.canvas.create_text(
            from_x, from_y,
            text=str(coin_value),
            font=('Arial', 10)
        )
       
        # Animation steps
        steps = 20
        dx = (to_x - from_x) / steps
        dy = (to_y - from_y) / steps
       
        def move_coin(step):
            if step < steps and not self.pause_requested and not self.stop_requested:
                self.canvas.move(coin, dx, dy)
                self.canvas.move(coin_text, dx, dy)
                self.root.after(self.animation_speed // steps, move_coin, step + 1)
            else:
                self.canvas.delete(coin)
                self.canvas.delete(coin_text)
                callback()
       
        move_coin(0)
   
    def animate_knight_move(self, from_pos, to_pos, callback):
        cell_size = 100
        from_col, from_row = from_pos[1], from_pos[0]
        to_col, to_row = to_pos[1], to_pos[0]
       
        from_x = from_col * cell_size + 50 + cell_size // 2
        from_y = from_row * cell_size + 50 + cell_size // 2
        to_x = to_col * cell_size + 50 + cell_size // 2
        to_y = to_row * cell_size + 50 + cell_size // 2
       
        # Find all knight pieces at the from position
        knight_items = []
        for item in self.canvas.find_all():
            x, y = self.canvas.coords(item)[0] + cell_size//3, self.canvas.coords(item)[1] + cell_size//3
            if abs(x - from_x) < 5 and abs(y - from_y) < 5 and self.canvas.type(item) == 'oval':
                knight_items.append(item)
                # Find corresponding text item
                for text_item in self.canvas.find_all():
                    if (self.canvas.type(text_item) == 'text' and
                        abs(self.canvas.coords(text_item)[0] - x) < 5 and
                        abs(self.canvas.coords(text_item)[1] - y) < 5):
                        knight_items.append(text_item)
       
        if not knight_items:
            callback()
            return
       
        # Animation steps
        steps = 20
        dx = (to_x - from_x) / steps
        dy = (to_y - from_y) / steps
       
        def move_knight(step):
            if step < steps and not self.pause_requested and not self.stop_requested:
                for item in knight_items:
                    self.canvas.move(item, dx, dy)
                self.root.after(self.animation_speed // steps, move_knight, step + 1)
            else:
                callback()
       
        move_knight(0)
   
    def animate_hanoi_move(self, from_peg, to_peg, callback):
        if not self.hanoi_pegs[from_peg]:
            callback()
            return
       
        # Get disk to move (top disk on from_peg)
        disk = self.hanoi_pegs[from_peg][-1]
       
        # Calculate positions
        peg_positions = {'A': 100, 'B': 250, 'C': 400, 'D': 550}
        base_y = 500
        disk_height = 20
        max_disk_width = 100
        min_disk_width = 30
       
        from_x = peg_positions[from_peg]
        to_x = peg_positions[to_peg]
       
        # Calculate y positions
        from_stack_height = len(self.hanoi_pegs[from_peg])
        from_y = base_y - (from_stack_height * disk_height)
       
        to_stack_height = len(self.hanoi_pegs[to_peg])
        to_y = base_y - ((to_stack_height + 1) * disk_height)
       
        # Find the disk using its tag
        disk_tag = f"disk_{from_peg}_{disk}"
        disk_items = self.canvas.find_withtag(disk_tag)
       
        if not disk_items:
            print(f"Couldn't find disk {disk} on peg {from_peg}")
            callback()
            return
       
        # Animation parameters
        steps = 30
        lift_height = 150  # How high to lift before moving
       
        # Calculate movement per step
        up_steps = steps // 3
        across_steps = steps // 3
        down_steps = steps // 3
       
        current_step = 0
   
        def move_disk():
            nonlocal current_step
            if current_step < steps and not self.pause_requested and not self.stop_requested:
                # Calculate movement for this step
                if current_step < up_steps:  # Move up
                    dy = -lift_height / up_steps
                    dx = 0
                elif current_step < up_steps + across_steps:  # Move across
                    dx = (to_x - from_x) / across_steps
                    dy = 0
                else:  # Move down
                    dx = 0
                    dy = (lift_height + (to_y - from_y)) / down_steps
               
                # Move all items with the disk tag
                for item in disk_items:
                    self.canvas.move(item, dx, dy)
               
                current_step += 1
                self.root.after(self.animation_speed // steps, move_disk)
            else:
                # Update the data structure
                moved_disk = self.hanoi_pegs[from_peg].pop()
                self.hanoi_pegs[to_peg].append(moved_disk)
               
                # Redraw to ensure clean state
                self.visualize_hanoi()
                callback()
       
        move_disk()
   
    def animate_peg_move(self, from_idx, over_idx, to_idx, callback):
        if (from_idx >= len(self.peg_board) or over_idx >= len(self.peg_board) or
            to_idx >= len(self.peg_board)):
            callback()
            return
       
        # Get positions
        from_x = 100 + from_idx * self.peg_cell_size + self.peg_cell_size // 2
        from_y = 100 + self.peg_cell_size // 2
        to_x = 100 + to_idx * self.peg_cell_size + self.peg_cell_size // 2
        to_y = 100 + self.peg_cell_size // 2
       
        # Create temporary moving peg
        peg = self.canvas.create_oval(
            from_x - 25, from_y - 25,
            from_x + 25, from_y + 25,
            fill=self.peg_colors['P'],
            outline='black',
            tags='moving_peg'
        )
       
        # Animation steps
        steps = 20
        dx = (to_x - from_x) / steps
        dy = (to_y - from_y) / steps
       
        def move_peg(step):
            if step < steps and not self.pause_requested and not self.stop_requested:
                self.canvas.move(peg, dx, dy)
                self.root.after(self.animation_speed // steps, move_peg, step + 1)
            else:
                self.canvas.delete(peg)
                callback()
       
        move_peg(0)
   
    def is_valid_move(self, board, from_idx, over_idx, to_idx):
        return (
            0 <= from_idx < len(board)
            and 0 <= over_idx < len(board)
            and 0 <= to_idx < len(board)
            and board[from_idx] == 'P'
            and board[over_idx] == 'P'
            and board[to_idx] == '_'
        )
   
    def apply_move(self, board, from_idx, over_idx, to_idx):
        new_board = board[:]
        new_board[from_idx] = '_'
        new_board[over_idx] = '_'
        new_board[to_idx] = 'P'
        return new_board
   
    def solve_all(self, board, path, solutions):
        if board.count('P') == 1:
            solutions.append((path + [board], board.index('P')))
            return

        for i in range(len(board)):
            # Right jump
            if self.is_valid_move(board, i, i + 1, i + 2):
                new_board = self.apply_move(board, i, i + 1, i + 2)
                self.solve_all(new_board, path + [board], solutions)

            # Left jump
            if self.is_valid_move(board, i, i - 1, i - 2):
                new_board = self.apply_move(board, i, i - 1, i - 2)
                self.solve_all(new_board, path + [board], solutions)
   
    def analyze_all_initial_positions(self, n):
        results = {}
        all_solutions = {}

        for empty in range(n):
            board = ['P'] * n
            board[empty] = '_'
            solutions = []
            self.solve_all(board, [], solutions)
           
            if solutions:
                final_positions = list(set(sol[1] for sol in solutions))
                results[empty] = final_positions
                all_solutions[empty] = solutions
        return results, all_solutions
   
    def start_animation(self):
        if not self.animation_running:
            self.animation_running = True
            self.pause_requested = False
            self.stop_requested = False
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.DISABLED)
            self.execute_next_move()
   
    def pause_animation(self):
        if self.animation_running:
            self.pause_requested = True
            self.animation_running = False
            self.start_btn.config(text="Resume", state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.step_btn.config(state=tk.NORMAL)
   
    def stop_animation(self):
        self.stop_requested = True
        self.animation_running = False
        self.pause_requested = False
        self.start_btn.config(text="Start", state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.step_btn.config(state=tk.NORMAL)
   
    def step_animation(self):
        if not self.animation_running:
            self.execute_next_move()
   
    def execute_next_move(self):
        if self.stop_requested:
            return
           
        if self.knight_solution:  # Task 3 animation
            if self.current_knight_step < len(self.knight_solution):
                step = self.knight_solution[self.current_knight_step]
                knight_id, from_pos, to_pos = step
                color = knight_id[0]
               
                # Ensure we have proper knight IDs (remove question marks)
                if '?' in knight_id:
                    # Try to find the correct ID based on position
                    current_positions = self.calculate_current_positions()
                    for i, pos in enumerate(current_positions[color]):
                        if pos == from_pos:
                            knight_id = f"{color}{i+1}"
                            break
               
                print(f"Move {self.current_knight_step+1}/{self.total_moves}: {knight_id} from {from_pos} to {to_pos}")
               
                def after_knight_move():
                    self.current_knight_step += 1
                    current_positions = self.calculate_current_positions()
                    self.visualize_knight_board(current_positions)
                   
                    if self.current_knight_step < len(self.knight_solution):
                        if self.animation_running and not self.pause_requested:
                            self.root.after(self.animation_speed, self.execute_next_move)
                    else:
                        print("\n✅ Knight movement complete!")
                        self.stop_animation()
               
                self.animate_knight_move(from_pos, to_pos, after_knight_move)
               
        elif self.penny_history:  # Task 4 animation
            if self.current_penny_step < len(self.penny_history) - 1:
                self.current_penny_step += 1
                print(f"Step {self.current_penny_step}: {self.penny_history[self.current_penny_step]}")
                self.visualize_penny_boxes()
               
                if self.animation_running and not self.pause_requested:
                    self.root.after(self.animation_speed, self.execute_next_move)
            else:
                print("\n✅ Penny machine complete!")
                self.stop_animation()
               
        elif self.hanoi_moves:  # Task 6 animation
            if self.current_hanoi_step < len(self.hanoi_moves):
                from_peg, to_peg = self.hanoi_moves[self.current_hanoi_step]
                print(f"Move disk from {from_peg} to {to_peg}")
                self.current_hanoi_step += 1
               
                def after_hanoi_move():
                    # Update the visualization
                    if self.current_hanoi_step < len(self.hanoi_moves):
                        if self.animation_running and not self.pause_requested:
                            self.root.after(self.animation_speed, self.execute_next_move)
                    else:
                        print("\n✅ Tower of Hanoi complete!")
                        self.stop_animation()
               
                self.animate_hanoi_move(from_peg, to_peg, after_hanoi_move)
            else:
                self.stop_animation()
               
        elif self.peg_moves:  # Task 2 animation
            total_steps = len(self.peg_moves)
           
            if self.current_peg_step < total_steps - 1:
                self.current_peg_step += 1
                self.peg_board = self.peg_moves[self.current_peg_step]
               
                # Print with 1-based numbering
                print(f"Step {self.current_peg_step+1}/{total_steps}: {' '.join(self.peg_board)}")
                self.visualize_peg_board()
               
                if self.animation_running and not self.pause_requested:
                    self.root.after(self.animation_speed, self.execute_next_move)
            else:
                print("\n✅ Peg Solitaire complete!")
                self.stop_animation()
                       
        elif self.switch_steps:  # Task 5 animation
            if self.current_switch_step < len(self.switch_steps) - 1:
                self.current_switch_step += 1
                step_num, states = self.switch_steps[self.current_switch_step]
                print(f"Step {self.current_switch_step}: Flipped switch {step_num} → {' '.join(str(s) for s in states)}")
                self.visualize_switches()
               
                if self.animation_running and not self.pause_requested:
                    self.root.after(self.animation_speed, self.execute_next_move)
            else:
                print("\n✅ Switch puzzle complete!")
                self.stop_animation()
               
        elif self.rows:  # Task 1 animation
            # First check if we've reached the target configuration
            current_sizes = {row["row_num"]: len(row["coins"]) for row in self.rows}
            if current_sizes == self.target_sizes:
                print("\n✅ Inversion complete!")
                print(f"Total moves made: {self.current_move}")
                self.stop_animation()
                return
               
            # If not at target, perform next move
            if self.current_move == 0:
                # First move: slide top coin to bottom
                if len(self.rows) > 0:
                    self.current_move += 1
                   
                    def after_first_move():
                        # Remove from top
                        top_coin = self.rows[0]["coins"].pop(0)
                       
                        # If top row is now empty, remove it
                        if not self.rows[0]["coins"]:
                            empty_row = self.rows.pop(0)
                        else:
                            empty_row = None

                        # Update row numbers
                        for row in self.rows:
                            row["row_num"] -= 1

                        # Add to bottom
                        if empty_row:
                            empty_row["coins"] = [top_coin]
                            empty_row["row_num"] = len(self.rows) + 1 if self.rows else 1
                            self.rows.append(empty_row)
                        else:
                            # Create new bottom row if needed
                            if not self.rows or self.rows[-1]["row_num"] != len(self.rows):
                                new_row_num = len(self.rows) + 1
                                self.rows.append({"row_num": new_row_num, "coins": [top_coin], "type": "Bottom"})
                            else:
                                self.rows[-1]["coins"].append(top_coin)

                        self.update_row_types()
                        self.visualize_triangle()
                       
                        if self.animation_running and not self.pause_requested:
                            self.root.after(self.animation_speed, self.execute_next_move)
                   
                    # Animate moving the first coin from top to bottom
                    self.animate_coin_move(0, 0, len(self.rows)-1, len(self.rows[-1]["coins"]), after_first_move)
            else:
                # Subsequent moves - find a coin to move to correct position
                moved = False
                for i, row in enumerate(self.rows):
                    current_size = len(row["coins"])
                    target_size = self.target_sizes.get(row["row_num"], 0)
                   
                    if current_size < target_size:
                        # Find a donor row with excess coins
                        for j, donor_row in enumerate(self.rows):
                            donor_current = len(donor_row["coins"])
                            donor_target = self.target_sizes.get(donor_row["row_num"], 0)
                           
                            if donor_current > donor_target:
                                # Found a donor row - move last coin from donor to current row
                                self.current_move += 1
                                moved = True
                               
                                def after_move(i=i, j=j):
                                    # Complete the move
                                    coin_to_move = self.rows[j]["coins"].pop()
                                    self.rows[i]["coins"].append(coin_to_move)
                                   
                                    # Clean up empty rows if needed
                                    if not self.rows[j]["coins"]:
                                        self.rows.pop(j)
                                        # Update row numbers
                                        for idx, row in enumerate(self.rows):
                                            row["row_num"] = idx + 1
                                   
                                    self.update_row_types()
                                    self.visualize_triangle()
                                   
                                    if self.animation_running and not self.pause_requested:
                                        self.root.after(self.animation_speed, self.execute_next_move)
                               
                                # Animate the coin movement
                                self.animate_coin_move(
                                    j, len(self.rows[j]["coins"])-1,
                                    i, len(self.rows[i]["coins"]),
                                    after_move
                                )
                                break  # Exit after starting one animation
                        if moved:
                            break
               
                if not moved and not self.stop_requested:
                    print("\n✅ Inversion complete!")
                    print(f"Total moves made: {self.current_move}")
                    self.stop_animation()
   
    def execute_adjustment(self):
        changed = False
        for row in self.rows:
            current_size = len(row["coins"])
            expected_size = self.target_sizes.get(row["row_num"], 0)

            if current_size < expected_size:
                # Find a donor row with excess coins
                donor = next((r for r in self.rows if len(r["coins"]) > self.target_sizes.get(r["row_num"], 0)), None)
                if donor:
                    self.current_move += 1
                    changed = True
                   
                    def after_adjustment_move():
                        # Complete the move
                        coin_to_move = donor["coins"].pop()
                        row["coins"].append(coin_to_move)
                       
                        self.update_row_types()
                        self.visualize_triangle()
                       
                        # Continue with next adjustment if needed
                        self.execute_adjustment()
                   
                    # Animate the coin movement
                    self.animate_coin_move(
                        self.rows.index(donor), len(donor["coins"])-1,
                        self.rows.index(row), len(row["coins"])-1,  # Changed to -1 here
                        after_adjustment_move
                    )
                    return  # Exit after starting one animation
           
        if not changed and not self.stop_requested:
            print("\n✅ Inversion complete!")
            print(f"Total moves made: {self.current_move}")
            self.stop_animation()
                   
                   
       
       
   
    def update_row_types(self):
        for idx, row in enumerate(self.rows):
            if idx == 0:
                row["type"] = "Top"
            elif idx == len(self.rows) - 1:
                row["type"] = "Bottom"
            else:
                row["type"] = "Middle"
   
    def get_integer_input(self, prompt, min_value=1):
        while True:
            try:
                value = simpledialog.askinteger("Input", prompt, parent=self.root)
                if value is None:
                    return None
                if value < min_value:
                    messagebox.showerror("Error", f"Value must be ≥ {min_value}")
                    continue
                return value
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer")

if __name__ == "__main__":
    root = tk.Tk()
    app = TasksApp(root)
    root.mainloop()