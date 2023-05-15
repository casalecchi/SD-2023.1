import os

os.system("gcc counter.c -o counter")
Ks = [1, 2, 4, 8, 16, 32, 64, 128, 256]
for K in Ks:
    print(f"Running for {K} threads")
    for _ in range(10):
        os.system(f"./counter {K}")
    print("Changing number of threads...")