from SquigTokens import *

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
        
