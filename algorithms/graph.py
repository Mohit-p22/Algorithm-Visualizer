import random
import tkinter.messagebox as messagebox
from queue import PriorityQueue

class GraphAlgorithms:
    @staticmethod
    def get_algorithm(name, nodes, edges, draw_func):
        algorithm_map = {
            "BFS": GraphAlgorithms.bfs,
            "DFS": GraphAlgorithms.dfs,
            "Breadth First Search": GraphAlgorithms.bfs,
            "Depth First Search": GraphAlgorithms.dfs,
            "Dijkstra's Algorithm": GraphAlgorithms.dijkstra
        }
        
        if name in algorithm_map:
            return algorithm_map[name](nodes, edges, draw_func)
        raise ValueError(f"Algorithm {name} not implemented")

    @staticmethod
    def generate_edge_weight():
        return random.randint(1, 10)

    @staticmethod
    def generate_vertical_graph(width, height, padding):
        nodes = {}
        edges = []
        levels = 4
        nodes_per_level = [1, 2, 4, 2]
        
        # Generate nodes
        node_id = 0
        level_nodes = []
        y_spacing = (height - 2 * padding) / (levels - 1)
        
        for level in range(levels):
            level_list = []
            n_nodes = nodes_per_level[level]
            x_spacing = (width - 2 * padding) / (n_nodes + 1)
            
            for i in range(n_nodes):
                x_pos = padding + (i + 1) * x_spacing
                y_pos = padding + (level * y_spacing)
                nodes[node_id] = (x_pos, y_pos)
                level_list.append(node_id)
                node_id += 1
            level_nodes.append(level_list)
        
        # Generate edges
        for level in range(levels - 1):
            current_level = level_nodes[level]
            next_level = level_nodes[level + 1]
            
            for current_node in current_level:
                # Ensure at least one connection
                next_node = random.choice(next_level)
                edges.append((current_node, next_node))
                
                # Add additional random connections
                for next_node in next_level:
                    if random.random() < 0.3 and (current_node, next_node) not in edges:
                        edges.append((current_node, next_node))
        
        return nodes, edges

    @staticmethod
    def reconstruct_path(visited, path_edges, start_node=None):
        if not path_edges:
            return []
            
        if start_node is None:
            start_node = min(visited)
            
        # Create adjacency list from path edges
        path_graph = {node: [] for node in visited}
        for start, end in path_edges:
            path_graph[start].append(end)
            
        # Reconstruct the path using DFS
        final_path = []
        stack = [(start_node, [start_node])]
        visited_in_path = set()
        
        while stack:
            current, current_path = stack.pop()
            
            if current not in visited_in_path:
                visited_in_path.add(current)
                final_path = current_path
                
                # Add neighbors in reverse order for DFS
                for neighbor in sorted(path_graph[current], reverse=True):
                    if neighbor not in visited_in_path:
                        stack.append((neighbor, current_path + [neighbor]))
        
        return final_path

    @staticmethod
    def bfs(nodes, edges, draw_func):
        graph = {node: set() for node in nodes}
        for start, end in edges:
            graph[start].add(end)
            graph[end].add(start)
        
        start_node = min(nodes.keys())
        visited = set()
        queue = [start_node]
        path = []
        
        while queue:
            current = queue.pop(0)
            
            if current not in visited:
                visited.add(current)
                
                neighbors = []
                for neighbor in sorted(graph[current]):
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
                        neighbors.append(neighbor)
                        path.append((current, neighbor))
                
                draw_func({
                    "current": current,
                    "visited": visited,
                    "path": path,
                    "queue": neighbors
                })
                yield
        
        # Reconstruct final path
        final_path = GraphAlgorithms.reconstruct_path(visited, path, start_node)
        draw_func({
            "visited": visited,
            "path": path,
            "complete": True,
            "final_path": final_path,
            "summary": {
                "algorithm": "BFS",
                "visited_count": len(visited),
                "path": final_path
            }
        })
        yield

    @staticmethod
    def dfs(nodes, edges, draw_func):
        graph = {node: set() for node in nodes}
        for start, end in edges:
            graph[start].add(end)
            graph[end].add(start)
        
        start_node = min(nodes.keys())
        visited = set()
        stack = [start_node]
        path = []
        
        while stack:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                
                neighbors = []
                for neighbor in sorted(graph[current], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        neighbors.append(neighbor)
                        path.append((current, neighbor))
                
                draw_func({
                    "current": current,
                    "visited": visited,
                    "path": path,
                    "stack": neighbors
                })
                yield
        
        # Reconstruct final path
        final_path = GraphAlgorithms.reconstruct_path(visited, path, start_node)
        draw_func({
            "visited": visited,
            "path": path,
            "complete": True,
            "final_path": final_path,
            "summary": {
                "algorithm": "DFS",
                "visited_count": len(visited),
                "path": final_path
            }
        })
        yield

    @staticmethod
    def dijkstra(nodes, edges, draw_func):
        graph = {node: {} for node in nodes}
        for start, end in edges:
            weight = GraphAlgorithms.generate_edge_weight()
            graph[start][end] = weight
            graph[end][start] = weight
        
        start_node = min(nodes.keys())
        distances = {node: float('infinity') for node in nodes}
        distances[start_node] = 0
        visited = set()
        path = []
        parent = {start_node: None}
        pq = PriorityQueue()
        pq.put((0, start_node))
        
        while not pq.empty():
            current_distance, current = pq.get()
            
            if current in visited:
                continue
                
            visited.add(current)
            
            neighbors = []
            for neighbor, weight in graph[current].items():
                if neighbor not in visited:
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        parent[neighbor] = current
                        pq.put((distance, neighbor))
                        neighbors.append(neighbor)
                        path.append((current, neighbor))
            
            draw_func({
                "current": current,
                "visited": visited,
                "path": path,
                "distances": distances,
                "queue": neighbors
            })
            yield
        
        # Reconstruct shortest paths
        final_paths = []
        for node in visited:
            if node != start_node:
                current = node
                path_to_node = []
                while current is not None:
                    path_to_node.append(current)
                    current = parent.get(current)
                final_paths.append(list(reversed(path_to_node)))
        
        draw_func({
            "visited": visited,
            "path": path,
            "complete": True,
            "final_paths": final_paths,
            "summary": {
                "algorithm": "Dijkstra",
                "visited_count": len(visited),
                "paths": final_paths,
                "distances": distances
            }
        })
        yield