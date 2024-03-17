'''
Analizador sintáctico - Lenguaje de Programación Latino
Reinaldo Toledo Leguizamón
Monitoría de Lenguajes de programación
2024-1

'''

import re

EOF = False

class Token():
    
    
    def __init__(self,token,lexem,line,position):
        self.token = token
        self.lexem = lexem
        self.line = line
        self.position = position

class Parser():
    
    prediction_set = set([])
    stack =[]
    error=False
    
    grammar = {
        'P':[
            ['R','V','F_P','M']
            ],
        'R':[
            ['registro','id','V','fin','registro'],
            ['empty']
            ],
        'V':[
            ['V_1','V'],
            ['empty']
            ],
        'V_1':[
            ['arreglo','tkn_opening_bra','PA','tkn_closing_bra','de','T','id','V_2'],
            ['T','id','V_2']
            ],
            
        'V_1_PF':[
            ['arreglo','tkn_opening_bra','PA','tkn_closing_bra','de','T','id'],
            ['T','id']
            ],
        
        'V_2':[
                ['tkn_comma','id','V_2'],
                ['empty']
            ],
            
        'PA':[
            ['tkn_integer','PAm'],
            ],
        'PAm':[
            ['tkn_comma','tkn_integer','PAm'],
            ['empty']
            ],
        'T':[
            ['entero'],
            ['real'],
            ['booleano'],
            ['cadena','tkn_opening_bra','tkn_integer','tkn_closing_bra'],
            ['caracter'],
            ['id'],
            ],
        'F_P':[
            ['F','F_P'],
            ['PR','F_P'],
            ['empty']
            ],
        'F':[
            ['funcion','id','PARp','tkn_colon','T','V','inicio','S','F_1','fin']
            ],
            
        'F_1':[
                ['retorne', 'EXP'],
                ['empty']
            ],
        'PAR':[
            ['tkn_opening_par','V_1','PAR_1','tkn_closing_par'],
            ['empty']
            ],
            
        'PAR_1':[
                ['tkn_comma','V_1','PAR_1'],
                ['empty']
            ],
        
        'PR':[
            ['procedimiento','id','PARp','V','inicio','S','fin']
            ],
        
        'PARp':[
            ['tkn_opening_par','PARp_1','tkn_closing_par'],
            ['empty']
            ],
        'PARp_1':[
                ['var','V_1_PF','PARp_2'],
                ['V_1_PF','PARp_2']
            ],
        'PARp_2':[
                ['tkn_comma','PARp_1'],
                ['empty']
            ],
        
        'M': [
            ['inicio','S','fin']
            ],
        
        'S':[
             ['L','S'],
             ['CO','S'],
             ['A','S'],
             ['E','S'],
             ['CA','S'],
             ['CAL','S'],
             ['empty'],
            ],
        
        'L':[
                ['mientras','EXP','haga','S','fin','mientras'],
                ['repita','S','hasta','EXP'],
                ['para','A','hasta','EXP','haga','S','fin','para'],
            ],
        'CO':[
                ['si','EXP','entonces','S','CO_1','fin','si']
                #['si','EXP_C','entonces','S','fin','si']
            ],
        'CO_1':[
                #['sino','si','EXP_C','entonces','S','CO_1','fin', 'si'],
                ['sino','S'],
                ['empty']
            ],
            
        'A':[
                ['id','AC','tkn_assign','EXP'],
        
            ],
        'AC':[
                ['tkn_period','id','AC'],
                ['tkn_opening_bra','EXP','AC_1','tkn_closing_bra','AC_2','AC'],
                ['empty']
            ],
            
        'AC_2':[
                ['tkn_period','id','AC_2','AC'],
                ['empty']
            ],
        
        'AC_1':[
                ['tkn_comma','EXP','AC_1'],
                ['empty']
            ],
        'E':[
                ['escriba','EXP','E_exp'],
                ['lea','id','AC','V_2']
            ],
        'E_exp':[
                ['tkn_comma','EXP','E_exp'],
                ['empty']
            ],
        
        'CAL':[
                ['llamar','CAL_ex'],
            ],
        
        'CAL_ex':[
                ['nueva_linea'],
                ['id','ARGS_CAL']
            ],
        'ARGS_CAL':[
                ['tkn_opening_par','ARGS_EXP','tkn_closing_par'],
                ['empty'],
                
            ],
        
        'ARGS_EXP':[
                ['EXP','AC_1'],
                ['empty']
            ],
            
        'ARGS':[
                ['tkn_opening_par','EXP','AC_1','tkn_closing_par'],
            ],
        
        'CA':[
                ['caso','id','AC','CA_SEC','tkn_colon','S','CA_OP','fin','caso']
            ],
        
        'CA_OP':[
                ['CA_SEC','tkn_colon','S','CA_OP'],
                ['sino','tkn_colon','S'],
                ['empty']
            ],
            
        'CA_SEC':[
                
                ['VAL','CA_SEC_1']
            ],
        'CA_SEC_1':[
                ['tkn_comma','VAL','CA_SEC_1'],
                ['empty']
            ],
        'VAL':[
                
                ['tkn_integer'],
                ['tkn_real'],
                ['tkn_char'],
                ['tkn_str'],
                ['verdadero'],
                ['falso']
            ],
        
        'EXP':[
                ['Te','OP_E'],
                ['tkn_opening_par','EXP','tkn_closing_par','OP_E'],
            ],
        
        
        
        'OP_E':[
                ['OP_A','EXP'],
                ['OP_L','EXP'],
                ['OP_R','OP_EA','OP_EL'],
                ['empty']
            ],
            
        'OP_EA':[
                ['tkn_opening_par','Te','OP_AOP','tkn_closing_par','OP_AOP'], # error partialy fixed
                #['tkn_opening_par','Te','OP_AOP','tkn_closing_par'],
                ['Te','OP_AOP'],
            ],
        
        'OP_AOP':[
                ['OP_A','OP_EA'],
                ['empty']
            ],
            
        'OP_EL':[
                ['OP_L','EXP'],
                ['empty']
            ],
        
        'Te':[
                ['tkn_minus','Te'],
                ['VAL'],
                ['id','Te_id'],
            ],
        
        'Te_id':[
                
                ['ARGS'],
                ['AC']
            ],
        
        'OP_A':[
                ['tkn_minus'],
                ['tkn_plus'],
                ['tkn_times'],
                ['tkn_power'],
                ['tkn_div'],
                ['div'],
                ['mod'],
            ],
        'EXP_C':[
                ['tkn_opening_par','EXP_C','tkn_closing_par','EXP_C_1'],
                ['EXP','OP_R','EXP'],
            ],
        
        'EXP_C_1':[
                ['OP_L','tkn_opening_par','EXP','OP_R','EXP','tkn_closing_par','EXP_C_1'],
                ['empty']
            ],
        'OP_R':[
            ['tkn_equal'],
            ['tkn_less'],
            ['tkn_greater'],
            ['tkn_leq'],
            ['tkn_geq'],
            ['tkn_neq']
        ],
        'OP_L':[
          ['o'],
          ['y']
        ],
        
        
    }

            
            
            
            
            
            
    
    
    
    def analize(self,token):
        #print("*************************** Next Token *******************")
        #self.showTokenInfo(token)
        #print("Prediction set before the match algorithm",self.prediction_set)
        match=False
        #print("Stack before the match algorithm: ",self.stack)
        
        #print("******************** Starting match process *******************")
    
        
        while(match==False):
          
            if(len(self.stack) < 1):
                self.error=True
                self.reportError(token)
                break
            
            current_element = self.stack.pop()
            
            
            
            
            if(current_element[0].isupper()):
                
                current_no_terminal = current_element
                
            
            
                #print("Current no terminal rules:",self.grammar[current_no_terminal])
                
                rule = self.lookForMatchRule(current_no_terminal,token)
                
                #print("Rule that must be applied",rule)
                
                #print("Updated prediction set: ",self.prediction_set)
                
                if(rule=='error'):
                    #print("Error sintáctico")
                    self.error=True
                    self.reportError(token)
                    break
                else:
                    for i in reversed(rule):
                        
                        if i!="empty":
                            self.stack.append(i)
                    
                    #print("Updated stack: ",self.stack)
                
                
                    
            else:
                
                self.prediction_set.add(current_element)
                
                if(current_element==token.token):
                    match=True
                    #print("*************************** Token matched successfully *******************")
                    self.prediction_set.clear()
                    break
                else:
                    self.error = True
                    self.reportError(token)
                    break
                
        
        
        self.finishCatchUp=False
    
    
    def lookForMatchRule(self,current_no_terminal,token):
        
        match = 'error'
        
        for i in self.grammar[current_no_terminal]:
            
            if(i[0][0].isupper()):
                possible = self.lookForMatchRule(i[0],token)
                
                #print("Possible match across another rule: "+i[0],possible)
                
                if(possible!='error'):
                    match = i
                    return match
                    break
                
            elif(i[0]=="empty"):
                #current_element=self.stack.pop()
                return i
                break
            
            elif(i[0]==token.token):
                return i
                break
                
            else:
                self.prediction_set.add(i[0])
                
            
        
        if(match == 'error'):
            return match
            
        
    
    def showTokenInfo(self,token):
        print("<"+str(token.token)+","+str(token.lexem)+","+str(token.line)+","+str(token.position)+">")
        
        
    
    
    
    
    
    def reportError(self,token):
        
        if token.lexem=='assign':
                token.lexem='<-'
                
        elif token.lexem == 'period':
            token.lexem ='.'
        
        elif token.lexem == 'comma':
            token.lexem=','
            
        elif token.lexem == 'colon':
            token.lexem=':'
        
        elif token.lexem == 'closing_bra':
            token.lexem=']'
        
        elif token.lexem == 'opening_bra':
            token.lexem='['
            
        elif token.lexem == 'closing_par':
            token.lexem=')'
            
        elif token.lexem == 'opening_par':
            token.lexem='('
            
        elif token.lexem == 'plus':
            token.lexem='+'
            
        elif token.lexem == 'minus':
            token.lexem='-'
            
        elif token.lexem == 'times':
            token.lexem='*'
            
        elif token.lexem == 'div':
            token.lexem='/'
            
        elif token.lexem == 'power':
            token.lexem='^'
            
        elif token.lexem == 'equal':
            token.lexem='='
            
        elif token.lexem == 'neq':
            token.lexem='<>'
            
        elif token.lexem == 'less':
            token.lexem='<'
            
        elif token.lexem == 'leq':
            token.lexem='<='
            
        elif token.lexem == 'greater':
            token.lexem='>'
            
        elif token.lexem == 'geq':
            token.lexem ='>='
            
        elif token.lexem == "EOF":
            token.lexem="final de archivo"
        
        
        print("<{}:{}> Error sintactico: se encontro: \"{}\"; se esperaba:".format(str(token.line),str(token.position),token.lexem),end="")
        
        
        report_prediction_set = list(self.prediction_set)
        
        
        for i in range(len(report_prediction_set)):
            if report_prediction_set[i]=='tkn_integer':
                report_prediction_set[i]='valor_entero'
                
            elif report_prediction_set[i]=='tkn_real':
                report_prediction_set[i]='valor_real'
                
            elif report_prediction_set[i]=='tkn_char':
                report_prediction_set[i]='caracter_simple'
                
            elif report_prediction_set[i]=='tkn_str':
                report_prediction_set[i]='cadena_de_caracteres'
        
        
        report_prediction_set.sort()
        
        
        for i in range(len(report_prediction_set)):
            
            if report_prediction_set[i]=='tkn_assign':
                report_prediction_set[i]='<-'
                
            elif report_prediction_set[i] == 'tkn_period':
                report_prediction_set[i]='.'
            
            elif report_prediction_set[i] == 'tkn_comma':
                report_prediction_set[i]=','
                
            elif report_prediction_set[i] == 'tkn_colon':
                report_prediction_set[i]=':'
            
            elif report_prediction_set[i] == 'tkn_closing_bra':
                report_prediction_set[i]=']'
            
            elif report_prediction_set[i] == 'tkn_opening_bra':
                report_prediction_set[i]='['
                
            elif report_prediction_set[i] == 'tkn_closing_par':
                report_prediction_set[i]=')'
                
            elif report_prediction_set[i] == 'tkn_opening_par':
                report_prediction_set[i]='('
                
            elif report_prediction_set[i] == 'tkn_plus':
                report_prediction_set[i]='+'
                
            elif report_prediction_set[i] == 'tkn_minus':
                report_prediction_set[i]='-'
                
            elif report_prediction_set[i] == 'tkn_times':
                report_prediction_set[i]='*'
                
            elif report_prediction_set[i] == 'tkn_div':
                report_prediction_set[i]='/'
                
            elif report_prediction_set[i] == 'tkn_power':
                report_prediction_set[i]='^'
                
            elif report_prediction_set[i] == 'tkn_equal':
                report_prediction_set[i]='='
                
            elif report_prediction_set[i] == 'tkn_neq':
                report_prediction_set[i]='<>'
                
            elif report_prediction_set[i] == 'tkn_less':
                report_prediction_set[i]='<'
                
            elif report_prediction_set[i] == 'tkn_leq':
                report_prediction_set[i]='<='
                
            elif report_prediction_set[i] == 'tkn_greater':
                report_prediction_set[i]='>'
                
            elif report_prediction_set[i] == 'tkn_geq':
                report_prediction_set[i]='>='
        
        if(len(report_prediction_set)==0):
            report_prediction_set.append('final de archivo')
        
        for i in range(len(report_prediction_set)):
            print(" \"{}\"".format(report_prediction_set[i]),end="")
            
            if(i!=len(report_prediction_set)-1):
                print(",",end="")
            else:
                print(".",end="")

