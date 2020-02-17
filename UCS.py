''' starter-file-for.py  CHANGE THIS WHEN YOU EDIT IT, TO UCS.py
by Wayne Wang
UWNetID: wyf9686
Student number: 1664873
Date: Oct 11, 2019

Assignment 2, in CSE 415, Autumn 2019.

STUDENTS: COMPLETE THE IMPLEMENTATION OF UCS.py BY WRITING CODE WHERE
INDICATED BELOW IN THE COMMENTS STARTING WITH "***STUDENTS".


This file Includes a priority queue implementation by
 S. Tanimoto, Univ. of Washington.
Paul G. Allen School of Computer Science and Engineering

Intended USAGE:
 python3 UCS.py FranceWithCosts


'''

VERBOSE = True  # Set to True to see progress; but it slows the search.

import sys

if sys.argv == [''] or len(sys.argv) < 2:
    try:
        import FranceWithCosts as Problem
    except:
        print("Note that the EightPuzzle formulation will be used in Assignment 3, not Assignment 2")
        print("Try python3 UCS.py FranceWithCosts")

else:
    import importlib

    Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to UCS, by Wayne Wang!")

COUNT = None  # Number of nodes expanded.
MAX_OPEN_LENGTH = None  # How long OPEN ever gets.
SOLUTION_PATH = []  # List of states from initial to goal, along lowest-cost path.
TOTAL_COST = None  # Sum of edge costs along the lowest-cost path.
BACKLINKS = {}  # Predecessor links, used to recover the path.

# The value g(s) represents the cost along the best path found so far
# from the initial state to state s.
g = {}  # We will use a global hash table to associate g values with states.


class My_Priority_Queue:
    def __init__(self):
        self.q = []  # Actual data goes in a list.

    def __contains__(self, elt):
        '''If there is a (state, priority) pair on the list
        where state==elt, then return True.'''
        # print("In My_Priority_Queue.__contains__: elt= ", str(elt))
        for pair in self.q:
            if pair[0] == elt:
                return True
        return False

    def delete_min(self):
        ''' Standard priority-queue dequeuing method.'''
        if self.q == []: return []  # Simpler than raising an exception.
        temp_min_pair = self.q[0]
        temp_min_value = temp_min_pair[1]
        temp_min_position = 0
        for j in range(1, len(self.q)):
            if self.q[j][1] < temp_min_value:
                temp_min_pair = self.q[j]
                temp_min_value = temp_min_pair[1]
                temp_min_position = j
        del self.q[temp_min_position]
        return temp_min_pair

    def insert(self, state, priority):
        '''We do not keep the list sorted, in this implementation.'''
        # print("calling insert with state, priority: ", state, priority)

        if self[state] != -1:
            print("Error: You're trying to insert an element into a My_Priority_Queue instance,")
            print(" but there is already such an element in the queue.")
            return
        self.q.append((state, priority))

    def __len__(self):
        '''We define length of the priority queue to be the
        length of its list.'''
        return len(self.q)

    def __getitem__(self, state):
        '''This method enables Pythons right-bracket syntax.
        Here, something like  priority_val = my_queue[state]
        becomes possible. Note that the syntax is actually used
        in the insert method above:  self[state] != -1  '''
        for (S, P) in self.q:
            if S == state: return P
        return -1  # This value means not found.

    def __delitem__(self, state):
        '''This method enables Python's del operator to delete
        items from the queue.'''
        # print("In MyPriorityQueue.__delitem__: state is: ", str(state))
        for count, (S, P) in enumerate(self.q):
            if S == state:
                del self.q[count]
                return

    def __str__(self):
        txt = "My_Priority_Queue: ["
        for (s, p) in self.q: txt += '(' + str(s) + ',' + str(p) + ') '
        txt += ']'
        return txt

def runUCS():
    '''This is an encapsulation of some setup before running
    UCS, plus running it and then printing some stats.'''
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH, SOLUTION_PATH
    COUNT = 0
    BACKLINKS = {}
    MAX_OPEN_LENGTH = 0
    SOLUTION_PATH = UCS(initial_state)
    print(str(COUNT) + " states expanded.")
    print('MAX_OPEN_LENGTH = ' + str(MAX_OPEN_LENGTH))

def UCS(initial_state):
    '''Uniform Cost Search. This is the actual algorithm.'''
    global g, COUNT, BACKLINKS, MAX_OPEN_LENGTH, CLOSED, TOTAL_COST
    CLOSED = []
    BACKLINKS[initial_state] = None
    TOTAL_COST = 0
    # The "Step" comments below help relate UCS's implementation to
    # those of Depth-First Search and Breadth-First Search.

    # STEP 1a. Put the start state on a priority queue called OPEN
    OPEN = My_Priority_Queue()
    OPEN.insert(initial_state, 0)
    # STEP 1b. Assign g=0 to the start state.
    g[initial_state] = 0.0

    # STEP 2. If OPEN is empty, output “DONE” and stop.
    while (len(OPEN) != 0):  # ***STUDENTS CHANGE THIS CONDITION***
        # LEAVE THE FOLLOWING CODE IN PLACE TO INSTRUMENT AND/OR DEBUG YOUR IMPLEMENTATION
        if VERBOSE: report(OPEN, CLOSED, COUNT)
        if len(OPEN) > MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

        # STEP 3. Select the state on OPEN having lowest priority value and call it S.
        #         Delete S from OPEN.
        #         Put S on CLOSED.
        #         If S is a goal state, output its description
        (S, P) = OPEN.delete_min()
        # print("In Step 3, returned from OPEN.delete_min with results (S,P)= ", (str(S), P))
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
            pass  # ***STUDENTS CHANGE THE BODY OF THIS IF.***
            # HANDLE THE BACKTRACING, RECORDING THE SOLUTION AND TOTAL COST,
            # AND RETURN THE SOLUTION PATH, TOO.
            TOTAL_COST = P
            return (backtrace(S))
        COUNT += 1

    # STEP 4. Generate each successor of S
    #         and if it is already on CLOSED, delete the new instance.
        cost = P
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                cost_update = cost + S.edge_distance(new_state)
                if new_state in OPEN:
                    past_cost = OPEN[new_state]
                    if cost_update < past_cost:
                        del OPEN[new_state]
                        OPEN.insert(new_state, cost_update)
                        BACKLINKS[new_state] = S
                        del new_state
                    else:
                        del new_state
                elif new_state in CLOSED:
                    del new_state
                else:
                    OPEN.insert(new_state, cost_update)
                    BACKLINKS[new_state] = S

    # STEP 6. Go to Step 2.
    return None  # No more states on OPEN, and no goal reached.


def print_state_queue(name, q):
    print(name + " is now: ", end='')
    print(str(q))

def backtrace(S):
    global BACKLINKS
    path = []
    while S:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print ("Solution path: ")
    print("[ ", end="")
    print(*path, sep=", ", end="")
    print(" ]")
    print ("Total Cost: " + str(float(TOTAL_COST)))
    return path

def report(open, closed, count):
    print("len(OPEN)=" + str(len(open)), end='; ')
    print("len(CLOSED)=" + str(len(closed)), end='; ')
    print("COUNT = " + str(count))


if __name__ == '__main__':
    runUCS()

