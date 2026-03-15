# tictactoe.py
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple


# All winning triplets in tic-tac-toe (indices 0..8).
WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


@dataclass(frozen=True)
class State:
    """
    Immutable game state.
    board: a tuple of 9 cells containing "X", "O", or " ".
    to_move: whose turn it is, "X" or "O".
    """
    board: Tuple[str, ...]
    to_move: str


def initial_state() -> State:
    """Creates the empty starting state with X to move."""
    return State(board=tuple([" "] * 9), to_move="X")


def player(state: State) -> str:
    """Returns whose turn it is."""
    return state.to_move


def actions(state: State) -> List[int]:
    """Returns all legal actions (empty cell indices)."""
    return [i for i, cell in enumerate(state.board) if cell == " "]


def result(state: State, action: int) -> State:
    """
    Returns a NEW state after applying 'action' for the current player.
    Raises if action is illegal.
    """
    if action < 0 or action > 8:
        raise ValueError("Action must be an index from 0 to 8.")
    if state.board[action] != " ":
        raise ValueError("That cell is not empty.")

    b = list(state.board)
    b[action] = state.to_move
    next_player = "O" if state.to_move == "X" else "X"
    return State(board=tuple(b), to_move=next_player)


def winner(state: State) -> Optional[str]:
    """Returns 'X' or 'O' if someone has won, otherwise None."""
    for a, b, c in WIN_LINES:
        if state.board[a] != " " and state.board[a] == state.board[b] == state.board[c]:
            return state.board[a]
    return None


def terminal_test(state: State) -> bool:
    """
    Matches the provided starter snippet behavior:
    Terminal if someone has won OR the board is full.
    """
    for a, b, c in WIN_LINES:
        if state.board[a] == state.board[b] == state.board[c] != " ":
            return True
    if all(cell != " " for cell in state.board):
        return True
    return False


def utility(state: State) -> int:
    """
    Matches the provided starter snippet convention:
    X win = +1, O win = -1, tie/non-terminal = 0.
    """
    for a, b, c in WIN_LINES:
        if state.board[a] == state.board[b] == state.board[c] == "X":
            return 1
        if state.board[a] == state.board[b] == state.board[c] == "O":
            return -1
    return 0


def print_board(state: State) -> None:
    """
    Matches the provided starter snippet printing format.
    """
    b = state.board
    print(
        " " + b[0] + " | " + b[1] + " | " + b[2] + "\n"
        "---|---|---\n"
        " " + b[3] + " | " + b[4] + " | " + b[5] + "\n"
        "---|---|---\n"
        " " + b[6] + " | " + b[7] + " | " + b[8]
    )
