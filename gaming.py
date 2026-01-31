import streamlit as st


def is_safe(board, row, col):
    n = len(board)

    # Check column
    for i in range(row):
        if board[i][col] == 1:
            return False

    # Check upper-left diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Check upper-right diagonal
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1

    return True


def solve_n_queens(board, row):
    n = len(board)
    if row == n:
        return True

    for col in range(n):
        if is_safe(board, row, col):
            board[row][col] = 1
            if solve_n_queens(board, row + 1):
                return True
            board[row][col] = 0

    return False


# Streamlit UI
st.set_page_config(page_title="N-Queens Solver")
st.title("N-Queens Solver")

# Sidebar controls
n_input = st.sidebar.number_input("Enter N (>=4)", min_value=4, value=4)

if st.sidebar.button("Start / Reset"):
    st.session_state.board = [[0 for _ in range(n_input)] for _ in range(n_input)]
    st.session_state.current_row = 0
    st.session_state.n = n_input
    st.rerun()

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.n = n_input
    st.session_state.board = [[0 for _ in range(n_input)] for _ in range(n_input)]
    st.session_state.current_row = 0

n = st.session_state.n
board = st.session_state.board
current_row = st.session_state.current_row

# Status and Auto Solve
if current_row < n:
    st.info(f"Place Queen in Row {current_row}")
    if st.sidebar.button("Auto Solve"):
        if solve_n_queens(board, current_row):
            st.session_state.current_row = n
            st.rerun()
        else:
            st.error("No solution exists from current state.")
else:
    st.success("Solved! 🎉")

# Display Board
for r in range(n):
    cols = st.columns(n)
    for c in range(n):
        is_queen = board[r][c] == 1
        label = "Q" if is_queen else "."
        
        # Logic for button state
        if r == current_row and current_row < n:
            # Active row
            if cols[c].button(label, key=f"{r}-{c}"):
                if is_safe(board, r, c):
                    board[r][c] = 1
                    st.session_state.current_row += 1
                    st.rerun()
                else:
                    st.error(f"Invalid move at Row {r}, Column {c}")
        else:
            # Inactive rows (past or future)
            cols[c].button(label, key=f"{r}-{c}", disabled=True)
