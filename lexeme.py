import sys

props = ['id', 'relation_op', 'num', 'keyword', 'assign_op']
ops = {'+': 'plus_op', '*': 'mul_op', '/': 'div_op', '-': 'sub_op', '=': 'assign_op'}
ops_assign = {'+=': 'mul_assign', '-=': 'abs_assign', '*=': 'mul_assign', '/=': 'div_assign'}
self_ops = {'++': 'self_inc', '--': 'self_dec'}
parenthesis = {'{': 'brace_l', '}': 'brace_r', '(': 'bracket_l', ')': 'bracket_r', '[': 'square_l', ']': 'square_r'}
rel_ops = {'<': 'lt_rel_op', '<=': 'le_rel_op', '>': 'gt_rel_op',
           '>=': 'ge_rel_op', '==': 'et_rel_op', '!=': 'ne_rel_op'}
specials = {';': 'delimiter', '#': 'macro', ',': 'comma', '&': 'at'}
keywords = ['include', 'main', 'int', 'float', 'if', 'else', 'while', 'break', 'printf', 'long', 'for']


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

    def __init__(self, value):
        self.value = value


class Lexical:
    # match method for each kind of symbol

    # symbols represents symbol manager
    # tokens represents token stream
    symbols = list()
    tokens = list()

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

            elif head == '"':
                head = self.string_matcher()

            elif head in self.white:
                head = self.source.read(1)

            elif head in ops:
                head = self.operator_matcher()

            elif head in parenthesis:
                self.tokens.append(Token(parenthesis[head], head))
                head = self.source.read(1)

            elif head in specials:
                self.tokens.append(Token(specials[head], head))
                head = self.source.read(1)
            else:
                self.error_handle()
                break

    # props = ['id', 'relation_op', 'num', 'keyword', 'assign_op']

    def id_matcher(self):
        head = self.source.read(1)
        while True:

            if ('a' <= head <= 'z') or ('A' <= head <= 'Z') or (head == '_'):
                self.cur_symbol += head
                head = self.source.read(1)

            else:
                break

        if self.cur_symbol not in keywords:
            self.symbol_allocator()
            # self.tokens.append(Token('id', '#' + str(len(self.symbols)-1)))
        else:
            self.tokens.append(Token('keyword', self.cur_symbol))

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

    def operator_matcher(self):
        head = self.source.read(1)

        if head == '=':
            self.cur_symbol += head
            self.tokens.append(Token(ops_assign[self.cur_symbol], ''))
            head = self.source.read(1)

        elif head in ['+', '-']:
            self.cur_symbol += head

            if self.cur_symbol in self_ops:
                self.tokens.append(Token(self_ops[self.cur_symbol], ''))
            else:
                self.error_handle()

            head = self.source.read(1)

        else:
            self.tokens.append(Token(ops[self.cur_symbol], ''))

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

    def string_matcher(self):
        self.tokens.append(Token('quote_l', ''))
        self.cur_symbol = ''
        head = self.source.read(1)
        while True:

            if head == '"':
                self.tokens.append(Token('string', self.cur_symbol))
                self.tokens.append(Token('quote_r', ''))
                head = self.source.read(1)
                break

            else:
                self.cur_symbol += head
                head = self.source.read(1)

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

    def symbol_allocator(self):
        for i, symbol in enumerate(self.symbols):
            if self.cur_symbol == symbol.value:
                self.tokens.append(Token('id', i))
                return

        self.symbols.append(Symbol(self.cur_symbol))
        self.tokens.append(Token('id', len(self.symbols)-1))

    def error_handle(self):
        print("error occur with {0}\n".format(self.cur_symbol))

    def print_tokens(self):
        for token in self.tokens:
            print('<{0}, {1}>'.format(token.prop, token.entry))

    def existed(self):
        pass


if __name__ == '__main__':
    # example test file './resource/test.txt'
    analyzer = Lexical(sys.argv[1])
    analyzer.analyze()

    analyzer.print_tokens()
