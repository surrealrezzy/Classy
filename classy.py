from classes import Parser, Lexer

import sys

class Classy:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        return Lexer(self.text).tokenize()

    def parse(self):
        return Parser(self.tokenize()).parse()

    def generate(self):
        generated_text = {}
        for element in self.parse():
            generated_text.update({element.name : {'type' : element.type, 'contents' : Generator(element.contents).generate() if isinstance(element, Container) else element.contents}})

        return generated_text

    def retrieve(self, path):
        location = path.split('.')
        root = location[0]

        current_level = self.generate().get(root)
        if not current_level:
            print(f'Retrieve Error: Element \'{root}\' does not exist')
            sys.exit(1)
        
        for index, item in enumerate(path.split('.')[1:]):
            current_level = current_level['contents'].get(item)
            if not current_level:
                print(f'Retrieve Error: {location[index]} has no child named \'{item}\'')
                sys.exit(1)

        return current_level

def main():
    try:
        if len(sys.argv) < 2:
            ('Insufficient arguments: Expected `classy FILE [RETRIEVE|TOKENIZE|PARSE|GENERATE] [PATH.TO.VALUE]`')
            sys.exit(1)
        classy = Classy(open(sys.argv[1], 'r').read())
    except FileNotFoundError:
        print(f'Error: File {sys.argv[1]} does not exist')
        sys.exit(1)
    
    if len(sys.argv) < 3:
        ('Insufficient arguments: Expected `classy FILE [RETRIEVE|TOKENIZE|PARSE|GENERATE] [PATH.TO.VALUE]`')
        sys.exit(1)
    command = sys.argv[2]

    if len(sys.argv) > 3:
        if command == 'retrieve':
            print(classy.retrieve(sys.argv[3])['contents'])

    elif len(sys.argv) > 2:
        if command == 'parse':
            print(classy.parse())
        elif command == 'tokenize':
            print(',\n'.join([str(token) for token in classy.tokenize()]))
        elif command == 'generate':
            print(classy.generate())
        else:
            print('Unknown command: Try \'retrieve\', \'tokenize\', \'parse\', or \'generate\'')
    else:
        ('Insufficient arguments: Expected `classy FILE [RETRIEVE|TOKENIZE|PARSE|GENERATE] [PATH.TO.VALUE]`')
        sys.exit(1)

if __name__ == "__main__":
    main()