## Eight Tile Puzzle solved with
#   1) Uniform Cost Search
#   2) A* with Misplaced Tile heuristic
#   3) A* with with Manhattan Distance heuristic
 
 
from copy import deepcopy
import time
import matplotlib.pyplot as plt # plot Runtime(s) v. Depth of Solution
 
def search(matrix_ini, search_choice):
    # 2nd param is cost to get to node, 3rd is heuristic min. cost to goal
    nodes = [(matrix_ini, 0, 0)]
    repeated_states = []
    nodes_expanded = 0
    max_queue_size = -1
    while True:
        if not nodes:
            return None
        if len(nodes) > max_queue_size:
            max_queue_size = len(nodes)
        node = choose_remove(nodes)
        nodes.remove(node) # remove node from list
        if goal_check(node):
            print("\nGoal State has been reached!\n")
            print("Depth of the Solution is",node[1])
            print("The number of nodes expanded is",nodes_expanded)
            print("The queue size was at",max_queue_size,"nodes at its maximum\n\n")
            return node
        if search_choice == 1:
            nodes = uniform(nodes, nodes_expand(node,repeated_states))
        elif search_choice == 2:
            nodes = misplaced_tile(nodes, nodes_expand(node,repeated_states))
        elif search_choice == 3:
            nodes = manhattan_dist(nodes, nodes_expand(node,repeated_states))
        nodes_expanded += 1
 
def choose_remove(nodes):
    # return node with lowest g(n) + h(n)
    low_node = nodes[0]
    for n in nodes:
        if n[1] + n[2] < low_node[1] + low_node[2]:
            low_node = n
    print("The state with the lowest g(n) + h(n) is: ")
    print(low_node[0])
    print("with g(n) = ",low_node[1]," and h(n) = ",low_node[2],"\n")
    return low_node
 
def goal_check(node):
    return [1,2,3,4,5,6,7,8,0] == node[0]  
 
## Check where the 0 is,
#  and swap in all possible valid locations
def nodes_expand(node,repeated_states):
    expanded = []
    idx = node[0].index(0) # index of blank
    mods = [-3, 3, -1, 1]
    if idx % 3 == 0: # left most can't move the left
        mods.remove(-1)
    elif idx % 3 == 2: # right most can't move the right
        mods.remove(1)
    if idx <= 2: # top row can't move up
        mods.remove(-3)
    elif idx >= 6: # bot row can't move down
        mods.remove(3)
 
    repeated_states.append(node[0])
    for mod in mods:
        mod_idx = idx + mod
        tNde = deepcopy(node)
        tNde[0][idx],tNde[0][mod_idx] = tNde[0][mod_idx],tNde[0][idx]
        nTNde = (tNde[0], tNde[1]+1, tNde[2]) # increase path cost
        if nTNde[0] not in repeated_states:
            expanded.append(nTNde)
            repeated_states.append(nTNde[0])
    return expanded
 
def uniform(nodes, expanded):
    return nodes + expanded
 
def misplaced_tile(nodes, expanded):
    for i in range(len(expanded)):
        n = expanded[i]
        tempN = (n[0], n[1], calc_misplaced(n[0])) # calc heur
        expanded[i] = tempN
    nodes = expanded + nodes
    return nodes
 
def calc_misplaced(node):
    heur = 0
    goal = [1,2,3,4,5,6,7,8,0]
    for i in range(0, len(node)):
        if node[i] != goal[i] and node[i] != 0:
            heur += 1
    return heur
 
def manhattan_dist(nodes, expanded):
    for i in range(len(expanded)):
        n = expanded[i]
        tempN = (n[0], n[1], calc_manhattan(n[0])) # calc heur
        expanded[i] = tempN
    nodes = expanded + nodes
    return nodes
 
def calc_manhattan(node):
    heur = 0
    goal = [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2)]
    for i in range(0, len(node)):
        if node[i] != 0:
            idx_src = goal[i]
            idx_dest = goal[node[i]-1]
            heur += abs(idx_dest[0] - idx_src[0]) + abs(idx_dest[1] - idx_src[1])
    return heur
 
