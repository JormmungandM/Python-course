#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python3.10.exe

import os, sys
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
    send401( "Basic Authorization header required" )
    exit()

# Декодируем логин и пароль
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

# Разделяем логин и пароль
user_login, user_password = cred.split(':', maxsplit=1)

sys.path.append("../")
import db
import dao
import mysql.connector

try:
    con = mysql.connector.connect(**db.conf)
except :
    send401( "Connection DB Error")
    exit()

# получаем пользователя по логину и паролю 
user = dao.UserDAO(con).auth_user( user_login, user_password)
if not user:
    send401( "Credentials rejected" )
    exit()  

# генерируем токен для пользователя 
access_token = dao.AccessTokenDAO( con ).checkActiveToken( user )
if not access_token :
    send401( "Token creation error")
    exit()




print( "Status: 200 OK" )
print( "Content-Type: application/json; charset=UTF-8" )
print( "Cache-Control: no-store" )
print( "Pragma: no-cache" )
print()
print( f'''{{
    "access_token": "{access_token.token}",
    "token_type": "Bearer",
    "expires_in": "{access_token.expires}"
}}''', end='' )