import sys
from datetime import datetime

def verify_write_counts():
    expected_counts = {}
    process_counts = {}
    with open("resultado.txt", 'r') as file:
        for line in file:
            process_info, _ = line.strip().split(" - ")
            process_id = process_info.split()[0]
            expected_counts[process_id] = expected_counts.get(process_id, 0) + 1
            process_counts[process_id] = process_counts.get(process_id, 0) + 1
    for process_id, expected_count in expected_counts.items():
        actual_count = process_counts.get(process_id, 0)
        if actual_count != expected_count:
            return False
    return True

def validate_result(n, r):
    previous_timestamp = None
    f = open("resultado.txt", "r")
    lines = f.readlines()
    if len(lines) != n * r:
        sys.exit("Wrong number of lines")
    else:
        print("Correct number of lines")
    for line in lines:
        process_id, timestamp_raw = line.strip().split(" - ")
        timestamp_str = timestamp_raw[11:] # Remove year, month and date
        timestamp = datetime.strptime(timestamp_str, '%H:%M:%S.%f')
        if previous_timestamp is not None and timestamp <= previous_timestamp:
            sys.exit("Wrong Timestamp")
        previous_timestamp = timestamp
    print("Correct Timestamps")
    if verify_write_counts():
        print("Each process wrote the expected number of times")
    else:
        sys.exit("Wrong count of process writes")

validate_result(32, 10)