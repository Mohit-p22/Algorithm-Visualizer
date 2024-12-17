import tkinter as tk
from tkinter import ttk, colorchooser
import random
from algorithms.sorting import SortingAlgorithms
import time

class SortingScreen:
    def __init__(self, algorithm, main_window):
        self.window = tk.Toplevel()
        self.window.title(f"Sorting Algorithm Visualizer")
        self.window.geometry("1400x700")
        self.window.configure(bg="#2c3e50")
        self.main_window = main_window
        self.algorithm = algorithm
        
        # Initialize variables
        self.array_size = 30
        self.min_val = 5
        self.max_val = 100
        self.speed = 100
        self.array = []
        self.sorting_in_progress = False
        self.sorting_completed = False  # Add new flag
        self.bar_color = "#3498db"  # Default color
        
        self.setup_ui()
        self.generate_array()
        
    def setup_ui(self):
        # Main content frame (left side)
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control panel (right side)
        control_panel = tk.Frame(self.window, bg="#34495e", width=250)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_panel.pack_propagate(False)  # Fix width
        
        # Algorithm Selection with larger radio buttons
        algo_frame = tk.LabelFrame(control_panel, text="Algorithm Selection",
                                 bg="#34495e", fg="white")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        algorithms = [
            "Bubble Sort",
            "Selection Sort",
            "Insertion Sort",
            "Quick Sort",
            "Merge Sort",
            "Heap Sort"
        ]
        
        self.algo_var = tk.StringVar(value=self.algorithm)
        for algo in algorithms:
            rb = tk.Radiobutton(algo_frame, text=algo, value=algo,
                              variable=self.algo_var,
                              bg="#34495e", fg="white",
                              selectcolor="black",
                              activebackground="#34495e",
                              activeforeground="white",
                              font=("Helvetica", 11, "bold"),  # Increased font size
                              pady=5)  # Added padding
            rb.pack(anchor=tk.W, padx=10, pady=3)  # Increased padding
        
        # Controls in control panel
        controls_frame = tk.LabelFrame(control_panel, text="Controls",
                                     bg="#34495e", fg="white")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Array size control with immediate update
        tk.Label(controls_frame, text="Array Size:", bg="#34495e",
                fg="white").pack(anchor=tk.W, padx=5)
        self.size_scale = tk.Scale(controls_frame, from_=5, to=100,
                                 orient=tk.HORIZONTAL,
                                 bg="#34495e", fg="white",
                                 highlightthickness=0,
                                 command=self.update_array_size)  # Added direct command
        self.size_scale.set(self.array_size)
        self.size_scale.pack(fill=tk.X, padx=5)
        
        # Speed control
        tk.Label(controls_frame, text="Speed:", bg="#34495e",
                fg="white").pack(anchor=tk.W, padx=5)
        self.speed_scale = tk.Scale(controls_frame, from_=1, to=200,
                                  orient=tk.HORIZONTAL,
                                  bg="#34495e", fg="white",
                                  highlightthickness=0)
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(fill=tk.X, padx=5)
        
        # Color picker
        tk.Button(controls_frame, text="Change Bar Color",
                 command=self.choose_color).pack(fill=tk.X, padx=5, pady=5)
        
        # Action buttons
        buttons_frame = tk.Frame(controls_frame, bg="#34495e")
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.generate_btn = tk.Button(buttons_frame, text="Generate Array",
                                    command=self.generate_array)
        self.generate_btn.pack(fill=tk.X, pady=2)
        
        self.sort_btn = tk.Button(buttons_frame, text="Start Sorting",
                                command=self.start_sorting)
        self.sort_btn.pack(fill=tk.X, pady=2)
        
        self.stop_btn = tk.Button(buttons_frame, text="Stop",
                                command=self.stop_sorting,
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
        color = colorchooser.askcolor(title="Choose Bar Color",
                                    color=self.bar_color)
        if color[1]:  # If color is chosen (not cancelled)
            self.bar_color = color[1]
            self.draw_array(self.array)
            
    def stop_sorting(self):
        self.sorting_in_progress = False
        self.enable_controls()
        self.stop_btn.config(state=tk.DISABLED)
        
    def disable_controls(self):
        self.sorting_in_progress = True
        self.generate_btn.config(state=tk.DISABLED)
        self.sort_btn.config(state=tk.DISABLED)
        self.size_scale.config(state=tk.DISABLED)
        self.speed_scale.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state=tk.DISABLED)
                
    def enable_controls(self):
        self.sorting_in_progress = False
        self.generate_btn.config(state=tk.NORMAL)
        self.sort_btn.config(state=tk.NORMAL)
        self.size_scale.config(state=tk.NORMAL)
        self.speed_scale.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state=tk.NORMAL)
                
    def draw_array(self, array, colors=None):
        """Draw the array with specified colors"""
        if self.sorting_completed and colors is None:
            # If sorting is complete and no colors specified, keep bars green
            colors = ["#2ecc71"] * len(array)
        elif colors is None:
            colors = [self.bar_color] * len(array)
            
        self.canvas.delete("all")
        canvas_width = 1100
        canvas_height = 600
        bar_width = canvas_width / (len(array) + 1)
        max_val = max(array)
        
        for i, val in enumerate(array):
            x0 = i * bar_width + 10
            y0 = canvas_height - (val/max_val * 500)
            x1 = (i + 1) * bar_width
            y1 = canvas_height - 20
            
            # Draw bar
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=colors[i],
                outline="black"
            )
            
            # Draw value on top of bar
            self.canvas.create_text(
                x0 + bar_width/2,
                y0 - 10,
                text=str(val),
                fill="black",
                font=("Helvetica", 8)
            )
            
            # Draw index below bar
            self.canvas.create_text(
                x0 + bar_width/2,
                canvas_height - 10,
                text=str(i),
                fill="black",
                font=("Helvetica", 8)
            )
        
        self.canvas.update()
        
    def start_sorting(self):
        """Start the sorting process"""
        if not self.sorting_in_progress and self.array:
            self.sorting_in_progress = True
            self.sort_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            # Reset statistics
            self.comparisons = 0
            self.swaps = 0
            self.start_time = time.time()
            
            # Get selected algorithm
            algorithm = self.algo_var.get()
            
            try:
                self.sort_generator = SortingAlgorithms.get_algorithm(
                    algorithm,
                    self.array,
                    self.draw_array,
                    self.speed_scale.get()
                )
                self.update_visualization()
                
            except Exception as e:
                print(f"Error: {str(e)}")
                self.sorting_in_progress = False
                self.sort_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
        
    def generate_array(self):
        """Generate new array and reset sorting status"""
        self.sorting_completed = False  # Reset completion flag
        self.array_size = self.size_scale.get()
        self.array = [random.randint(self.min_val, self.max_val)
                     for _ in range(self.array_size)]
        self.comparisons = 0
        self.time_label.config(text="Time: 0.00 seconds")
        self.comparison_label.config(text="Comparisons: 0")
        self.draw_array(self.array)
        
    def back_to_main(self):
        self.window.destroy()
        self.main_window.deiconify()
    
    def update_array_size(self, val):
        """Update array size only if not sorting"""
        if not self.sorting_in_progress:
            self.array_size = int(val)
            self.generate_array()
        
    def update_visualization(self):
        if self.sorting_in_progress:
            try:
                next(self.sort_generator)
                delay = int(1000 / self.speed_scale.get())
                self.window.after(delay, self.update_visualization)
            except StopIteration:
                self.sorting_in_progress = False
                self.sorting_completed = True  # Set completion flag
                self.enable_controls()
                elapsed_time = time.time() - self.start_time
                self.time_label.config(text=f"Time: {elapsed_time:.2f} seconds")
                self.comparison_label.config(text=f"Comparisons: {self.comparisons}")
                # Draw final sorted array in green
                self.draw_final_sorted_array()
        
    def draw_final_sorted_array(self):
        """Draw the final sorted array in green"""
        colors = ["#2ecc71"] * len(self.array)  # All bars in green
        self.draw_array(self.array, colors)
        self.window.update()