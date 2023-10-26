# pylint: disable=redefined-outer-name
from datetime import datetime

import pytest

from ..src.db.db import DbManager, Ticket


@pytest.fixture(scope="module")
def obj():
    yield DbManager(db_host='localhost', db_port=5432, db_name='mydatabase', db_user='postgres', db_password='postgres')


@pytest.fixture(scope="module")
def new_ticket():
    return Ticket(
        ticket_id='1',
        category='bug',
        start_date=datetime.now(),
        user_id='user1',
        user_name='User One',
        link='http://example.com',
        metadata={},
    )


class TestDb:
    """
    Testing db connection, create and close ticket
    """

    def test_create_ticket_on_db(self, obj, new_ticket):
        success = obj.create_ticket_on_db('public', 'tickets', new_ticket)
        assert success is True

    def test_close_ticket_on_db(self, obj):
        success = obj.close_ticket_on_db('public', 'tickets', '1', datetime.now())
        assert success is True
