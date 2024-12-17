import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
from algorithms.dynamic import DynamicAlgorithms

class DynamicScreen:
    def __init__(self, algorithm, main_window):
        self.window = tk.Toplevel()
        self.window.title(f"Dynamic Programming - {algorithm}")
        self.window.geometry("1000x600")
        self.window.configure(bg="#2c3e50")
        self.main_window = main_window
        self.algorithm = algorithm
        self.is_running = False
        self.canvas = None  # Initialize canvas attribute
        self.steps = 0
        self.start_time = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main content frame
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control panel
        control_panel = tk.Frame(self.window, bg="#34495e", width=300)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_panel.pack_propagate(False)  # Prevent control panel from shrinking
        
        # Input frame
        input_frame = tk.LabelFrame(control_panel, text="Input",
                                  bg="#34495e", fg="white")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        if "Fibonacci" in self.algorithm:
            self.setup_fibonacci_inputs(input_frame)
        else:
            self.setup_lcs_inputs(input_frame)
        
        # Controls frame
        controls_frame = tk.LabelFrame(control_panel, text="Controls",
                                     bg="#34495e", fg="white")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Speed control
        tk.Label(controls_frame, text="Animation Speed:",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.speed_scale = tk.Scale(controls_frame, from_=1, to=10,
                                  orient=tk.HORIZONTAL, bg="#34495e", fg="white",
                                  highlightthickness=0)
        self.speed_scale.set(5)
        self.speed_scale.pack(padx=5, pady=2, fill=tk.X)
        
        # Control buttons
        self.start_btn = tk.Button(controls_frame, text="Solve",
                                 command=self.start_visualization)
        self.start_btn.pack(padx=5, pady=2, fill=tk.X)
        
        self.stop_btn = tk.Button(controls_frame, text="Stop",
                                command=self.stop_visualization,
                                state=tk.DISABLED)
        self.stop_btn.pack(padx=5, pady=2, fill=tk.X)
        
        # Reset button
        tk.Button(controls_frame, text="Reset",
                 command=self.reset_visualization,
                 bg="#3498db",
                 fg="white").pack(padx=5, pady=2, fill=tk.X)
        
        # Back button
        tk.Button(controls_frame, text="Back to Main Menu",
                 command=self.back_to_main,
                 bg="#e74c3c",
                 fg="white",
                 activebackground="#c0392b",
                 activeforeground="white").pack(padx=5, pady=2, fill=tk.X)
        
        # Steps Panel
        self.steps_panel = tk.LabelFrame(control_panel, text="Progress",
                                     bg="#34495e", fg="white")
        self.steps_panel.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        # Step counter
        self.step_counter = tk.Label(self.steps_panel, 
                                   text="Steps: 0",
                                   bg="#34495e", fg="white")
        self.step_counter.pack(padx=5, pady=2)
        
        # Current operation
        self.current_operation = tk.Label(self.steps_panel,
                                        text="Current: -",
                                        bg="#34495e", fg="white",
                                        wraplength=250)
        self.current_operation.pack(padx=5, pady=2)
        
        # Time taken
        self.time_label = tk.Label(self.steps_panel,
                                 text="Time: 0.00s",
                                 bg="#34495e", fg="white")
        self.time_label.pack(padx=5, pady=2)
        
        # Step history
        self.step_history = tk.Text(self.steps_panel, 
                                  height=8,
                                  bg="#2c3e50", fg="white",
                                  wrap=tk.WORD)
        self.step_history.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Add scrollbar for step history
        scrollbar = tk.Scrollbar(self.steps_panel, command=self.step_history.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_history.config(yscrollcommand=scrollbar.set)
        
        # Canvas for visualization (in main frame)
        self.canvas = tk.Canvas(main_frame, bg="white", height=400)
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Step description
        self.step_label = tk.Label(main_frame, 
                                 text="Enter sequence or generate random one",
                                 bg="#2c3e50", fg="white", wraplength=700)
        self.step_label.pack(padx=10, pady=5)

    def setup_fibonacci_inputs(self, input_frame):
        # Initialize sequence_var as class attribute
        self.sequence_var = tk.StringVar(value="1, 1, 2, 3, 5, 8")
        
        # Sequence input
        tk.Label(input_frame, text="Enter sequence (comma-separated):",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.sequence_entry = tk.Entry(input_frame, textvariable=self.sequence_var)
        self.sequence_entry.pack(padx=5, pady=2, fill=tk.X)
        
        # Length slider for random generation
        tk.Label(input_frame, text="Random Sequence Length:",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.length_scale = tk.Scale(input_frame, from_=3, to=15,
                                   orient=tk.HORIZONTAL, bg="#34495e", fg="white",
                                   highlightthickness=0)
        self.length_scale.set(6)
        self.length_scale.pack(padx=5, pady=2, fill=tk.X)
        
        # Generate random button
        tk.Button(input_frame, text="Generate Random Sequence",
                 command=self.generate_random).pack(padx=5, pady=5, fill=tk.X)

    def setup_lcs_inputs(self, input_frame):
        # String 1 input
        tk.Label(input_frame, text="String 1:",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.str1_var = tk.StringVar(value="ABCBDAB")
        self.str1_entry = tk.Entry(input_frame, textvariable=self.str1_var)
        self.str1_entry.pack(padx=5, pady=2, fill=tk.X)
        
        # String 2 input
        tk.Label(input_frame, text="String 2:",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.str2_var = tk.StringVar(value="BDCAB")
        self.str2_entry = tk.Entry(input_frame, textvariable=self.str2_var)
        self.str2_entry.pack(padx=5, pady=2, fill=tk.X)
        
        # Generate Grid button
        tk.Button(input_frame, text="Generate Grid",
                 command=self.generate_lcs_grid).pack(padx=5, pady=5, fill=tk.X)

    def generate_lcs_grid(self):
        str1 = self.str1_var.get()
        str2 = self.str2_var.get()
        
        if not str1 or not str2:
            messagebox.showerror("Error", "Please enter both strings")
            return
            
        # Create initial grid state
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Draw initial grid
        self.draw_lcs({
            'type': 'lcs',
            'dp': dp,
            'str1': str1,
            'str2': str2,
            'i': None,
            'j': None,
            'step': 'Grid generated. Click Solve to start visualization.',
            'complete': False
        })
        
        # Enable solve button
        self.start_btn.config(state=tk.NORMAL)
        
        # Update step label
        self.step_label.config(text="Grid generated. Click Solve to start visualization.")

    def back_to_main(self):
        """Return to main menu"""
        if self.is_running:
            self.stop_visualization()
        self.window.destroy()
        self.main_window.deiconify()
        
    def generate_random(self):
        length = self.length_scale.get()
        sequence = DynamicAlgorithms.generate_random_sequence(length)
        self.sequence_var.set(", ".join(map(str, sequence)))
        self.draw_initial_sequence(sequence)
        
    def draw_initial_sequence(self, sequence):
        if self.canvas:  # Check if canvas exists
            self.canvas.delete("all")
            # Rest of your drawing code...
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            box_size = min(width // (len(sequence) + 2), height // 6)
            label_margin = 80
            start_x = label_margin + (width - label_margin - (len(sequence) * (box_size + 10))) // 2
            y = height // 2
            
            self.canvas.create_text(10, y, text="Initial Sequence:",
                                  anchor="w", font=("Arial", 12, "bold"))
            
            for i, num in enumerate(sequence):
                x = start_x + i * (box_size + 10)
                self.canvas.create_rectangle(x, y - box_size//2,
                                          x + box_size, y + box_size//2,
                                          fill="#ecf0f1", outline="#2c3e50")
                self.canvas.create_text(x + box_size//2, y,
                                      text=str(num),
                                      font=("Arial", int(box_size//3 * 0.6)))
        
    def parse_sequence(self):
        try:
            sequence = [int(x.strip()) for x in self.sequence_var.get().split(",")]
            return sequence
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers separated by commas")
            return None
        
    def draw_visualization(self, state):
        self.update_step_info(state)
        self.canvas.delete("all")
        
        if state.get('type') == 'lcs':
            self.draw_lcs(state)
        else:
            self.draw_fibonacci(state)

    def draw_lcs(self, state):
        dp = state['dp']
        str1 = state['str1']
        str2 = state['str2']
        curr_i = state['i']
        curr_j = state['j']
        
        # Calculate dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cell_size = min(width // (len(dp[0]) + 3), height // (len(dp) + 3))
        start_x = (width - (len(dp[0]) * cell_size)) // 2
        start_y = (height - (len(dp) * cell_size)) // 2
        
        # Draw column headers (str2)
        self.canvas.create_text(start_x - cell_size//2, start_y - cell_size//2,
                              text="", font=("Arial", 12, "bold"))
        
        for j, char in enumerate([" "] + list(str2)):
            x = start_x + j * cell_size + cell_size//2
            y = start_y - cell_size//2
            # Draw header cell
            self.canvas.create_rectangle(x - cell_size//2, y - cell_size//2,
                                      x + cell_size//2, y + cell_size//2,
                                      fill="#bdc3c7", outline="#2c3e50")
            self.canvas.create_text(x, y, text=char,
                                  font=("Arial", 12, "bold"),
                                  fill="#2c3e50")
        
        # Draw row headers (str1)
        for i, char in enumerate([" "] + list(str1)):
            x = start_x - cell_size//2
            y = start_y + i * cell_size + cell_size//2
            # Draw header cell
            self.canvas.create_rectangle(x - cell_size//2, y - cell_size//2,
                                      x + cell_size//2, y + cell_size//2,
                                      fill="#bdc3c7", outline="#2c3e50")
            self.canvas.create_text(x, y, text=char,
                                  font=("Arial", 12, "bold"),
                                  fill="#2c3e50")
        
        # Draw grid
        for i in range(len(dp)):
            for j in range(len(dp[0])):
                x = start_x + j * cell_size
                y = start_y + i * cell_size
                
                # Determine cell color
                color = "#ecf0f1"  # Default color
                if i == curr_i and j == curr_j:
                    color = "#f1c40f"  # Current cell
                elif state.get('backtrack', False) and dp[i][j] > 0:
                    color = "#2ecc71"  # Backtracking path
                elif i == curr_i or j == curr_j:
                    color = "#bdc3c7"  # Current row/column
                
                # Draw cell
                self.canvas.create_rectangle(x, y,
                                          x + cell_size, y + cell_size,
                                          fill=color, outline="#2c3e50")
                self.canvas.create_text(x + cell_size//2, y + cell_size//2,
                                      text=str(dp[i][j]),
                                      font=("Arial", int(cell_size//3)))
        
        # Draw LCS if available
        if 'lcs' in state:
            lcs_text = f"Longest Common Subsequence: {state['lcs']}"
            self.canvas.create_text(width//2, start_y - cell_size*2,
                                  text=lcs_text,
                                  font=("Arial", 14, "bold"),
                                  fill="#2c3e50")

    def start_visualization(self):
        if "Fibonacci" in self.algorithm:
            sequence = self.parse_sequence()
            if not sequence:
                return
            inputs = sequence
        else:  # LCS
            str1 = self.str1_var.get()
            str2 = self.str2_var.get()
            if not str1 or not str2:
                messagebox.showerror("Error", "Please enter both strings")
                return
            inputs = (str1, str2)
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Reset counters and history
        self.reset_progress()
        
        self.start_time = time.time()
        self.visualization = DynamicAlgorithms.get_algorithm(
            self.algorithm,  # Use the exact algorithm name
            inputs,
            self.draw_visualization
        )
        
        self.continue_visualization(self.start_time)
        
    def continue_visualization(self, start_time):
        if not self.is_running:
            return
            
        try:
            result = next(self.visualization)
            
            if isinstance(result, bool):
                end_time = time.time()
                elapsed_time = end_time - start_time
                self.stop_visualization()
                messagebox.showinfo("Success", 
                                  f"Visualization completed successfully!\n"
                                  f"Time taken: {elapsed_time:.2f} seconds")
                return
                
            delay = int(1000 / self.speed_scale.get())
            self.window.after(delay, self.continue_visualization, start_time)
            
        except StopIteration:
            self.stop_visualization()
            
    def stop_visualization(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        if self.start_time:
            total_time = time.time() - self.start_time
            self.time_label.config(text=f"Time: {total_time:.2f}s")
            self.current_operation.config(text="Current: Stopped")
            self.step_history.insert(tk.END, f"\nVisualization stopped after {self.steps} steps\n")
            self.step_history.see(tk.END)
        
    def reset_visualization(self):
        """Reset the visualization state"""
        self.stop_visualization()
        self.canvas.delete("all")
        self.reset_progress()
        
        if "LCS" in self.algorithm:
            # Reset LCS specific elements
            self.str1_var.set("ABCBDAB")
            self.str2_var.set("BDCAB")
            self.step_label.config(text="Enter strings and click Generate Grid")
        else:
            # Reset Fibonacci specific elements
            self.sequence_var.set("1, 1, 2, 3, 5, 8")
            self.step_label.config(text="Enter sequence or generate random one")
        
        self.start_btn.config(state=tk.NORMAL)
        
    def update_step_info(self, state):
        self.steps += 1
        current_time = time.time() - self.start_time
        
        # Update step counter
        self.step_counter.config(text=f"Steps: {self.steps}")
        
        # Update time
        self.time_label.config(text=f"Time: {current_time:.2f}s")
        
        # Update current operation
        operation_text = state.get('step', '-')
        self.current_operation.config(text=f"Current: {operation_text}")
        
        # Add to step history
        self.step_history.insert(tk.END, f"Step {self.steps}: {operation_text}\n")
        self.step_history.see(tk.END)

    def draw_fibonacci(self, state):
        sequence = state['sequence']
        original = state['original']
        current = state['current']
        prev1 = state['prev1']
        prev2 = state['prev2']
        
        # Calculate dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        box_size = min(width // (len(sequence) + 2), height // 6)
        label_margin = 80
        start_x = label_margin + (width - label_margin - (len(sequence) * (box_size + 10))) // 2
        
        # Draw original sequence
        y_orig = height // 3
        self.canvas.create_text(10, y_orig, text="Original:",
                              anchor="w", font=("Arial", 12, "bold"))
        
        for i, num in enumerate(original):
            x = start_x + i * (box_size + 10)
            self.canvas.create_rectangle(x, y_orig - box_size//2,
                                      x + box_size, y_orig + box_size//2,
                                      fill="#bdc3c7", outline="#2c3e50")
            self.canvas.create_text(x + box_size//2, y_orig,
                                  text=str(num),
                                  font=("Arial", int(box_size//3 * 0.6)))
        
        # Draw Fibonacci sequence
        y = height * 2 // 3
        self.canvas.create_text(10, y, text="Fibonacci:",
                              anchor="w", font=("Arial", 12, "bold"))
        
        for i, num in enumerate(sequence):
            x = start_x + i * (box_size + 10)
            color = "#ecf0f1"
            if i == current:
                color = "#f1c40f"
            elif i == prev1:
                color = "#e74c3c"
            elif i == prev2:
                color = "#e67e22"
                
            self.canvas.create_rectangle(x, y - box_size//2,
                                      x + box_size, y + box_size//2,
                                      fill=color, outline="#2c3e50")
            self.canvas.create_text(x + box_size//2, y,
                                  text=str(num),
                                  font=("Arial", int(box_size//3 * 0.6)))
            
            self.canvas.create_text(x + box_size//2, y + box_size//2 + 10,
                                  text=f"F({i})",
                                  font=("Arial", 8))
            
        if current is not None and prev1 is not None and prev2 is not None:
            curr_x = start_x + current * (box_size + 10) + box_size//2
            prev1_x = start_x + prev1 * (box_size + 10) + box_size//2
            prev2_x = start_x + prev2 * (box_size + 10) + box_size//2
            
            self.canvas.create_line(prev1_x, y - box_size//2 - 10,
                                 curr_x, y - box_size//2 - 20,
                                 arrow=tk.LAST, fill="#e74c3c", width=2)
            self.canvas.create_line(prev2_x, y - box_size//2 - 10,
                                 curr_x, y - box_size//2 - 20,
                                 arrow=tk.LAST, fill="#e67e22", width=2)

    def reset_progress(self):
        self.steps = 0
        self.step_counter.config(text="Steps: 0")
        self.current_operation.config(text="Current: Starting...")
        self.time_label.config(text="Time: 0.00s")
        self.step_history.delete(1.0, tk.END)