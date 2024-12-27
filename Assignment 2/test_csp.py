from csp import CSP, alldiff

csp = None


def test_initialization():
    grid = open("sudoku_medium.txt").read().split()

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

    global csp
    csp = CSP(
        variables=[f"X{row+1}{col+1}" for row in range(WIDTH) for col in range(WIDTH)],
        domains=domains,
        edges=edges,
    )


def test_get_subgrid():
    assert "X11" not in list(csp.get_subgrid("X11"))

    assert list(csp.get_subgrid("X11")) == [
        "X12",
        "X13",
        "X21",
        "X22",
        "X23",
        "X31",
        "X32",
        "X33",
    ]
    assert list(csp.get_subgrid("X12")) == [
        "X11",
        "X13",
        "X21",
        "X22",
        "X23",
        "X31",
        "X32",
        "X33",
    ]
    assert list(csp.get_subgrid("X21")) == [
        "X11",
        "X12",
        "X13",
        "X22",
        "X23",
        "X31",
        "X32",
        "X33",
    ]
    assert list(csp.get_subgrid("X44")) == [
        "X45",
        "X46",
        "X54",
        "X55",
        "X56",
        "X64",
        "X65",
        "X66",
    ]
    assert list(csp.get_subgrid("X77")) == [
        "X78",
        "X79",
        "X87",
        "X88",
        "X89",
        "X97",
        "X98",
        "X99",
    ]


def test_get_column():
    assert list(csp.get_column("X11")) == [
        "X21",
        "X31",
        "X41",
        "X51",
        "X61",
        "X71",
        "X81",
        "X91",
    ]


def test_get_row():
    assert list(csp.get_row("X11")) == [
        "X12",
        "X13",
        "X14",
        "X15",
        "X16",
        "X17",
        "X18",
        "X19",
    ]
