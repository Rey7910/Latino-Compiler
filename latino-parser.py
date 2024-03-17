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
            ['S']
            ],
        'S':[
            ['S_ME','S'],
            ['empty']
        ],
        'S_ME':[
            ['FUN'],
            ['limpiar','tkn_opening_par','tkn_closing_par'],
            ['imprimirf','tkn_opening_par','EXP','tkn_comma','EXP','tkn_closing_par'],
            ['PR_S'],
            ['L_C'],
            ['S_C'],
            ['A'],
            ['CO']
        ],
        'S_M':[
            ['S_ME','S'],
            ['empty']
        ],
        'FUN':[
            ['TKN_FUN','id','tkn_opening_par','AR_FUN','tkn_closing_par','OP_FUN','fin']
        ],
        'AR_FUN':[
            ['id','AR_FUN2'],
            ['empty']
        ],
        'AR_FUN2':[
            ['tkn_comma','id','AR_FUN2'],
            ['empty']
        ],
        'OP_FUN':[
            ['S_M','OP_RET'],
            ['RET_TKN','EXP'],
        ],
        'OP_RET':[
            ['RET_TKN','EXP'],
            ['empty']
        ],
        'RET_TKN':[
            ['retorno'],
            ['retornar']
        ],

        'PR_S':[
            ['PR_TKN','tkn_opening_par','EXP_PR','tkn_closing_par'],
        ],

        'EXP_PR':[
            ['EXP'],
            ['empty'],

        ],

        'PR_TKN':[
            ['imprimir'],
            ['poner'],
            ['escribir'],
        ],

        'L_C':[
            ['F_L'],
            ['W_L'],
            ['D_L'],
            ['DW_L']
        ],
        'F_L':[
            ['para','id','en','rango','tkn_opening_par','ARGS','tkn_closing_par','S_M','fin'],
        ],
        'W_L':[
            ['mientras','EXP','S_M','fin'],
        ],
        'D_L':[
            ['desde','tkn_opening_par','id','AC','AS_OP','EXP','tkn_semicolon','EXP','tkn_semicolon','A','tkn_closing_par','S_M','fin']
        ],
        'DW_L':[
            ['repetir','S_M','hasta','EXP'],
        ],
        'S_C':[
            ['elegir','tkn_opening_par','EXP','tkn_closing_par','C_S_M','DEF','fin']
        ],
        'C_S_M':[
            ['caso','VAL','tkn_colon','C_S2','S_M','C_S']
        ],
        'C_S':[
            ['caso','VAL','tkn_colon','C_S2','S_M','C_S'],
            ['empty']
        ],
        'C_S2':[
            ['caso','VAL',':','C_S2'],
            ['empty']
        ],
        'DEF':[
            ['DEF_TKN','tkn_colon','S_M'],
            ['empty']
        ],
        'DEF_TKN':[
            ['otro'],
            ['defecto']
        ],
        'A':[
            ['id','AC','EFF']
        ],
        'AC':[
            ['tkn_period','id','AC','AC_1'],
            ['tkn_opening_bra','EXP','tkn_closing_bra','AC','AC_1'],
            ['empty']
        ],
        'AC_1':[
            ['tkn_comma','id','AC'],
            ['empty']
        ],
        'ASGBL':[
            ['id','AC_EX']
        ],
        'EFF':[
            ['AS_OP','CONT'],
            ['IN_DEC']
        ],
        'CONT':[
            ['EXP'],
            ['leer','tkn_opening_par','tkn_closing_par']
        ],
        'CO':[
            ['si','EXP','S_M','CO_1','fin']
        ],
        'CO_1':[
            ['osi','EXP','S_M','CO_1'],
            ['empty']
        ],
        'BN':[
            ['acadena','tkn_opening_par','EXP','tkn_closing_par'],
            ['alogico','tkn_opening_par','EXP','tkn_closing_par'],
            ['anumero','tkn_opening_par','EXP','tkn_closing_par'],
            ['tipo','tkn_opening_par','EXP','tkn_closing_par'],
        ],
        'DIC':[
            ['tkn_opening_key','DIC_CONT','tkn_closing_key'],
        ],
        'DIC_CONT':[
            ['EXP','tkn_colon','INNER','DIC_CONT2'],
            ['empty']
        ],
        'DIC_CONT2':[
            ['tkn_comma','EXP','tkn_colon','INNER','DIC_CONT2'],
            ['empty']
        ],
        'LIST':[
            ['tkn_opening_key','LIST_CONT','tkn_closing_key'],
        ],
        'LIST_CONT':[
            ['INNER','LIST_CONT2'],
            ['empty']
        ],
        'LIST_CONT2':[
            ['tkn_comma','INNER','LIST_CONT2'],
            ['empty']
        ],
        'INNER':[
            ['EXP','FUNN_IN']
        ],
        'FUNN_IN':[
            ['TKN_FUN','tkn_opening_par','AR_FUN','tkn_closing_par','OP_FUN','fin']
        ],
        'TKN_FUN':[
            ['fun'],
            ['funcion']
        ],
        
        'EXP':[
            ['TE','OP_E'],
            ['tkn_opening_par','EXP','tkn_closing_par','OP_E']
        ],
        'OP_E':[
            ['OP_A','EXP'],
            ['OP_L','EXP'],
            ['OP_R','OP_EA','OP_EL'],
            ['empty']
        ],
        'OP_EA':[
            ['tkn_opening_par','TE','OP_AOP','tkn_closing_par','OP_AOP'],
            ['TE','OP_AOP']
        ],
        'OP_AOP':[
            ['OP_A','OP_EA'],
            ['empty']
        ],
        'OP_EL':[
            ['OP_L','EXP'],
            ['empty']
        ],
        'TE':[
            ['tkn_plus','TE'],
            ['tkn_not','TE'],
            ['tkn_minus','TE'],
            ['VAL'],
            ['id','TE_ID'],
            ['BN'],
            ['DIC'],
            ['LIST']
        ],
        'TE_ID':[
            ['tkn_opening_par','ARGS_G','tkn_closing_par','TE_ID'],
            ['tkn_opening_bra','EXP','tkn_closing_par','TE_ID'],
            ['empty']
        ],
        'ARGS_G':[
            ['EXP','ACG_1'],
            ['empty']
        ],
        'ACG_1':[
            ['tkn_comma','EXP','ACG_1'],
            ['empty']
        ],
        'IN_DEC':[
            ['tkn_increment'],
            ['tkn_decrement']
        ],
        'OP_A':[
            ['tkn_minus'],
            ['tkn_plus'],
            ['tkn_div'],
            ['tkn_times'],
            ['tkn_power'],
            ['tkn_mod'],
            ['tkn_concat']
        ],
        'OP_R':[
            ['tkn_equal'],
            ['tkn_neq'],
            ['tkn_leq'],
            ['tkn_geq'],
            ['tkn_greater'],
            ['tkn_less'],
            ['tkn_regex'],
            
        ],
        'OP_L':[
            ['tkn_and'],
            ['tkn_or']
        ],
        'AS_OP':[
            ['tkn_assign'],
            ['tkn_plus_assign'],
            ['tkn_minus_assign'],
            ['tkn_times_assign'],
            ['tkn_div_assign'],
            ['tkn_mod_assign'],
        ],
        'VAL':[
            ['tkn_real'],
            ['tkn_str'],
            ['verdadero'],
            ['cierto'],
            ['falso'],
            ['nulo']
        ]
        
    }


    def analize(self,token):
        #print("*************************** Next Token *******************")
        #self.showTokenInfo(token)
        #print("Prediction set before the match algorithm",self.prediction_set)
        match=False
        #print("Stack before the match algorithm: ",self.stack)
        
        #print("******************** Starting match process *******************")
    
        
        while(match==False):
          
            if(len(self.stack) < 1 and EOF==False):
                self.error=True
                
                self.reportError(token)
                break

            elif(len(self.stack) < 1 and EOF==True):
                self.error=True
                print("El analisis sintactico ha finalizado exitosamente.")
                break
            
            current_element = self.stack.pop()
            
            
            
            
            if(current_element[0].isupper()):
                
                current_no_terminal = current_element
                
            
            
                #print("Current no terminal rules:",self.grammar[current_no_terminal])
                
                rule = self.lookForMatchRule(current_no_terminal,token)
                
                #print("Rule that must be applied",rule)
                
                #print("Updated prediction set: ",self.prediction_set)
                
                if(rule=='error'):
                    #print("Error sintáctico -> A punto de reportar error")
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
                    #print("No way, error")
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
                token.lexem='='
        elif token.lexem == 'plus_assign':
            token.lexem ='+='

        elif token.lexem == 'minus_assign':
            token.lexem ='-='

        elif token.lexem == 'times_assign':
            token.lexem ='*='      

        elif token.lexem == 'div_assign':
            token.lexem ='/='    

        elif token.lexem == 'mod_assign':
            token.lexem ='%='
       
        elif token.lexem == 'increment':
            token.lexem ='++'
        
        elif token.lexem == 'decrement':
            token.lexem ='--'      

        elif token.lexem == 'period':
            token.lexem ='.'
        
        elif token.lexem == 'comma':
            token.lexem=','
            
        elif token.lexem == 'colon':
            token.lexem=':'
        
        elif token.lexem == 'semicolon':
            token.lexem=';'
        
        elif token.lexem == 'closing_bra':
            token.lexem=']'
        
        elif token.lexem == 'opening_bra':
            token.lexem='['
            
        elif token.lexem == 'closing_par':
            token.lexem=')'
            
        elif token.lexem == 'opening_par':
            token.lexem='('
        
        elif token.lexem == 'closing_key':
            token.lexem='}'
            
        elif token.lexem == 'opening_key':
            token.lexem='{'
            
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

        elif token.lexem == 'mod':
            token.lexem='%'

        elif token.lexem == 'concat':
            token.lexem='..'
        
        elif token.lexem == 'not':
            token.lexem='!'
            
        elif token.lexem == 'equal':
            token.lexem='=='
            
        elif token.lexem == 'neq':
            token.lexem='!='
            
        elif token.lexem == 'less':
            token.lexem='<'
            
        elif token.lexem == 'leq':
            token.lexem='<='
            
        elif token.lexem == 'greater':
            token.lexem='>'
            
        elif token.lexem == 'geq':
            token.lexem ='>='

        elif token.lexem == 'regex':
            token.lexem ='~='
        
        elif token.lexem == 'and':
            token.lexem ='&&'
        elif token.lexem == 'or':
            token.lexem ='||'
            
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
            
            if report_prediction_set[i]=='tkn_and':
                report_prediction_set[i]='&&'
                
            elif report_prediction_set[i] == 'tkn_or':
                report_prediction_set[i]='||'
            
            elif report_prediction_set[i] == 'tkn_concat':
                report_prediction_set[i]='..'

            elif report_prediction_set[i] == 'tkn_plus_assign':
                report_prediction_set[i]='+='
            
            elif report_prediction_set[i] == 'tkn_minus_assign':
                report_prediction_set[i]='-='

            elif report_prediction_set[i] == 'tkn_times_assign':
                report_prediction_set[i]='*='

            elif report_prediction_set[i] == 'tkn_div_assign':
                report_prediction_set[i]='/='

            elif report_prediction_set[i] == 'tkn_mod_assign':
                report_prediction_set[i]='%='

            elif report_prediction_set[i] == 'tkn_increment':
                report_prediction_set[i]='++'

            elif report_prediction_set[i] == 'tkn_decrement':
                report_prediction_set[i]='--'

            elif report_prediction_set[i] == 'tkn_period':
                report_prediction_set[i]='.'

            elif report_prediction_set[i] == 'tkn_comma':
                report_prediction_set[i]=','

            elif report_prediction_set[i] == 'tkn_semicolon':
                report_prediction_set[i]=';'

            elif report_prediction_set[i] == 'tkn_colon':
                report_prediction_set[i]=':'

            elif report_prediction_set[i] == 'tkn_opening_key':
                report_prediction_set[i]='{'

            elif report_prediction_set[i] == 'tkn_closing_key':
                report_prediction_set[i]='}'

            elif report_prediction_set[i] == 'tkn_opening_bra':
                report_prediction_set[i]='['

            elif report_prediction_set[i] == 'tkn_closing_bra':
                report_prediction_set[i]=']'

            elif report_prediction_set[i] == 'tkn_opening_par':
                report_prediction_set[i]='('     

            elif report_prediction_set[i] == 'tkn_closing_par':
                report_prediction_set[i]=')'

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

            elif report_prediction_set[i] == 'tkn_mod':
                report_prediction_set[i]='%'
            
            elif report_prediction_set[i] == 'tkn_equal':
                report_prediction_set[i]='=='

            elif report_prediction_set[i] == 'tkn_neq':
                report_prediction_set[i]='!='

            elif report_prediction_set[i] == 'tkn_leq':
                report_prediction_set[i]='<='

            elif report_prediction_set[i] == 'tkn_geq':
                report_prediction_set[i]='>='

            elif report_prediction_set[i] == 'tkn_greater':
                report_prediction_set[i]='>'

            elif report_prediction_set[i] == 'tkn_less':
                report_prediction_set[i]='<'

            elif report_prediction_set[i] == 'tkn_regex':
                report_prediction_set[i]='~='

            elif report_prediction_set[i] == 'tkn_assign':
                report_prediction_set[i]='='

            elif report_prediction_set[i] == 'tkn_not':
                report_prediction_set[i]='!'
            

                
        
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

    def __init__(self,parser):
        
        self.parser = parser
    
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

            if(self.parser.error == True):
                break
            
            code = code[end_index:]
            
            #print("Code by this iteration: ",code)
            
            line_size=len(code)
            
            if(len(code)==0):
                break
            
    def report_token(self,token,lexem,line,position,key_word):
        '''
        if(key_word):
            print("<{},{},{}>".format(token,line,position))
        else:
            print("<{},{},{},{}>".format(token,lexem,line,position))

        current_token = Token(token,lexem,line,position)

        '''

        current_token = Token(token,lexem,line,position)
        
        self.parser.analize(current_token)
    
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
        #print("posible error sintactico - pila llena: ",Lpp_lexer.parser.stack)
        EOF_tkn= Token('EOF','EOF',line,1)
        
        Lpp_lexer.parser.analize(EOF_tkn)
        
    else:
        print("El analisis sintactico ha finalizado exitosamente.")