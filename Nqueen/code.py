from random import randrange
from random import choice
from copy import deepcopy


# Class to create the state of queen and check all the possible moves depending on the no. of queens attacking
class Q_State:

    instCount= 0
    def __init__(self, q_pos=None, parent=None,f_cost=0,):

        self.s_len = int(n)

        if q_pos == None:
            self.q_num = self.s_len
            self.q_pos = frozenset(self.rand_position())
        else:
            self.q_pos = frozenset(q_pos)
            self.q_num = len(self.q_pos)

        self.path_cost = 0
        self.f_cost = f_cost
        self.parent = parent
        self.id = Q_State.instCount

        Q_State.instCount+= 1

    # randomly generate queen positions
    def rand_position(self):
        ''' Each queen is in a random row in separate columns '''
        valid_columns = list(range(self.s_len))
        q_pos = [(valid_columns.pop(randrange(len(valid_columns))), randrange(self.s_len)) for _ in range(self.q_num)]
        return q_pos

    # function to get the possible children from current node
    def possible_children(self):
        children = []
        parent_q_pos = list(self.q_pos)
        for  q_index, queen in enumerate(parent_q_pos):
            positions = [(queen[0], row) for row in range(self.s_len) if row != queen[1]]
            for new_pos in positions:
                q_pos = deepcopy(parent_q_pos)
                q_pos[q_index] = new_pos
                children.append(Q_State(q_pos))
        return children

    # Identifying attacking queens
    def q_attacks(self):

        def range_in(x, y):
            if x > y:
                return range(x-1, y, -1)
            elif x < y:
                return range(x+1, y)
            else:
                return [x]

        def repeat(x, y):
            if len(x) == 1:
                x = x*len(y)
            elif len(y) == 1:
                y = y*len(x)
            return zip(x, y)

        def points(x, y):
            return repeat(list(range_in(x[0], y[0])), list(range_in(x[1], y[1])))

        def ifattacking(queens, x, y):
            if (x[0] == y[0]) or (x[1] == y[1]) or (abs(x[0]-y[0]) == abs(x[1] - y[1])):
                for between in points(x, y):
                    if between in queens:
                        return False
                return True
            else:
                return False

        att_pairs = []
        q_pos = list(self.q_pos)
        check_remaining = deepcopy(q_pos)
        while check_remaining:
            x = check_remaining.pop()
            for y in check_remaining:
                if ifattacking(q_pos, x, y):
                    att_pairs.append([x, y])

        return att_pairs

    def num_q_attacks(self):
        return len(self.q_attacks())

    def __str__(self):
        return '\n'.join([' '.join(['0' if (col, row) not in self.q_pos else 'Q' for col in range(
            self.s_len)]) for row in range(self.s_len)])

    def __hash__(self):
        return hash(self.q_pos)

    def __eq__(self, other):
        return self.q_pos == other.q_pos

    def __lt__(self, other):
        return self.f_cost < other.f_cost or (self.f_cost == other.f_cost and self.id > other.id)

print("Select the algorithm that you want to execute :\n 1. Steepest Ascent(without sidemoves) \n 2. Hill Climbing with Sideway Moves\n 3. Random Restart")
x=input()#Input from User
def steepest_without_sidemoves(state_of_queen,count,allow_sidemoves=False, max_sidemoves=100):
    # This function will be called when Steepest Ascent(without sidemoves) is chosen
    node = state_of_queen
    p = [] #path
    s_moves = 0 #count to record number of side moves 
    while True:
        p.append(node)
        children = node.possible_children()
        num_attacks_children = [child.num_q_attacks() for child in children]
        min_attacks = min(num_attacks_children)
        # The algorithm will go into infinite loop if best child is not chosen randomly with least number of attacks
        best_choice_child = choice([child for child_index, child in enumerate(children) if num_attacks_children[child_index] == min_attacks])
	# 'for' loop to check best heuristic by checking attackingmoves of current child
        if (best_choice_child.num_q_attacks() > node.num_q_attacks()):#break if better heuristic exists
            break
        elif best_choice_child.num_q_attacks() == node.num_q_attacks():
            if not allow_sidemoves or s_moves == max_sidemoves:#checking if limit for max allowed moves is reached
                break
            else:
                s_moves += 1
        else:
            s_moves = 0
        node = best_choice_child
        if count <4:
            print('Search Sequence :',count,'\n', best_choice_child, '\n')# Print first three sequences found while finding the solution
    return {'outcome': 'success' if node.num_q_attacks()==0 else 'failure',
            'solution': p}