class Lexer():
    
    error=False
    block_comment=False
    block_comment_line=0
    block_comment_position=0
    
    regex_dict={
    'acadena':r'\bacadena\b(?![\w_])',
    'alogico':r'\balogico\b(?![\w_])',
    'anumero':r'\banumero\b(?![\w_])',
    'caso':r'\bcaso\b(?![\w_])',
    'cierto':r'\bcierto\b(?![\w_])',
    'defecto':r'\bdefecto\b(?![\w_])',
    'desde':r'\bdesde\b(?![\w_])',
    'elegir':r'\belegir\b(?![\w_])',
    'en':r'\ben\b(?![\w_])',
    'escribir':r'\bescribir\b(?![\w_])',
    'falso':r'\bfalso\b(?![\w_])',
    'fin':r'\bfin\b(?![\w_])',
    'fun':r'\bfun\b(?![\w_])',
    'funcion':r'\bfuncion\b(?![\w_])',
    'hasta':r'\bhasta\b(?![\w_])',
    'imprimir':r'\bimprimir\b(?![\w_])',
    'imprimirf':r'\bimprimirf\b(?![\w_])',
    'leer':r'\bleer\b(?![\w_])',
    'limpiar':r'\blimpiar\b(?![\w_])',
    'mientras':r'\bmientras\b(?![\w_])',
    'nulo':r'\bnulo\b(?![\w_])',
    'osi':r'\bosi\b(?![\w_])',
    'otro':r'\botro\b(?![\w_])',
    'para':r'\bpara\b(?![\w_])',
    'poner':r'\bponer\b(?![\w_])',
    'fin':r'\bfin\b(?![\w_])',
    'rango':r'\brango\b(?![\w_])',
    'repetir':r'\brepetir\b(?![\w_])',
    'ret':r'\bret\b(?![\w_])',
    'retornar':r'\bretornar\b(?![\w_])',
    'retorno':r'\bretorno\b(?![\w_])',
    'romper':r'\bromper\b(?![\w_])',
    'si':r'\bsi\b(?![\w_])',
    'sino':r'\bsino\b(?![\w_])',
    'tipo':r'\btipo\b(?![\w_])',
    'verdadero':r'\bverdadero\b(?![\w_])',
    }
    
    
    symbols_regex_dict = {
        'and':r'&&',
        'or':r'\|\|',
        'concat':r'\.\.',
        'plus_assign':r'\+=',
        'minus_assign':r'\-=',
        'times_assign':r'\*=',
        'div_assign':r'/=',
        'mod_assign':r'%=',
        'increment':r'\+\+',
        'decrement':r'\-\-',
        'period':r'\.',
        'comma':r',',
        'semicolon':r';',
        'colon':r':',
        'opening_key':r'{',
        'closing_key':r'}',
        'closing_bra':r'\]',
        'opening_bra':r'\[',
        'closing_par':r'\)',
        'opening_par':r'\(',
        'plus':r'\+',
        'minus':r'\-',
        'times':r'\*',
        'div':r'/',
        'power':r'\^',
        'mod':r'%',
        'equal':r'==',
        'neq':r'!=',
        'leq':r'<=',
        'geq':r'>=',
        'greater':r'>',
        'less':r'<',
        'regex':r'~=',
        'assign':r'=',
        'not':r'!',
        
        
    }
    
    def match_symbol(self,code,line,end_index,position):
        
        found=False
        
        for key in self.symbols_regex_dict:
            
            #print("the code: ",code ,"; and the regex: ",self.symbols_regex_dict[key])
            #print(key,": ",re.match(self.symbols_regex_dict[key],code))
            
           
            if re.match(self.symbols_regex_dict[key], code) != None:

                self.report_token("tkn_"+key,key,line,position+1,True)
                end_index = re.match(self.symbols_regex_dict[key], code).end()
                position+=end_index
                found=True
                break
        
        if(found==False):
            self.report_error(line,position+1)
        
        return end_index
    
    def match_string(self,code,line,end_index,position):
        
        string_match = r'\"(.*?[^\\])\"|\'(.*?[^\\])\'|\"\"|\'\''
        
        
        if re.match(string_match, code) != None:
            #print("match: ",re.match(string_match, code))
            self.report_token('tkn_str',re.match(string_match, code).group()[1:-1],line,position+1,False)
            end_index = re.match(string_match, code).end()
            position+=end_index
        
        else:
            self.report_error(line,position+1)
        
        return end_index
        
    def match_number(self,code,line,end_index,position):
        
        real_match = r'[0-9]+\.[0-9]+'
        integer_match = r'[0-9]+'
        
        if re.match(real_match, code) != None:
            self.report_token('tkn_real',re.match(real_match, code).group(),line,position+1,False)
            end_index = re.match(real_match, code).end()
            position+=end_index
        
        elif re.match(integer_match, code) != None:
            self.report_token('tkn_real',re.match(integer_match, code).group(),line,position+1,False)
            end_index = re.match(integer_match, code).end()
            position+=end_index
        
        return end_index
    
    def match_char(self,code,line,end_index,position):
        
        char_match = r'\'(.?)\''
        
        if re.match(char_match, code) != None:
            self.report_token('tkn_char',re.match(char_match, code).group().replace('\'',''),line,position+1,False)
            end_index = re.match(char_match, code).end()
            position+=end_index
        else:
            self.report_error(line,position+1)
        
        return end_index
        
    
    
    def match_id(self,code,line,end_index,position):
        
        # Match the id
        
        id_match = r'[a-zA-Z_][0-9a-zA-Z_]*'
        
        if re.match(id_match, code) != None:
            self.report_token('id',re.match(id_match, code).group(),line,position+1,False)
            end_index = re.match(id_match, code).end()
            position+=end_index
        
        return end_index

    
    def match_keywords(self,code,line,end_index,position):
        
        # Match the key words 
        found=False
            
        for key in self.regex_dict:
            
            if re.match(self.regex_dict[key], code) != None:

                self.report_token(key,key,line,position+1,True)
                end_index = re.match(self.regex_dict[key], code).end()
                position+=end_index
                found=True
                break
        
        # Match the ids that start with any letter and those who were not recognized as key words
        if(found==False):
            end_index=self.match_id(code,line,end_index,position)
        
        return end_index
            
    

    def analize(self,code,line):
        end_index=0
        single_line_comment=False
        line_size=len(code)
        position=0
        end_of_line=False
        
        while(line_size>0):
            
            i=0
        
            while(code[i]==' '):
                
                i+=1;
                position+=1;
                if(i==len(code)):
                    break
            
            code = code[i:]
            
            if(len(code)==0):
                break
            
            # Matching comments of single line denoted by //
            if(code[0]=='#' and self.block_comment==False):
                break
            elif(len(code)>=2 and code[0]=='/'):
                if(code[1]=='/' and self.block_comment==False):
                    
                    break
                elif(code[1]=='*'):
                    #print("found block comment: ",code)
                    self.block_comment=True
                    self.block_comment_line=line
                    self.block_comment_position=position
                    code = code[2:]
                    #print("found block comment after cut: ",code)
                    position+=2

                    
            if(len(code)>=2 and code[0]=='*'):
                # Close block comment
                if(code[1]=='/'):
                    #print("code after block comment: ",code)
                    self.block_comment=False
                    self.block_comment_line=0
                    self.block_comment_position=0
                    code = code[2:]
                    position+=2
                    i=0
                    #print("cut code after block comment: ",code)

                    
                    if(len(code)>0):
        
                        if(code[0]==' '):
                            continue
            
            if(len(code)==0):
                break
           

                    
            
            #print("Code by this iteration: ",code)
            if(self.block_comment==False):
                # Match the keywords 
                if(re.match(r'[a-zA-Z]',code[0],re.IGNORECASE)!=None):
                    end_index = self.match_keywords(code,line,end_index,position) #could be commented
                
                # Match the ids that start with _ 
                elif(code[0]=='_'):
                    end_index = self.match_id(code,line,end_index,position) #could be commented
                
                elif(code[0]=='\"' or code[0]=='\''):
                    end_index = self.match_string(code,line,end_index,position)
                    
                elif(re.match(r'[0-9]',code[0])!=None):
                    end_index= self.match_number(code,line,end_index,position)
                
                else:
                    end_index = self.match_symbol(code,line,end_index,position)
                
                position+=end_index
            
            else:
                end_index=1
                position+=1
            
            if(self.error==True):
                break
            
            code = code[end_index:]
            
            #print("Code by this iteration: ",code)
            
            line_size=len(code)
            
            if(len(code)==0):
                break
            
    def report_token(self,token,lexem,line,position,key_word):
        
        if(key_word):
            print("<{},{},{}>".format(token,line,position))
        else:
            print("<{},{},{},{}>".format(token,lexem,line,position))
    
    def report_error(self,line,position):
        self.error=True
        print(">>> Error lexico (linea: {}, posicion: {})".format(line,position))
        


try:
    line=1
    Lpp_parser = Parser()
    Lpp_parser.stack.append('P')
    Lpp_lexer = Lexer(Lpp_parser)
    while True:
        current_line = input()
        Lpp_lexer.analize(current_line,line)
        
        if(Lpp_lexer.error==True):
            break
        
        if(Lpp_lexer.parser.error==True):
            
            #print("Error sintáctico")
            #print("Se esperaba: ",Lpp_lexer.parser.prediction_set)
            break
        line+=1
        
except EOFError:
    EOF=True
    #print("Parser stack after EOF found: ",Lpp_lexer.parser.stack)
    if(EOF==True and Lpp_lexer.block_comment==True):
        Lpp_lexer.report_error(Lpp_lexer.block_comment_line,Lpp_lexer.block_comment_position+1)
    
    if(EOF==True and len(Lpp_lexer.parser.stack)>0):
        #print("Error sintáctico en final de archivo")
        
        EOF_tkn= Token('EOF','EOF',line,1)
        
        Lpp_lexer.parser.analize(EOF_tkn)
        
    else:
        print("El analisis sintactico ha finalizado exitosamente.")