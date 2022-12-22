#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python.exe

import os
import base64
 
auth_header = None 
 
if 'HTTP_AUTHORIZATION' in os.environ.keys() : 
    auth_header = os.environ['HTTP_AUTHORIZATION'] 
elif 'REDIRECT_HTTP_AUTHORIZATION' in os.environ.keys() : 
    auth_header = os.environ['REDIRECT_HTTP_AUTHORIZATION'] 
 
if not auth_header : 
    print("Status: 401 Unauthorized") 
    print(f"WWW-Authenticate: Bearer realm='Login:Password expected'") 
    print() 
    cred = "admin:123" # YWRtaW46MTIz
    code64 = base64.b64encode( cred.encode('utf-8') ).decode( 'ascii' )
    print( cred + " -> " + code64 )
    exit() 

if auth_header.startswith( 'Basic' ):
    try:
        cred = base64.b64decode( auth_header[6:], validate=True ).decode( 'utf-8' )\
        
        # 'admin:12:3' = 'YWRtaW46MTI6Mw=='
        # Валидация. Если символова нету или он повторяется, то вызывается ошибка
        if ((':' in cred) and (cred.count(':') == 1)) is False:
            raise ValueError("Authorization invalid: error format data")   

    except ValueError as er:
        print("Status: 401 Unauthorized") 
        print(f"WWW-Authenticate: Bearer realm='Login:Password expected'") 
        print("Content-Type: text/plain") 
        print() 
        print(er) 
    except:
        print("Status: 401 Unauthorized") 
        print(f"WWW-Authenticate: Bearer realm='Login:Password expected'") 
        print("Content-Type: text/plain") 
        print() 
        print("Malformed credentials: Login:Password base54 encoded expected") 
    else:
        print("Status: 200 OK") 
        print("Content-Type: text/plain") 
        print("") 
        print( cred, end='')
