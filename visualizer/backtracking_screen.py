import tkinter as tk
from tkinter import ttk, messagebox
import time
from algorithms.backtracking import BacktrackingAlgorithms

class BacktrackingScreen:
    def __init__(self, algorithm, main_window):
        self.window = tk.Toplevel()
        self.window.title(f"Backtracking - {algorithm}")
        self.window.geometry("800x800")
        self.window.configure(bg="#2c3e50")
        self.main_window = main_window
        self.algorithm = algorithm
        
        # Initialize variables
        self.visualization_speed = 100
        self.is_running = False
        self.board_size = 8 if "N-Queens" in algorithm else 9
        self.cell_size = 60
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.original_board = None
        self.current_cell = None
        self.analysis_time = 2
        
        self.setup_ui()
        self.draw_board()
        
    def setup_ui(self):
        # Main content frame (left side)
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control panel (right side)
        control_panel = tk.Frame(self.window, bg="#34495e", width=250)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_panel.pack_propagate(False)
        
        # Algorithm Info
        info_frame = tk.LabelFrame(control_panel, text="Algorithm Info",
                                 bg="#34495e", fg="white")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.info_label = tk.Label(info_frame,
                                 text=f"Current Algorithm: {self.algorithm}",
                                 bg="#34495e", fg="white",
                                 wraplength=230)
        self.info_label.pack(padx=5, pady=5)
        
        # Controls Frame
        controls_frame = tk.LabelFrame(control_panel, text="Controls",
                                     bg="#34495e", fg="white")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Speed control
        tk.Label(controls_frame, text="Speed:",
                bg="#34495e", fg="white").pack(anchor=tk.W, padx=5)
        self.speed_scale = tk.Scale(controls_frame, from_=1, to=10,
                                  orient=tk.HORIZONTAL)
        self.speed_scale.set(5)
        self.speed_scale.pack(fill=tk.X, padx=5)
        
        # Buttons
        buttons_frame = tk.Frame(controls_frame, bg="#34495e")
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(buttons_frame, text="Generate Puzzle",
                 command=self.generate_puzzle).pack(fill=tk.X, pady=2)
        
        self.start_btn = tk.Button(buttons_frame, text="Solve",
                                 command=self.start_visualization)
        self.start_btn.pack(fill=tk.X, pady=2)
        
        self.stop_btn = tk.Button(buttons_frame, text="Stop",
                                command=self.stop_visualization,
                                state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=2)
        
        tk.Button(buttons_frame, text="Reset",
                 command=self.reset_visualization).pack(fill=tk.X, pady=2)
        
        tk.Button(buttons_frame, text="Back to Menu",
                 command=self.back_to_main).pack(fill=tk.X, pady=2)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(main_frame, bg="white", width=540, height=540)
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
    def draw_board(self):
        self.canvas.delete("all")
        
        if "N-Queens" in self.algorithm:
            # Calculate board dimensions
            board_size = len(self.board)
            cell_size = min(500 // board_size, 60)
            board_pixel_size = cell_size * board_size
            
            # Center the board
            offset_x = (self.canvas.winfo_width() - board_pixel_size) // 2
            offset_y = (self.canvas.winfo_height() - board_pixel_size) // 2
            
            # Draw chess board
            for i in range(board_size):
                for j in range(board_size):
                    x1 = offset_x + j * cell_size
                    y1 = offset_y + i * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    
                    # Chess board pattern
                    color = "#f0d9b5" if (i + j) % 2 == 0 else "#b58863"
                    
                    # Highlight current cell
                    if (i, j) == self.current_cell:
                        color = "#aaa23a"
                    
                    # Draw square
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                              fill=color, outline="")
                    
                    # Draw queen
                    if self.board[i][j] == 1:
                        self.canvas.create_text(x1 + cell_size//2,
                                             y1 + cell_size//2,
                                             text="♕",
                                             font=("Arial", int(cell_size * 0.8)),
                                             fill="#2c3e50")
            
            # Draw border
            self.canvas.create_rectangle(offset_x - 2,
                                      offset_y - 2,
                                      offset_x + board_pixel_size + 2,
                                      offset_y + board_pixel_size + 2,
                                      outline="#4a4a4a",
                                      width=2)
            
            # Draw coordinates
            for i in range(board_size):
                # Row numbers
                self.canvas.create_text(offset_x - 15,
                                     offset_y + i * cell_size + cell_size//2,
                                     text=str(board_size - i),
                                     font=("Arial", 12),
                                     fill="#2c3e50")
                
                # Column letters
                self.canvas.create_text(offset_x + i * cell_size + cell_size//2,
                                     offset_y + board_pixel_size + 15,
                                     text=chr(97 + i),
                                     font=("Arial", 12),
                                     fill="#2c3e50")
        else:
            # Original Sudoku drawing code
            # Draw background for 3x3 boxes
            for box_i in range(3):
                for box_j in range(3):
                    if (box_i + box_j) % 2 == 0:  # Alternate coloring
                        x1 = box_j * self.cell_size * 3
                        y1 = box_i * self.cell_size * 3
                        x2 = x1 + self.cell_size * 3
                        y2 = y1 + self.cell_size * 3
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                  fill="#f0f0f0", outline="")
            
            # Draw cells and numbers
            for i in range(self.board_size):
                for j in range(self.board_size):
                    x1 = j * self.cell_size
                    y1 = i * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    
                    # Highlight current cell being processed
                    cell_color = "white"
                    if (i, j) == self.current_cell:
                        cell_color = "#fff3cd"  # Light yellow for current cell
                    
                    # Draw cell
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                              fill=cell_color, outline="gray")
                    
                    # Draw number
                    if self.board[i][j] != 0:
                        # Original numbers in black, solved numbers in blue
                        color = "black" if self.original_board and self.board[i][j] == self.original_board[i][j] else "blue"
                        self.canvas.create_text(x1 + self.cell_size//2,
                                              y1 + self.cell_size//2,
                                              text=str(self.board[i][j]),
                                              font=("Helvetica", 20, "bold" if color == "black" else "normal"),
                                              fill=color)
            
            # Draw grid lines
            for i in range(self.board_size + 1):
                # Determine line width
                width = 3 if i % 3 == 0 else 1
                color = "#2c3e50" if i % 3 == 0 else "gray"
                
                # Vertical lines
                self.canvas.create_line(i * self.cell_size, 0,
                                      i * self.cell_size, self.board_size * self.cell_size,
                                      width=width, fill=color)
                
                # Horizontal lines
                self.canvas.create_line(0, i * self.cell_size,
                                      self.board_size * self.cell_size, i * self.cell_size,
                                      width=width, fill=color)
                    
    def generate_puzzle(self):
        if "N-Queens" in self.algorithm:
            self.board = [[0] * self.board_size for _ in range(self.board_size)]
        else:
            # Original Sudoku generation code
            self.board = BacktrackingAlgorithms.generate_sudoku()
            self.original_board = [row[:] for row in self.board]
        
        self.current_cell = None
        self.draw_board()
        
    def start_visualization(self):
        if self.is_running:
            return
            
        if not any(0 in row for row in self.board):
            messagebox.showinfo("Info", "Please generate or reset the puzzle first!")
            return
            
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.steps = 0
        
        # Add analysis delay
        self.info_label.config(text="Analyzing puzzle...")
        self.window.after(int(self.analysis_time * 1000), self.begin_solving)
        
    def begin_solving(self):
        self.info_label.config(text=f"Solving {self.algorithm}...")
        start_time = time.time()
        
        self.visualization = BacktrackingAlgorithms.get_algorithm(
            self.algorithm,
            self.board,
            self.update_visualization
        )
        
        self.continue_visualization(start_time)
        
    def continue_visualization(self, start_time):
        if not self.is_running:
            return
            
        try:
            result = next(self.visualization)
            self.steps += 1
            
            if isinstance(result, bool):
                if result:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    self.stop_visualization()
                    messagebox.showinfo("Success", 
                                      f"Sudoku solved successfully!\n"
                                      f"Time taken: {elapsed_time:.2f} seconds\n"
                                      f"Steps: {self.steps}")
                    return
            
            # Faster speed = smaller delay
            delay = int(200 / self.speed_scale.get())
            self.window.after(delay, self.continue_visualization, start_time)
            
        except StopIteration:
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.stop_visualization()
            if not any(0 in row for row in self.board):
                messagebox.showinfo("Success", 
                                  f"Sudoku solved successfully!\n"
                                  f"Time taken: {elapsed_time:.2f} seconds\n"
                                  f"Steps: {self.steps}")
            
    def stop_visualization(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
    def reset_visualization(self):
        self.stop_visualization()
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.original_board = None
        self.current_cell = None
        self.info_label.config(text=f"Current Algorithm: {self.algorithm}")
        self.draw_board()
        
    def update_visualization(self, board, current_cell=None):
        self.board = board
        self.current_cell = current_cell
        self.draw_board()
        
    def back_to_main(self):
        self.window.destroy()
        self.main_window.deiconify()