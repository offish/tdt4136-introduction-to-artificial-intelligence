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

    # def ac_3(self) -> bool:
    #     """Performs AC-3 on the CSP.

    #     Returns:
    #         False if a domain becomes empty, otherwise True
    #     """
    #     queue = [(x, y) for (x, y) in self.binary_constraints]

    #     while queue:
    #         (xi, xj) = queue.pop(0)

    #         if self.revise(xi, xj):
    #             if len(self.domains[xi]) == 0:
    #                 return False

    #             for xk, _ in self.binary_constraints:
    #                 if xk != xj:
    #                     queue.append((xk, xi))

    #     return True

    # def revise(self, xi: str, xj: str) -> bool:
    #     """Revise the domain of xi based on the binary constraint between xi and xj."""
    #     revised = False
    #     for x in set(self.domains[xi]):
    #         # Check if there is no valid y in the domain of xj that satisfies the constraint
    #         if not any(
    #             (x, y) in self.binary_constraints[(xi, xj)] for y in self.domains[xj]
    #         ):
    #             self.domains[xi].remove(x)
    #             revised = True
    #     return revised

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.

        Returns:
            A solution if any exists, otherwise None
        """
        # print(self.binary_constraints)
        # return

        def are_neighbors(a: str, b: str) -> bool:
            return (a, b) in self.binary_constraints or (
                b,
                a,
            ) in self.binary_constraints

        def is_legal(var: str, value: Any, assignment: dict[str, Any]) -> bool:
            for neighbor in self.variables:
                if var == neighbor:
                    continue

                if neighbor not in assignment:
                    continue

                neighbor_value = assignment[neighbor]

                if are_neighbors(var, neighbor):
                    if value == neighbor_value:
                        return False

            return True

        def backtrack(assignment: dict[str, Any]) -> dict[str, Any]:
            """The recursive backtracking function."""

            if len(assignment) == len(self.variables):
                return assignment

            # Select an unassigned variable
            # unassigned_vars = [v for v in self.variables if v not in assignment]
            # var = unassigned_vars[0]

            for var in self.variables:
                if var in assignment:
                    continue

                for value in self.domains[var]:
                    if is_legal(var, value, assignment):
                        # Assign the value
                        assignment[var] = value

                        # Recur with the updated assignment
                        result = backtrack(assignment)

                        if result:
                            return result

                        # If failure, remove the assignment (backtrack)
                        assignment.pop(var)

                return {}

        return backtrack({})


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
