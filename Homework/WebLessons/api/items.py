#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python3.10.exe

import os, sys
import asyncio
sys.path.append( "../" )  # доп. папка для поиска модулей
import db
import dao
import mysql.connector


def send401( message:str = None ) -> None:
    print( "Status: 401 Unauthorized" )
    if message : print ( "Content-Type: text/plain" )
    print()
    if message : print( message, end='' )
    return

async def checkHeader():
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
    if not auth_header.startswith( 'Bearer' ):
        send401( "Bearer Authorization header required" )
        exit()
        
    # Извлекаем токен
    access_token = auth_header[7:]   # убираем 'Bearer' + space

    return access_token

async def connection() -> mysql.connector :
    try:
        con = mysql.connector.connect(**db.conf)
    except asyncio.CancelledError :    
        send401( "Connection DB Error -> Task Error" )
        exit()
    except :
        send401( "Connection DB Error")
        exit()

    return con

async def getToken():
    
    connection_task =  asyncio.create_task( connection())
    auth_task =  asyncio.create_task( checkHeader())
    access_token = await auth_task
    
    if not access_token:
        connection_task.cancel()
    
    con = await connection_task

    token = dao.AccessTokenDAO( con ).get( access_token )
    if not token :
        send401( "Token rejected" )
        exit()



print("Content-Type: text/plain") 
print("") 
print("Secret item coming soon", end='')