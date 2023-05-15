import os

os.system("gcc prod_cons.c -o prod_cons")
p_c = [(1, 1), (1, 2), (1, 4), (1, 8), (2, 1), (4, 1), (8, 1)]
for p, c in p_c:
    print(f"Running for {p} producers and {c} consumers")
    for _ in range(10):
        os.system(f"./prod_cons {p} {c}")
    print("Changing number of producers and consumers...")