tok_plus         = 'plus'
tok_minus        = 'minus'
tok_divide       = 'divide'
tok_mul          = 'mul'
tok_power        = 'power'
tok_mod          = 'mod'
tok_var          = 'var'
tok_digits       = '0123456789'
tok_letters      = 'abcdefghijklmnopqrstuvwxyz'
tok_int          = 'int'
tok_float        = 'float'
tok_lparen       = 'lparen'
tok_rparen       = 'rparen'
tok_colon        = 'colon'
tok_keyword      = 'keyword'
tok_semicolon    = 'semicolon'
tok_lbre         = 'lbre'
tok_rbre         = 'rbre'
tok_greater      = 'greater'
tok_lesser       = 'lesser'
tok_greater_eql  = 'greatereql'
tok_lesser_eql   = 'lessereql'
tok_not_eql      = 'noteql'
tok_eql          = 'eql'
tok_and          = 'and'
tok_or           = 'or'
tok_not          = 'not'
tok_string       = 'string'
tok_input_string = 'inputstring'
tok_true         = 'true'
tok_false        = 'false'
tok_comma        = 'comma'
tok_floor        = 'floor'
tok_lsqr         = 'lsqr'
tok_rsqr         = 'rsqr'
tok_dot          = 'dot'

keywords = ('if','else','elif','for','function','clear')

class Token:

    def __init__(self,typ,val=None):
        self.typ = typ
        self.val = val

    def __repr__(self):
        if self.val:
            return f"{self.typ}:{self.val}"
        return f"{self.typ}"

    def match(self,typ,val):
        return self.typ == typ and self.val == val

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
class NumberNode:

    def __init__(self,number_tok):
        self.number_tok = number_tok

    def __repr__(self):
        return f"{self.number_tok}"

class BinaryOperatorNode:

    def __init__(self,left_tok,operator_tok,right_tok):
        self.left_operand_tok = left_tok
        self.operator_tok = operator_tok
        self.right_operand_tok = right_tok

    def __repr__(self):
        return f"({self.left_operand_tok},{self.operator_tok},{self.right_operand_tok})"

class UnaryOperatorNode:

    def __init__(self,operator_tok,value_tok):
        self.operator_tok = operator_tok
        self.value_tok = value_tok

    def __repr__(self):
        return f'{self.operator_tok}{self.value_tok}'


class VariableNode:

    def __init__(self,var_name_tok,var_val_tok):
        self.var_name_tok = var_name_tok
        self.var_val_tok = var_val_tok

    def __repr__(self):
        return f"{self.var_val_tok}"

class VariableCallNode:

    def __init__(self,var_name_tok):
        self.var_name_tok = var_name_tok

    def __repr__(self):
        return f"VariableCall : {self.var_name_tok}"

class IfNode:

    def __init__(self,cases,else_case):
        self.cases = cases
        self.else_case = else_case

class StringNode:

    def __init__(self,string_tok,index_tok):
        self.string_tok = string_tok
        self.index_tok = index_tok

    def __repr__(self):
        return f"{self.string_tok} {self.index_tok}"

class InputNode:

    def __init__(self,input_string_tok):
        self.input_string_tok = input_string_tok

    def __repr__(self):
        return f"{self.input_string_tok}"


class ForNode:

    def __init__(self,var_name_tok,start_val_tok,end_val_tok,step_val_tok,body_tok):
        self.var_name_tok = var_name_tok
        self.start_val_tok = start_val_tok
        self.end_val_tok = end_val_tok
        self.step_val_tok = step_val_tok
        self.body_tok = body_tok

    def __repr__(self):
        return f"({self.var_name_tok},{self.start_val_tok},{self.end_val_tok},{self.step_val_tok},{self.body_tok})"

class FunctionNode:

    def __init__(self,var_name_tok,args_tok,body_tok):
        self.var_name_tok = var_name_tok
        self.args_tok = args_tok
        self.body_tok = body_tok

    def __repr__(self):
        if self.var_name_tok:
            return f"function:{self.var_name_tok.val} {self.args_tok} {self.body_tok}"
        return f"function:Anonymous {self.args_tok} {self.body_tok}"

class FunctionCallNode:

    def __init__(self,var_name_tok,args_tok):
        self.var_name_tok = var_name_tok
        self.args_tok = args_tok

    def __repr__(self):
        return f"functionCall:{self.var_name_tok.var_name_tok.val} {self.args_tok}"


