props = ['id', 'relation_op', 'num', 'keyword', 'assign_op']
ops = {'+': 'plus_op', '*': 'mul_op', '/': 'div_op', '-': 'sub_op', '=': 'assign_op'}
rel_ops = {'<': 'lt_rel_op', '<=': 'le_rel_op', '>': 'gt_rel_op',
           '>=': 'ge_rel_op', '==': 'et_rel_op', '!=': 'ne_rel_op'}


class Token:
    # prop for the type of symbol, e.g. id, op
    # props is the tuple containing the legal prop to be assigned
    # entry for the entry of the corresponding symbol in the symbol table
    __slots__ = ('prop', 'entry')

    def __init__(self, prop, entry):
        self.prop = prop
        self.entry = entry


class Symbol:
    __slots__ = ('prop', 'value')

    def __init__(self, prop, value):
        self.prop = prop
        self.value = value


class Analyzer:
    # match method for each kind of symbol

    # symbols represents symbol manager
    # tokens represents token stream
    symbols = list()
    tokens = list()

    keywords = ['include', 'main', 'int', 'float', 'if', 'else', 'while', 'break', 'printf']
    parenthesis = ['{', '}', '(', ')']
    white = ['\t', ' ', '\n']

    def __init__(self, source_file):
        self.cur_symbol = ''

        # source stands for source file
        self.source = open(source_file, 'r')

    def analyze(self):
        head = self.source.read(1)

        while True:
            self.cur_symbol = head

            if (head is None) or (head == ''):
                # empty string for reaching the end of the file
                return self.symbols

            if ('a' <= head <= 'z') or ('A' <= head <= 'Z') or (head == '_'):
                head = self.id_matcher()

            elif '0' <= head <= '9':
                head = self.num_matcher()

            elif (head == '>') or (head == '<') or (head == '!'):
                head = self.relation_matcher()

            elif head == '=':
                head = self.assign_or_relation()

            elif head == '/':
                head = self.comment_matcher()

            elif head in self.white:
                head = self.source.read(1)
                continue

            else:
                self.error_handle()

    # props = ['id', 'relation_op', 'num', 'keyword', 'assign_op']

    def id_matcher(self):
        head = self.source.read(1)
        while True:

            if ('a' <= head <= 'z') or ('A' <= head <= 'Z') or (head == '_'):
                self.cur_symbol += head
                head = self.source.read(1)

            else:
                break

        if self.cur_symbol not in self.keywords:
            self.symbols.append(Symbol('id', self.cur_symbol))
            self.tokens.append(Token('id', '#' + str(len(self.symbols)-1)))

        return head

    def num_matcher(self):
        head = self.source.read(1)
        while True:

            if '0' <= head <= '9':
                self.cur_symbol += head
                head = self.source.read(1)

            else:
                break

        self.tokens.append(Token('num', self.cur_symbol))

        return head

    def relation_matcher(self):
        head = self.source.read(1)
        if head == '=':
            self.cur_symbol += head
            head = self.source.read(1)

        self.tokens.append(Token(rel_ops[self.cur_symbol], ''))

        return head

    def assign_or_relation(self):
        head = self.source.read(1)

        if head == '=':
            self.cur_symbol += head
            self.tokens.append(Token(rel_ops[self.cur_symbol], ''))
            head = self.source.read(1)
        else:
            self.tokens.append(Token(ops[self.cur_symbol], ''))

        return head

    def comment_matcher(self):
        head = self.source.read(1)

        if head == '/':
            # line comment
            while True:
                head = self.source.read(1)
                if head == '\n':
                    head = self.source.read(1)
                    break

        elif head == '*':
            # block comment
            while True:
                head = self.source.read(1)
                if head == '*':
                    head = self.source.read(1)
                    if head == '/':
                        head = self.source.read(1)
                        break
        else:
            self.error_handle()

        return head

    def error_handle(self):
        print("error occur with " + self.cur_symbol)

    def print_tokens(self):
        for token in self.tokens:
            print('<{0}, {1}>'.format(token.prop, token.entry))

    def existed(self):
        pass