def steepest_with_sidemoves(state_of_queen,count,allow_sidemoves=True, max_sidemoves=100):
    # This function will be called when Steepest Ascent with sidemoves is chosen
    node = state_of_queen
    p = []
    s_moves = 0
    while True:
        p.append(node)
        children = node.possible_children()
        num_attacks_children = [child.num_q_attacks() for child in children]
        min_attacks = min(num_attacks_children)
        # The algorithm will go into infinite loop if best child is not chosen randomly with least number of attacks
        best_choice_child = choice([child for child_index, child in enumerate(children) if num_attacks_children[
            child_index] == min_attacks])
        if (best_choice_child.num_q_attacks() > node.num_q_attacks()):
            break
        elif best_choice_child.num_q_attacks() == node.num_q_attacks():
            if not allow_sidemoves or s_moves == max_sidemoves:
                break
            else:
                s_moves += 1
        else:
            s_moves = 0
        node = best_choice_child
        if count <4:
            print('Search Sequence :', count, '\n', best_choice_child, '\n')
            #printing best child
    return {'outcome': 'success' if node.num_q_attacks()==0 else 'failure',
            'solution': p}

def steepest_ascent(state_of_queen,allow_sidemoves, max_sidemoves=100):
    node = state_of_queen
    p = []
    s_moves = 0
    while True:
        p.append(node)
        children = node.possible_children()
        num_attacks_children = [child.num_q_attacks() for child in children]
        min_attacks = min(num_attacks_children)
        # The algorithm will be stuck between two non-random best children if best child is not chosen randomly with 
        # least number of attacks when sidemoves is allowed
        best_choice_child = choice([child for child_index, child in enumerate(children) if num_attacks_children[
            child_index] == min_attacks])
        if (best_choice_child.num_q_attacks() > node.num_q_attacks()):
            break
        elif best_choice_child.num_q_attacks() == node.num_q_attacks():
            if not allow_sidemoves or s_moves == max_sidemoves:
                break
            else:
                s_moves += 1
        else:
            s_moves = 0
        node = best_choice_child
    return {'outcome': 'success' if node.num_q_attacks()==0 else 'failure',
            'solution': p}

def random_restart(random_generator,allow_sidemoves,num_restart=100, max_sidemoves=100):
    global total
    p = [] 
    for _ in range(num_restart):
        # Perform the steepest ascent algorithm with or without sidemoves n times.
        result = steepest_ascent(random_generator(),allow_sidemoves=allow_sidemoves,
                                        max_sidemoves=max_sidemoves)
        p += result['solution']
        num_restart -= 1
        temp =0
        if result['outcome'] == 'success':
            temp = 100-num_restart #calculating num of restarts for each iteration
            break
    result['solution'] = p
    array.append(temp)#Appending each restart in array
    total = 0
    for i in array:
        total += i # total restarts
    return result

class QueensProblem:
    global n,iterations 
    print("Enter the number of queens")
    n = input()#n is no. of queens to be taken in the board
    print("Enter the number of interations")
    iterations = input()#num of iterations that the user needs, to be taken
    iterations = int(iterations)
    def __init__(self, start_state=Q_State()):
        self.start_state = start_state

