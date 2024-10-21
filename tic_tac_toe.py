from copy import deepcopy
import math

State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is),
# and board
Action = tuple[int, int]  # Where to place the player's piece


class Game:
    @staticmethod
    def initial_state() -> State:
        return (
            0,
            [
                [None, None, None],
                [None, None, None],
                [None, None, None],
            ],
        )

    @staticmethod
    def to_move(state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        player_index, board = state
        actions = []

        for row in range(3):
            for col in range(3):
                if board[row][col] is not None:
                    continue

                actions.append((row, col))

        for action in actions:
            next_board = deepcopy(board)
            next_board[action[0]][action[1]] = player_index
            state = (player_index, next_board)

            if self.is_winner(state, player_index):
                return [action]

        return actions

    @staticmethod
    def is_winner(state: State, player: int) -> bool:
        _, board = state

        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True

        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True

        if all(board[i][i] == player for i in range(3)):
            return True

        return all(board[i][2 - i] == player for i in range(3))

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)

        return (self.to_move(state) + 1) % 2, next_board

    def is_terminal(self, state: State) -> bool:
        _, board = state

        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True

        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state: State, player: int) -> int:
        assert self.is_terminal(state)

        if self.is_winner(state, player):
            return 1

        if self.is_winner(state, (player + 1) % 2):
            return -1

        return 0

    def print(self, state: State) -> None:
        _, board = state

        print()

        for row in range(3):
            cells = [
                " " if board[row][col] is None else "x" if board[row][col] == 0 else "o"
                for col in range(3)
            ]

            print(f" {cells[0]} | {cells[1]} | {cells[2]}")

            if row < 2:
                print("---+---+---")

        print()

        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print("P1 won")
            elif self.utility(state, 1) > 0:
                print("P2 won")
            else:
                print("The game is a draw")
        else:
            print(f"It is P{self.to_move(state)+1}'s turn to move")


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
