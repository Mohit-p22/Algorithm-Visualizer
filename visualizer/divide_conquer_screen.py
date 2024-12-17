import tkinter as tk
from tkinter import ttk, messagebox
import time
from algorithms.divide_conquer import DivideConquerAlgorithms

class DivideConquerScreen:
    def __init__(self, algorithm, main_window):
        self.window = tk.Toplevel()
        self.window.title(f"Divide & Conquer - {algorithm}")
        self.window.geometry("1000x600")
        self.window.configure(bg="#2c3e50")
        self.main_window = main_window
        self.algorithm = algorithm
        self.is_running = False
        self.array = []
        self.setup_ui()

    def setup_ui(self):
        # Main content frame
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(main_frame, bg="white", height=400)
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Step description
        self.step_label = tk.Label(main_frame, text="Generate array to start",
                                 bg="#2c3e50", fg="white", wraplength=700)
        self.step_label.pack(padx=10, pady=5)
        
        # Control panel
        control_panel = tk.Frame(self.window, bg="#34495e", width=300)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_panel.pack_propagate(False)
        
        # Input frame
        input_frame = tk.LabelFrame(control_panel, text="Input",
                                  bg="#34495e", fg="white")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Array size slider
        tk.Label(input_frame, text="Array Size:",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.size_scale = tk.Scale(input_frame, from_=5, to=20,
                                 orient=tk.HORIZONTAL, bg="#34495e", fg="white",
                                 highlightthickness=0)
        self.size_scale.set(10)
        self.size_scale.pack(padx=5, pady=2, fill=tk.X)
        
        # Generate array button
        tk.Button(input_frame, text="Generate Random Array",
                 command=self.generate_array).pack(padx=5, pady=5, fill=tk.X)
        
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
        self.start_btn = tk.Button(controls_frame, text="Sort",
                                 command=self.start_visualization,
                                 state=tk.DISABLED)
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
        
        # Progress panel
        self.setup_progress_panel(control_panel)

    def setup_progress_panel(self, control_panel):
        progress_frame = tk.LabelFrame(control_panel, text="Progress",
                                     bg="#34495e", fg="white")
        progress_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        # Initialize progress tracking variables
        self.steps = 0
        self.start_time = 0
        
        # Step counter
        self.step_counter = tk.Label(progress_frame, 
                                   text="Steps: 0",
                                   bg="#34495e", fg="white")
        self.step_counter.pack(padx=5, pady=2)
        
        # Current operation
        self.current_operation = tk.Label(progress_frame,
                                        text="Current: -",
                                        bg="#34495e", fg="white",
                                        wraplength=250)
        self.current_operation.pack(padx=5, pady=2)
        
        # Time taken
        self.time_label = tk.Label(progress_frame,
                                 text="Time: 0.00s",
                                 bg="#34495e", fg="white")
        self.time_label.pack(padx=5, pady=2)
        
        # Step history
        self.step_history = tk.Text(progress_frame, 
                                  height=8,
                                  bg="#2c3e50", fg="white",
                                  wrap=tk.WORD)
        self.step_history.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to step history
        scrollbar = tk.Scrollbar(progress_frame, command=self.step_history.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_history.config(yscrollcommand=scrollbar.set)

    def reset_progress(self):
        """Reset all progress tracking elements"""
        self.steps = 0
        self.step_counter.config(text="Steps: 0")
        self.current_operation.config(text="Current: Starting...")
        self.time_label.config(text="Time: 0.00s")
        self.step_history.delete(1.0, tk.END)

    def draw_visualization(self, state):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        array = state['array']
        n = len(array)
        max_val = max(array)
        bar_width = (width - 100) // n
        scale_factor = (height - 100) / max_val
        
        if state['type'] == 'merge':
            self.draw_merge_visualization(state, array, bar_width, scale_factor)
        else:  # quick sort
            self.draw_quick_visualization(state, array, bar_width, scale_factor)
        
        self.update_step_info(state)

    def draw_merge_visualization(self, state, array, bar_width, scale_factor):
        for i, val in enumerate(array):
            x1 = 50 + i * bar_width
            y1 = self.canvas.winfo_height() - 50
            x2 = x1 + bar_width - 2
            y2 = y1 - val * scale_factor
            
            # Determine color
            color = "#3498db"  # Default blue
            
            if state['comparing'] and i in state['comparing']:
                color = "#f1c40f"  # Comparing (yellow)
            elif state['left'] <= i <= state['mid']:
                color = "#2ecc71"  # Left partition (green)
            elif state['mid'] < i <= state['right']:
                color = "#e74c3c"  # Right partition (red)
            
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                      fill=color, outline="#2c3e50")
            self.canvas.create_text((x1 + x2)//2, y1 + 15,
                                  text=str(val))

    def draw_quick_visualization(self, state, array, bar_width, scale_factor):
        for i, val in enumerate(array):
            x1 = 50 + i * bar_width
            y1 = self.canvas.winfo_height() - 50
            x2 = x1 + bar_width - 2
            y2 = y1 - val * scale_factor
            
            # Determine color
            color = "#3498db"  # Default blue
            
            if i == state['pivot_idx']:
                color = "#f1c40f"  # Pivot (yellow)
            elif i == state['current_idx']:
                color = "#e74c3c"  # Current (red)
            elif i == state['partition_idx']:
                color = "#2ecc71"  # Partition index (green)
            elif state['range'] and state['range'][0] <= i <= state['range'][1]:
                color = "#95a5a6"  # Current range (gray)
            
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                      fill=color, outline="#2c3e50")
            self.canvas.create_text((x1 + x2)//2, y1 + 15,
                                  text=str(val))

    def generate_array(self):
        size = self.size_scale.get()
        self.array = DivideConquerAlgorithms.generate_random_array(size)
        self.draw_initial_array()
        self.start_btn.config(state=tk.NORMAL)
        self.step_label.config(text="Array generated. Click Sort to start.")

    def draw_initial_array(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        n = len(self.array)
        max_val = max(self.array)
        bar_width = (width - 100) // n
        scale_factor = (height - 100) / max_val
        
        for i, val in enumerate(self.array):
            x1 = 50 + i * bar_width
            y1 = height - 50
            x2 = x1 + bar_width - 2
            y2 = y1 - val * scale_factor
            
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                      fill="#3498db", outline="#2c3e50")
            self.canvas.create_text((x1 + x2)//2, y1 + 15,
                                  text=str(val))

    def start_visualization(self):
        try:
            if not self.array:
                messagebox.showerror("Error", "Please generate an array first")
                return
            
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.reset_progress()
            
            self.start_time = time.time()
            self.visualization = DivideConquerAlgorithms.get_algorithm(
                self.algorithm,
                self.array.copy(),
                self.draw_visualization
            )
            
            if self.visualization is None:
                messagebox.showerror("Error", "Failed to initialize algorithm")
                self.reset_visualization()
                return
            
            self.continue_visualization(self.start_time)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.reset_visualization()

    def stop_visualization(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def reset_visualization(self):
        self.stop_visualization()
        self.array = []
        self.canvas.delete("all")
        self.reset_progress()
        self.step_label.config(text="Generate array to start")
        self.start_btn.config(state=tk.DISABLED)

    def back_to_main(self):
        if self.is_running:
            self.stop_visualization()
        self.window.destroy()
        self.main_window.deiconify() 

    def continue_visualization(self, start_time):
        if not self.is_running:
            return
            
        try:
            if self.visualization is None:
                self.stop_visualization()
                return
                
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
        except Exception as e:
            messagebox.showerror("Error", f"Visualization error: {str(e)}")
            self.stop_visualization()

    def update_step_info(self, state):
        """Update the progress panel information"""
        self.steps += 1
        current_time = time.time() - self.start_time
        
        self.step_counter.config(text=f"Steps: {self.steps}")
        self.time_label.config(text=f"Time: {current_time:.2f}s")
        self.current_operation.config(text=f"Current: {state['step']}")
        self.step_history.insert(tk.END, f"Step {self.steps}: {state['step']}\n")
        self.step_history.see(tk.END)
  