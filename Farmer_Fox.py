'''Farmer_Fox.py
by Wayne Wang
Date: Oct 11, 2019

Assignment 2, in CSE 415, Autumn 2019.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

'''Farmer_Fox.py
("Farmer, fox, Chicken and Grain" problem)
'''
# <METADATA>
SOLUZION_VERSION = "2.0"
PROBLEM_NAME = "The Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "2.0"
PROBLEM_AUTHORS = ['Wayne Wang']
PROBLEM_CREATION_DATE = "09-SEPT-2019"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC = \
    ''' A Farmer has to get his fox, chicken, and grain across the river. 
     The boat can hold only the Farmer and one item. 
     The fox cannot be left alone with the chicken.
     The chicken cannot be left alone with the grain.
'''
# </METADATA>

# <COMMON_DATA>
# </COMMON_DATA>

# <COMMON_CODE>
FA = 0  # array index to access whether Farmer is on left bank or right bank
FO = 1  # same idea for Fox
C = 2  # same idea for Chicken
G = 3  # same idea for Grain
LEFT = 0  # If on the left bank, then it is indicated by 0
RIGHT = 1  # If on the right bank, then it is indicated by 1
creatures_names = ["Farmer", "Fox", "Chicken", "Grain"]


class State():

    def __init__(self, d=None):
        if d == None:
            d = {'creatures': [0, 0, 0, 0],
                 'boat': LEFT}
        self.d = d

    def __eq__(self, s2):
        for prop in ['creatures', 'boat']:
            if self.d[prop] != s2.d[prop]:
                return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        p = self.d['creatures']
        left = ""
        right = ""
        for indice in range(4):
            if p[indice] == 0:
                left = left + creatures_names[indice] + "  "
            else:
                right = right + creatures_names[indice] + "  "

        txt = "\n Creatures on the Left Bank: " + left + "\n"
        txt += " Creatures on the Right Bank: " + right + "\n"

        side = 'left'
        if self.d['boat'] == 1:
            side = 'right'
        txt += " Boat is on the " + side + ".\n"
        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        for name in [FA, FO, C, G]:
            news.d['creatures'] = self.d['creatures'][:]
        return news

    def can_move(self, creature):
        '''Tests whether it's legal to move the boat and take
     m missionaries and c cannibals.'''
        side = self.d['boat']  # Where the boat is.
        p = self.d['creatures']

        # When the creature is not on this side
        if p[creature] != side:
            return False

        available = [0, 0, 0, 0]
        for i in range(4):
          available[i] = p[i]

        if creature != 0:
            for i in range(1, 4):
                if i == creature:
                    available[i] = 1 - side
                    break
        available[0] = 1 - side

        farmer_remaining = available[0]
        fox_remaining = available[1]
        chicken_remaining = available[2]
        grain_remaining = available[3]

        # If Chicken and Grain are left alone on one side:
        if farmer_remaining == 0 and fox_remaining == 0 and chicken_remaining == 1 and grain_remaining == 1:
            return False
        # If Fox and Chicken are left alone on one side:
        if farmer_remaining == 0 and fox_remaining == 1 and chicken_remaining == 1 and grain_remaining == 0:
            return False
        if farmer_remaining == 1 and fox_remaining == 1 and chicken_remaining == 0 and grain_remaining == 0:
            return False
        # If Fox and Chicken are left alone on one side:
        if farmer_remaining == 1 and fox_remaining == 0 and chicken_remaining == 0 and grain_remaining == 1:
            return False
        # Fox, Chicken and Grain can't be on the same side as well.
        if farmer_remaining == 0 and fox_remaining == 1 and chicken_remaining == 1 and grain_remaining == 1:
            return False
        if farmer_remaining == 1 and fox_remaining == 0 and chicken_remaining == 0 and grain_remaining == 0:
            return False

        return True

    def move(self, creature):
        '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the boat carrying
     m missionaries and c cannibals.'''
        news = self.copy()  # start with a deep copy.
        side = self.d['boat']  # where is the boat?
        p = news.d['creatures']  # get the array of creatures.
        p[FA] = 1 - side  # remove Farmer from current side & add Farmer to the other side
        if creature != 0:
            p[creature] = 1 - side  # remove the given creature from current side
            # & add the given creature to the other side
        news.d['boat'] = 1 - side  # Move the boat itself.
        return news

def goal_test(s):
    '''If all Ms and Cs are on the right, then s is a goal state.'''
    p = s.d['creatures']
    return p[FA] == 1 and p[FO] == 1 and p[C] == 1 and p[G] == 1


def goal_message(s):
    return "Congratulations on successfully helping the Farmer to get his fox, chicken and grain across the river!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: State(d={'creatures': [0, 0, 0, 0], 'boat': LEFT})
# </INITIAL_STATE>

# <OPERATORS>
# 0 indicates only the Farmer is on boat
# 1 indicates Farmer and Fox
# 2 indicates Farmer and Chicken
# 3 indicates Farmer and Grains
Ff_combinations = [0, 1, 2, 3]

OPERATORS = [Operator(
    "Farmer cross the river with the " + str(creatures_names[creature]),
    lambda s, creature1=creature: s.can_move(creature1),
    lambda s, creature1=creature: s.move(creature1))
    for creature in Ff_combinations]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>
