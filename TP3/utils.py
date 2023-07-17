from datetime import datetime
from typing import Tuple


def create_request_message(process_id: int, message_size: int) -> str:
    """Return a request message"""
    separator = "|"
    padding_zeros = "0" * (message_size - 2 - 1 - len(str(process_id)))
    message = f"1{separator}{process_id}{separator}{padding_zeros}"
    return message


def create_grant_message(process_id: int, message_size: int) -> str:
    """Return a grant message"""
    separator = "|"
    padding_zeros = "0" * (message_size - 2 - 1 - len(str(process_id)))
    message = f"2{separator}{process_id}{separator}{padding_zeros}"
    return message


def create_release_message(process_id: int, message_size: int) -> str:
    """Return a release message"""
    separator = "|"
    padding_zeros = "0" * (message_size - 2 - 1 - len(str(process_id)))
    message = f"3{separator}{process_id}{separator}{padding_zeros}"
    return message


def decode_message(data: bytes) -> Tuple[int, int]:
    """Returns (type, pid) given a message received"""
    decoded = data.decode()
    message_type, pid, _ = decoded.split('|')
    return int(message_type), int(pid)


def create_log_message(data: bytes) -> str:
    """Return a log message based on the data given"""
    current_time = str(datetime.now())
    message_type, pid = decode_message(data)

    log_message = ""
    if message_type == 1:
        log_message += "[R] Request"
    elif message_type == 2:
        log_message += "[S] Grant"
    elif message_type == 3:
        log_message += "[R] Release"
    
    log_message += f" - {pid} - {current_time[11:19]}\n"
    return log_message