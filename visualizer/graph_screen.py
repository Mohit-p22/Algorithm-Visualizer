import tkinter as tk
from tkinter import ttk, scrolledtext
import time
from algorithms.graph import GraphAlgorithms

class GraphScreen:
    def __init__(self, algorithm, main_window):
        self.window = tk.Toplevel()
        self.window.title(f"Graph Algorithm - {algorithm}")
        self.window.geometry("1400x700")
        self.window.configure(bg="#2c3e50")
        self.main_window = main_window
        self.algorithm = algorithm
        
        # Initialize variables
        self.visualization_speed = 100
        self.is_running = False
        self.nodes = {}
        self.edges = []
        self.current_state = {}
        self.visualization = None
        self.edge_weights = {}
        self.traversal_history = []
        
        self.setup_ui()
        self.initialize_visualization()
        
    def setup_ui(self):
        # Main content frame (left side)
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control panel (right side)
        control_panel = tk.Frame(self.window, bg="#34495e", width=300)  # Increased width
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_panel.pack_propagate(False)
        
        # Algorithm Selection
        algo_frame = tk.LabelFrame(control_panel, text="Algorithm Selection",
                                 bg="#34495e", fg="white")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        algorithms = [
            "Breadth First Search",
            "Depth First Search",
            "Dijkstra's Algorithm"
        ]
        
        self.algo_var = tk.StringVar(value=self.algorithm)
        self.algo_menu = ttk.Combobox(algo_frame, 
                                    textvariable=self.algo_var,
                                    values=algorithms)
        self.algo_menu.pack(fill=tk.X, padx=5, pady=5)
        self.algo_menu.bind('<<ComboboxSelected>>', self.on_algorithm_change)
        
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
        
        self.start_btn = tk.Button(buttons_frame, text="Start",
                                 command=self.start_visualization)
        self.start_btn.pack(fill=tk.X, pady=2)
        
        self.stop_btn = tk.Button(buttons_frame, text="Stop",
                                command=self.stop_visualization,
                                state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=2)
        
        tk.Button(buttons_frame, text="Reset",
                 command=self.reset_visualization).pack(fill=tk.X, pady=2)
        
        tk.Button(buttons_frame, text="Generate New Graph",
                 command=self.generate_new_graph).pack(fill=tk.X, pady=2)
        
        tk.Button(buttons_frame, text="Back to Menu",
                 command=self.back_to_main).pack(fill=tk.X, pady=2)
        
        # Statistics
        stats_frame = tk.LabelFrame(control_panel, text="Statistics",
                                  bg="#34495e", fg="white")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.steps_label = tk.Label(stats_frame, text="Steps: 0",
                                  bg="#34495e", fg="white")
        self.steps_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.visited_label = tk.Label(stats_frame, text="Visited: 0",
                                    bg="#34495e", fg="white")
        self.visited_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Current Node Info
        self.current_node_label = tk.Label(stats_frame, 
                                         text="Current Node: None",
                                         bg="#34495e", fg="white")
        self.current_node_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Traversal History
        history_frame = tk.LabelFrame(control_panel, text="Traversal History",
                                    bg="#34495e", fg="white")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrolled text widget for traversal history
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            width=30,
            height=10,
            bg="#2c3e50",
            fg="white",
            font=("Courier", 10)
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(main_frame, bg="white")
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
    def initialize_visualization(self):
        self.canvas.delete("all")
        self.generate_new_graph()
        
    def generate_new_graph(self):
        width = self.canvas.winfo_width() or 800
        height = self.canvas.winfo_height() or 600
        padding = 50
        self.nodes, self.edges = GraphAlgorithms.generate_vertical_graph(width, height, padding)
        
        # Generate edge weights for Dijkstra's
        self.edge_weights = {}
        for edge in self.edges:
            weight = GraphAlgorithms.generate_edge_weight()
            self.edge_weights[edge] = weight
            self.edge_weights[(edge[1], edge[0])] = weight
            
        self.draw_graph()
        
    def draw_graph(self, current_node=None, visited=None, path=None, queue=None, stack=None, distances=None):
        self.canvas.delete("all")
        
        # Draw edges
        for edge in self.edges:
            start_node, end_node = edge
            start_x, start_y = self.nodes[start_node]
            end_x, end_y = self.nodes[end_node]
            
            # Edge color
            color = "#95a5a6"  # Default gray
            width = 2
            if path and any(e in path for e in [(start_node, end_node), (end_node, start_node)]):
                color = "#3498db"  # Blue for path
                width = 3
                
            self.canvas.create_line(start_x, start_y, end_x, end_y,
                                  fill=color, width=width)
            
            # Draw weight if it's Dijkstra's
            if "Dijkstra" in self.algorithm:
                mid_x = (start_x + end_x) / 2
                mid_y = (start_y + end_y) / 2
                weight = self.edge_weights.get(edge, "")
                self.canvas.create_text(mid_x, mid_y - 10,
                                      text=str(weight),
                                      font=("Helvetica", 10),
                                      fill="#2c3e50")
        
        # Draw nodes
        for node, (x, y) in self.nodes.items():
            # Node color
            color = "#2ecc71"  # Default green
            if visited and node in visited:
                color = "#3498db"  # Blue for visited
            if queue and node in queue:
                color = "#f1c40f"  # Yellow for queue
            if stack and node in stack:
                color = "#f1c40f"  # Yellow for stack
            if node == current_node:
                color = "#e74c3c"  # Red for current
                
            # Draw node circle
            node_radius = 20
            self.canvas.create_oval(x - node_radius,
                                  y - node_radius,
                                  x + node_radius,
                                  y + node_radius,
                                  fill=color, outline="black", width=2)
            
            # Draw node label
            label = str(node)
            if distances:
                dist = distances.get(node, float('infinity'))
                label += f"\n{dist if dist != float('infinity') else '∞'}"
                
            self.canvas.create_text(x, y,
                                  text=label,
                                  font=("Helvetica", 12, "bold"))
    
    def on_algorithm_change(self, event=None):
        self.algorithm = self.algo_var.get()
        self.reset_visualization()
        
    def start_visualization(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.steps = 0
        
        self.visualization = GraphAlgorithms.get_algorithm(
            self.algorithm,
            self.nodes,
            self.edges,
            self.update_visualization
        )
        self.continue_visualization()
        
    def continue_visualization(self):
        if not self.is_running:
            return
            
        try:
            next(self.visualization)
            self.steps += 1
            self.steps_label.config(text=f"Steps: {self.steps}")
            
            delay = int(1000 / self.speed_scale.get())
            self.window.after(delay, self.continue_visualization)
        except StopIteration:
            self.stop_visualization()
        
    def stop_visualization(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
    def reset_visualization(self):
        self.stop_visualization()
        self.initialize_visualization()
        self.steps = 0
        self.steps_label.config(text="Steps: 0")
        self.visited_label.config(text="Visited: 0")
        self.current_node_label.config(text="Current Node: None")
        self.traversal_history = []
        self.history_text.delete(1.0, tk.END)
        
    def update_traversal_history(self, current_node, next_nodes=None, distances=None):
        if next_nodes is None:
            step = f"Visiting Node {current_node}\n"
        else:
            if isinstance(next_nodes, list):
                connections = []
                for node in next_nodes:
                    if distances and node in distances:
                        connections.append(f"{node}(dist: {distances[node]})")
                    else:
                        connections.append(str(node))
                step = f"Node {current_node} → {', '.join(connections)}\n"
            else:
                if distances and next_nodes in distances:
                    step = f"Node {current_node} → {next_nodes} (dist: {distances[next_nodes]})\n"
                else:
                    step = f"Node {current_node} → {next_nodes}\n"
            
        self.traversal_history.append(step)
        self.history_text.insert(tk.END, step)
        self.history_text.see(tk.END)
        
    def update_visualization(self, state):
        if not state:
            return
            
        self.current_state = state
        self.draw_graph(
            current_node=state.get("current"),
            visited=state.get("visited"),
            path=state.get("path"),
            queue=state.get("queue"),
            stack=state.get("stack"),
            distances=state.get("distances")
        )
        
        current = state.get("current")
        if current is not None:
            self.current_node_label.config(text=f"Current Node: {current}")
            
            if "distances" in state:
                neighbors_with_distances = {}
                for neighbor, dist in state.get("distances", {}).items():
                    if dist != float('infinity'):
                        neighbors_with_distances[neighbor] = dist
                if neighbors_with_distances:
                    self.update_traversal_history(current, list(neighbors_with_distances.keys()), neighbors_with_distances)
            else:
                neighbors = state.get("queue", []) or state.get("stack", [])
                if neighbors:
                    self.update_traversal_history(current, neighbors)
                else:
                    self.update_traversal_history(current)
        
        if "visited" in state:
            self.visited_label.config(text=f"Visited: {len(state['visited'])}")
            
        if state.get("complete", False):
            self.show_final_path(state.get("visited", []), 
                               state.get("path", []),
                               state.get("summary"))
    
    def show_final_path(self, visited, path, summary=None):
        if not summary:
            return
            
        self.history_text.insert(tk.END, "\n" + "="*40 + "\n")
        self.history_text.insert(tk.END, f"{summary['algorithm']} Traversal Complete\n")
        self.history_text.insert(tk.END, f"Visited Nodes: {summary['visited_count']}\n")
        self.history_text.insert(tk.END, "-"*40 + "\n")
        
        if summary['algorithm'] == "Dijkstra":
            self.history_text.insert(tk.END, "Shortest Paths from Start:\n")
            for path in summary['paths']:
                dist = summary['distances'][path[-1]]
                path_str = " → ".join(map(str, path))
                self.history_text.insert(tk.END, f"To Node {path[-1]}: {path_str} (Distance: {dist})\n")
        else:
            self.history_text.insert(tk.END, "Complete Traversal Path:\n")
            path_str = " → ".join(map(str, summary['path']))
            self.history_text.insert(tk.END, f"{path_str}\n")
            
        self.history_text.insert(tk.END, "="*40 + "\n")
        self.history_text.see(tk.END)
        
    def back_to_main(self):
        self.window.destroy()
        self.main_window.deiconify()
        