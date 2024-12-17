import random

class DynamicAlgorithms:
    @staticmethod
    def get_algorithm(name, inputs, draw_func):
        algorithm_map = {
            "Fibonacci Sequence": DynamicAlgorithms.fibonacci,
            "Longest Common Subsequence": DynamicAlgorithms.longest_common_subsequence
        }
        
        return algorithm_map.get(name, lambda x, y: None)(inputs, draw_func)

    @staticmethod
    def fibonacci(sequence, draw_func):
        n = len(sequence)
        # Initialize dp array
        dp = [0] * n
        
        # Copy first two numbers from sequence
        if n > 0:
            dp[0] = sequence[0]
        if n > 1:
            dp[1] = sequence[1]
            
        # Draw initial state
        draw_func({
            'sequence': dp,
            'original': sequence,
            'current': None,
            'prev1': None,
            'prev2': None,
            'step': 'Initial sequence loaded',
            'complete': False
        })
        yield
        
        # Calculate Fibonacci numbers
        for i in range(2, n):
            # Highlight previous two numbers being used
            draw_func({
                'sequence': dp,
                'original': sequence,
                'current': i,
                'prev1': i-1,
                'prev2': i-2,
                'step': f'Adding {dp[i-1]} and {dp[i-2]}',
                'complete': False
            })
            yield
            
            # Calculate new number
            dp[i] = dp[i-1] + dp[i-2]
            
            # Show result
            draw_func({
                'sequence': dp,
                'original': sequence,
                'current': i,
                'prev1': None,
                'prev2': None,
                'step': f'Position {i}: {dp[i]}',
                'complete': False
            })
            yield
        
        # Show completion
        draw_func({
            'sequence': dp,
            'original': sequence,
            'current': None,
            'prev1': None,
            'prev2': None,
            'step': 'Fibonacci sequence complete!',
            'complete': True
        })
        yield True

    @staticmethod
    def generate_random_sequence(length):
        """Generate a random sequence of numbers"""
        return [random.randint(1, 100) for _ in range(length)]

    @staticmethod
    def longest_common_subsequence(inputs, draw_func):
        str1, str2 = inputs
        m, n = len(str1), len(str2)
        
        # Create a 2D array to store lengths of LCS
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Draw initial state
        draw_func({
            'type': 'lcs',
            'dp': dp,
            'str1': str1,
            'str2': str2,
            'i': None,
            'j': None,
            'step': 'Initialized DP table',
            'complete': False
        })
        yield
        
        # Build the dp array
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Compare characters
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    step_text = f"Match found: {str1[i-1]}, adding 1 to diagonal"
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                    step_text = f"No match between {str1[i-1]} and {str2[j-1]}, taking max of left and up"
                
                # Draw current state
                draw_func({
                    'type': 'lcs',
                    'dp': dp,
                    'str1': str1,
                    'str2': str2,
                    'i': i,
                    'j': j,
                    'step': step_text,
                    'complete': False
                })
                yield
        
        # Find the LCS string
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if str1[i-1] == str2[j-1]:
                lcs.append(str1[i-1])
                i -= 1
                j -= 1
                draw_func({
                    'type': 'lcs',
                    'dp': dp,
                    'str1': str1,
                    'str2': str2,
                    'i': i,
                    'j': j,
                    'step': f"Found character {str1[i]} in LCS",
                    'complete': False,
                    'backtrack': True,
                    'lcs': ''.join(reversed(lcs))
                })
                yield
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        # Show completion
        draw_func({
            'type': 'lcs',
            'dp': dp,
            'str1': str1,
            'str2': str2,
            'i': None,
            'j': None,
            'step': f'LCS is {"".join(reversed(lcs))} with length {dp[m][n]}',
            'complete': True,
            'lcs': ''.join(reversed(lcs))
        })
        yield True