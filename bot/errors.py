"""
Custom errors classes created for the need ot the project
"""


class NoSourceFound(Exception):
    """
    Exception raised when picture searched return no good result.
    """

    def __init__(self, reason: str = "No source found."):
        self.reason = reason

        super(NoSourceFound, self).__init__(reason)
