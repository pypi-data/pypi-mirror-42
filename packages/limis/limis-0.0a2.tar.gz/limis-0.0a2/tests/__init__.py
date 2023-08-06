import logging
import socket

from pathlib import Path


def remove_logfile(log_filename: str = None):
    logger = logging.getLogger()
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.flush()
        handler.close()

    log_file = Path().cwd() / 'limis.log'

    if log_file.exists():
        log_file.unlink()


def listening(port):
    test_socket = socket.socket()

    try:
        test_socket.connect(('localhost', port))
    except socket.error:
        return False
    finally:
        test_socket.close()

    return True
