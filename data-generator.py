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

    # Enumerate the applicable N values up to N=n i.e. N=5,10,15...n
    N_set = range(5, n + 5, 5)
    print(f"\n {N_set}")

    # Create a list to hold the final travel_time matrices for N=5,10,15,... up to the function argument n 
    # (which should be 75 at max i.e. 16 matrices in total)
    travel_time_matrices_list = []

    for i in N_set:
        print(f"\nCurrent N: {i}")
        # Enumerate num of variants from 1 to (i)(ln(i)) where i is a member of N=5,10,15,...
        variants = range(1, math.ceil(i * math.log(i)))
        print(f"\t {variants}")

        # Initialize an empty matrix with shape (i,i)
        ith_travel_time_matrix = np.zeros((i + 1, i + 1))

        # Enumerate (i)(ln(i)) and get their average
        for variant_num in variants:
            # Generate a variant
            current_variant = (np.round((valid_travel_time_range[1] - valid_travel_time_range[0]
            
                                         ) * np.random.rand(i + 1, i + 1) + valid_travel_time_range[0]))
            print("\n")
            print(current_variant)
            
            # Add it elementwise to accumulator matrix
            ith_travel_time_matrix = ith_travel_time_matrix + current_variant

        print(variant_num)

        # divide by the i(ln(i)) to get element-wise average matrix
        ith_travel_time_matrix = np.round(ith_travel_time_matrix/variant_num)

        # change the diagonal values (i,i) to zero
        for x in range(0, ith_travel_time_matrix.shape[0]):
            ith_travel_time_matrix[x][x] = 0

            for y in range(0, ith_travel_time_matrix.shape[1] ):
                ith_travel_time_matrix[x][y] = ith_travel_time_matrix[y][x]
        print(ith_travel_time_matrix)

        # Append averaged travel_time matrix to list of travel_time matricess
        travel_time_matrices_list.append(ith_travel_time_matrix)

    # Print all of the calculated matrices
    for i in range(len(N_set)):
        print(
            f"\n\n THIS IS THE FIRST TRAVEL_TIME MATRIX FOR N = {N_set[i]} \n {travel_time_matrices_list[i]}")


if __name__ == "__main__":
    n = int(sys.argv[1])
    # print (n)
    generate_data(n)
