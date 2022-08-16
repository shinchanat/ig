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
