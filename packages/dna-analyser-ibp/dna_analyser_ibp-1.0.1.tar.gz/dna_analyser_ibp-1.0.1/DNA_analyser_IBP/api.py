# api.py
# !/usr/bin/env python3
"""
Library with API object for manipulation with BPI REST API.
Available classes:
- Api: object encapsulation whole rest api.
"""

from .callers.user_caller import User

from .g4hunter import G4hunter
from .sequence import Sequence
# from p53 import P53


class Api:
    """Api class contains all methods for working with BPI REST API."""

    def __init__(
        self,
        email: str = "host",
        password: str = "host",
        server: str = "http://localhost:8080/api",
    ):
        """
        Creates Api object and auto login
        :param email: user email
        :param password: user password
        :param server: custom server address
        """
        self.user = User(email=email, password=password, server=server)
        self.sequence = Sequence(self.user)
        self.g4hunter = G4hunter(user=self.user)
        # self.p53 = P53(user=self.user)

    def __repr__(self):
        return f"<Api: {self.user.server} user: {self.user.email}>"

    def __str__(self):
        return f"Api: {self.user.server} user: {self.user.email}"


if __name__ == "__main__":
    pass
