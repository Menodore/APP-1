import streamlit as st
import numpy as np
import random

# Initialize the board
def init_board():
    return np.array([['', '', ''], ['', '', ''], ['', '', '']])

# Check for a winner
def check_winner(board, player):
    # Rows, columns, and diagonals check
    for i in range(3):
        if all([cell == player for cell in board[i, :]]) or all([cell == player for cell in board[:, i]]):
            return True
    if board[0, 0] == board[1, 1] == board[2, 2] == player or board[0, 2] == board[1, 1] == board[2, 0] == player:
        return True
    return False

# Check if the board is full
def is_draw(board):
    return not any(cell == '' for row in board for cell in row)

# Make a random move for the computer
def computer_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i, j] == '']
    if empty_cells:
        move = random.choice(empty_cells)
        board[move[0], move[1]] = 'O'

# Render symbols with colors
def render_symbol(symbol):
    if symbol == 'X':
        return '<span style="color: red; font-size: 48px;">&#10060;</span>'  # Red cross (X)
    elif symbol == 'O':
        return '<span style="color: green; font-size: 48px;">&#11093;</span>'  # Green circle (O)
    return '<span style="font-size: 48px;">&nbsp;</span>'  # Empty space for buttons

# Main function for the Streamlit app
def main():
    st.title("Tic Tac Toe 🎮")

    # Select mode: Human vs. Human or Human vs. Computer
    mode = st.selectbox("Choose Game Mode:", ["Human vs. Human", "Human vs. Computer"])

    # Initialize the game board in session state to retain state
    if 'board' not in st.session_state:
        st.session_state.board = init_board()
        st.session_state.current_player = 'X'  # X always starts
        st.session_state.winner = None
        st.session_state.draw = False

    # Display the game board with styled layout
    for i in range(3):
        cols = st.columns(3)  # Create three equal columns for the board
        for j in range(3):
            # Check if cell is empty and clickable
            if st.session_state.board[i, j] == '':
                # Create a button for empty cells and handle clicks
                if cols[j].button(" ", key=f'{i}{j}', help="Click to play"):
                    if st.session_state.current_player == 'X' or mode == "Human vs. Human":
                        st.session_state.board[i, j] = st.session_state.current_player
                        # Check for winner or draw
                        if check_winner(st.session_state.board, st.session_state.current_player):
                            st.session_state.winner = st.session_state.current_player
                        elif is_draw(st.session_state.board):
                            st.session_state.draw = True
                        else:
                            # Switch player
                            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

                    # Computer move in Human vs. Computer mode
                    if mode == "Human vs. Computer" and not st.session_state.winner and not st.session_state.draw:
                        computer_move(st.session_state.board)
                        if check_winner(st.session_state.board, 'O'):
                            st.session_state.winner = 'O'
                        elif is_draw(st.session_state.board):
                            st.session_state.draw = True
            else:
                # Display the symbol using markdown to render it with color
                cols[j].markdown(render_symbol(st.session_state.board[i, j]), unsafe_allow_html=True)

        # Add row dividers to resemble the board structure
        if i < 2:
            st.markdown('___|___|___')

    # Display winner or draw message
    if st.session_state.winner:
        st.success(f"Player {st.session_state.winner} wins!")
    elif st.session_state.draw:
        st.info("It's a draw!")

    # Restart game button
    if st.button("Restart Game"):
        st.session_state.board = init_board()
        st.session_state.current_player = 'X'
        st.session_state.winner = None
        st.session_state.draw = False

# Run the app
if __name__ == "__main__":
    main()
