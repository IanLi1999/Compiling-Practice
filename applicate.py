from lexeme import Lexical

analyzer = Lexical('./resource/test.txt')
analyzer.analyze()

analyzer.print_tokens()
