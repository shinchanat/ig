import  ply.lex as lex
import  ply.yacc as yacc



with open('Squig_logo.txt') as logo:
    print(logo.read())


sym = {}
condition_state = 0

tokens = ['string','id','float','assign','num','lbrace','rbrace','typecast']

t_lbrace = r'\{'
t_rbrace = r'\}'
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
    r'([iflrtvmV]\{)'
    return t

def t_string(t):
    r'\"[^\n"]*\"'
    return t


def t_id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t):
    t.lexer.skip(1)
    
t_ignore = ' \t\n'

lexer = lex.lex()

def p_assign_num(p):
    '''statement : id assign num'''
    if p[3] in sym:
        sym[p[1]] = p[3]
    elif type(p[3]) == int:
        sym[p[1]] = p[3]
    elif type(p[3]) == float:
        sym[p[1]] = p[3]
    else:
        sym[p[1]] = p[3]
        
def p_assign_float(p):
    '''statement : id assign float'''
    sym[p[1]] = p[3]
    
def p_assign_id(p):
    '''statement : id assign id'''
    if p[3] in sym:
        sym[p[1]] = p[3]
    else:
        print(f"IDError : name '{p[3]}' is not defined.")
        
def p_assign_string(p):
    '''statement : id assign string'''
    sym[p[1]] = p[3][1:-1]

def p_input_statement(p):
    '''statement : id assign lbrace string rbrace'''
    sym[p[1]] = input(p[4][1:-1])

def p_print_string(p):
    
    '''statement : lbrace string rbrace'''
    p[0] = p[2][1:-1]

def p_print_num(p):
    
    '''statement : lbrace num rbrace
                 | lbrace float rbrace '''

    if type(p[2]) == int:
        p[0]=int(p[2])
    elif type(p[2]) == float:
        p[0]=float(p[2])

def p_print_id(p):

    '''statement : lbrace id rbrace'''
    
    if type(p[2]) == int:
        p[0]=int(sym[p[2]])
    elif type(p[2]) == str:
        p[0]=sym[p[2]]
    elif type(p[2]) == float:
        p[0]=float(sym[p[2]])
    
def p_typecast_input(p):
    
    '''statement : id assign typecast string rbrace'''
    
    match p[3]:
        case 'i{':
            sym[p[1]] = int(input(p[4][1:-1]))
        case 'f{':
            sym[p[1]] = float(input(p[4][1:-1]))
        case 'l{':
            sym[p[1]] = len(input(p[4][1:-1]))
        case 'r{':
            sym[p[1]] = input(p[4][1:-1])[::-1]
        case 't{':
            tab = ''
            sym[p[1]] = input(p[4][1:-1])
            for char in sym[p[1]]:
                tab += char+' '
            sym[p[1]] = tab
        case 'v{':
            ver = ''
            sym[p[1]] = input(p[4][1:-1])
            for char in sym[p[1]]:
                ver += char+'\n'
            sym[p[1]] = ver

def p_media_statement(p):
    '''statement : typecast string rbrace
                 | typecast id rbrace'''
    
    if p[1] == 'm{':
        import pygame,os
        from pygame import mixer_music as music
        pygame.init()
        try:
            if '\"' in p[2]:
                if '.mp3' in p[2]:
                    music.load(p[2][1:-1])
                    music.play()
                elif '.mp4' in p[2]:
                    os.startfile(p[2][1:-1])
            elif p[2] in sym:
                if '.mp3' in sym[p[2]]:
                    music.load(sym[p[2]])
                    music.play()
                elif '.mp4' in sym[p[2]]:
                    os.startfile(sym[p[2]])
        except:
                print("FileNotFoundError")

def p_error(p):
    pass
            
parser = yacc.yacc()

while True:
    try:
        prompt = input('\n$~$~$ ')
        if prompt == 'exit' or prompt == 'quit':
            break
    except:
        break

    stdout = parser.parse(prompt)

    if stdout:
        print(stdout)
