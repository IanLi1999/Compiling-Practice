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
        self.auto = None
        self.file = None        # result file

    def analyze(self, filepath):
        # build automation and generate analysis table
        self.auto = Automation(self.productions, self.v, self.t, self.s)
        self.action, self.goto = self.auto.generate_table()
        self.auto.result_to_file('./Syntax Result.txt')

        self.file = open('./Syntax Result.txt', 'a')
        self.file.write('对输入记号流的分析过程\n')

        self.process(filepath)
        
        self.file.flush()
        self.file.close()


    def process(self, filepath):
        self.tokens = open(filepath, 'r')
        self.stack = [[0, '$']]  # stack bottom
        
        self.head = self.tokens.read(1)
        while True:
            state = self.stack[-1][0]
            
            # validate token 
            if self.head is None or self.head == ' ' or self.head == '':
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
        record = deepcopy(self.stack)
        if actions[move[0]] == 'Shift':
            # just to make the code more clear to understand           
            self.stack.append([move[1], deepcopy(self.head)])       # push into stack
            self.head = self.tokens.read(1)                         # shift right
            if self.head is None or self.head == ' ' or self.head == '':
                self.head = '$'

            print('%-120s %s %d' % (record, actions[move[0]], move[1]))
            self.file.write('%-120s %s %d\n' % (record, actions[move[0]], move[1]))

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

            print('%-120s%s %s->%s' % (record, actions[move[0]], production[0], production[1]))
            self.file.write('%-120s%s %s->%s\n' % (record, actions[move[0]], production[0], production[1]))

        elif actions[move[0]] == 'ACCEPT':
            print('%-120s %s' % (record, actions[move[0]]))
            self.file.write('%-120s %s\n' % (record, actions[move[0]]))
            return 0
    
        elif actions[move[0]] == 'ERROR':
            print('Analysis has been processing, but error occurs')
            self.file.write('Analysis has been processing, but error occurs\n')
            return -1
        else:
            print('Wrong Move Code of ' + move[0])
            self.file.write('Wrong Move Code of ' + move[0] + '\n')
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

    analyzer = Syntactic(productions, example_v, example_t, 'S')
    analyzer.analyze('./Syntactic Analyzer Test File.txt')
