from enum import Enum
import sys

class Tokens(Enum):
    identifier = 0
    container_start = 1
    container_end = 2
    object_start = 3
    object_end = 4

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.type} {self.value}' if self.value else f'{self.type}'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_character = self.text[self.pos]
    
    def advance(self):
        self.pos += 1
        self.current_character = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.current_character != None:
            if self.current_character == '{':
                tokens.append(Token(Tokens.container_start))
                self.advance()
            elif self.current_character == '}':
                tokens.append(Token(Tokens.container_end))
                self.advance()
            elif self.current_character == '[':
                tokens.append(Token(Tokens.object_start))
                self.advance()
            elif self.current_character == ']':
                tokens.append(Token(Tokens.object_end))
                self.advance()
            elif self.current_character in ' \t\n':
                self.advance()
            else:
                word = ''
                while self.current_character != None:
                    if self.current_character in ' \t\n' :
                        break
                    word += self.current_character
                    self.advance()
                if word:
                    tokens.append(Token(Tokens.identifier, word))
                self.advance()
        
        return tokens

class Container:
    def __init__(self, type_, name, contents):
        self.type = type_
        self.name = name
        self.contents = contents

    def add(self, item):
        self.contents.append(item)

    def __repr__(self):
        return f'{self.type} {self.name} {self.contents}'

class Object:
    def __init__(self, type_, name, contents):
        self.type = type_
        self.name = name
        self.contents = contents

    def add(self, item):
        self.contents.update(item)

    def __repr__(self):
        return f'{self.type} {self.name} {self.contents}'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]
    
    def advance(self, advance=True):
        if advance:
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

        return self.current_token

    def parse(self):
        elements = []

        while self.current_token != None:
            if self.current_token.type == Tokens.container_start:
                if elements:
                    name = elements.pop()
                else:
                    print('Parse error: Container type and name required [0/2]')
                    sys.exit(1)
                if elements:
                    type_ = elements.pop()
                else:
                    print('Parse error: Container type and name required [1/2]')
                    sys.exit(1)
                elements.append(Container(type_, name, self.parse_container()))
                self.advance()
            elif self.current_token.type == Tokens.object_start:
                if elements:
                    name = elements.pop()
                else:
                    print('Parse error: Object type and name required [0/2]')
                    sys.exit(1)
                if elements:
                    type_ = elements.pop()
                else:
                    print('Parse error: Object type and name required [1/2]')
                    sys.exit(1)
                elements.append(Object(type_, name, self.parse_object()))
                self.advance()
            else:
                elements.append(self.current_token.value)
                self.advance()

        return elements

    def parse_container(self):
        container_tokens = []

        self.advance()
        while self.current_token.type != Tokens.container_end:
            if self.current_token.type == Tokens.container_start:
                if container_tokens:
                    name = container_tokens.pop()
                else:
                    print('Parse error: Container type and name required [0/2]')
                    sys.exit(1)
                if container_tokens:
                    type_ = container_tokens.pop()
                else:
                    print('Parse error: Container type and name required [1/2]')
                    sys.exit(1)
                container_tokens.append(Container(type_, name, self.parse_container()))
            elif self.current_token.type == Tokens.object_start:
                if container_tokens:
                    name = container_tokens.pop()
                else:
                    print('Parse error: Object type and name required [0/2]')
                    sys.exit(1)
                if container_tokens:
                    type_ = container_tokens.pop()
                else:
                    print('Parse error: Object type and name required [1/2]')
                    sys.exit(1)
                container_tokens.append(Object(type_, name, self.parse_object()))
            elif self.current_token.type == Tokens.object_end:
                print('Parse error: Reached \']\' before \'}\'')
                sys.exit(1)
            else:
                container_tokens.append(self.current_token.value)
            self.advance()
            if self.current_token == None:
                print('Parse error: Reached EOF before \'}\'')
                sys.exit(1)

        self.advance()

        return container_tokens

    def parse_object(self):
        object_tokens = {}

        self.advance()
        while self.current_token.type != Tokens.object_end:
            if self.current_token.type == Tokens.object_start:
                key = self.current_token.value
                if not key:
                    print('Parse error: Key without value')
                    sys.exit(1)
                object_tokens[key] = self.parse_object()
                    
            elif self.current_token.type == Tokens.container_end:
                print(object_tokens)
                print('Parse error: Reached \'}\' before \']\'')
                sys.exit(1)
            else:
                key = self.current_token.value
                value = self.advance().value
                if not value:
                    print('Parse Error: Key without value')
                    sys.exit(1)
                object_tokens[key] = value
                self.advance()
            if self.current_token == None:
                print('Parse error: Reached EOF before \']\'')
                sys.exit(1)     
        
        return object_tokens
    
class Generator:
    def __init__(self, elements):
        self.elements = elements
        self.pos = 0
        self.current_element = self.elements[0]

    def advance(self):
        self.pos += 1
        self.current_element = self.elements[self.pos] if self.pos < len(self.elements) else None
