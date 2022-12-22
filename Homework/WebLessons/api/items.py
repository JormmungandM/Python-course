#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python.exe

import os 
 
def send401( message:str = None ) -> None:
    print( "Status: 401 Unauthorized" )
    if message : print ( "Content-Type: text/plain" )
    print()
    if message : print( message, end='' )
    return

auth_header = None 
 
if 'HTTP_AUTHORIZATION' in os.environ.keys() : 
    auth_header = os.environ['HTTP_AUTHORIZATION'] 
# elif 'REDIRECT_HTTP_AUTHORIZATION' in os.environ.keys() : 
#     auth_header = os.environ['REDIRECT_HTTP_AUTHORIZATION'] 
 
if not 'HTTP_AUTHORIZATION' in os.environ.keys(): 
    send401()
    exit() 
     

print("Content-Type: text/plain") 
print("") 
print("Secret item coming soon", end='')