class CollectionNode:

    def __init__(self,elements_tok,index_tok = None):
        self.elements_tok = elements_tok
        self.index_tok = index_tok

    def __repr__(self):
        return f"Collection : {self.elements_tok}"

class CollectionAssignmentNode:

    def __init__(self,var_name_tok,index_tok,val_tok):
        self.var_name_tok = var_name_tok
        self.index_tok = index_tok
        self.val_tok = val_tok

    def __repr__(self):
        return f"CollectionAssignment : {self.var_name_tok} {self.index_tok} {self.val_tok}"

class CollectionAccessNode:

    def __init__(self,var_name_tok,index_tok):
        self.var_name_tok = var_name_tok
        self.index_tok = index_tok

    def __repr__(self):
        return f"CollectionAccess : {self.var_name_tok}"

class Parser:

    def __init__(self,tokens):
        self.tokens = tokens
        self.token = None
        self.index = -1
        self.nextToken()

    def nextToken(self):
        self.index +=1
        self.token = self.tokens[self.index] if self.index<len(self.tokens) else Token('eof')

    def parse(self):

        return self.expression()

    def expression(self):

        """if self.token.typ == tok_var:
            
            var_name_tok = self.token
            self.nextToken()

            if self.token.typ != tok_colon:
                raise Exception(f"Expecteed a ':' after variable '{var_name_tok.val}'")
            self.nextToken()
            var_val_tok = self.expression()
            return VariableNode(var_name_tok,var_val_tok)"""
        
        if self.token.typ == tok_lbre:
            self.nextToken()
            comp_tok = self.comparision_expression()
            if self.token.typ != tok_rbre:
                raise SyntaxError("Expected a '}'")
            self.nextToken()
            return comp_tok
        return self.comparision_expression()

    def comparision_expression(self):
                    
        
        return self.binaryOperatorRule(self.relational_expression,(tok_and,tok_or))

        

    def relational_expression(self):
        if self.token.typ == tok_not:
            operator_tok = self.token
            self.nextToken()
            relation_expression_tok = self.relational_expression()
            return UnaryOperatorNode(operator_tok,relation_expression_tok)

        return self.binaryOperatorRule(self.arithmatic_expression,(tok_lesser,tok_greater,tok_lesser_eql,tok_greater_eql,tok_not_eql,tok_eql))
        
    def arithmatic_expression(self):
        return self.binaryOperatorRule(self.term,(tok_plus,tok_minus,tok_floor))
        

    def term(self):

        return self.binaryOperatorRule(self.factor,(tok_mul,tok_divide,tok_mod))

    def binaryOperatorRule(self,rule_a,operators,rule_b = None):
        if rule_b == None:
            rule_b = rule_a

        left_rule_tok = rule_a()
        while self.token.typ in operators:
            operator_tok = self.token
            self.nextToken()
            right_rule_tok = rule_b()
            left_rule_tok = BinaryOperatorNode(left_rule_tok,operator_tok,right_rule_tok)
        return left_rule_tok

    def factor(self):

        if self.token.typ in (tok_plus,tok_minus):
            operator_tok = self.token
            self.nextToken()
            value_tok = self.factor()
            return UnaryOperatorNode(operator_tok,value_tok)
        return self.power()

    def power(self):

        return self.binaryOperatorRule(self.call,(tok_power,),self.factor)


    def call(self):
        args_node_tok = []
        var_name_node_tok = self.atom()
        if self.token.typ == tok_lbre:
            self.nextToken()
            if self.token.typ == tok_rbre:
                self.nextToken()
            else:
                args_node_tok.append(self.expression())
                while self.token.typ == tok_comma:
                    self.nextToken()
                    args_node_tok.append(self.expression())
                if self.token.typ != tok_rbre:
                    raise SyntaxError("Error in call")
            return FunctionCallNode(var_name_node_tok,args_node_tok)
        return var_name_node_tok
        
    def atom(self):
        if self.token.typ == tok_var:
            var_name_tok = self.token
            self.nextToken()
            if self.token.typ == tok_colon:
                self.nextToken()
                var_val_tok = self.expression()
                return VariableNode(var_name_tok,var_val_tok)

            elif self.token.match(tok_keyword,'function'):
                return self.function_expression(var_name_tok)

            elif self.token.typ == tok_lsqr:
                index_tok = []
                self.nextToken()
                if self.token.typ == tok_rsqr:
                    raise SyntaxError("Expecting a index value.")
                index_tok.append(self.expression())
                if self.token.typ != tok_rsqr:
                    raise SyntaxError("Expecting a ']' .")
                self.nextToken()
                while self.token.typ == tok_lsqr:
                    self.nextToken()
                    index_tok.append(self.expression())
                    if self.token.typ != tok_rsqr:
                        raise SyntaxError("Expecting a ']'.")
                    self.nextToken()
                    
                if self.token.typ == tok_colon:
                    self.nextToken()
                    var_val_tok = self.expression()
                    return CollectionAssignmentNode(var_name_tok,index_tok,var_val_tok)
                return CollectionAccessNode(var_name_tok,index_tok)
            
            
            return VariableCallNode(var_name_tok)
            
        
        elif self.token.typ == tok_string:
            string_tok = self.token
            index_tok = None
            self.nextToken()
            if self.token.typ == tok_lbre:
                self.nextToken()
                if self.token.typ == tok_rbre:
                    raise SyntaxError("Expecting a index value.")
                index_tok = self.expression()
                if self.token.typ != tok_rbre:
                    raise SyntaxError("Expecting a '}'.")
                self.nextToken()
            return StringNode(string_tok,index_tok)

        elif self.token.typ == tok_input_string:
            inputString = self.token
            self.nextToken()
            return InputNode(inputString)

        elif self.token.match(tok_keyword,'for'):
            return self.for_expression()
        
        elif self.token.typ in (tok_int,tok_float):
            factor_tok = self.token
            self.nextToken()
            return NumberNode(factor_tok)
        elif self.token.typ == tok_lparen:
            self.nextToken()
            expr_tok = self.expression()
            if self.token.typ != tok_rparen:
                raise Exception("Excepted a ')'")
            self.nextToken()
            return expr_tok
        elif self.token.match(tok_keyword,'if'):
            return self.if_experssion()
        elif self.token.typ == tok_lsqr:
            return self.collection_expression()
        


    def collection_expression(self):

        elements_tok = []
        index_val_tok = None
        if self.token.typ != tok_lsqr:
            raise SyntaxError("Expecting a '['")
        self.nextToken()
        if self.token.typ == tok_rsqr:
            self.nextToken()
            return CollectionNode(elements_tok)
        else:
            elements_tok.append(self.expression())
            while self.token.typ == tok_comma:
                self.nextToken()
                if self.token.typ == tok_rsqr:
                    raise SyntaxError("Expecting a value.")
                elements_tok.append(self.expression())
        if self.token.typ != tok_rsqr:
            raise SyntaxError("Expecting a ']'")
        self.nextToken()
        if self.token.typ == tok_lsqr:
            self.nextToken()
            if self.token.typ == tok_rsqr:
                raise SyntaxError("Expecting a index value.")
            index_val_tok = self.expression()
            if self.token.typ != tok_rsqr:
                raise SyntaxError("Expecting a '}'.")
            self.nextToken()
        return CollectionNode(elements_tok,index_val_tok)
        
    def for_expression(self):

        if not self.token.match(tok_keyword,'for'):
            raise SyntaxError('Expected a \'for\' keyword')
        self.nextToken()
        
        if self.token.typ != tok_var:
            raise SyntaxError("Expected a 'variable' after 'for' keyword")
        var_name_tok = self.token
        self.nextToken()
        if self.token.typ != tok_lbre:
            raise SyntaxError("Expected a '{'")
        self.nextToken()
        start_val_tok = self.expression()
        if self.token.typ != tok_comma and self.token.typ == tok_rbre:
            self.nextToken()
            if self.token.typ != tok_colon:
                raise SyntaxError("Expected a ':'")
            self.nextToken()
            body_tok = self.expression()
            step_val_tok = NumberNode(Token(tok_int,1))
            end_val_tok = start_val_tok
            start_val_tok = NumberNode(Token(tok_int,0))

            return ForNode(var_name_tok,start_val_tok,end_val_tok,step_val_tok,body_tok)
        self.nextToken()
        end_val_tok = self.expression()
        step_val_tok = None
        if self.token.typ == tok_comma:
            self.nextToken()
            step_val_tok = self.expression()
        
        if self.token.typ != tok_rbre:
            raise SyntaxError("Expected a '}'")
        self.nextToken()
        if self.token.typ != tok_colon:
            raise SyntaxError("Expected  a ':'")
        self.nextToken()
        body_tok = self.expression()

        return ForNode(var_name_tok,start_val_tok,end_val_tok,step_val_tok,body_tok)

    def if_experssion(self):
        cases = []
        else_case = None
        self.nextToken()
        if self.token.typ != tok_lbre:
            return SyntaxError("Expecting a '}'")
        self.nextToken()
        condition = self.expression()
        if self.token.typ != tok_rbre:
            raise SyntaxError("Expected a '}'")
        self.nextToken()
        if self.token.typ != tok_colon:
            raise SyntaxError("Expected a ':'")
        self.nextToken()
        expr = self.expression()
        cases.append((condition,expr))

        while self.token.match(tok_keyword,'elif'):
            self.nextToken()
            if self.token.typ != tok_lbre:
                raise SyntaxError("Expeecting a '{'")
            self.nextToken()
            condition = self.expression()
            if self.token.typ != tok_rbre:
                raise SyntaxError("Expecting a '}'")
            self.nextToken()
            if self.token.typ != tok_colon:
                raise SyntaxError("Expected a ':'")
            self.nextToken()
            expr = self.expression()
            cases.append((condition,expr))
            if self.token.typ == tok_colon:
                raise SyntaxError("UnExpected ':")
        if self.token.match(tok_keyword,'else'):
            self.nextToken()
            if self.token.typ != tok_colon:
                raise SyntaxError("Expected a ':' after 'else' keyword")
            self.nextToken()
            else_case = self.expression()
        
        return IfNode(cases,else_case)


    def function_expression(self,var_name_tok = None):
        args_name_tok = []
        if not self.token.match(tok_keyword,'function'):
            raise SyntaxError("Expected a 'function' keyword")
        self.nextToken()
        if self.token.typ != tok_lbre:
            raise SyntaxError("Expecting a '{' after 'function'  keyword")
        self.nextToken()
        if self.token.typ == tok_var:
            args_name_tok.append(self.token)
            self.nextToken()
            while self.token.typ == tok_comma:
                self.nextToken()
                args_name_tok.append(self.token)
                self.nextToken()
        if self.token.typ != tok_rbre:
            raise SyntaxError("Expecting a '}' ")
        self.nextToken()
        if self.token.typ != tok_colon:
            raise SyntaxError("Expecting a ':'")
        self.nextToken()
        body_node_tok = self.expression()
        return FunctionNode(var_name_tok,args_name_tok,body_node_tok)
    
