import tkinter as tk
from tkinter import ttk
from visualizer.backtracking_screen import BacktrackingScreen
from visualizer.divide_conquer_screen import DivideConquerScreen
from visualizer.dynamic_screen import DynamicScreen
from visualizer.greedy_screen import GreedyScreen
from visualizer.sorting_screen import SortingScreen
from visualizer.searching_screen import SearchingScreen
from visualizer.graph_screen import GraphScreen

class AlgorithmVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Algorithm Visualizer")
        self.root.geometry("800x500")
        self.root.configure(bg="#2c3e50")
        
        self.setup_main_screen()
        
    def setup_main_screen(self):
        # Title
        title = tk.Label(self.root, text="Algorithm Visualizer",
                        font=("Helvetica", 24, "bold"),
                        bg="#2c3e50", fg="white")
        title.pack(pady=20)
        
        # Frame for algorithm selection
        selection_frame = tk.Frame(self.root, bg="#2c3e50")
        selection_frame.pack(pady=20)
        
        # Algorithm type selection
        self.algo_types = ["Sorting", "Searching", "Graph", "Backtracking",
                           "Dynamic Programming", "Greedy", "Divide and Conquer"]
        self.algo_type_var = tk.StringVar()
        
        algo_type_label = tk.Label(selection_frame, text="Select Algorithm Type:",
                                 font=("Helvetica", 12),
                                 bg="#2c3e50", fg="white")
        algo_type_label.grid(row=0, column=0, padx=10, pady=5)
        
        algo_type_menu = ttk.Combobox(selection_frame,
                                    textvariable=self.algo_type_var,
                                    values=self.algo_types)
        algo_type_menu.grid(row=0, column=1, padx=10, pady=5)
        algo_type_menu.bind('<<ComboboxSelected>>', self.update_algorithms)
        
        # Specific algorithm selection
        self.algo_var = tk.StringVar()
        
        self.algo_label = tk.Label(selection_frame, text="Select Algorithm:",
                                 font=("Helvetica", 12),
                                 bg="#2c3e50", fg="white")
        self.algo_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.algo_menu = ttk.Combobox(selection_frame,
                                    textvariable=self.algo_var)
        self.algo_menu.grid(row=1, column=1, padx=10, pady=5)
        
        # Visualize button
        visualize_btn = tk.Button(self.root, text="Visualize",
                                command=self.start_visualization,
                                font=("Helvetica", 12),
                                bg="#3498db", fg="white",
                                padx=20, pady=10)
        visualize_btn.pack(pady=20)
        
    def update_algorithms(self, event=None):
        algorithms = {
            "Sorting": ["Bubble Sort", "Insertion Sort", "Selection Sort",
                       "Quick Sort", "Merge Sort", "Heap Sort"],
            "Searching": ["Linear Search", "Binary Search",
                         "Jump Search", "Interpolation Search"],
            "Graph": ["Breadth First Search", "Depth First Search",
                      "Dijkstra's Algorithm", "A* Search"],
            "Backtracking": ["N-Queens Problem", "Sudoku Solver"],
            "Dynamic Programming": ["Fibonacci Sequence", "Longest Common Subsequence"],
            "Greedy": ["Fractional Knapsack", "Activity Selection Problem"],
            "Divide and Conquer": ["Merge Sort", "Quick Sort"]
        }
        
        selected_type = self.algo_type_var.get()
        self.algo_menu['values'] = algorithms.get(selected_type, [])
        self.algo_menu.set("")
        
    def start_visualization(self):
        algo_type = self.algo_type_var.get()
        algorithm = self.algo_var.get()
        
        if not algo_type or not algorithm:
            return
            
        self.root.withdraw()  # Hide main window
        
        if algo_type == "Sorting":
            visualization_window = SortingScreen(algorithm, self.root)
        elif algo_type == "Searching":
            visualization_window = SearchingScreen(algorithm, self.root)
        elif algo_type == "Graph":  
            visualization_window = GraphScreen(algorithm, self.root)
        elif algo_type == "Backtracking":
            visualization_window = BacktrackingScreen(algorithm, self.root)
        elif algo_type == "Dynamic Programming":
            visualization_window = DynamicScreen(algorithm, self.root)
        elif algo_type == "Greedy":
            visualization_window = GreedyScreen(algorithm, self.root)
        elif algo_type == "Divide and Conquer":
            visualization_window = DivideConquerScreen(algorithm, self.root)
                        
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AlgorithmVisualizer()
    app.run()