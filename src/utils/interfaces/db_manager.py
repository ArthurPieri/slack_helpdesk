# pylint: disable=relative-beyond-top-level
from abc import ABC, abstractmethod

from .ticket_interface import Ticket

from ..log_ticket import LoggingBot


class DbInterface(ABC, LoggingBot):
    """
    Interface for the database
    """

    def __init__(self, **kwargs):
        """
        Start your db manager class
        ## Args:
        - db_name: The name of the database
        - db_user: The username of the database
        - db_password: The password of the database
        - db_host: The host of the database
        - db_port: The port of the database
        """
        super().__init__()
        self.db_name = kwargs['db_name']
        self.conn = self._connect_to_db(**kwargs)

    @abstractmethod
    def create_ticket_on_db(self, ticket: Ticket, **kwargs) -> bool:
        """
        Save the ticket on the database
        """

    @abstractmethod
    def close_ticket_on_db(self, ticket_id: str, **kwargs) -> bool:
        """
        Close the ticket on the database
        """

    @abstractmethod
    def _connect_to_db(self, **kwargs):
        """
        Connect to the database
        """
