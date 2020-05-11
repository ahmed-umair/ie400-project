# IE-400 Project data-generator
import numpy as np
import pandas as pd
import sys
import pprint
import math
import time
import os
import func_timeout
from docplex.mp.model import Model
from docplex.util.environment import get_environment

# Since the numpy function used to generate the random matrices returns values in the range [a,b),
# we specify the our ranges as [a,b+1) to make them [a,b]
valid_hw_time_range = (300, 500)
valid_travel_time_range = (100, 300)



def generate_data(n: int):
    # Generate one-time (1,75) matrix for student times
    # np.random.rand generates 75 numbers with values in [0,1)
    # [300, 500]
    # [0,1) + 300 = [300, 301)
    # ([0,1) * 201) --> 0 to 199.99 + 300 = 300 to 500

    student_times_Xi = (valid_hw_time_range[1] - valid_hw_time_range[0]
                        ) * np.random.rand(1, 76) + valid_hw_time_range[0]

    student_times_Xi = np.round(student_times_Xi)
    student_times_Xi[0][0] = 0
    print(student_times_Xi)

    # Enumerate the applicable N values up to N=n i.e. N=5,10,15...n
    N_set = range(5, n + 5, 5)
    # print(f"\n {N_set}")

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
            # print("\n")
            # print(current_variant)

            # Add it elementwise to accumulator matrix
            ith_travel_time_matrix = ith_travel_time_matrix + current_variant

        print(variant_num)

        # divide by the i(ln(i)) to get element-wise average matrix
        ith_travel_time_matrix = np.round(ith_travel_time_matrix/variant_num)

        # change the diagonal values (i,i) to zero
        for x in range(0, ith_travel_time_matrix.shape[0]):
            ith_travel_time_matrix[x][x] = 0

            for y in range(0, ith_travel_time_matrix.shape[1]):
                ith_travel_time_matrix[x][y] = ith_travel_time_matrix[y][x]
        # print(ith_travel_time_matrix)

        # Append averaged travel_time matrix to list of travel_time matricess
        travel_time_matrices_list.append(ith_travel_time_matrix)

    for i in travel_time_matrices_list:
        tt_df = pd.DataFrame(i)
        tt_df.to_excel(os.path.join(os.getcwd(), 'generated_data', f'travel_times_{travel_time_matrices_list.index(i)}.xls'), index=True)
    st_df = pd.DataFrame(student_times_Xi)
    st_df.to_excel(os.path.join(os.getcwd(), 'generated_data', 'student_times.xls'), index=True)

    return student_times_Xi, travel_time_matrices_list


def solve_problem(student_times, num_of_nodes):
    start_time = time.time()
    # num_of_nodes = len(student_times[0])
    mdl = Model(name="traveling-salesman")
    student_nums_list = []
    for i in range(0, num_of_nodes):
        student_nums_list.append(i)
        # [0, 1, 2 ,3 .. 5]

    # Variable declarations
    mdl.u_vars = mdl.integer_var_list(keys=student_nums_list, name="U")

    mdl.order_vars = mdl.binary_var_matrix(
        keys1=student_nums_list, keys2=student_nums_list, name="Y")
    # Yij = Y_0_0 to Y 5_5

    mdl.add_constraints((mdl.sum(mdl.order_vars[student_i, student_j] for student_j in student_nums_list)
                         == 1, 'ct_single_departure_student_%d' % student_i) for student_i in student_nums_list)
    # sum(Yij for fixed i = 1)
    mdl.add_constraints((mdl.sum(mdl.order_vars[student_i, student_j] for student_i in student_nums_list)
                         == 1, 'ct_single_arrival_student_%d' % student_j) for student_j in student_nums_list)
    # sum(Yij for fixed j = 1)
    mdl.add_constraints((mdl.sum(mdl.order_vars[student_i, student_j]) == 0, 'ct_cannot_come_back_to_same_student_%d' % student_i)
                        for student_j in student_nums_list for student_i in student_nums_list if student_i == student_j)
    # (Yii = 0)

    # Subtour elimination
    # Ui - Uj + n * Yij <= n - 1 where i >=1 and j >= 1
    mdl.add_constraints((mdl.u_vars[student_i] - mdl.u_vars[student_j] + num_of_nodes * mdl.order_vars[student_i, student_j] <= num_of_nodes-1)
                        for student_i in student_nums_list for student_j in student_nums_list if student_i != student_j and student_i >= 1 and student_j >= 1)

    mdl.add_constraints((mdl.u_vars[student_i] >= 0)
                        for student_i in student_nums_list if student_i >= 1)

    mdl.add_constraints((mdl.u_vars[student_i] <= (num_of_nodes-1))
                        for student_i in student_nums_list if student_i >= 1)

    # print(student_nums_list)
    # print(student_times[0])
    # print(tt_args)

    mdl.minimize(mdl.sum(mdl.order_vars[student_i, student_j] * (tt_args[student_i][student_j]) 
                         for student_j in student_nums_list for student_i in student_nums_list)+ mdl.sum(student_times[0][i] for i in student_nums_list))
    #  + mdl.sum(student_times[0][i] for i in range(0, n - 1)))

    # print("### VARIABLES ###")
    # for variable in mdl.iter_variables():
    #     print(variable)
    # print("\n")

    # print("### CONSTRAINTS ###")
    # for constraint in mdl.iter_constraints():
    #     print(constraint)
    # print("\n")

    # print("### OBJECTIVE FUNCTION ###")
    # print(mdl.get_objective_expr())
    # print("\n")

    travel_vals = (travel_times[student_i][student_j]
                   for student_j in student_nums_list for student_i in student_nums_list)

    mdl.solve()

    print("### TRAVEL TIMES MATRIX ###")
    print(tt_args)
    print("\n")

    print("### IP SOLUTION ###")
    print("--- %s seconds ---" % (time.time() - start_time))
    mdl.print_solution()


