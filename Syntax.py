from copy import deepcopy

from Automation import Automation

actions = {1: 'Shift', 2: 'Reduce', 3: 'ACCEPT', -1: 'ERROR'}
class Syntactic:
    def __init__(self, productions, v, t, s):
        self.productions = productions
        self.v = v              # non-terminate symbols
        self.t = t              # terminite symbols
        self.s = s              # start symbol
        self.action = None
        self.goto = None
        self.tokens = None
        self.stack = []
        self.head = None

    def analyze(self, filepath):
        automation = Automation(self.productions, self.v, self.t, self.s)
        self.action, self.goto = automation.generate_table()

        self.tokens = open(filepath, 'r')
        self.stack = [[0, '$']]  # stack bottom
        
        self.head = self.tokens.read(1)
        while True:
            state = self.stack[-1][0]
            
            # validate token 
            if self.head is None or self.head == ' ':
                self.head = '$'

            if self.head not in self.t:
                print('Invalid token of ' + self.head)
                return False

            move = self.action[state][self.t[self.head]]
            if move[0] == -1:
                print('This is a breakpoint')
            status = self.make_action(move)
            if status == 0 or status == -1:
                return


    def make_action(self, move):
        if actions[move[0]] == 'Shift':
            # just to make the code more clear to understand           
            self.stack.append([move[1], deepcopy(self.head)])       # push into stack
            self.head = self.tokens.read(1)                         # shift right
            if self.head is None or self.head == ' ':
                self.head = '$'

            print('%-120s %s %d' % (self.stack, actions[move[0]], move[1]))

        elif actions[move[0]] == 'Reduce':
            production = self.productions[move[1]]
            for i in range(len(production[1])):
                self.stack.pop()
            # old out
            
            incoming = production[0]
            old_state = self.stack[-1][0]
            new_state = self.goto[old_state][self.v[incoming]]
            # calculate new state due to the goto table

            self.stack.append([new_state, incoming])
            # push the new state and V into stack 

            print('%-120s%s %s->%s' % (self.stack, actions[move[0]], production[0], production[1]))

        elif actions[move[0]] == 'ACCEPT':
            print('%-120s %s' % (self.stack, actions[move[0]]))
            return 0
    
        elif actions[move[0]] == 'ERROR':
            print('Analysis has been processing, but error occurs')
            return -1
        else:
            print('Wrong Move Code of ' + move[0])
            return -1

        return 1


if __name__ == '__main__':
    example_v = {'S': 0, 'E': 1, 'T': 2, 'F': 3}
    example_t = {'n': 0, '+': 1, '-': 2, '*': 3, '/': 4, '(': 5, ')': 6, '$': 7}
    productions = [['S', 'E'], 
                   ['E', 'E+T'], 
                   ['E', 'E-T'], 
                   ['E', 'T'], 
                   ['T', 'T*F'],
                   ['T', 'T/F'],
                   ['T', 'F'],
                   ['F', '(E)'],
                   ['F', 'n']]
    #             # E, T, F
    # goto_table = [[1, 2, 3],             # 0
    #             [-1, -1, -1],          # 1
    #             [-1, -1, -1],          # 2
    #             [-1, -1, -1],          # 3
    #             [10, 2, 3],          # 4
    #             [-1, -1, -1],          # 5
    #             [-1, 11, 3],           # 6
    #             [-1, 12, 3],           # 7
    #             [-1, -1, 13],          # 8
    #             [-1, -1, 14],          # 9
    #             [-1, -1, -1],          # 10 
    #             [-1, -1, -1],          # 11
    #             [-1, -1, -1],          # 12
    #             [-1, -1, -1],          # 13
    #             [-1, -1, -1],          # 14
    #             [-1, -1, -1]]          # 15

    # # actions = {1: 'Shift', 2: 'Reduce', 3: 'ACCEPT'}
    # # {'n': 0, '+': 1, '-': 2, '*': 3, '/': 4, '(': 5, ')': 6, '$': 7}
    # action_table = [[[1, 5], [-1], [-1], [-1], [-1], [1, 4], [-1], [-1]],  # 0
    #                 [[-1], [1, 6], [1, 7], [-1], [-1], [-1], [-1], [3]],   # 1
    #                 [[-1], [2, 3], [2, 3], [1, 8], [1, 9], [-1], [2, 3], [2, 3]],  # 2
    #                 [[-1], [2, 6], [2, 6], [2, 6], [2, 6], [-1], [2, 6], [2, 6]],  # 3
    #                 [[1, 5], [-1], [-1], [-1], [-1], [1, 4], [-1], [-1]],  # 4
    #                 [[-1], [2, 8], [2, 8], [2, 8], [2, 8], [-1], [2, 8], [2, 8]],  # 5
    #                 [[1, 5], [-1], [-1], [-1], [-1], [1, 4], [-1], [-1]],  # 6
    #                 [[1, 5], [-1], [-1], [-1], [-1], [1, 4], [-1], [-1]],  # 7
    #                 [[1, 5], [-1], [-1], [-1], [-1], [1, 4], [-1], [-1]],  # 8
    #                 [[1, 5], [-1], [-1], [-1], [-1], [1, 4], [-1], [-1]],  # 9
    #                 [[-1], [1, 6], [1, 7], [-1], [-1], [-1], [1, 15], [-1]],  # 10
    #                 [[-1], [2, 1], [2, 1], [1, 8], [1, 9], [-1], [2, 1], [2, 1]],  # 11
    #                 [[-1], [2, 2], [2, 2], [1, 8], [1, 9], [-1], [2, 2], [2, 2]],  # 12
    #                 [[-1], [2, 4], [2, 4], [2, 4], [2, 4], [-1], [2, 4], [2, 4]],  # 13
    #                 [[-1], [2, 5], [2, 5], [2, 5], [2, 5], [-1], [2, 5], [2, 5]],  # 14
    #                 [[-1], [2, 7], [2, 7], [2, 7], [2, 7], [-1], [2, 7], [2, 7]]]  # 15

    analyzer = Syntactic(productions, example_v, example_t, 'S')
    analyzer.analyze('./Syntactic Analyzer Test File.txt')