choice = int(input("Enter \"0\" for user determined puzzle, \"1\" for predetermined puzzle -> "))
if choice == 0:
    # Get user to input tiles in the puzzle
    frst_row = [int(n) for n in input("Enter first row -> ").split()]
    scnd_row = [int(n) for n in input("Enter second row -> ").split()]
    thrd_row = [int(n) for n in input("Enter third row -> ").split()]
 
    matrix_ini = frst_row + scnd_row + thrd_row
    print(matrix_ini)
 
    search_choice = int(input("Enter search algorithm: \"1\" for Uniform Cost Search, \"2\" for A* with Misplaced Tile heuristic, \"3\" for A* with Manhattan Distance heuristic -> "))
    start = time.time()
    solved = search(matrix_ini, search_choice)
    print(solved)
    tot_time = time.time() - start
    print("This search finished in",tot_time,"seconds\n")
 
else: # predetermined puzzle
    all_puzzles = [ [1,2,3,5,0,6,4,7,8], [1,3,6,5,0,2,4,7,8], [1,3,6,5,0,7,4,8,2] , [1,6,7,5,0,3,4,8,2] , [7,1,2,4,8,5,6,3,0], [0,7,2,4,6,1,3,5,8]]
    depthList = [4, 8, 12, 16, 20, 24] # depths of above puzzles
    max_uni_depth = 16 # uniform takes too long otherwise
    max_tile_depth = 20
 
    uni_times = [] # store times
    tile_times = []
    manhat_times = []
    for i in range(len(depthList)):
        matrix_ini = all_puzzles[i]
        print("\nInitial Puzzle is: ",matrix_ini,"\n")
       
        if depthList[i] <= max_uni_depth:
            start = time.time()
            print("Running Uniform Cost Search...\n")
            solved = search(matrix_ini, 1)
            print(solved)
            tot_time = time.time() - start
            uni_times.append(tot_time)
            print("Uniform Cost Search finished in ",tot_time,"seconds\n")
            print("-"*75)
 
        if depthList[i] <= max_tile_depth:
            start = time.time()
            print("Running A* with Misplaced Tile heuristic...\n")
            solved = search(matrix_ini, 2)
            print(solved)
            tot_time = time.time() - start
            tile_times.append(tot_time)
            print("A* with Misplaced Tile heuristic finished in ",tot_time,"seconds\n")
            print("-"*75)
 
        start = time.time()
        print("Running A* with Manhattan Distance heuristic...\n")
        solved = search(matrix_ini, 3)
        print(solved)
        tot_time = time.time() - start
        manhat_times.append(tot_time)
        print("A* with Manhattan Distance heuristic finished in ",tot_time,"seconds\n")
        print("-"*75)
 
    # Scatters for each Search
    plt.scatter(depthList[:depthList.index(max_uni_depth)+1], uni_times, marker="*",color="black", label="Uniform Cost Search")
    plt.xlabel('Depth of Puzzle Solution')
    plt.ylabel('Runtime (seconds)')
    plt.legend(loc = "upper left")
    plt.title('Runtime (seconds) vs. Depth of Solution of Eight Tile Puzzle')
    plt.show()
 
    plt.scatter(depthList[:depthList.index(max_tile_depth)+1], tile_times, marker="o",color="red",label="A* with Misplaced Tile Heuristic")
    plt.xlabel('Depth of Puzzle Solution')
    plt.ylabel('Runtime (seconds)')
    plt.legend(loc = "upper left")
    plt.title('Runtime (seconds) vs. Depth of Solution of Eight Tile Puzzle')
    plt.show()
 
    plt.scatter(depthList, manhat_times, marker="s",color="purple",label="A* with Manhattan Distance Heuristic")
    plt.xlabel('Depth of Puzzle Solution')
    plt.ylabel('Runtime (seconds)')
    plt.legend(loc = "upper left")
    plt.title('Runtime (seconds) vs. Depth of Solution of Eight Tile Puzzle')
    plt.show()
