import subprocess


def str_to_int(num, default):
    if num.isnumeric():
        return int(n)
    else:
        return default

# Get inputs fromthe user
n = input("Number of processes [2]: ")
n = str_to_int(n, 2)

r = input("Repetition for each process [10]: ")
r = str_to_int(r, 10)

k = input("Wait time [2]: ")
k = str_to_int(k, 2)

for i in range(128):
    subprocess.Popen(["python3", "client.py", f"{r}", f"{k}"])

