import streamlit as st
import random

# --- Game Initialization ---
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "winner" not in st.session_state:
    st.session_state.winner = None
if "current_player" not in st.session_state:
    st.session_state.current_player = "X"
if "first_player" not in st.session_state:
    st.session_state.first_player = "You (X)"
if "game_running" not in st.session_state:
    st.session_state.game_running = False
if "mode" not in st.session_state:
    st.session_state.mode = "Player vs AI"
if "history" not in st.session_state:
    st.session_state.history = []
if "scores" not in st.session_state:
    st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}

# --- Utility Functions ---
def available_moves(board):
    return [i for i, v in enumerate(board) if v == ""]

def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for a, b, c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell != "" for cell in board):
        return "Draw"
    return None

def minimax(board, depth, is_max, alpha, beta):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "Draw":
        return 0

    if is_max:
        best = -float("inf")
        for move in available_moves(board):
            board[move] = "O"
            val = minimax(board, depth + 1, False, alpha, beta)
            board[move] = ""
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float("inf")
        for move in available_moves(board):
            board[move] = "X"
            val = minimax(board, depth + 1, True, alpha, beta)
            board[move] = ""
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def best_move():
    best_val = -float("inf")
    move = None
    for i in available_moves(st.session_state.board):
        st.session_state.board[i] = "O"
        move_val = minimax(st.session_state.board, 0, False, -float("inf"), float("inf"))
        st.session_state.board[i] = ""
        if move_val > best_val:
            best_val = move_val
            move = i
    return move

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.winner = None
    st.session_state.current_player = "X" if st.session_state.first_player == "You (X)" else "O"
    st.session_state.history = []

# --- AI Logic ---
def auto_ai_turn():
    if st.session_state.winner or not st.session_state.game_running:
        return
    if st.session_state.current_player == "O":
        move = best_move()
        if move is not None:
            apply_move(move)

# --- Move Logic ---
def apply_move(idx):
    if st.session_state.board[idx] == "" and not st.session_state.winner:
        st.session_state.history.append(st.session_state.board[:])
        st.session_state.board[idx] = st.session_state.current_player
        st.session_state.winner = check_winner(st.session_state.board)
        if st.session_state.winner:
            st.session_state.scores[st.session_state.winner] += 1
            st.session_state.game_running = False
        else:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# --- UI Layout ---
st.set_page_config(page_title="Tic-Tac-Toe", layout="centered")
st.title("🎮 Minimax Tic-Tac-Toe")

with st.sidebar:
    st.header("Game Settings")
    disable_inputs = st.session_state.game_running

    st.session_state.mode = st.radio(
        "Game Mode",
        ["Player vs AI", "Player vs Player"],
        disabled=disable_inputs
    )

    st.selectbox(
        "First Turn",
        ["You (X)", "AI (O)"],
        index=0 if st.session_state.first_player == "You (X)" else 1,
        key="first_player",
        disabled=disable_inputs or st.session_state.mode != "Player vs AI"
    )

    if not st.session_state.game_running:
        if st.button("▶️ Start"):
            reset_game()
            st.session_state.game_running = True
            st.rerun()
    else:
        if st.button("⏹ Stop"):
            st.session_state.game_running = False
            reset_game()
            st.rerun()

    if st.session_state.mode == "Player vs Player":
        st.button("↩️ Undo", disabled=not st.session_state.game_running or not st.session_state.history)
    else:
        st.button("↩️ Undo", disabled=True)

    st.markdown("### Score")
    st.write(f"You (X): {st.session_state.scores['X']}")
    st.write(f"AI (O): {st.session_state.scores['O']}")
    st.write(f"Draws: {st.session_state.scores['Draw']}")

# --- Board UI ---
st.markdown("""
    <style>
    div.stButton > button {
        height: 80px;
        width: 80px;
        font-size: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    for j in range(3):
        idx = i * 3 + j
        with cols[j]:
            if st.button(st.session_state.board[idx] or " ", key=f"cell{idx}"):
                if st.session_state.game_running and st.session_state.board[idx] == "" and not st.session_state.winner:
                    apply_move(idx)
                    st.rerun()

# --- Auto AI Move if Needed ---
if st.session_state.mode == "Player vs AI" and st.session_state.current_player == "O" and st.session_state.game_running:
    auto_ai_turn()
    st.rerun()

# --- Status ---
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.success("It's a draw!")
    else:
        st.success(f"{st.session_state.winner} wins!")
else:
    st.info(f"Turn: {st.session_state.current_player}")
