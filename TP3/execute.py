import subprocess
import pandas as pd
from log_validator import validate
from result_validator import validate_result, calculate_timestamp_difference

# SCALABILITY TEST 1
print("SCALABILITY TEST 1")
r, k = 10, 2
n = [2, 4, 8, 16, 32]
scalability_test_1 = []
for num_of_processes in n:
    print(f"Number of processes {num_of_processes}")
    filename = 'resultado.txt'
    with open(filename, 'w') as file: # RESETTING RESULTADO.TXT FILE
        pass
    subprocess.run(["python", "main.py", f"{num_of_processes}", f"{r}", f"{k}"], capture_output=True, text=True)
    time = calculate_timestamp_difference("resultado.txt")
    result_validation = validate_result(num_of_processes, r)
    print(f"RESULT VALIDATION FOR N = {num_of_processes} ; R = {r} ; K = {k}")
    print(result_validation)
    scalability_test_1.append(time)

df = pd.DataFrame(scalability_test_1, columns=['Time'])
df.to_csv('scalability_test_1.csv', index=False)

# SCALABILITY TEST 2
print("SCALABILITY TEST 2")
r, k = 5, 1
n = [2, 4, 8, 16, 32, 64]
scalability_test_2 = []
for num_of_processes in n:
    print(f"Number of processes {num_of_processes}")
    filename = 'resultado.txt'
    with open(filename, 'w') as file:
        pass
    subprocess.run(["python", "main.py", f"{num_of_processes}", f"{r}", f"{k}"], capture_output=True, text=True)
    time = calculate_timestamp_difference("resultado.txt")
    result_validation = validate_result(num_of_processes, r)
    print(f"RESULT VALIDATION FOR N = {num_of_processes} ; R = {r} ; K = {k}")
    print(result_validation)
    scalability_test_2.append(time)

df = pd.DataFrame(scalability_test_2, columns=['Time'])
df.to_csv('scalability_test_2.csv', index=False)

# SCALABILITY TEST 3
print("SCALABILITY TEST 3")
r, k = 3, 0
n = [2, 4, 8, 16, 32, 64, 128]
scalability_test_3 = []
for num_of_processes in n:
    print(f"Number of processes {num_of_processes}")
    filename = 'resultado.txt'
    with open(filename, 'w') as file:
        pass
    subprocess.run(["python", "main.py", f"{num_of_processes}", f"{r}", f"{k}"], capture_output=True, text=True)
    time = calculate_timestamp_difference("resultado.txt")
    result_validation = validate_result(num_of_processes, r)
    print(f"RESULT VALIDATION FOR N = {num_of_processes} ; R = {r} ; K = {k}")
    print(result_validation)
    scalability_test_3.append(time)

df = pd.DataFrame(scalability_test_3, columns=['Time'])
df.to_csv('scalability_test_3.csv', index=False)

# VALIDATE LOG FILE CREATED BY COORDINATOR
print("LOG VALIDATION")
validate()