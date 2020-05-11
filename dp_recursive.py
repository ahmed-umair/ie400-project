def dp_recursive(source, unvisited_set):
    
    # print("\n\n #### NEW CALL ####")
    # print(f"Unvisited Set: {unvisited_set}")
    # print(f"Source Node: {source}")
    
    if len(unvisited_set) == 0:
        return (travel_times[0][source][0], str(source) + "-->0")

    return_values = []

    for i in range(len(unvisited_set)):
        new_source = unvisited_set[i]
        new_unvisited_set = unvisited_set[:]
        new_unvisited_set.remove(unvisited_set[i])
        # print(f"\t -----------------------------------")
        # print(f"\t Candidate Unvisited Set: {new_unvisited_set}")
        # print(f"\t Candidate Dest Node: {new_source}")

        return_values.append(dp_recursive(new_source, new_unvisited_set))

    comparison_list = [travel_times[0][source][unvisited_set[i]] + return_values[i][0] for i in range(len(unvisited_set))]
    # print(f"Comparison list is: {comparison_list}")

    min_path_val = min(comparison_list)
    min_dist_index = comparison_list.index(min_path_val)
    # min_dist_node = return_values[min_dist_index][1]
    min_dist_complete_path = return_values[min_dist_index][1]

    # return (travel_times[0][source][min_dist_node] + min_path_val, f"{min_dist_node}-->" + min_dist_complete_path)
    tabs = ""
    for i in range(6 - len(unvisited_set)):
        tabs = tabs + "\t"
    # print (tabs, min_path_val, f"{source}-->" + min_dist_complete_path)

    return (min_path_val, f"{source}-->" + min_dist_complete_path)