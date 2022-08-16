from SquigTokens import *

class Lexer:

    def __init__(self,text):
        self.text = text
        self.char = None
        self.index = -1 
        self.nextChar()
    
    def nextChar(self):
        self.index +=1
        self.char = self.text[self.index] if self.index < len(self.text) else None

    def lexNumber(self):

        number = ''
        decimal_point_count = 0
        while self.char != None and self.char in tok_digits+'.':
            if self.char == '.':
                if decimal_point_count == 1:
                    break
                decimal_point_count +=1
            number += self.char
            self.nextChar()

        if decimal_point_count == 1:
            return Token(tok_float,float(number))
        return Token(tok_int,int(number))

    def lexMulOrPower(self):
        operator = ''
        while self.char != None and self.char =='*':
            operator+=self.char
            self.nextChar()
        if operator == '*':
            return Token(tok_mul)
        elif operator == '**':
            return Token(tok_power)
        else:
            raise Exception(f"Invalid Operator '{operator}'")

    def lexGreaterOrGreaterEql(self):

        self.nextChar()
        if self.char == '=':
            self.nextChar()
            return Token(tok_greater_eql)
        return Token(tok_greater)

    def lexLesserORLesserEql(self):
        self.nextChar()
        if self.char == '=':
            self.nextChar()
            return Token(tok_lesser_eql)
        
        return Token(tok_lesser)

    

    def lexNotEqlOrNot(self):
        self.nextChar()
        if self.char == '=':
            self.nextChar()
            return Token(tok_not_eql)
        self.nextChar()
        return Token(tok_not)

    def lexVariable(self):
        variable = ''
        while self.char != None and self.char in tok_letters+tok_letters.upper()+tok_digits+'_':
            variable += self.char
            self.nextChar()
        if variable in keywords:
            return Token(tok_keyword,variable)
        return Token(tok_var,variable)
    
    def lexEql(self):
        self.nextChar()
        if self.char != '=':
            raise SyntaxError("Expected another '=' after the '='.")
        self.nextChar()
        return Token(tok_eql)

    def lexString(self):
        string = ''
        escape = False
        self.nextChar()
        escape_sequences = {
            'n' : '\n',
            't' : '\t'
            }
        while self.char != None and (self.char !='\"' or escape):
            if escape:
                
                string += escape_sequences.get(self.char,self.char)
                escape = False
                
            elif self.char == '\\':
                escape = True
            else:
                string += self.char
            self.nextChar()
        if self.char != '\"':
            raise Exception("invalid literal")
        self.nextChar()
        return Token(tok_string,string)

    def lexInputString(self):
        inputString = ''
        self.nextChar()
        while self.char != None and self.char != "'":
            inputString += self.char
            self.nextChar()
        self.nextChar()
        return Token(tok_input_string,inputString)

    def lexDivideOrFloor(self):
        operator = ''
        while self.char != None and self.char =='/':
            operator+=self.char
            self.nextChar()
        if operator == '/':
            return Token(tok_divide)
        elif operator == '//':
            return Token(tok_floor)
        else:
            raise Exception(f"Invalid Operator '{operator}'")

    def tokenize(self):

        tokens = []
        while self.char != None:
            
            if self.char in ' \t':
                self.nextChar()
            elif self.char == '+':
                tokens.append(Token(tok_plus))
                self.nextChar()
            elif self.char == '-':
                tokens.append(Token(tok_minus))
                self.nextChar()
            elif self.char == '*':
                tokens.append(self.lexMulOrPower())
            elif self.char == '/':
                tokens.append(self.lexDivideOrFloor())
            elif self.char == '%':
                tokens.append(Token(tok_mod))
                self.nextChar()
            elif self.char == '(':
                tokens.append(Token(tok_lparen))
                self.nextChar()
            elif self.char ==')':
                tokens.append(Token(tok_rparen))
                self.nextChar()
            elif self.char == '{':
                tokens.append(Token(tok_lbre))
                self.nextChar()
            elif self.char == '}':
                tokens.append(Token(tok_rbre))
                self.nextChar()
            elif self.char == ':':
                tokens.append(Token(tok_colon))
                self.nextChar()
            elif self.char == '!':
                tokens.append(self.lexNotEqlOrNot())
            elif self.char == '<':
                tokens.append(self.lexLesserORLesserEql())
            elif self.char == '>':
                tokens.append(self.lexGreaterOrGreaterEql())
            elif self.char == '=':
                tokens.append(self.lexEql())
            elif self.char == '&':
                tokens.append(Token(tok_and))
                self.nextChar()
            elif self.char == '|':
                tokens.append(Token(tok_or))
                self.nextChar()
            elif self.char == '~':
                tokens.append(Token(tok_not))
                self.nextChar()
            elif self.char in tok_digits:
                
                tokens.append(self.lexNumber())
            elif self.char in tok_letters+tok_letters.upper()+'_':
                tokens.append(self.lexVariable())
            elif self.char == '"':
                tokens.append(self.lexString())
            elif self.char == "'":
                tokens.append(self.lexInputString())
            elif self.char == ",":
                tokens.append(Token(tok_comma))
                self.nextChar()
            elif self.char == '[':
                tokens.append(Token(tok_lsqr))
                self.nextChar()
            elif self.char == ']':
                tokens.append(Token(tok_rsqr))
                self.nextChar()
            else:
                print(self.char)
                print("Invalid syntax")
                self.nextChar() 
        return tokens

