import tkinter as tk
from tkinter import ttk, messagebox
import time
from algorithms.greedy import GreedyAlgorithms

class GreedyScreen:
    def __init__(self, algorithm, main_window):
        self.window = tk.Toplevel()
        self.window.title(f"Greedy Algorithm - {algorithm}")
        self.window.geometry("1000x600")
        self.window.configure(bg="#2c3e50")
        self.main_window = main_window
        self.algorithm = algorithm
        self.is_running = False
        self.items = []
        self.setup_ui()

    def setup_ui(self):
        # Main content frame
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(main_frame, bg="white", height=400)
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Step description
        self.step_label = tk.Label(main_frame, text="Generate items to start",
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
        
        if "Knapsack" in self.algorithm:
            self.setup_knapsack_inputs(input_frame)
        else:
            self.setup_activity_inputs(input_frame)
        
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

    def setup_knapsack_inputs(self, input_frame):
        # Capacity input
        tk.Label(input_frame, text="Knapsack Capacity:",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.capacity_var = tk.StringVar(value="50")
        self.capacity_entry = tk.Entry(input_frame, textvariable=self.capacity_var)
        self.capacity_entry.pack(padx=5, pady=2, fill=tk.X)
        
        # Number of items slider
        tk.Label(input_frame, text="Number of Items:",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.items_scale = tk.Scale(input_frame, from_=3, to=10,
                                  orient=tk.HORIZONTAL, bg="#34495e", fg="white",
                                  highlightthickness=0)
        self.items_scale.set(5)
        self.items_scale.pack(padx=5, pady=2, fill=tk.X)
        
        # Generate items button
        tk.Button(input_frame, text="Generate Random Items",
                 command=self.generate_items).pack(padx=5, pady=5, fill=tk.X)

    def setup_activity_inputs(self, input_frame):
        # Number of activities slider
        tk.Label(input_frame, text="Number of Activities:",
                bg="#34495e", fg="white").pack(padx=5, pady=2)
        self.items_scale = tk.Scale(input_frame, from_=3, to=10,
                                  orient=tk.HORIZONTAL, bg="#34495e", fg="white",
                                  highlightthickness=0)
        self.items_scale.set(6)
        self.items_scale.pack(padx=5, pady=2, fill=tk.X)
        
        # Generate activities button
        tk.Button(input_frame, text="Generate Random Activities",
                 command=self.generate_items).pack(padx=5, pady=5, fill=tk.X)

    def draw_visualization(self, state):
        if state.get('type') == 'activity':
            self.draw_activity_visualization(state)
        else:
            self.draw_knapsack_visualization(state)
        self.update_step_info(state)

    def draw_knapsack_visualization(self, state):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Draw knapsack
        knapsack_height = height * 0.6
        knapsack_width = width * 0.3
        knapsack_x = width * 0.1
        knapsack_y = height * 0.2
        
        # Draw knapsack outline
        self.canvas.create_rectangle(knapsack_x, knapsack_y,
                                   knapsack_x + knapsack_width,
                                   knapsack_y + knapsack_height,
                                   outline="#2c3e50", width=2)
        
        # Draw capacity indicator
        fill_height = (state['current_weight'] / state['capacity']) * knapsack_height
        self.canvas.create_rectangle(knapsack_x, knapsack_y + knapsack_height - fill_height,
                                   knapsack_x + knapsack_width,
                                   knapsack_y + knapsack_height,
                                   fill="#3498db", outline="")
        
        # Draw capacity text
        self.canvas.create_text(knapsack_x + knapsack_width//2,
                              knapsack_y - 20,
                              text=f"Capacity: {state['capacity']}\n"
                                   f"Current: {state['current_weight']:.2f}",
                              font=("Arial", 10))
        
        # Draw items
        item_width = min((width - knapsack_width - 100) // (len(state['items'])), 80)
        start_x = knapsack_x + knapsack_width + 50
        
        for i, item in enumerate(state['items']):
            x = start_x + i * (item_width + 20)
            y = height // 2
            
            # Determine item color
            color = "#3498db"  # Default blue
            if state['current_item'] == i:
                color = "#f1c40f"  # Current item (yellow)
            elif any(s['id'] == item['id'] for s in state['selected_items']):
                color = "#2ecc71"  # Selected item (green)
            
            # Draw item box
            self.canvas.create_rectangle(x, y - item_width//2,
                                      x + item_width, y + item_width//2,
                                      fill=color, outline="#2c3e50")
            
            # Draw item details
            self.canvas.create_text(x + item_width//2, y - 10,
                                  text=f"V: {item['value']}")
            self.canvas.create_text(x + item_width//2, y + 10,
                                  text=f"W: {item['weight']}")
            
            # Draw ratio
            self.canvas.create_text(x + item_width//2, y + 30,
                                  text=f"R: {item['ratio']:.2f}")
            
            # Draw fraction if item is selected
            selected = next((s for s in state['selected_items'] if s['id'] == item['id']), None)
            if selected and selected['fraction'] < 1:
                self.canvas.create_text(x + item_width//2, y + 50,
                                      text=f"Used: {selected['fraction']:.2f}",
                                      fill="#e74c3c")
        
        # Draw current value
        self.canvas.create_text(width//2, height - 30,
                              text=f"Total Value: {state['current_value']:.2f}",
                              font=("Arial", 12, "bold"))

    def draw_activity_visualization(self, state):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Find time range
        max_time = max(act['finish'] for act in state['activities'])
        time_unit = width * 0.8 / (max_time + 1)
        start_x = width * 0.1
        
        # Draw timeline
        timeline_y = height * 0.8
        self.canvas.create_line(start_x, timeline_y,
                              start_x + (max_time + 1) * time_unit, timeline_y,
                              width=2, fill="#2c3e50")
        
        # Draw time markers
        for t in range(max_time + 1):
            x = start_x + t * time_unit
            self.canvas.create_line(x, timeline_y - 5,
                                  x, timeline_y + 5,
                                  fill="#2c3e50")
            self.canvas.create_text(x, timeline_y + 20,
                                  text=str(t))
        
        # Draw activities
        activity_height = 30
        current_y = timeline_y - 50
        
        for i, activity in enumerate(state['activities']):
            x1 = start_x + activity['start'] * time_unit
            x2 = start_x + activity['finish'] * time_unit
            
            # Determine color
            color = "#3498db"  # Default blue
            if state['current'] == i:
                color = "#f1c40f"  # Current (yellow)
            elif activity in state['selected']:
                color = "#2ecc71"  # Selected (green)
            
            # Draw activity bar
            self.canvas.create_rectangle(x1, current_y - activity_height//2,
                                      x2, current_y + activity_height//2,
                                      fill=color, outline="#2c3e50")
            
            # Draw activity label
            self.canvas.create_text((x1 + x2)//2, current_y,
                                  text=f"A{activity['id']}\n({activity['start']}-{activity['finish']})")
            
            current_y -= activity_height * 1.5

    def generate_items(self):
        try:
            if "Activity" in self.algorithm:
                num_activities = self.items_scale.get()
                self.items = GreedyAlgorithms.generate_random_activities(num_activities)
                self.draw_initial_activities()
            else:
                num_items = self.items_scale.get()
                self.items = GreedyAlgorithms.generate_random_items(num_items)
                self.draw_initial_knapsack_items()
            
            self.start_btn.config(state=tk.NORMAL)
            self.step_label.config(text="Items generated. Click Solve to start.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def draw_initial_knapsack_items(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        item_width = min(width // (len(self.items) + 2), 100)
        start_x = (width - (len(self.items) * (item_width + 20))) // 2
        
        for i, item in enumerate(self.items):
            x = start_x + i * (item_width + 20)
            y = height // 2
            
            # Draw item box
            self.canvas.create_rectangle(x, y - item_width//2,
                                      x + item_width, y + item_width//2,
                                      fill="#3498db", outline="#2c3e50")
            
            # Draw item details
            self.canvas.create_text(x + item_width//2, y - 10,
                                  text=f"V: {item['value']}")
            self.canvas.create_text(x + item_width//2, y + 10,
                                  text=f"W: {item['weight']}")
            
            # Draw ratio
            ratio = item['value'] / item['weight']
            self.canvas.create_text(x + item_width//2, y + 30,
                                  text=f"R: {ratio:.2f}")

    def draw_initial_activities(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Find time range
        max_time = max(act['finish'] for act in self.items)
        time_unit = width * 0.8 / (max_time + 1)
        start_x = width * 0.1
        
        # Draw timeline
        timeline_y = height * 0.8
        self.canvas.create_line(start_x, timeline_y,
                              start_x + (max_time + 1) * time_unit, timeline_y,
                              width=2, fill="#2c3e50")
        
        # Draw time markers
        for t in range(max_time + 1):
            x = start_x + t * time_unit
            self.canvas.create_line(x, timeline_y - 5,
                                  x, timeline_y + 5,
                                  fill="#2c3e50")
            self.canvas.create_text(x, timeline_y + 20,
                                  text=str(t))
        
        # Draw activities
        activity_height = 30
        current_y = timeline_y - 50
        
        for i, activity in enumerate(self.items):
            x1 = start_x + activity['start'] * time_unit
            x2 = start_x + activity['finish'] * time_unit
            
            # Draw activity bar
            self.canvas.create_rectangle(x1, current_y - activity_height//2,
                                      x2, current_y + activity_height//2,
                                      fill="#3498db", outline="#2c3e50")
            
            # Draw activity label
            self.canvas.create_text((x1 + x2)//2, current_y,
                                  text=f"A{activity['id']}\n({activity['start']}-{activity['finish']})")
            
            current_y -= activity_height * 1.5

    def start_visualization(self):
        try:
            if "Knapsack" in self.algorithm:
                capacity = float(self.capacity_var.get())
                if capacity <= 0:
                    raise ValueError("Capacity must be positive")
                inputs = (capacity, self.items.copy())
            else:
                inputs = self.items.copy()
            
            if not self.items:
                messagebox.showerror("Error", "Please generate items first")
                return
            
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.reset_progress()
            
            self.start_time = time.time()
            algorithm_name = "Fractional Knapsack" if "Knapsack" in self.algorithm else "Activity Selection"
            self.visualization = GreedyAlgorithms.get_algorithm(
                algorithm_name,
                inputs,
                self.draw_visualization
            )
            
            if self.visualization is None:
                messagebox.showerror("Error", "Failed to initialize algorithm")
                self.reset_visualization()
                return
                
            self.continue_visualization(self.start_time)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.reset_visualization()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.reset_visualization()

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

    def stop_visualization(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def reset_visualization(self):
        self.stop_visualization()
        self.items = []
        self.canvas.delete("all")
        self.reset_progress()
        self.step_label.config(text="Generate items to start")
        self.start_btn.config(state=tk.DISABLED)

    def reset_progress(self):
        self.steps = 0
        self.step_counter.config(text="Steps: 0")
        self.current_operation.config(text="Current: Starting...")
        self.time_label.config(text="Time: 0.00s")
        self.step_history.delete(1.0, tk.END)

    def update_step_info(self, state):
        self.steps = getattr(self, 'steps', 0) + 1
        current_time = time.time() - self.start_time
        
        self.step_counter.config(text=f"Steps: {self.steps}")
        self.time_label.config(text=f"Time: {current_time:.2f}s")
        self.current_operation.config(text=f"Current: {state['step']}")
        self.step_history.insert(tk.END, f"Step {self.steps}: {state['step']}\n")
        self.step_history.see(tk.END)

    def back_to_main(self):
        if self.is_running:
            self.stop_visualization()
        self.window.destroy()
        self.main_window.deiconify() 

    def setup_progress_panel(self, control_panel):
        """Setup the progress tracking panel"""
        progress_frame = tk.LabelFrame(control_panel, text="Progress",
                                     bg="#34495e", fg="white")
        progress_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        
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