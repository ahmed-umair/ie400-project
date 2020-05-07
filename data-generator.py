# IE-400 Project data-generator
import numpy as np
import sys
import pprint
import math

# Since the numpy function used to generate the random matrices returns values in the range [a,b),
# we specify the our ranges as [a,b+1) to make them [a,b]
valid_hw_time_range = (300, 501)
valid_travel_time_range = (100, 301)


def generate_data(n: int):
    # Generate one-time (1,75) matrix for student times
    student_times_Xi = (valid_hw_time_range[1] - valid_hw_time_range[0]
                        ) * np.random.rand(1, 75) + valid_hw_time_range[0]
    student_times_Xi = np.round(student_times_Xi)
    print(student_times_Xi)

    # Enumerate the applicable N values up to N
    N_set = range(5, n + 5, 5)
    print(f"\n {N_set}")
    N = []
    for i in N_set:
        print(f"\nCurrent N: {i}")
        variants = range(1, math.ceil(i * math.log(i)))
        print(f"\t {variants}")
        
        ith_travel_time_matrix = np.zeros((i,i))
        for variant_num in variants:
            current_variant =   (np.round((valid_travel_time_range[1] - valid_travel_time_range[0]
                                            ) * np.random.rand(i,i) + valid_travel_time_range[0]))
            print(current_variant)
            ith_travel_time_matrix = ith_travel_time_matrix + current_variant
        
        print(variant_num)
        ith_travel_time_matrix = ith_travel_time_matrix/variant_num
        print(ith_travel_time_matrix)
        N.append(ith_travel_time_matrix)
    
    print(N[0])

if __name__ == "__main__":
    n = int(sys.argv[1])
    # print (n)
    generate_data(n)
