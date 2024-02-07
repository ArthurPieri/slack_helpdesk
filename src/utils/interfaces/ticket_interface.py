from typing import NamedTuple

from datetime import datetime


class Ticket(NamedTuple):
    """
    Deffinition of a basic ticket
    """

    ticket_id: str
    category: str
    start_date: datetime
    user_id: str
    user_name: str
    link: str
    metadata: dict
    end_date: datetime = None
