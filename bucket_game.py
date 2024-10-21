import math

State = tuple[int, list[str | int]]  # Tuple of player (whose turn it is),
# and the buckets (as str)
# or the number in a bucket
Action = str | int  # Bucket choice (as str) or choice of number


class Game:
    @staticmethod
    def initial_state() -> State:
        return 0, ["A", "B", "C"]

    @staticmethod
    def to_move(state: State) -> int:
        player, _ = state
        return player

    @staticmethod
    def actions(state: State) -> list[Action]:
        _, actions = state
        return actions

    @staticmethod
    def is_terminal(state: State) -> bool:
        _, actions = state
        return len(actions) == 1

    def result(self, state: State, action: Action) -> State:
        if action == "A":
            return (self.to_move(state) + 1) % 2, [-50, 50]

        if action == "B":
            return (self.to_move(state) + 1) % 2, [3, 1]

        if action == "C":
            return (self.to_move(state) + 1) % 2, [-5, 15]

        assert type(action) is int
        return (self.to_move(state) + 1) % 2, [action]

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        _, actions = state
        assert type(actions[0]) is int

        return actions[0] if player == self.to_move(state) else -actions[0]

    def print(self, state):
        print(f"The state is {state} and ", end="")

        if self.is_terminal(state):
            print(f"P1's utility is {self.utility(state, 0)}")
        else:
            print(f"it is P{self.to_move(state)+1}'s turn")


def max_value(game: Game, state: State) -> float:
    if game.is_terminal(state):
        return game.utility(state, 0)

    v = -math.inf

    for action in game.actions(state):
        result = game.result(state, action)
        v = max(v, min_value(game, result))

    assert v != -math.inf

    return v


def min_value(game: Game, state: State) -> float:
    if game.is_terminal(state):
        return game.utility(state, 0)

    v = math.inf

    for action in game.actions(state):
        result = game.result(state, action)
        v = min(v, max_value(game, result))

    assert v != math.inf

    return v


def minimax_search(game: Game, state: State) -> Action | None:
    best_action = None
    best_value = -math.inf

    for action in game.actions(state):
        result = game.result(state, action)
        v = min_value(game, result)

        if v > best_value:
            best_value = v
            best_action = action

    return best_action


if __name__ == "__main__":
    game = Game()

    state = game.initial_state()
    game.print(state)

    while not game.is_terminal(state):
        player = game.to_move(state)
        action = minimax_search(game, state)  # The player whose turn it is
        # is the MAX player
        print(f"P{player+1}'s action: {action}")

        assert action is not None

        state = game.result(state, action)
        game.print(state)
