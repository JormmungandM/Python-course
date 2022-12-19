#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python.exe

import os, sys 
import urllib.parse

# метод запроса
method = os.environ["REQUEST_METHOD"]

# URL - параметры
query_string = urllib.parse.unquote(os.environ["QUERY_STRING"])
params = urllib.parse.parse_qs( query_string, True )
# Переработка в словарь
# params = dict( param.split("=") for param in query_string.split("&"))

# Заголовоки
headers = dict( ((k[5:] if k.startswith( 'HTTP_' ) else k).lower(), v)
    for k,v in os.environ.items()
        if k.startswith( 'HTTP_' )
            or k in [ "CONTENT_LENGTH", "CONTENT_TYPE" ] )

# Тело
body = sys.stdin.read()

print( "Content-Type: text/plain; charset=cp1251" )
print( "" )
print( method )
print( f"QR: {query_string}\nEdit QR: {params}")
print( headers )
print( body, end='' )


