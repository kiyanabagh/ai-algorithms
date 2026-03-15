# alphabeta_agents.py
from __future__ import annotations

import random
from typing import Dict, List, Optional

from tictactoe import State, actions, initial_state, print_board, result, terminal_test, utility, winner

Counter = Dict[str, int]


def alphabeta_decision(state: State, counter: Counter) -> int:
    """
    Alpha-beta search that returns the best action for the player to move.
    Node expansion counted at non-terminal nodes when expanding successors.
    """
    if terminal_test(state):
        raise ValueError("alphabeta_decision called on terminal state")

    legal = actions(state)
    alpha = -10
    beta = 10

    if state.to_move == "X":
        best_val = -10
        best_act = legal[0]
        for a in legal:
            v = _ab_min_value(result(state, a), alpha, beta, counter)
            if v > best_val:
                best_val = v
                best_act = a
            alpha = max(alpha, best_val)
        return best_act
    else:
        best_val = 10
        best_act = legal[0]
        for a in legal:
            v = _ab_max_value(result(state, a), alpha, beta, counter)
            if v < best_val:
                best_val = v
                best_act = a
            beta = min(beta, best_val)
        return best_act


def _ab_max_value(state: State, alpha: int, beta: int, counter: Counter) -> int:
    if terminal_test(state):
        return utility(state)

    counter["expanded"] += 1
    v = -10
    for a in actions(state):
        v = max(v, _ab_min_value(result(state, a), alpha, beta, counter))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def _ab_min_value(state: State, alpha: int, beta: int, counter: Counter) -> int:
    if terminal_test(state):
        return utility(state)

    counter["expanded"] += 1
    v = 10
    for a in actions(state):
        v = min(v, _ab_max_value(result(state, a), alpha, beta, counter))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def ordered_actions(state: State) -> List[int]:
    """
    Move ordering heuristic for tic-tac-toe.
    The PDF says "best successor first". For tic-tac-toe, a strong "best-first"
    ordering is:
      1) winning move now
      2) blocking opponent win next
      3) center
      4) corners
      5) edges
    """
    legal = actions(state)
    cur = state.to_move
    opp = "O" if cur == "X" else "X"

    def opp_has_immediate_win(st: State, who: str) -> bool:
        if terminal_test(st):
            return False
        for a in actions(st):
            b = list(st.board)
            b[a] = who
            # quick winner test on a constructed state
            if winner(State(tuple(b), st.to_move)) == who:
                return True
        return False

    def score(a: int) -> int:
        s1 = result(state, a)
        if winner(s1) == cur:
            return 100
        before = opp_has_immediate_win(state, opp)
        after = opp_has_immediate_win(s1, opp)
        if before and not after:
            return 80
        if a == 4:
            return 60
        if a in (0, 2, 6, 8):
            return 40
        return 20

    return sorted(legal, key=score, reverse=True)


def alphabeta_ordered_decision(state: State, counter: Counter) -> int:
    """
    Same alpha-beta search, but iterates successors in best-first order.
    """
    if terminal_test(state):
        raise ValueError("alphabeta_ordered_decision called on terminal state")

    legal = ordered_actions(state)
    alpha = -10
    beta = 10

    if state.to_move == "X":
        best_val = -10
        best_act = legal[0]
        for a in legal:
            v = _ab_min_value_ordered(result(state, a), alpha, beta, counter)
            if v > best_val:
                best_val = v
                best_act = a
            alpha = max(alpha, best_val)
        return best_act
    else:
        best_val = 10
        best_act = legal[0]
        for a in legal:
            v = _ab_max_value_ordered(result(state, a), alpha, beta, counter)
            if v < best_val:
                best_val = v
                best_act = a
            beta = min(beta, best_val)
        return best_act


def _ab_max_value_ordered(state: State, alpha: int, beta: int, counter: Counter) -> int:
    if terminal_test(state):
        return utility(state)

    counter["expanded"] += 1
    v = -10
    for a in ordered_actions(state):
        v = max(v, _ab_min_value_ordered(result(state, a), alpha, beta, counter))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def _ab_min_value_ordered(state: State, alpha: int, beta: int, counter: Counter) -> int:
    if terminal_test(state):
        return utility(state)

    counter["expanded"] += 1
    v = 10
    for a in ordered_actions(state):
        v = min(v, _ab_max_value_ordered(result(state, a), alpha, beta, counter))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


# ----------------------------
# "Training" and efficiency
# ----------------------------
def train_alphabeta(games: int = 50, seed: Optional[int] = 7) -> int:
    """
    Simulate games where X uses alpha-beta and O plays randomly.
    Count total nodes expanded by X across all its moves.
    """
    if seed is not None:
        random.seed(seed)

    total_expanded_by_x = 0

    for _ in range(games):
        state = initial_state()
        while not terminal_test(state):
            if state.to_move == "X":
                counter: Counter = {"expanded": 0}
                a = alphabeta_decision(state, counter)
                total_expanded_by_x += counter["expanded"]
                state = result(state, a)
            else:
                # Using random O for a simple, valid simulation.
                # The assignment does not specify MIN behavior here.
                a = random.choice(actions(state))
                state = result(state, a)

    return total_expanded_by_x


def train_alphabeta_ordered(games: int = 50, seed: Optional[int] = 7) -> int:
    """
    Same as train_alphabeta, but using move ordering version.
    """
    if seed is not None:
        random.seed(seed)

    total_expanded_by_x = 0

    for _ in range(games):
        state = initial_state()
        while not terminal_test(state):
            if state.to_move == "X":
                counter: Counter = {"expanded": 0}
                a = alphabeta_ordered_decision(state, counter)
                total_expanded_by_x += counter["expanded"]
                state = result(state, a)
            else:
                a = random.choice(actions(state))
                state = result(state, a)

    return total_expanded_by_x


# ----------------------------
# Play mode: user vs agent
# ----------------------------
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


def play_human_vs_ai(ai_name: str, ai_fn) -> None:
    """
    User plays O, AI plays X.
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
            a = ai_fn(state, counter)
            print(f"{ai_name} chooses: {a}")
            print(f"Nodes expanded (this move): {counter['expanded']}\n")
            state = result(state, a)
        else:
            a = _prompt_human_move(state)
            state = result(state, a)


def main() -> None:
    vanilla_total = train_alphabeta(games=50, seed=7)
    print(f"Training complete: Vanilla alpha-beta total nodes expanded by X: {vanilla_total}")

    ordered_total = train_alphabeta_ordered(games=50, seed=7)
    print(f"Training complete: Move-ordered alpha-beta total nodes expanded by X: {ordered_total}")

    if vanilla_total > 0:
        reduction = (vanilla_total - ordered_total) / vanilla_total * 100.0
        print(f"Efficiency (reduction vs vanilla): {reduction:.2f}%")
    else:
        print("Efficiency: n/a")


    while True:
        print("\nMenu")
        print("1) Play vs vanilla alpha-beta")
        print("2) Play vs move-ordered alpha-beta")
        print("3) Quit")

        choice = input("Choose 1-3: ").strip()
        if choice == "1":
            play_human_vs_ai("AlphaBeta", alphabeta_decision)
        elif choice == "2":
            play_human_vs_ai("AlphaBeta Ordered", alphabeta_ordered_decision)
        elif choice == "3":
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()