#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python.exe

import os, sys 
import urllib.parse
import json

# метод запроса
method = os.environ["REQUEST_METHOD"]

# Заголовоки
headers = dict( ((k[5:] if k.startswith( 'HTTP_' ) else k).lower(), v)
    for k,v in os.environ.items()
        if k.startswith( 'HTTP_' )
            or k in [ "CONTENT_LENGTH", "CONTENT_TYPE" ] )
# Переработка в словарь
# params = dict( param.split("=") for param in query_string.split("&"))


# URL - параметры

query_string = urllib.parse.unquote(os.environ["QUERY_STRING"])
params = urllib.parse.parse_qs( query_string, True )
result = f"QR: {query_string}\nEdit QR: {params}"

# Тело
body = sys.stdin.read()

if(headers["CONTENT_TYPE".lower()] == "application/json"):
    try:
        params = json.loads(body)
        persons = '\nJSON\n'  
        for person in params['Persons']:
            persons += f"Person: {person['Name']}; Age: {person['Age']}\n"
    except Exception as ex:
        body = ex
    else: 
        body = persons

print( "Content-Type: text/plain; charset=cp1251" )
print( "" )
print( method )
print( result )
print( headers )
print( body, end='' )


