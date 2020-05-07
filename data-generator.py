#IE-400 Project data-generator
import numpy as np
import sys


def generate_data(n:int):
    for i in range(5,n + 5,5) :
        print(i)

if __name__ == "__main__":
    n = int(sys.argv[1])
    # print (n)
    generate_data(n)
