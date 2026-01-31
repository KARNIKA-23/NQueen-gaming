import copy

class NQueensModel:
    def __init__(self, n=8):
        self.n = n
        self.board = [-1] * n  # board[row] = col. -1 means empty
        self.solutions = []
        self.current_step = 0
    
    def reset(self):
        """Resets the board to empty state."""
        self.board = [-1] * self.n
    
    def set_size(self, n):
        """Sets the board size and resets."""
        self.n = max(4, n)
        self.reset()
        
    def is_safe(self, row, col, board_state=None):
        """
        Check if it's safe to place a queen at board[row] = col.
        row: The row index (0 to N-1)
        col: The column index (0 to N-1)
        board_state: Optional custom board state (list of cols). uses self.board if None.
        """
        if board_state is None:
            board_state = self.board
            
        # Check against existing queens
        for r in range(self.n):
            if r == row:
                continue # Don't check against self if we are updating a row
                
            c = board_state[r]
            if c == -1:
                continue # No queen in this row
            
            # 1. Column check
            if c == col:
                return False
            
            # 2. Diagonal check
            if abs(r - row) == abs(c - col):
                return False
                
        return True

    def toggle_queen(self, row, col):
        """
        Toggles a queen at (row, col).
        Returns True if a change was made, False otherwise.
        """
        if self.board[row] == col:
            self.board[row] = -1 # Remove
            return True
        else:
            # Try to place
            # Note: The game might allow placing invalid queens to show they are invalid, 
            # or strictly enforce valid moves only.
            # Here we enforce 1 queen per row strictly since we use a 1D array.
            # If the user clicks a different column in the same row, it moves the queen.
            self.board[row] = col
            return True
            
    def get_placed_queens_count(self):
        return sum(1 for x in self.board if x != -1)
        
    def is_solved(self):
        if self.get_placed_queens_count() != self.n:
            return False
            
        # Verify all
        for r in range(self.n):
            if not self.is_safe(r, self.board[r]):
                return False
        return True

    def get_invalid_queens(self):
        """Returns a list of (row, col) tuples that are in invalid positions."""
        invalid = []
        for r in range(self.n):
            c = self.board[r]
            if c != -1:
                # Temporarily remove self to check if others attack it
                temp_board = list(self.board)
                # We need to check if THIS queen is being attacked by ANY OTHER queen
                # is_safe checks if (r, c) is safe from others. 
                # So we just run is_safe on the current state but ignore 'self' inside is_safe logic?
                # Actually my is_safe implementation skips 'r == row', so it works directly on current board
                if not self.is_safe(r, c):
                    invalid.append((r, c))
        return invalid

    def solve_step_generator(self):
        """
        A generator that yields the board state at each step of the backtracking algorithm.
        Useful for visualization.
        """
        
        # We start with an empty board for the solver
        # Or should we try to solve from current state? usually solve from scratch.
        solver_board = [-1] * self.n
        
        def backtrack(row):
            if row == self.n:
                return True
            
            for col in range(self.n):
                solver_board[row] = col
                yield list(solver_board) # Yield state for animation
                
                if self.is_safe(row, col, solver_board):
                    if (yield from backtrack(row + 1)):
                        return True
                
                solver_board[row] = -1
                yield list(solver_board) # Backtrack visualization
            
            return False

        yield from backtrack(0)
        self.board = list(solver_board) # Update main board at end
