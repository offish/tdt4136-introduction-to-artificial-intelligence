# Sudoku problems.
# The CSP.ac_3() and CSP.backtrack() methods need to be implemented

from csp import CSP, alldiff
import time


def print_solution(solution: dict, width: int) -> None:
    """
    Convert the representation of a Sudoku solution, as returned from
    the method CSP.backtracking_search(), into a Sudoku board.
    """
    for row in range(width):
        for col in range(width):
            print(solution[f"X{row+1}{col+1}"], end=" ")

            if col == 2 or col == 5:
                print("|", end=" ")

        print("")

        if row == 2 or row == 5:
            print("------+-------+------")


def main(problem: str) -> None:
    # Choose Sudoku problem
    grid = open(problem).read().split()

    print(f"\n\nSudoku problem: {problem}")

    WIDTH = 9
    BOX_WIDTH = 3
    domains = {}

    for row in range(WIDTH):
        for col in range(WIDTH):
            if grid[row][col] == "0":
                domains[f"X{row+1}{col+1}"] = set(range(1, 10))
            else:
                domains[f"X{row+1}{col+1}"] = {int(grid[row][col])}

    edges = []

    for row in range(WIDTH):
        edges += alldiff([f"X{row+1}{col+1}" for col in range(WIDTH)])

    for col in range(WIDTH):
        edges += alldiff([f"X{row+1}{col+1}" for row in range(WIDTH)])

    for box_row in range(BOX_WIDTH):
        for box_col in range(BOX_WIDTH):
            edges += alldiff(
                [
                    f"X{row+1}{col+1}"
                    for row in range(box_row * BOX_WIDTH, (box_row + 1) * BOX_WIDTH)
                    for col in range(box_col * BOX_WIDTH, (box_col + 1) * BOX_WIDTH)
                ]
            )

    csp = CSP(
        variables=[f"X{row+1}{col+1}" for row in range(WIDTH) for col in range(WIDTH)],
        domains=domains,
        edges=edges,
    )

    # print(csp.get_box("X11"))
    # print(csp.get_box("X12"))
    # print(csp.get_box("X21"))
    # print(csp.get_box("X44"))
    # print(csp.get_box("X77"))
    # print(csp.get_box("X99"))
    # Expected output:
    # X44 X45 X46
    # X54 X55 X56
    # X64 X65 X66

    # return

    start_time = time.time()
    print(csp.ac_3())

    print(csp.domains)

    solution_time = time.time()
    print_solution(csp.backtracking_search(), WIDTH)
    end_time = time.time()

    print(f"AC3 runtime: {solution_time-start_time}")
    print(f"Backtracking runtime: {end_time-solution_time}")
    print(f"Total time: {end_time-start_time}")
    print(f"Total calls: {csp.backtrack_called}")
    print(f"Total failed: {csp.backtrack_failures}")

    # Expected output after implementing csp.ac_3() and csp.backtracking_search():
    # True
    # 7 8 4 | 9 3 2 | 1 5 6
    # 6 1 9 | 4 8 5 | 3 2 7
    # 2 3 5 | 1 7 6 | 4 8 9
    # ------+-------+------
    # 5 7 8 | 2 6 1 | 9 3 4
    # 3 4 1 | 8 9 7 | 5 6 2
    # 9 2 6 | 5 4 3 | 8 7 1
    # ------+-------+------
    # 4 5 3 | 7 2 9 | 6 1 8
    # 8 6 2 | 3 1 4 | 7 9 5
    # 1 9 7 | 6 5 8 | 2 4 3


if __name__ == "__main__":
    for problem in [
        "sudoku_easy.txt",
        "sudoku_medium.txt",
        "sudoku_hard.txt",
        "sudoku_very_hard.txt",
    ]:
        main(problem)
