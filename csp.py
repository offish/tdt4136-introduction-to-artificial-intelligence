from typing import Any


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains, and edges.

        Args:
            variables: The variables for the CSP
            domains: The domains of the variables
            edges: Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable_1=value1, variable_2=value2 is in violation of a binary constraint:
        # if (
        #     (variable_1, variable_2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable_1, variable_2)]
        # ) or (
        #     (variable_2, variable_1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable_2, variable_1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}

        for variable_1, variable_2 in edges:
            self.binary_constraints[(variable_1, variable_2)] = set()

            for value1 in self.domains[variable_1]:
                for value2 in self.domains[variable_2]:
                    if value1 == value2:
                        continue

                    self.binary_constraints[(variable_1, variable_2)].add(
                        (value1, value2)
                    )
                    self.binary_constraints[(variable_1, variable_2)].add(
                        (value2, value1)
                    )

    def get_column(self, variable: str) -> list[str]:
        return [var for var in self.variables if var[1] == variable[1]]

    def get_row(self, variable: str) -> list[str]:
        return [var for var in self.variables if var[2] == variable[2]]

    def get_box(self, variable: str) -> list[str]:
        # X11
        # -> X11, X12, X13
        # -> X21, X22, X23
        # -> X31, X32, X33
        row_index = int(variable[1])
        column_index = int(variable[2])

        start_row = (row_index - 1) // 3 * 3 + 1
        start_column = (column_index - 1) // 3 * 3 + 1

        box = []

        for i in range(3):
            for j in range(3):
                position = f"X{start_row + i}{start_column + j}"
                box.append(position)

        return box

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.

        Returns:
            False if a domain becomes empty, otherwise True
        """
        for i in self.domains:
            value = self.domains[i]

            if len(value) != 1:
                continue

            for j in self.get_column(i):
                if i == j:
                    continue

                self.domains[j] -= value

            for j in self.get_row(i):
                if i == j:
                    continue

                self.domains[j] -= value

            for j in self.get_box(i):
                if i == j:
                    continue

                self.domains[j] -= value

        return len(self.domains) > 1

    def are_neighbors(self, a: str, b: str) -> bool:
        return (a, b) in self.binary_constraints or (
            b,
            a,
        ) in self.binary_constraints

    def get_neighbor(self, var: str):
        for neighbor in self.variables:
            if neighbor == var:
                continue

            yield neighbor

    def is_allowed(self, var: str, value: Any, assignment: dict[str, Any]) -> bool:
        for neighbor in self.get_neighbor(var):
            if neighbor not in assignment:
                continue

            neighbor_value = assignment[neighbor]

            if self.are_neighbors(var, neighbor) and value == neighbor_value:
                return False

        return True

    def backtrack(self, assignment: dict[str, Any]) -> dict[str, Any]:
        """The recursive backtracking function."""

        if len(assignment) == len(self.variables):
            return assignment

        for var in self.variables:
            if var in assignment:
                continue

            for value in self.domains[var]:
                if self.is_allowed(var, value, assignment):
                    # Assign the value
                    assignment[var] = value

                    # Recur with the updated assignment
                    result = self.backtrack(assignment)

                    if result:
                        return result

                    # If failure, remove the assignment (backtrack)
                    del assignment[var]

            return {}

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.

        Returns:
            A solution if any exists, otherwise None
        """
        return self.backtrack({})


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables

    Args:
        variables: The variables that all must be different

    Returns:
        List of edges in the form (a, b)
    """
    return [
        (variables[i], variables[j])
        for i in range(len(variables) - 1)
        for j in range(i + 1, len(variables))
    ]