def dp_recursive(source, unvisited_set):
    
    start_time = time.time()
    # print("\n\n #### NEW CALL ####")
    # print(f"Unvisited Set: {unvisited_set}")
    # print(f"Source Node: {source}")
    
    if len(unvisited_set) == 0:
        return (tt_args[source][0], "[" + str(source) + "]" + "<-->[0]")

    return_values = []

    for i in range(len(unvisited_set)):
        new_source = unvisited_set[i]
        new_unvisited_set = unvisited_set[:]
        new_unvisited_set.remove(unvisited_set[i])
        # print(f"\t -----------------------------------")
        # print(f"\t Candidate Unvisited Set: {new_unvisited_set}")
        # print(f"\t Candidate Dest Node: {new_source}")

        return_values.append(dp_recursive(new_source, new_unvisited_set))

    comparison_list = [tt_args[source][unvisited_set[i]] + return_values[i][0] for i in range(len(unvisited_set))]
    # print(f"Comparison list is: {comparison_list}")

    min_path_val = min(comparison_list)
    min_dist_index = comparison_list.index(min_path_val)
    # min_dist_node = return_values[min_dist_index][1]
    min_dist_complete_path = return_values[min_dist_index][1]

    # return (tt_args[source][min_dist_node] + min_path_val, f"{min_dist_node}-->" + min_dist_complete_path)
    # tabs = ""
    # for i in range(6 - len(unvisited_set)):
    #     tabs = tabs + "\t"
    # print (tabs, min_path_val, f"{source}-->" + min_dist_complete_path)

    
    return (min_path_val, f"[{source}]<-->" + min_dist_complete_path)

@func_timeout.func_set_timeout(30)
def dp_wrapper(num_of_nodes):
    start_time = time.time()
    unvisited_nodes_set = []

    for i in range(0, num_of_nodes + 1):
        if i != 0:
            unvisited_nodes_set.append(i)
    
    travel_result = dp_recursive(0, unvisited_nodes_set)

    homework_sum = 0

    for i in range(0, num_of_nodes + 1):
        homework_sum = homework_sum + student_times[0][i]

    print("\n")
    print("### DP SOLUTION ###")
    print("--- %s seconds ---" % (time.time() - start_time))
    return (homework_sum + travel_result[0], travel_result[1])



if __name__ == "__main__":
    n = int(sys.argv[1])
    student_times, travel_times = generate_data(n)
    
    
    for i in range(0, n//5):
        tt_args = travel_times[i]
        print(f"N = {(i+1)*(5)}")
        solve_problem(student_times, (i+1)*(5) + 1)

    for i in range(0, n//5):
        tt_args = travel_times[i]
        print(f"N = {(i+1)*(5)}")
        
        print(dp_wrapper((i+1)*(5)))
#         solve_problem(student_times, (i+1)*(5) + 1)

