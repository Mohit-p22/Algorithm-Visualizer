class SearchingAlgorithms:
    @staticmethod
    def linear_search(arr, target, draw_func, speed):
        comparisons = 0
        for i in range(len(arr)):
            comparisons += 1
            draw_func(arr, current_idx=i)
            yield comparisons
            
            if arr[i] == target:
                draw_func(arr, current_idx=i, found_idx=i)
                return i
        return -1
        
    @staticmethod
    def binary_search(arr, target, draw_func, speed):
        left, right = 0, len(arr) - 1
        comparisons = 0
        
        while left <= right:
            mid = (left + right) // 2
            comparisons += 1
            
            # Visualize current state
            draw_func(arr, current_idx=mid)
            yield comparisons
            
            if arr[mid] == target:
                draw_func(arr, current_idx=mid, found_idx=mid)
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return -1
        
    @staticmethod
    def jump_search(arr, target, draw_func, speed):
        n = len(arr)
        step = int(n ** 0.5)  # Optimal jump size
        comparisons = 0
        
        # Finding the block where element may be present
        prev = 0
        while prev < n and arr[min(step, n) - 1] < target:
            comparisons += 1
            draw_func(arr, current_idx=min(step, n) - 1)
            yield comparisons
            
            prev = step
            step += int(n ** 0.5)
            if prev >= n:
                return -1
                
        # Linear search in the identified block
        while prev < n:
            comparisons += 1
            draw_func(arr, current_idx=prev)
            yield comparisons
            
            if arr[prev] == target:
                draw_func(arr, current_idx=prev, found_idx=prev)
                return prev
            elif arr[prev] > target:
                break
                
            prev += 1
            
        return -1

    @staticmethod
    def interpolation_search(arr, target, draw_func, speed):
        low = 0
        high = len(arr) - 1
        comparisons = 0
        
        while low <= high and target >= arr[low] and target <= arr[high]:
            comparisons += 1
            
            if low == high:
                if arr[low] == target:
                    draw_func(arr, current_idx=low, found_idx=low)
                    return low
                return -1
                
            # Interpolation formula
            pos = low + int(((high - low) * (target - arr[low]) /
                           (arr[high] - arr[low])))
                           
            draw_func(arr, current_idx=pos)
            yield comparisons
            
            if arr[pos] == target:
                draw_func(arr, current_idx=pos, found_idx=pos)
                return pos
                
            if arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1
                
        return -1

    @staticmethod
    def exponential_search(arr, target, draw_func, speed):
        comparisons = 0
        if arr[0] == target:
            draw_func(arr, current_idx=0, found_idx=0)
            return 0
            
        # Find range for binary search
        i = 1
        n = len(arr)
        while i < n and arr[i] <= target:
            comparisons += 1
            draw_func(arr, current_idx=i)
            yield comparisons
            i *= 2
            
        # Binary search in the found range
        for comp in SearchingAlgorithms.binary_search_range(
            arr, target, i//2, min(i, n-1), draw_func, speed, comparisons):
            yield comp

    @staticmethod
    def binary_search_range(arr, target, left, right, draw_func, speed, comparisons=0):
        while left <= right:
            mid = (left + right) // 2
            comparisons += 1
            
            draw_func(arr, current_idx=mid)
            yield comparisons
            
            if arr[mid] == target:
                draw_func(arr, current_idx=mid, found_idx=mid)
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return -1
        
    # Add other searching algorithms (jump_search, interpolation_search) 