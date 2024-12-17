class DivideConquerAlgorithms:
    @staticmethod
    def get_algorithm(name, inputs, draw_func):
        algorithm_map = {
            "Merge Sort": DivideConquerAlgorithms.merge_sort,
            "Quick Sort": DivideConquerAlgorithms.quick_sort
        }
        return algorithm_map.get(name, lambda x, y: None)(inputs, draw_func)

    @staticmethod
    def merge_sort(inputs, draw_func):
        array = inputs.copy()
        n = len(array)
        
        def merge(arr, left, mid, right):
            left_part = arr[left:mid + 1]
            right_part = arr[mid + 1:right + 1]
            
            i = j = 0
            k = left
            
            while i < len(left_part) and j < len(right_part):
                # Draw comparison state
                draw_func({
                    'type': 'merge',
                    'array': arr.copy(),
                    'left': left,
                    'mid': mid,
                    'right': right,
                    'comparing': (left + i, mid + 1 + j),
                    'current_left': left_part,
                    'current_right': right_part,
                    'step': f"Comparing {left_part[i]} and {right_part[j]}",
                    'complete': False
                })
                yield
                
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
                k += 1
                
                # Draw merge state
                draw_func({
                    'type': 'merge',
                    'array': arr.copy(),
                    'left': left,
                    'mid': mid,
                    'right': right,
                    'comparing': None,
                    'current_left': left_part[i:],
                    'current_right': right_part[j:],
                    'step': f"Merged element at position {k-1}",
                    'complete': False
                })
                yield
            
            while i < len(left_part):
                arr[k] = left_part[i]
                i += 1
                k += 1
                draw_func({
                    'type': 'merge',
                    'array': arr.copy(),
                    'left': left,
                    'mid': mid,
                    'right': right,
                    'comparing': None,
                    'current_left': left_part[i:],
                    'current_right': right_part[j:],
                    'step': f"Adding remaining left elements",
                    'complete': False
                })
                yield
            
            while j < len(right_part):
                arr[k] = right_part[j]
                j += 1
                k += 1
                draw_func({
                    'type': 'merge',
                    'array': arr.copy(),
                    'left': left,
                    'mid': mid,
                    'right': right,
                    'comparing': None,
                    'current_left': left_part[i:],
                    'current_right': right_part[j:],
                    'step': f"Adding remaining right elements",
                    'complete': False
                })
                yield

        def merge_sort_recursive(arr, left, right):
            if left < right:
                mid = (left + right) // 2
                
                # Draw division state
                draw_func({
                    'type': 'merge',
                    'array': arr.copy(),
                    'left': left,
                    'mid': mid,
                    'right': right,
                    'comparing': None,
                    'current_left': arr[left:mid + 1],
                    'current_right': arr[mid + 1:right + 1],
                    'step': f"Dividing array at position {mid}",
                    'complete': False
                })
                yield
                
                # Recursively sort first and second halves
                yield from merge_sort_recursive(arr, left, mid)
                yield from merge_sort_recursive(arr, mid + 1, right)
                
                # Merge the sorted halves
                yield from merge(arr, left, mid, right)
        
        # Start the recursive process
        yield from merge_sort_recursive(array, 0, n - 1)
        
        # Show completion
        draw_func({
            'type': 'merge',
            'array': array,
            'left': 0,
            'mid': n//2,
            'right': n-1,
            'comparing': None,
            'current_left': [],
            'current_right': [],
            'step': 'Array sorted successfully!',
            'complete': True
        })
        yield True

    @staticmethod
    def quick_sort(inputs, draw_func):
        array = inputs.copy()
        n = len(array)
        
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            
            # Draw pivot selection
            draw_func({
                'type': 'quick',
                'array': arr.copy(),
                'pivot_idx': high,
                'current_idx': None,
                'partition_idx': i,
                'range': (low, high),
                'step': f"Selected pivot: {pivot}",
                'complete': False
            })
            yield
            
            for j in range(low, high):
                # Draw comparison state
                draw_func({
                    'type': 'quick',
                    'array': arr.copy(),
                    'pivot_idx': high,
                    'current_idx': j,
                    'partition_idx': i,
                    'range': (low, high),
                    'step': f"Comparing {arr[j]} with pivot {pivot}",
                    'complete': False
                })
                yield
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    
                    # Draw swap state
                    draw_func({
                        'type': 'quick',
                        'array': arr.copy(),
                        'pivot_idx': high,
                        'current_idx': j,
                        'partition_idx': i,
                        'range': (low, high),
                        'step': f"Swapped {arr[i]} and {arr[j]}",
                        'complete': False
                    })
                    yield
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            
            # Draw final partition state
            draw_func({
                'type': 'quick',
                'array': arr.copy(),
                'pivot_idx': i + 1,
                'current_idx': None,
                'partition_idx': i + 1,
                'range': (low, high),
                'step': f"Placed pivot {pivot} in final position",
                'complete': False
            })
            yield
            
            return i + 1

        def quick_sort_recursive(arr, low, high):
            if low < high:
                # Find partition index
                pi = yield from partition(arr, low, high)
                
                # Recursively sort elements before and after partition
                yield from quick_sort_recursive(arr, low, pi - 1)
                yield from quick_sort_recursive(arr, pi + 1, high)
        
        # Start the recursive process
        yield from quick_sort_recursive(array, 0, n - 1)
        
        # Show completion
        draw_func({
            'type': 'quick',
            'array': array,
            'pivot_idx': None,
            'current_idx': None,
            'partition_idx': None,
            'range': (0, n-1),
            'step': 'Array sorted successfully!',
            'complete': True
        })
        yield True

    @staticmethod
    def generate_random_array(size=10):
        """Generate random array for sorting"""
        import random
        return [random.randint(1, 100) for _ in range(size)] 