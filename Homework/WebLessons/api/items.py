#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python.exe

import os 
 
auth_header = None 
 
if 'HTTP_AUTHORIZATION' in os.environ.keys() : 
    auth_header = os.environ['HTTP_AUTHORIZATION'] 
# elif 'REDIRECT_HTTP_AUTHORIZATION' in os.environ.keys() : 
#     auth_header = os.environ['REDIRECT_HTTP_AUTHORIZATION'] 
 
if not 'HTTP_AUTHORIZATION' in os.environ.keys(): 
    print("Status: 401 Unauthorized") 
    #print("WWW-Authenticate: Bearer realm='Get token on /auth'") 
    print() 
    exit() 
     
print("Content-Type: text/plain") 
print("") 
print("Secret item coming soon", end='')