from copy import deepcopy

class Automation:
    def __init__(self, productions, v, t, s):
        self.productions = productions
        self.collections = []
        self.go = {}
        self.goto = None
        self.action = None
        self.first = {}
        self.follow = {}
        self.status_total = 0
        self.v = v
        self.t = t
        self.s = s
    
    def generate_table(self):
        self.generate_collections()
        self.cal_first_follow()
        self.fill_table()
        return self.action, self.goto


    def fill_table(self):
        # initialize all
        self.goto = []
        self.action = []
        for i in range(0, self.status_total + 1):
            self.goto.append([])
            for j in range(0, len(self.v)):
                self.goto[i].append(-1)
            self.action.append([])
            for j in range(0, len(self.t)):
                self.action[i].append([-1])
        
        # fill in go and shift 
        for state in self.go:
            outs = self.go[state]
            for out in outs:
                if out[1] in self.v:
                    self.goto[state][self.v[out[1]]] = out[0]
                else:
                    self.action[state][self.t[out[1]]] = [1, out[0]]
        
        # fill in reduce and accept
        for i, collection in enumerate(self.collections):
            # collection corresponds to each state's programs
            # i corresponds to the state number
            for program in collection:
                if program[2] == len(program[1]):
                    # reduce program
                    if program[0] == self.s:
                        # ACCEPT program
                        self.action[i][self.t['$']] = [3]
                    else:
                        for token in self.follow[program[0]]:
                            self.action[i][self.t[token]] = [2, self.productions.index([program[0], program[1]])]


    def cal_first_follow(self):
        for token in self.v:
            if token not in self.first:
                self.cal_first(token)
        self.cal_follow()

    def cal_follow(self):
        new_follow = {}     # for comparison use

        for token in self.v:        # initialize all
            new_follow[token] = []

        new_follow[self.s] = ['$']     # start symbol

        while new_follow != self.follow:
            self.follow = deepcopy(new_follow)
            for production in self.productions:              
                for i, token in enumerate(production[1]):
                    if token in self.v:
                        if i < len(production[1])-1:
                            if production[1][i+1] in self.v:
                                # get fisrt or the right
                                new_follow[token] += self.first[production[1][i+1]]
                                new_follow[token] = list(set(new_follow[token]))
                            else:
                                # get right t
                                if production[1][i+1] not in new_follow[token]:
                                    new_follow[token].append(production[1][i+1])
                        else:
                            # right get follow from left
                            new_follow[token] += new_follow[production[0]]
                            new_follow[token] = list(set(new_follow[token]))


    def cal_first(self, token):
        for production in self.productions:
            if production[0] == token:
                if production[1][0] in self.v and production[1][0] != token:
                    if production[1][0] not in self.first:
                        part = self.cal_first(production[1][0])
                    else:
                        part = self.first[production[1][0]]
                    if token in self.first:
                        self.first[token] += part
                        self.first[token] = list(set(self.first[token]))  # get rid of the repeat items
                    else:
                        self.first[token] = part
                elif production[1][0] in self.t:
                    if token in self.first and production[1][0] not in self.first[token]:
                        self.first[token].append(production[1][0])
                    else:
                        self.first[token] = [production[1][0]]
        return self.first[token]

    
    def generate_collections(self):
        program_0 = [self.productions[0][0], self.productions[0][1], 0]
        # ['E', 'E+T', 0-3]
        self.collections.append(self.calculate_closure([program_0]))

        for i, collection in enumerate(self.collections):
            collections_from = self.partition(collection)        
            for token in collections_from:
                result = self.calculate_closure(collections_from[token])
                next_state = -1
                if result not in self.collections:
                    self.collections.append(result)
                    self.status_total += 1    # corresponding to the status number
                    next_state = self.status_total
                else:
                    next_state = self.collections.index(result)
                
                if i in self.go:
                    self.go[i].append([next_state, token])     # self.status_total = go(0, function)
                else:
                    self.go[i] = [[next_state, token]]
            

    def calculate_closure(self, programs):
        collection = deepcopy(programs)
        # add itself to the collection

        for program in collection:
            if program[2] < len(program[1]):
                next_token = program[1][program[2]]

                if next_token in self.v:
                    for production in self.productions:
                        if production[0] == next_token:
                            new = [production[0], production[1], 0]
                            if new not in collection:
                                collection.append(new)
        return collection

    def partition(self, collection):
        # partition programs belongs to the same next start programs 
        # e.g. {E->·E+T, E->·E-T}
        programs = {}
        # {'E': [['E', 'E+T', 0], ['E', 'E-T', 0]]}
        for program in collection:
            if program[2] < len(program[1]):
                next_token = program[1][program[2]]
                if next_token in programs:
                    programs[next_token].append([program[0], program[1], program[2]+1])
                
                else:
                    programs[next_token] = [[program[0], program[1], program[2]+1]]
        
        return programs

    def result_to_file(self, path):
        file = open(path, 'w')
        
        # write fisrt & follow
        file.write('FIRST集与fOLLOW集\n')
        for token in self.v:
            file.write('FIRST(%s)=%-20s\tFOLLOW(%s)=%-20s\n' % (token, self.first[token], token, self.follow[token]))
        file.write('\n')

        # write collections
        file.write('项目集规范族\n')
        for i, collection in enumerate(self.collections):
            file.write('I{0}\t{1}\n'.format(i, collection))
        file.write('\n')
        
        # write action & goto table
        file.write('SLR(1)分析表\n')
        counter = 0
        file.write('  \t%-70s\t%-50s\n' % ('Action', 'Goto'))
        for act, go in zip(self.action, self.goto):
            file.write('%2d\t%-70s\t%-50s\n' % (counter, act, go))
        file.write('\n')

        file.flush()
        file.close()

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
    auto = Automation(productions, example_v, example_t, 'S')
    auto.generate_table()
