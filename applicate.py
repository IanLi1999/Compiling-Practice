from lex.lexeme import Analyzer

analyzer = Analyzer('./resource/test.txt')
analyzer.analyze()

analyzer.print_tokens()
