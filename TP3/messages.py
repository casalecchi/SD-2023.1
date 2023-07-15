# Message type = 1
def create_request_message(process_id, message_size):
    separator = "|"
    padding_zeros = "0" * (message_size - 2 - 1 - len(str(process_id)))
    message = f"1{separator}{process_id}{separator}{padding_zeros}"
    return message


# Message type = 2
def create_grant_message(process_id, message_size):
    separator = "|"
    padding_zeros = "0" * (message_size - 2 - 1 - len(str(process_id)))
    message = f"2{separator}{process_id}{separator}{padding_zeros}"
    return message


# Message type = 3
def create_release_message(process_id, message_size):
    separator = "|"
    padding_zeros = "0" * (message_size - 2 - 1 - len(str(process_id)))
    message = f"3{separator}{process_id}{separator}{padding_zeros}"
    return message