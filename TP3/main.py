import subprocess
import sys

def str_to_int(num, default):
    if num.isnumeric():
        return int(num)
    else:
        return default

# Get inputs from the user
n = sys.argv[1]
n = str_to_int(n, 10)

r = sys.argv[2]
r = str_to_int(r, 10)

k = sys.argv[3]
k = str_to_int(k, 2)

print(f"n={n} | r={r} | k= {k}")

for i in range(n):
    subprocess.Popen(["python", "client.py", f"{r}", f"{k}"])