def status(search_func,count=1, n_iterations =iterations):
    results = []
    for iter in range(n_iterations):
        result = search_func(Q_State(),count)#create function and call any of the three methods
        count += 1
        result['p_length'] = len(result['solution'])-1#Storing path length of an iteration in the result array
        results.append(result)
    arr = [[result for result in results if result['outcome'] == 'success'], #array arr holds all SUCCESS's and FAILURE's
           [result for result in results if result['outcome'] == 'failure']]
    success = []
    failure = []

    for i in arr[0]:
        success.append(i['p_length'])#0 index is corresponding to Success hence append all success's
    for i in arr[1]:
        failure.append(i['p_length'])#1 index is corresponding to Failurehence add all failure's 
    if len(success) != 0: #print average for success
        print('Average steps when success: ', int(round(sum(success) / float(len(success)))))
    if len(failure) != 0: # Print average for failure
        print('Average steps when failure: ', int(round(sum(failure) / float(len(failure)))))

    results = [results,
               [result for result in results if result['outcome'] == 'success'],
               [result for result in results if result['outcome'] == 'failure']]
    title_column= 30
    data_column = 15

    def print_row_data(row_title, rdata_string, rdata_func, results):
        #Printing in matrix form
        nonlocal title_column, data_column
        row = (row_title + '\t').rjust(title_column)
        for result_group in results:
            row += rdata_string.format(**rdata_func(result_group)).ljust(data_column)
        print(row)

    print('\t'.rjust(title_column) +
          'All Problems'.ljust(data_column) +
          'Successes'.ljust(data_column) +
          'Failures'.ljust(data_column))
    print_row_data('Number of Problems:',
                   '{count:.0f} ({percent:.1%})',
                   lambda x: {'count':len(x), 'percent': len(x)/n_iterations },
                   results)

section_break = '\n' + '_'*100 + '\n'

def rand_stats(search_func, n_iterations =iterations):
    global array
    array = []
    results = []
    for iter in range(n_iterations ):
        result = search_func(Q_State())#Creating an object of QueenState and call steepest_ascent or steepest_without_sidemoves
        result['p_length'] = len(result['solution'])-1#Storing the path length of each iteration in result
        results.append(result)
    arr = [[result for result in results if result['outcome'] == 'success'],#array arr will have all the result of SUCCESS and FAILURE
           [result for result in results if result['outcome'] == 'failure']]
    success = []
    failure = []

    for i in arr[0]:
        success.append(i['p_length'])#0 index is corresponding to Success hence append all success's
    for i in arr[1]:
        failure.append(i['p_length'])#1 index is corresponding to Failure hence add all failure's
    if len(success) != 0: # Print average for success
        print('Average steps when success: ', int(round(sum(success) / float(len(success)))))
    if len(failure) != 0:# Print average for failure
        print('Average steps when failure: ', int(round(sum(failure) / float(len(failure)))))

    print(' '*50 + '\r', end='', flush=True)

    results = [results,
               [result for result in results if result['outcome'] == 'success'],
               [result for result in results if result['outcome'] == 'failure']]
    #print(results[0])
    title_column= 30
    data_column = 15

    def print_row_data(row_title, rdata_string, rdata_func, results):
        nonlocal title_column, data_column
        row = (row_title + '\t').rjust(title_column)
        for result_group in results:
            row += rdata_string.format(**rdata_func(result_group)).ljust(data_column)
        print(row)

    print('Avg Restarts Required: ', int((total / n_iterations )))
    print('\t'.rjust(title_column) +
          'All Problems'.ljust(data_column) +
          'Successes'.ljust(data_column) +
          'Failures'.ljust(data_column))

    print_row_data('Number of Problems:',
                   '{count:.0f} ({percent:.1%})',
                   lambda x: {'count':len(x), 'percent': len(x)/n_iterations },
                   results)

if x=='1':
    print('**********************Steepest ascent hill climb(without sidemoves)********************:\n')
    status(steepest_without_sidemoves)
    print(section_break)
elif x=='2':
    print('*********************Hill Climbing with Sidemoves*********************:\n')
    status(steepest_with_sidemoves)
    print(section_break)
else:
    print("******************* Random Restart without Sidemoves ******************")
    print('random_restart:\n')
    rand_stats(lambda x: random_restart(Q_State, allow_sidemoves=False))
    print(section_break)
    print("******************* Random Restart with Sidemoves ******************")
    print('random_restart:\n')
    rand_stats(lambda x: random_restart(Q_State, allow_sidemoves=True))
    print(section_break)