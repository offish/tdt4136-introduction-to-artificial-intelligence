from typing import Any
from queue import Queue


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.

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

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.

        Returns:
            False if a domain becomes empty, otherwise True
        """
        # YOUR CODE HERE (and remove the assertion below)
        assert False, "Not implemented"

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.

        Returns:
            A solution if any exists, otherwise None
        """

        def backtrack(assignment: dict[str, Any]):
            # YOUR CODE HERE (and remove the assertion below)
            assert False, "Not implemented"

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
