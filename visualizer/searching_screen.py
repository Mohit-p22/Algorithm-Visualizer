import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import random
from algorithms.searching import SearchingAlgorithms
import time

class SearchingScreen:
    def __init__(self, algorithm, main_window):
        self.window = tk.Toplevel()
        self.window.title("Searching Algorithm Visualizer")
        self.window.geometry("1400x700")
        self.window.configure(bg="#2c3e50")
        self.main_window = main_window
        self.algorithm = algorithm
        
        self.array_size = 15
        self.min_val = 1
        self.max_val = 100
        self.speed = 100
        self.array = []
        self.searching_in_progress = False
        self.bar_color = "#3498db"
        self.target = None
        
        self.setup_ui()
        self.generate_array()
        
    def setup_ui(self):
        # Main content frame (left side)
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control panel (right side)
        control_panel = tk.Frame(self.window, bg="#34495e", width=250)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_panel.pack_propagate(False)
        
        # Algorithm Selection
        algo_frame = tk.LabelFrame(control_panel, text="Algorithm Selection",
                                 bg="#34495e", fg="white")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        algorithms = ["Linear Search", "Binary Search", 
                     "Jump Search", "Interpolation Search"]
        
        self.algo_var = tk.StringVar(value=self.algorithm)
        for algo in algorithms:
            rb = tk.Radiobutton(algo_frame, text=algo, value=algo,
                              variable=self.algo_var,
                              bg="#34495e", fg="white",
                              selectcolor="black",
                              activebackground="#34495e",
                              activeforeground="white",
                              font=("Helvetica", 11, "bold"),
                              pady=5)
            rb.pack(anchor=tk.W, padx=10, pady=3)
        
        # Controls
        controls_frame = tk.LabelFrame(control_panel, text="Controls",
                                     bg="#34495e", fg="white")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search value input
        tk.Label(controls_frame, text="Search Value:",
                bg="#34495e", fg="white").pack(anchor=tk.W, padx=5)
        self.search_entry = tk.Entry(controls_frame)
        self.search_entry.pack(fill=tk.X, padx=5, pady=2)
        
        # Array size control
        tk.Label(controls_frame, text="Array Size:",
                bg="#34495e", fg="white").pack(anchor=tk.W, padx=5)
        self.size_scale = tk.Scale(controls_frame, from_=5, to=50,
                                 orient=tk.HORIZONTAL,
                                 bg="#34495e", fg="white",
                                 highlightthickness=0,
                                 command=self.update_array_size)
        self.size_scale.set(self.array_size)
        self.size_scale.pack(fill=tk.X, padx=5)
        
        # Speed control
        tk.Label(controls_frame, text="Speed:",
                bg="#34495e", fg="white").pack(anchor=tk.W, padx=5)
        self.speed_scale = tk.Scale(controls_frame, from_=1, to=200,
                                  orient=tk.HORIZONTAL,
                                  bg="#34495e", fg="white",
                                  highlightthickness=0)
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(fill=tk.X, padx=5)
        
        # Color picker
        tk.Button(controls_frame, text="Change Element Color",
                 command=self.choose_color).pack(fill=tk.X, padx=5, pady=5)
        
        # Action buttons
        buttons_frame = tk.Frame(controls_frame, bg="#34495e")
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.generate_btn = tk.Button(buttons_frame, text="Generate Array",
                                    command=self.generate_array)
        self.generate_btn.pack(fill=tk.X, pady=2)
        
        self.search_btn = tk.Button(buttons_frame, text="Start Search",
                                  command=self.start_search)
        self.search_btn.pack(fill=tk.X, pady=2)
        
        self.stop_btn = tk.Button(buttons_frame, text="Stop",
                                command=self.stop_search,
                                state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=2)
        
        tk.Button(buttons_frame, text="Back to Menu",
                 command=self.back_to_main).pack(fill=tk.X, pady=2)
        
        # Stats frame
        stats_frame = tk.LabelFrame(control_panel, text="Statistics",
                                  bg="#34495e", fg="white")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.comparison_label = tk.Label(stats_frame,
                                       text="Comparisons: 0",
                                       bg="#34495e", fg="white")
        self.comparison_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.time_label = tk.Label(stats_frame,
                                 text="Time: 0.00 seconds",
                                 bg="#34495e", fg="white")
        self.time_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(main_frame, width=1100, height=600,
                              bg="white")
        self.canvas.pack(padx=10, pady=10)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Element Color",
                                    color=self.bar_color)
        if color[1]:
            self.bar_color = color[1]
            self.draw_array(self.array)
            
    def draw_array(self, array, current_idx=None, found_idx=None):
        self.canvas.delete("all")
        width = 1100
        height = 600
        element_width = width // (len(array) + 2)
        element_height = 60
        start_x = (width - (element_width * len(array))) // 2
        start_y = height // 2 - element_height
        
        for i, val in enumerate(array):
            x = start_x + (i * element_width)
            
            # Determine element color
            if i == found_idx:
                color = "#2ecc71"  # Green for found
            elif i == current_idx:
                color = "#e74c3c"  # Red for current
            else:
                color = self.bar_color
                
            # Draw element box
            self.canvas.create_rectangle(
                x, start_y,
                x + element_width - 2,
                start_y + element_height,
                fill=color,
                outline="black"
            )
            
            # Draw value
            self.canvas.create_text(
                x + element_width//2,
                start_y + element_height//2,
                text=str(val),
                font=("Helvetica", 12, "bold")
            )
            
            # Draw index
            self.canvas.create_text(
                x + element_width//2,
                start_y + element_height + 20,
                text=f"[{i}]",
                font=("Helvetica", 10)
            )
            
        self.window.update_idletasks()
        
    def update_array_size(self, val):
        if not self.searching_in_progress:
            self.array_size = int(val)
            self.generate_array()
            
    def generate_array(self):
        self.array = sorted([random.randint(self.min_val, self.max_val)
                           for _ in range(self.array_size)])
        self.draw_array(self.array)
        
    def disable_controls(self):
        self.searching_in_progress = True
        self.generate_btn.config(state=tk.DISABLED)
        self.search_btn.config(state=tk.DISABLED)
        self.size_scale.config(state=tk.DISABLED)
        self.speed_scale.config(state=tk.DISABLED)
        self.search_entry.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
    def enable_controls(self):
        self.searching_in_progress = False
        self.generate_btn.config(state=tk.NORMAL)
        self.search_btn.config(state=tk.NORMAL)
        self.size_scale.config(state=tk.NORMAL)
        self.speed_scale.config(state=tk.NORMAL)
        self.search_entry.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
    def stop_search(self):
        self.searching_in_progress = False
        self.enable_controls()
        
    def start_search(self):
        if self.searching_in_progress:
            return
            
        try:
            target = int(self.search_entry.get())
            self.target = target
            
            self.disable_controls()
            
            algorithm_map = {
                "Linear Search": SearchingAlgorithms.linear_search,
                "Binary Search": SearchingAlgorithms.binary_search,
                "Jump Search": SearchingAlgorithms.jump_search,
                "Interpolation Search": SearchingAlgorithms.interpolation_search
            }
            
            search_algo = algorithm_map.get(self.algo_var.get())
            if not search_algo:
                return
                
            self.comparisons = 0
            self.start_time = time.time()
            
            def update_visualization():
                if not self.searching_in_progress:
                    self.enable_controls()
                    return
                    
                try:
                    self.comparisons = next(self.search_generator)
                    self.comparison_label.config(
                        text=f"Comparisons: {self.comparisons}")
                    elapsed_time = time.time() - self.start_time
                    self.time_label.config(
                        text=f"Time: {elapsed_time:.2f} seconds")
                    
                    delay = int(1000 * (1 / self.speed_scale.get()))
                    self.window.after(delay, update_visualization)
                    
                except StopIteration as result:
                    elapsed_time = time.time() - self.start_time
                    self.time_label.config(
                        text=f"Time: {elapsed_time:.2f} seconds")
                    
                    if result.value != -1:
                        messagebox.showinfo("Success",
                            f"Found {target} at index {result.value}")
                    else:
                        messagebox.showinfo("Not Found",
                            f"Value {target} not found in array")
                    
                    self.enable_controls()
                    
            self.search_generator = search_algo(
                self.array,
                target,
                self.draw_array,
                self.speed_scale.get()
            )
            
            update_visualization()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            
    def back_to_main(self):
        self.window.destroy()
        self.main_window.deiconify() 