class NumberType:

    def __init__(self,number):
        self.number = number

    def __repr__(self):
        return f"{self.number}"

    def __add__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(self.number+operand.number)
        
    def __mul__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(self.number*operand.number)
    def __divide__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(self.number/operand.number)
        
    def __minus__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(self.number-operand.number)
        
    def __floor__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(self.number//operand.number)
        
    def __mod__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(self.number%operand.number)
        
    def __power__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(self.number**operand.number)
        
    def __lesser__(self,operand):
        if isinstance(operand,NumberType):
            return BoolType(tok_true if self.number < operand.number else tok_false)
        
    def __lessereql__(self,operand):
        if isinstance(operand,NumberType):
            return BoolType(tok_true if self.number <= operand.number else tok_false)
        
    def __greater__(self,operand):
        if isinstance(operand,NumberType):
            return BoolType(tok_true if self.number > operand.number else tok_false)
        
    def __greatereql__(self,operand):
        if isinstance(operand,NumberType):
            return BoolType(tok_true if self.number >= operand.number else tok_false)
        
    def __noteql__(self,operand):
        if isinstance(operand,NumberType):
            return BoolType(tok_true if self.number != operand.number else tok_false)
        
    def __eql__(self,operand):
        if isinstance(operand,NumberType):
            return BoolType(tok_true if self.number == operand.number else tok_false)
        
    
    def __andGate__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(int(self.number and operand.number))

    def __orGate__(self,operand):
        if isinstance(operand,NumberType):
            return NumberType(int(self.number or operand.number))

    def __notGate__(self):
        return NumberType(not self.value)

    def __true__(self):
        return self.number != 0

class BoolType:

    def __init__(self,bool_type):
        self.bool_type = bool_type

    def __repr__(self):
        return f"{self.bool_type}"

    def __true__(self):
        if self.bool_type == tok_true:
            return True
        return False

class StringType:

    def __init__(self,string):
        self.string = string

    def __repr__(self):
        return f"{self.string}"

    def __add__(self,operand):
        if isinstance(operand,StringType):
            return StringType(self.string+operand.string)

    def __mul__(self,number):
        if isinstance(number,NumberType):
                return StringType(self.string*number.number)
            
    def __lesser__(self,operand):
        if isinstance(operand,StringType):
            
            return BoolType(tok_true if self.string<operand.string else tok_fasle)
    def __lessereql__(self,operand):
        if isinstance(operand,StringType):
            return BoolType(tok_true if self.string<=operand.string else tok_false)
    def __greater__(self,operand):
        if isinstance(operand,StringType):
            return BoolType(tok_true if self.string>operand.string else tok_false)
    def __greatereql__(self,operand):
        if isinstance(operand,StringType):
            return BoolType(tok_true if self.string>=operand.string else tok_false)
    def __noteql__(self,operand):
        if isinstance(operand,StringType):
            return BoolType(tok_true if self.string!=operand.string else tok_false)
    def __eql__(self,operand):
        if isinstance(operand,StringType):
            return BoolType(tok_true if self.string==operand.string else tok_false)
    
    def __andGate__(self,operand):
        if isinstance(operand,StringType):
            return NumberType(self.string and operand.string)

    def __orGate__(self,operand):
        if isinstance(operand,StringType):
            return NumberType(self.string or operand.string)


    def __true__(self):
        return len(self.string)>0

class FunctionType:

    def __init__(self,fun_name,fun_args,fun_body):
        self.fun_name = fun_name
        self.fun_args = fun_args
        self.fun_body = fun_body

    def __repr__(self):
        return f"functionType:{self.fun_name} {self.fun_args}"

    def execute(self,args):
        interpretor = Interpretor()
        if len(args)>len(self.fun_args):
            return f"Too many arguments passed to function {self.fun_name}"
        elif len(args)<len(self.fun_args):
            return f"Too low arguments passed to function {self.fun_name}"

        for args_no in range(len(self.fun_args)):
            symboltable[self.fun_args[args_no]] = args[args_no]

        return interpretor.process(self.fun_body)

class CollectionType:

    def __init__(self,elements):
        self.elements = elements

    def __repr__(self):
        return f"{self.elements}"

    def __add__(self,operand):
        if isinstance(operand,CollectionType):
            return CollectionType(self.elements+operand.elements)

    def __index__(self,index):
        
        if isinstance(index,NumberType):
            return self.elements[index.number]
        elif isinstance(index,list):
            print("list")

    def __mul__(self,operand):
        if isinstance(operand,NumberType):
            return CollectionType(self.elements*operand.number)

        
symboltable = {}

class Interpretor:

    def process(self,node):
        method = getattr(self,f'process_{type(node).__name__}',self.no_process)
        return method(node)

    def process_VariableNode(self,node):
        var_name_val = node.var_name_tok.val
        symboltable[var_name_val] = self.process(node.var_val_tok)

    
    def process_VariableCallNode(self,node):
        var_name_val = node.var_name_tok.val
        try:
            if var_name_val in symboltable:
                return symboltable[var_name_val]
            raise NameError(f"NameError : variable '{var_name_val}' is not defined.")
        except Exception as error:
            return error

    def process_FunctionNode(self,node):
        function_name = node.var_name_tok.val if node.var_name_tok else None
        function_body_node = node.body_tok
        function_args = [args.val for args in node.args_tok]
        function = FunctionType(function_name,function_args,function_body_node)
        if function_name:
            symboltable[function_name] = function
            return
        return function

    def process_FunctionCallNode(self,node):
        function = self.process(node.var_name_tok)
        function_args = []
        for args in node.args_tok:
            function_args.append(self.process(args))

        return function.execute(function_args)

    def process_BinaryOperatorNode(self,node):
        left_operand_val = self.process(node.left_operand_tok)
        right_operand_val = self.process(node.right_operand_tok)

        if node.operator_tok.typ == tok_plus:
            return left_operand_val.__add__(right_operand_val)
        elif node.operator_tok.typ == tok_minus:
            return left_operand_val.__minus__(right_operand_val)
        elif node.operator_tok.typ == tok_mul:
            return left_operand_val.__mul__(right_operand_val)
        elif node.operator_tok.typ == tok_divide:
            return left_operand_val.__divide__(right_operand_val)
        elif node.operator_tok.typ == tok_mod:
            return left_operand_val.__mod__(right_operand_val)
        elif node.operator_tok.typ == tok_power:
            return left_operand_val.__power__(right_operand_val)
        elif node.operator_tok.typ == tok_floor:
            return left_operand_val.__floor__(right_operand_val)
        elif node.operator_tok.typ == tok_lesser:
            return left_operand_val.__lesser__(right_operand_val)
        elif node.operator_tok.typ == tok_lesser_eql:
            return left_operand_val.__lessereql__(right_operand_val)
        elif node.operator_tok.typ == tok_greater:
            return left_operand_val.__greater__(right_operand_val)
        elif node.operator_tok.typ == tok_greater_eql:
            return left_operand_val.__greatereql__(right_operand_val)
        elif node.operator_tok.typ == tok_not_eql:
            return left_operand_val.__noteql__(right_operand_val)
        elif node.operator_tok.typ == tok_eql:
            return left_operand_val.__eql__(right_operand_val)
        elif node.operator_tok.typ == tok_and:
            return left_operand_val.__andGate__(right_operand_val)
        elif node.operator_tok.typ == tok_or:
            return left_operand_val.__orGate__(right_operand_val)
        elif node.operator_tok.typ == tok_not:
            return left_operand_val.__notGate__()


    def process_NumberNode(self,node):
        return NumberType(node.number_tok.val)

    def process_UnaryOperatorNode(self,node):
        number = self.process(node.value_tok)
        if node.operator_tok.typ == tok_minus:
            return number.__mul__(NumberType(-1))
        return number

    def process_CollectionNode(self,node):
    
        elements = [self.process(elements_node) for elements_node in node.elements_tok]
        return CollectionType(elements)

    
    def process_CollectionAssignmentNode(self,node):
        collection_name = node.var_name_tok.val
        index_val = [self.process(index_tok) for index_tok in node.index_tok]
        assign_val = self.process(node.val_tok)
        nested_table = {}
        if len(index_val) == 1:
            symboltable[collection_name].elements[index_val[0].number] = assign_val


    def process_CollectionAccessNode(self,node):
        collection_name = node.var_name_tok.val
        index_val = [self.process(index_tok) for index_tok in node.index_tok]
        if isinstance(symboltable[collection_name],CollectionType):
            stored_value_in_collection = None
            for index in index_val:
                if not stored_value_in_collection:
                    stored_value_in_collection = symboltable[collection_name].elements[index.number]
                else:
                    if isinstance(stored_value_in_collection,CollectionType):
                        stored_value_in_collection = stored_value_in_collection.elements[index.number]
                    else:
                        stored_value_in_collection = stored_value_in_collection[index.number]
            return stored_value_in_collection
        
    def process_ForNode(self,node):
        start_val = self.process(node.start_val_tok)
        end_val = self.process(node.end_val_tok)
        step_val = self.process(node.step_val_tok)
        var_name = node.var_name_tok.val
        condition = None

        
        if start_val.number < end_val.number:
            condition = lambda : start_val.number<end_val.number
        else:
            condition = lambda : start_val.number>end_val.number

        if step_val == None:
            step_val = NumberType(1)
        while condition():
            
            symboltable[var_name] = start_val
            val_tok = self.process(node.body_tok)
            if val_tok: print(val_tok)
            start_val.number = start_val.number + step_val.number
        return None



    def process_IfNode(self,node):

        for condition,expr in node.cases:
            condition = self.process(condition)
            if condition.__true__():
                expr = self.process(expr)
                return expr
        else_case = self.process(node.else_case)
        return else_case

    def process_StringNode(self,node):
        return StringType(node.string_tok.val)

    def process_InputNode(self,node):
        input_val = input(node.input_string_tok.val)
        if not input_val.isdigit():
            return StringType(input_val)
        return NumberType(int(input_val))
    
    def no_process(self,node):
        return
        return f"no process_{type(node).__name__}"


def IDE():
    import os
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
