#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python.exe

import os 
import base64 
 
auth_header = None 
 
if 'HTTP_AUTHORIZATION' in os.environ.keys() : 
    auth_header = os.environ['HTTP_AUTHORIZATION'] 
elif 'REDIRECT_HTTP_AUTHORIZATION' in os.environ.keys() : 
    auth_header = os.environ['REDIRECT_HTTP_AUTHORIZATION'] 
 
if not 'HTTP_AUTHORIZATION' in os.environ.keys(): 
    print("Status: 401 Unauthorized") 
    print("WWW-Authenticate: Basic realm=Login:Password expected'") 
    print() 
    cred = "admin:123" 
    code64 = base64.b64dencode(cred.encode("utf-8")).decode('ascii') 
    print(code64) 
    exit()

if auth_header.startswith('Basic'): 
    try : 
        cred = base64.b64decode(auth_header[6:], validate=True).decode('utf-8') 
    except: 
        print("Status: 401 Unauthorized") 
        print("WWW-Authenticate: Basic realm=Login:Password expected'") 
        print() 
        print("Malformed credentials:") 
        pass 
    else: 
        print("Status: 200 OK") 
        print("Content-type: text/plain") 
        print() 
        print(cred,end='')