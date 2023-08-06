import logging
import socket

from pathlib import Path


def listening(port):
    test_socket = socket.socket()

    try:
        test_socket.connect(('localhost', port))
    except socket.error:
        return False
    finally:
        test_socket.close()

    return True


def remove_logfile():
    logger = logging.getLogger()
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.flush()
        handler.close()

    log_file = Path().cwd() / 'limis.log'

    if log_file.exists():
        log_file.unlink()


def string_in_file(filename: str, string: str):
    found = False

    with open(filename) as file:
        lines = file.readlines()

        if len(list(filter(lambda x: string in x, lines))) > 0:
            found = True

        file.close()

    return found
