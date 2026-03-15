# minimax_agents.py
from __future__ import annotations

import random
from typing import Callable, Dict, Optional

from tictactoe import State, actions, initial_state, print_board, result, terminal_test, utility

Counter = Dict[str, int]


def minimax_decision(state: State, counter: Counter) -> int:
    """
    Returns the best action for the player to move using minimax.
    Utility is from X perspective:
    +1 X wins, 0 tie, -1 O wins.
    """
    if terminal_test(state):
        raise ValueError("minimax_decision called on terminal state")

    legal = actions(state)

    if state.to_move == "X":
        best_val = -10
        best_act = legal[0]
        for a in legal:
            v = _min_value(result(state, a), counter)
            if v > best_val:
                best_val = v
                best_act = a
        return best_act
    else:
        best_val = 10
        best_act = legal[0]
        for a in legal:
            v = _max_value(result(state, a), counter)
            if v < best_val:
                best_val = v
                best_act = a
        return best_act


def _max_value(state: State, counter: Counter) -> int:
    """
    MAX-VALUE from lecture pseudocode.
    Count a node expansion when we expand a non-terminal node and iterate actions.
    """
    if terminal_test(state):
        return utility(state)

    counter["expanded"] += 1
    v = -10
    for a in actions(state):
        v = max(v, _min_value(result(state, a), counter))
    return v


def _min_value(state: State, counter: Counter) -> int:
    """
    MIN-VALUE from lecture pseudocode.
    Count a node expansion when we expand a non-terminal node and iterate actions.
    """
    if terminal_test(state):
        return utility(state)

    counter["expanded"] += 1
    v = 10
    for a in actions(state):
        v = min(v, _max_value(result(state, a), counter))
    return v


def op_min(state: State, counter: Counter) -> int:
    """
    PDF: op_min() is the optimal MIN agent.
    MIN is player O, so it chooses the action that minimizes X's utility.
    """
    if state.to_move != "O":
        raise ValueError("op_min called when it's not O's turn")

    legal = actions(state)
    best_val = 10
    best_act = legal[0]
    for a in legal:
        v = _max_value(result(state, a), counter)
        if v < best_val:
            best_val = v
            best_act = a
    return best_act


def rand_min(state: State) -> int:
    """
    PDF: rand_min() chooses a random legal action.
    """
    if state.to_move != "O":
        raise ValueError("rand_min called when it's not O's turn")
    return random.choice(actions(state))


def par_min(state: State, counter: Counter) -> int:
    """
    PDF: par_min() chooses randomly 40% of the time and optimally 60% of the time.
    """
    if state.to_move != "O":
        raise ValueError("par_min called when it's not O's turn")

    if random.random() < 0.4:
        return rand_min(state)
    return op_min(state, counter)


def train_max_vs_min(min_policy: str, games: int = 50, seed: Optional[int] = 7) -> int:
    """
    The PDF uses the word "train" but this assignment is minimax, not learning.
    Here, "training" means simulating games and reporting the number of nodes expanded
    by the MAX (X) minimax search across those games.
    """
    if seed is not None:
        random.seed(seed)

    total_expanded_by_x = 0

    for _ in range(games):
        state = initial_state()
        while not terminal_test(state):
            if state.to_move == "X":
                counter: Counter = {"expanded": 0}
                a = minimax_decision(state, counter)
                total_expanded_by_x += counter["expanded"]
                state = result(state, a)
            else:
                if min_policy == "op":
                    counter = {"expanded": 0}
                    a = op_min(state, counter)
                elif min_policy == "rand":
                    a = rand_min(state)
                elif min_policy == "par":
                    counter = {"expanded": 0}
                    a = par_min(state, counter)
                else:
                    raise ValueError("Unknown min_policy")

                state = result(state, a)

    return total_expanded_by_x


def _prompt_human_move(state: State) -> int:
    legal = set(actions(state))
    while True:
        raw = input("Your move (0-8): ").strip()
        try:
            a = int(raw)
        except ValueError:
            print("Invalid input. Enter a number 0-8.")
            continue
        if a not in legal:
            print("Illegal move. Pick an empty cell index 0-8.")
            continue
        return a


def play_human_vs_max(max_name: str) -> None:
    """
    User plays O, MAX agent plays X using minimax.
    """
    state = initial_state()
    print("\nYou are O. Agent is X.")
    print("Index layout:")
    print("0 | 1 | 2\n--|---|--\n3 | 4 | 5\n--|---|--\n6 | 7 | 8\n")

    while True:
        print_board(state)
        print()

        if terminal_test(state):
            u = utility(state)
            if u == 1:
                print("Result: X wins.")
            elif u == -1:
                print("Result: O wins.")
            else:
                print("Result: Tie.")
            return

        if state.to_move == "X":
            counter: Counter = {"expanded": 0}
            a = minimax_decision(state, counter)
            print(f"{max_name} chooses: {a}")
            print(f"Nodes expanded (this move): {counter['expanded']}\n")
            state = result(state, a)
        else:
            a = _prompt_human_move(state)
            state = result(state, a)


def main() -> None:
    total_op = train_max_vs_min("op", games=50, seed=7)
    print(f"Training complete: MAX vs op_min, total nodes expanded by MAX: {total_op}")

    total_rand = train_max_vs_min("rand", games=50, seed=7)
    print(f"Training complete: MAX vs rand_min, total nodes expanded by MAX: {total_rand}")

    total_par = train_max_vs_min("par", games=50, seed=7)
    print(f"Training complete: MAX vs par_min, total nodes expanded by MAX: {total_par}")


    while True:
        print("\nMenu")
        print("1) Play vs MAX trained vs op_min")
        print("2) Play vs MAX trained vs rand_min")
        print("3) Play vs MAX trained vs par_min")
        print("4) Quit")

        choice = input("Choose 1-4: ").strip()
        if choice == "1":
            play_human_vs_max("MAX (minimax, trained vs op_min)")
        elif choice == "2":
            play_human_vs_max("MAX (minimax, trained vs rand_min)")
        elif choice == "3":
            play_human_vs_max("MAX (minimax, trained vs par_min)")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()