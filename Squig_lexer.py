import  ply.lex as lex
import  ply.yacc as yacc

sym = {}
tokens = ('string',
          'id',
          'float',
          'assign',
          'plus',
          'num',
          'lbrace',
          'rbrace',
          'typecast')


t_lbrace = r'\{'
t_rbrace = r'\}'
t_plus = r'\+'
t_assign = r'='


def t_float(t):
    r'([0-9]*\.[0-9]+)'
    t.value = float(t.value)
    return t

def t_num(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_typecast(t):
    r'[iflrtvm]\{'
    return t

def t_id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_string(t):
    r'\"[^\n"]*\"'
    return t

def t_error(t):
    t.lexer.skip(1)
    
t_ignore = ' \t\n'

lexer = lex.lex()

def p_assign(p):
    ''' statement : id assign string
                  | id assign id
                  | id assign num
                  | id assign float
                  | id plus assign string'''
    
    if type(p[3]) == int:
        sym[p[1]] = p[3]
    elif type(p[3]) == float:
        sym[p[1]]  = p[3]
    elif p[3] in sym:
        sym[p[1]] = sym[p[3]]
    elif '\"' in p[3]:
        sym[p[1]] = p[3][1:-1]
    elif p[2]+p[3] == '+=':
        sym[p[1]] = sym[p[1]]+p[4][1:-1]
    else:
        print(f"AssigmentError : Operand {p[2]} is invalid.")



def p_print_statement(p):
    '''statement : lbrace string rbrace
                 | lbrace num rbrace
                 | lbrace id rbrace
    '''
    if p[2] in sym:
        print(sym[p[2]])
    elif type(p[2]) == int:
        print(p[2])
        os.startfile(p[4])
    elif '\"' in p[2]:
        print(p[2][1:-1])
    else:
        print(f"IdError : name '{p[2]}' is not defined.")

def p_input_statement(p):
    '''statement : id assign lbrace string rbrace
                 | id assign typecast string rbrace
    '''
    if p[3] == 'i{':
        sym[p[1]] = int(input(p[4][1:-1]))
    elif p[3] == 'f{':
        sym[p[1]] = float(input(p[4][1:-1]))
    elif p[3] == 'l{':
        sym[p[1]] = len(input(p[4][1:-1]))
    elif p[3] == 'r{':
        sym[p[1]] = input(p[4][1:-1])[::-1]
    elif p[3] == 't{':
        tab = ''
        sym[p[1]] = input(p[4][1:-1])
        for char in sym[p[1]]:
            tab += char+' '
        sym[p[1]] = tab
    elif p[3] == 'v{':
        ver = ''
        sym[p[1]] = input(p[4][1:-1])
        for char in sym[p[1]]:
            ver += char+'\n'
        sym[p[1]] = ver
    else:
        sym[p[1]] = input(p[4][1:-1])

def p_music_statement(p):
    '''statement : typecast string rbrace
                 | typecast id rbrace'''
    import pygame
    from pygame import mixer_music as music
    pygame.init()
    if p[1] == 'm{':
        if '\"' in p[2]:
            music.load(p[2][1:-1])
        elif p[2] in sym:
            music.load(sym[p[2]])
        music.play()
                   
parser = yacc.yacc()

while True:
    try:
        prompt = input('\n>>>')
    except:
        break

    parser.parse(prompt)
    
