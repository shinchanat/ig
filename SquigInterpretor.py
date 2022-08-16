from SquigDatatypes import *

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
