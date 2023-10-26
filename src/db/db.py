from logging import getLogger

from typing import NamedTuple

from datetime import datetime

from psycopg2 import connect


class Ticket(NamedTuple):
    """
    Deffinition of a basic ticket
    """

    _id: str
    category: str
    end_date: datetime = None
    start_date: datetime
    user_id: str
    user_name: str
    link: str
    metadata: dict


class DbManager:
    """
    Use this class to create a simple interface to a database.
    In this basic example we'll use a PostgresSQL database.
    """

    def __init__(self, db_host: str, db_port: int, db_name: str, db_user: str, db_password: str):
        """
        Args:
        - db_name: The name of the database
        - db_user: The username of the database
        - db_password: The password of the database
        - db_host: The host of the database
        - db_port: The port of the database
        """
        self._start_log()
        self._connect_to_db(db_host=db_host, db_port=db_port, db_name=db_name, db_user=db_user, db_password=db_password)

    def create_ticket_on_db(self, db_schema: str, db_table: str, ticket: Ticket) -> bool:
        """
        Save the ticket on the database
        """
        cur = self.conn.cursor()
        query = f"INSERT INTO {db_schema}.{db_table} (id, category, link, metadata, start_date, user_id, user_name)"
        query = query + "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(
                query,
                (
                    ticket["_id"],
                    ticket["category"],
                    ticket["link"],
                    ticket["metadata"],
                    ticket["start_date"],
                    ticket["user_id"],
                    ticket["user_name"],
                ),
            )
            self.conn.commit()
            cur.close()
            return True
        except Exception as exc:  # pylint: disable=broad-except
            self.log.error("Error inserting ticket on database: %s", exc)
            return False

    def close_ticket_on_db(self, db_schema: str, db_table: str, _id: str, end_date: datetime) -> bool:
        cur = self.conn.cursor()
        update_query = f"UPDATE {db_schema}.{db_table}"
        update_query = update_query + " SET end_date = %s WHERE id = %s"
        try:
            cur.execute(update_query, (end_date, _id))
            self.conn.commit()
            cur.close()
            return True
        except Exception as exc:  # pylint: disable=broad-except
            self.log.error("Error closing ticket on database: %s", exc)
            return False

    def _connect_to_db(self, db_host: str, db_port: int, db_name: str, db_user: str, db_password: str):
        """
        Connect to the database
        """
        self.log.info("Connecting to database %s", db_name)
        try:
            self.conn = connect(
                database=db_name, user=db_user, password=db_password, host=db_host, port=db_port
            )  # pylint: disable=attribute-defined-outside-init
            self.log.info("Connected to database %s", db_name)
        except Exception as exc:  # pylint: disable=broad-except
            self.log.error("Error connecting to database: %s", exc)

    def _start_log(self) -> None:
        """
        Start logging for class
        """
        self.log = getLogger(__name__)  # pylint: disable=attribute-defined-outside-init
        self.log.info("-----------------------------------------")
        self.log.info("Initializing %s class", self.__class__.__name__)
        self.log.info("-----------------------------------------")
