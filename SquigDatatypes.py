
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

        
