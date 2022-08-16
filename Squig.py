from SquigLexer import *
from SquigParser import *
from SquigInterpretor import *
import os



def IDE():
    while True:
        prompt = input("Squig >")
        if prompt == 'clear':
            os.system('cls')
        lex = Lexer(prompt)
        #print(lex.tokenize())
        parser = Parser(lex.tokenize())
        #print(parser.parse())
        ide = Interpretor()
        ide = ide.process(parser.parse())
        if ide:
            print(ide)
        del lex,parser,ide

##def load(filename):
##
##    file = open(filename)
##    while True:
##        lex = Lexer(file.read())
##        parser = Parser(lex.tokenize())
##        ide = Interpretor()
##        ide = ide.process(parser.parse())
##        if ide:
##            print(ide)


if __name__ == '__main__':

    IDE()

