import json

from psycopg2 import connect

from .interfaces.db_manager import DbInterface
from .interfaces.ticket_interface import Ticket


class PostgresDb(DbInterface):
    """
    Use this class to create a simple interface to a database.
    In this basic example we'll use a PostgresSQL database.
    """

    def create_ticket_on_db(self, ticket: Ticket, **kwargs) -> bool:
        """
        Save the ticket on the database
        ## Args:
        - db_schema: Name of schema, collection or similar of the database
        - db_table: The table, document or similar of the database
        - ticket: The ticket to be saved
        """
        if "db_schema" not in kwargs or "db_table" not in kwargs:
            raise ValueError("You must provide a schema and a table to save the ticket")

        cur = self.conn.cursor()

        query = f"INSERT INTO {kwargs['db_schema']}.{kwargs['db_table']}"
        query = query + " (ticket_id, category, link, metadata, start_date, user_id, user_name) "
        query = query + "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(
                query,
                (
                    ticket.ticket_id,
                    ticket.category,
                    ticket.link,
                    json.dumps(ticket.metadata),
                    ticket.start_date,
                    ticket.user_id,
                    ticket.user_name,
                ),
            )
            self.conn.commit()
            return True
        except Exception as exc:  # pylint: disable=broad-except
            self.log.error("Error inserting ticket on database: %s", exc)
            return False
        finally:
            cur.close()

    def close_ticket_on_db(self, ticket_id: str, **kwargs) -> bool:
        """
        Close the ticket on the database
        ## Args:
        - db_schema: The schema, collection or similar of the database
        - db_table: The table, document or similar of the database
        - ticket_id: The id of the ticket to be closed
        - end_date: The date of the ticket closing
        """
        if "db_schema" not in kwargs or "db_table" not in kwargs:
            raise ValueError("You must provide a schema and a table to close the ticket")
        if not ticket_id:
            raise ValueError("You must provide a ticket_id to close the ticket")
        if "end_date" not in kwargs:
            raise ValueError("You must provide an end_date to close the ticket")

        cur = self.conn.cursor()
        update_query = f"UPDATE {kwargs['db_schema']}.{kwargs['db_table']}"
        update_query = update_query + " SET end_date = %s WHERE ticket_id = %s"
        try:
            cur.execute(update_query, (kwargs['end_date'], ticket_id))
            self.conn.commit()
            return True
        except Exception as exc:  # pylint: disable=broad-except
            self.log.error("Error closing ticket on database: %s", exc)
            return False
        finally:
            cur.close()

    def _connect_to_db(self, **kwargs):
        """
        Connect to the database
        """
        if "db_name" not in kwargs or "db_user" not in kwargs or "db_password" not in kwargs:
            raise ValueError("You must provide a db_name, db_user and db_password to connect to the database")

        self.log.info("Connecting to database %s", kwargs['db_name'])
        try:
            conn = connect(
                database=kwargs['db_name'],
                user=kwargs['db_user'],
                password=kwargs['db_password'],
                host=kwargs['db_host'],
                port=kwargs['db_port'],
            )
            self.log.info("Connected to database %s", kwargs['db_name'])
            return conn
        except Exception as exc:  # pylint: disable=broad-except
            self.log.error("Error connecting to database: %s", exc)
            raise exc
