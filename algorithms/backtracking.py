import random

class BacktrackingAlgorithms:
    @staticmethod
    def get_algorithm(name, board, draw_func):
        algorithm_map = {
            "N-Queens Problem": BacktrackingAlgorithms.n_queens,
            "Sudoku": BacktrackingAlgorithms.sudoku,
            "Sudoku Solver": BacktrackingAlgorithms.sudoku
        }
        
        if name in algorithm_map:
            return algorithm_map[name](board, draw_func)
        raise ValueError(f"Algorithm {name} not implemented")

    @staticmethod
    def generate_sudoku():
        board = [[0] * 9 for _ in range(9)]
        
        # Fill diagonal 3x3 boxes
        for i in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for r in range(3):
                for c in range(3):
                    board[i + r][i + c] = nums[r * 3 + c]
        
        # Solve the rest of the board
        def solve_board(board):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        for num in range(1, 10):
                            if BacktrackingAlgorithms.is_valid_sudoku(board, i, j, num):
                                board[i][j] = num
                                if solve_board(board):
                                    return True
                                board[i][j] = 0
                        return False
            return True
            
        solve_board(board)
        
        # Remove some numbers to create puzzle
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, j in cells[35:]:  # Leave 35 numbers, remove the rest
            board[i][j] = 0
            
        return board

    @staticmethod
    def is_valid_sudoku(board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    @staticmethod
    def sudoku(board, draw_func):
        def solve(board):
            found = False
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        found = True
                        for num in range(1, 10):
                            if BacktrackingAlgorithms.is_valid_sudoku(board, i, j, num):
                                board[i][j] = num
                                draw_func([row[:] for row in board])
                                yield
                                
                                for _ in solve(board):
                                    yield
                                
                                if all(all(cell != 0 for cell in row) for row in board):
                                    return
                                    
                                board[i][j] = 0
                                draw_func([row[:] for row in board])
                                yield
                        if board[i][j] == 0:
                            return
            if not found:
                return
                
        for step in solve(board):
            yield step

    @staticmethod
    def n_queens(board, draw_func):
        def is_safe(board, row, col):
            # Check row on left side
            for j in range(col):
                if board[row][j] == 1:
                    return False
            
            # Check upper diagonal on left side
            for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
                if board[i][j] == 1:
                    return False
            
            # Check lower diagonal on left side
            for i, j in zip(range(row, len(board)), range(col, -1, -1)):
                if board[i][j] == 1:
                    return False
            return True

        def solve(board, col):
            # Base case: If all queens are placed, return True
            if col >= len(board):
                return True
            
            # Try placing queen in each row of this column
            for row in range(len(board)):
                draw_func([row[:] for row in board], (row, col))
                yield
                
                if is_safe(board, row, col):
                    # Place queen
                    board[row][col] = 1
                    draw_func([row[:] for row in board], (row, col))
                    yield
                    
                    # Recur for next column
                    solver = solve(board, col + 1)
                    try:
                        while True:
                            next(solver)
                            if col + 1 >= len(board):
                                return True
                            yield
                    except StopIteration:
                        if col + 1 >= len(board):
                            return True
                    
                    # If placing queen doesn't lead to solution, backtrack
                    board[row][col] = 0
                    draw_func([row[:] for row in board], (row, col))
                    yield
            
            return False

        # Start solving from first column
        solver = solve(board, 0)
        try:
            while True:
                next(solver)
                if all(sum(row) == 1 for row in board) and sum(sum(row) for row in board) == len(board):
                    yield True
                    return
                yield False
        except StopIteration:
            yield False