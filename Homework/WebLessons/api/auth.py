#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python.exe

import os
import base64
 
def send401( message:str = None ) -> None:
    print( "Status: 401 Unauthorized" )
    if message : print ( "Content-Type: text/plain" )
    print()
    if message : print( message, end='' )
    return

auth_header = None 
 
if 'HTTP_AUTHORIZATION' in os.environ.keys() : 
    auth_header = os.environ['HTTP_AUTHORIZATION'] 
elif 'REDIRECT_HTTP_AUTHORIZATION' in os.environ.keys() : 
    auth_header = os.environ['REDIRECT_HTTP_AUTHORIZATION'] 
 
 # Проверяем наличие заголовка
if not auth_header : 
    send401( "Authorization header required" )
    exit() 

 # Проверяем схему авторизации 
if not auth_header.startswith( 'Basic' ):
    send401( "Authorization header required" )
    exit()

try:
    cred = base64.b64decode( auth_header[6:], validate=True ).decode( 'utf-8' )  

    # Валидация. Если символова нету то вызывается ошибка
    if (':' in cred) is False:
        raise ValueError("Authorization invalid: error format data")   
        
except ValueError as er:
    send401( er )
    exit()
except:
    send401( "Malformed credentials: Login:Password base54 encoded expected" )
    exit()

print("Status: 200 OK") 
print("Content-Type: text/plain") 
print("") 
print( cred, end='')    
