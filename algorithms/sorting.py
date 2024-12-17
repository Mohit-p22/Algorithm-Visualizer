class SortingAlgorithms:
    @staticmethod
    def get_algorithm(name, array, draw_func, speed):
        algorithm_map = {
            "Bubble Sort": SortingAlgorithms.bubble_sort,
            "Selection Sort": SortingAlgorithms.selection_sort,
            "Insertion Sort": SortingAlgorithms.insertion_sort,
            "Quick Sort": SortingAlgorithms.quick_sort,
            "Merge Sort": SortingAlgorithms.merge_sort,
            "Heap Sort": SortingAlgorithms.heap_sort
        }
        
        if name in algorithm_map:
            return algorithm_map[name](array, draw_func, speed)
        raise ValueError(f"Algorithm {name} not implemented")

    @staticmethod
    def bubble_sort(arr, draw_func, speed):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                # Create color array for visualization
                colors = ["#3498db"] * n  # Default blue
                colors[j] = "#e74c3c"     # Current red
                colors[j+1] = "#f1c40f"   # Next yellow
                
                draw_func(arr, colors)
                
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    colors[j] = "#2ecc71"   # Swapped green
                    colors[j+1] = "#2ecc71"
                    draw_func(arr, colors)
                    
                yield True  # For animation timing

    @staticmethod
    def selection_sort(arr, draw_func, speed):
        n = len(arr)
        for i in range(n):
            min_idx = i
            colors = ["#3498db"] * n
            colors[i] = "#e74c3c"  # Current position red
            
            for j in range(i+1, n):
                colors[j] = "#f1c40f"  # Comparing yellow
                draw_func(arr, colors)
                
                if arr[j] < arr[min_idx]:
                    colors[min_idx] = "#3498db"  # Reset previous min
                    min_idx = j
                    colors[min_idx] = "#2ecc71"  # New min green
                    
                colors[j] = "#3498db"  # Reset compared
                yield True
            
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                colors[i] = "#2ecc71"
                colors[min_idx] = "#2ecc71"
                draw_func(arr, colors)
            yield True

    @staticmethod
    def insertion_sort(arr, draw_func, speed):
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i-1
            colors = ["#3498db"] * n
            colors[i] = "#e74c3c"  # Current element red
            
            while j >= 0 and arr[j] > key:
                colors[j] = "#f1c40f"  # Comparing yellow
                draw_func(arr, colors)
                arr[j+1] = arr[j]
                colors[j] = "#2ecc71"  # Moved green
                j -= 1
                yield True
                
            arr[j+1] = key
            colors[j+1] = "#2ecc71"
            draw_func(arr, colors)
            yield True

    @staticmethod
    def quick_sort(arr, draw_func, speed):
        def partition(low, high):
            colors = ["#3498db"] * len(arr)
            pivot = arr[high]
            colors[high] = "#e74c3c"  # Pivot red
            i = low - 1
            
            for j in range(low, high):
                colors[j] = "#f1c40f"  # Current yellow
                draw_func(arr, colors)
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    colors[i] = "#2ecc71"  # Swapped green
                    colors[j] = "#2ecc71"
                    draw_func(arr, colors)
                yield True
                
            arr[i+1], arr[high] = arr[high], arr[i+1]
            colors[i+1] = "#2ecc71"
            colors[high] = "#2ecc71"
            draw_func(arr, colors)
            yield True
            return i + 1

        def quick_sort_helper(low, high):
            if low < high:
                pi = yield from partition(low, high)
                yield from quick_sort_helper(low, pi-1)
                yield from quick_sort_helper(pi+1, high)

        yield from quick_sort_helper(0, len(arr)-1)

    @staticmethod
    def merge_sort(arr, draw_func, speed):
        def merge(l, m, r):
            left = arr[l:m+1]
            right = arr[m+1:r+1]
            i = j = 0
            k = l
            colors = ["#3498db"] * len(arr)
            
            while i < len(left) and j < len(right):
                colors[k] = "#f1c40f"  # Comparing yellow
                draw_func(arr, colors)
                
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                    
                colors[k] = "#2ecc71"  # Placed green
                k += 1
                yield True
                
            while i < len(left):
                colors[k] = "#2ecc71"
                arr[k] = left[i]
                i += 1
                k += 1
                draw_func(arr, colors)
                yield True
                
            while j < len(right):
                colors[k] = "#2ecc71"
                arr[k] = right[j]
                j += 1
                k += 1
                draw_func(arr, colors)
                yield True

        def merge_sort_helper(l, r):
            if l < r:
                m = (l + r) // 2
                yield from merge_sort_helper(l, m)
                yield from merge_sort_helper(m+1, r)
                yield from merge(l, m, r)

        yield from merge_sort_helper(0, len(arr)-1)

    @staticmethod
    def heap_sort(arr, draw_func, speed):
        def heapify(n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            colors = ["#3498db"] * len(arr)
            colors[i] = "#e74c3c"  # Current red
            
            if left < n:
                colors[left] = "#f1c40f"  # Comparing yellow
                draw_func(arr, colors)
                if arr[left] > arr[largest]:
                    largest = left
                yield True
                
            if right < n:
                colors[right] = "#f1c40f"
                draw_func(arr, colors)
                if arr[right] > arr[largest]:
                    largest = right
                yield True
                
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                colors[i] = "#2ecc71"  # Swapped green
                colors[largest] = "#2ecc71"
                draw_func(arr, colors)
                yield True
                yield from heapify(n, largest)

        n = len(arr)
        # Build max heap
        for i in range(n//2-1, -1, -1):
            yield from heapify(n, i)
            
        # Extract elements
        for i in range(n-1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            colors = ["#3498db"] * len(arr)
            colors[0] = "#2ecc71"
            colors[i] = "#2ecc71"
            draw_func(arr, colors)
            yield True
            yield from heapify(i, 0)