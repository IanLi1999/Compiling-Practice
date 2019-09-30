props = ['id', 'relation_op', 'constant', 'keyword', 'assign_op']


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

    def __init__(self, source_file):
        self.cur_symbol = ''

        # source stands for source file
        self.source = open(source_file, 'r')

    def analyze(self):
        head = self.source.read(1)

        while True:
            self.cur_symbol = head

            if head == '':
                # empty string for reaching the end of the file
                return self.symbols

            if ('a' <= head <= 'z') or ('A' <= head <= 'Z') or (head == '_'):
                head = self.id_matcher()

            elif '0' <= head <= '9':
                head = self.constant_matcher()

            elif (head == '>') or (head == '<') or (head == '!'):
                head = self.relation_matcher()

            elif head == '=':
                head = self.assign_or_relation()

            elif head == '/':
                head = self.comment_matcher()

            else:
                self.error_handle()

    # props = ['id', 'relation_op', 'constant', 'keyword', 'assign_op']

    def id_matcher(self):
        while True:
            head = self.source.read(1)

            return head

    def constant_matcher(self):
        while True:
            head = self.source.read(1)

            return head

    def relation_matcher(self):
        while True:
            head = self.source.read(1)
            if head == '=':
                self.cur_symbol += head

            else:
                self.symbols.append(Symbol('relation_op', self.cur_symbol))
                self.tokens.append(Token('relation_op', len(self.symbols)-1))

                return head

    def assign_or_relation(self):
        while True:
            head = self.source.read(1)

            return head

    def comment_matcher(self):
        while True:
            head = self.source.read(1)

            return head

    def error_handle(self):
        print("error occur with " + self.cur_symbol)
