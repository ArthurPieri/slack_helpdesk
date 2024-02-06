# pylint: disable=too-few-public-methods, unused-private-member
import logging
import sys


class LoggingBot:
    """
    Centralizing logging into a class.
    """

    def __init__(self):
        """
        Start logging for class.
        """
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.INFO,
            format="[TICKET_BOT][%(levelname)s]%(filename)s:%(lineno)d %(asctime)s - %(message)s",
        )
        self.log = logging.LoggerAdapter(
            logging.getLogger(self.__class__.__name__),
            {"class": self.__class__.__name__},
        )
