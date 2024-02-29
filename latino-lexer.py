'''
Analizador léxico - Lenguaje de Programación Latino
Reinaldo Toledo Leguizamón
Monitoría de Lenguajes de programación
2024-1

'''

import re

EOF = False

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
    'global':r'\bglobal\b(?![\w_])',
    'hasta':r'\bhasta\b(?![\w_])',
    'imprimir':r'\bimprimir\b(?![\w_])',
    'imprimirf':r'\bimprimirf\b(?![\w_])',
    'incluir':r'\bincluir\b(?![\w_])',
    'leer':r'\bleer\b(?![\w_])',
    'limpiar':r'\blimpiar\b(?![\w_])',
    'mientras':r'\bmientras\b(?![\w_])',
    'nulo':r'\bnulo\b(?![\w_])',
    'osi':r'\bosi\b(?![\w_])',
    'otro':r'\botro\b(?![\w_])',
    'para':r'\bpara\b(?![\w_])',
    'poner':r'\bponer\b(?![\w_])',
    'fin':r'\bfin\b(?![\w_])',
    'repetir':r'\brepetir\b(?![\w_])',
    'ret':r'\bret\b(?![\w_])',
    'retornar':r'\bretornar\b(?![\w_])',
    'retorno':r'\bretorno\b(?![\w_])',
    'romper':r'\bverdadero\b(?![\w_])',
    'si':r'\bverdadero\b(?![\w_])',
    'sino':r'\bverdadero\b(?![\w_])',
    'tipo':r'\bverdadero\b(?![\w_])',
    'verdadero':r'\by\b(?![\w_])',
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
        'angle_neq':r'<>',
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
        
        string_match = r'\"(.*?)\"'
        
        if re.match(string_match, code, re.IGNORECASE) != None:
            self.report_token('tkn_str',re.match(string_match, code).group().replace('\"',''),line,position+1,False)
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
            self.report_token('tkn_integer',re.match(integer_match, code).group(),line,position+1,False)
            end_index = re.match(integer_match, code).end()
            position+=end_index
        
        return end_index
    
    def match_char(self,code,line,end_index,position):
        
        char_match = r'\'(.?)\''
        
        if re.match(char_match, code, re.IGNORECASE) != None:
            self.report_token('tkn_char',re.match(char_match, code).group().replace('\'',''),line,position+1,False)
            end_index = re.match(char_match, code).end()
            position+=end_index
        else:
            self.report_error(line,position+1)
        
        return end_index
        
    
    
    def match_id(self,code,line,end_index,position):
        
        # Match the id
        
        id_match = r'[a-zA-Z_][0-9a-zA-Z_]*'
        
        if re.match(id_match, code, re.IGNORECASE) != None:
            self.report_token('id',re.match(id_match, code, re.IGNORECASE).group().lower(),line,position+1,False)
            end_index = re.match(id_match, code, re.IGNORECASE).end()
            position+=end_index
        
        return end_index

    
    def match_keywords(self,code,line,end_index,position):
        
        # Match the key words 
        found=False
            
        for key in self.regex_dict:
            
            if re.match(self.regex_dict[key], code, re.IGNORECASE) != None:

                self.report_token(key,key,line,position+1,True)
                end_index = re.match(self.regex_dict[key], code, re.IGNORECASE).end()
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
            if(code[0]=='#'):
                break
            elif(len(code)>=2 and code[0]=='/'):
                if(code[1]=='/'):
                    break
                elif(code[1]=='*'):
                    # Match block comment
                    self.block_comment=True
                    self.block_comment_line=line
                    self.block_comment_position=position
                    code = code[2:]
                    position+=2
                    
            if(len(code)>=2 and code[0]=='*'):
                # Close block comment
                if(code[1]=='/'):
                    self.block_comment=False
                    self.block_comment_line=0
                    self.block_comment_position=0
                    code = code[2:]
                    position+=2
                    i=0
                    
                    if(len(code)>0):
                    #Recover the next char different to a blank space
                        while(code[i]==' '):
                            i+=1;
                            position+=1;
                            if(i==len(code)):
                                break
                        code = code[i:]
            
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
                
                elif(code[0]=='\''):
                    end_index= self.match_char(code,line,end_index,position)
                
                elif(code[0]=='\"'):
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
    Lpp_lexer = Lexer()
    while True:
        current_line = input()
        Lpp_lexer.analize(current_line,line)
        
        if(Lpp_lexer.error==True):
            break
        line+=1
        
except EOFError:
    EOF=True
    
    if(EOF==True and Lpp_lexer.block_comment==True):
        Lpp_lexer.report_error(Lpp_lexer.block_comment_line,Lpp_lexer.block_comment_position+1)