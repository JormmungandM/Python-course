#!C:\Users\Jormmungand\AppData\Local\Microsoft\WindowsApps\python3.10.exe

import os

objName = ["REQUEST_METHOD" , "QUERY_STRING" , "REQUEST_URI" , "REMOTE_ADDR" , "REQUEST_SCHEME" ]
envs = "<ul>" + ''.join( f"<li>{k} = {v}</li>" for k,v in os.environ.items() ) + "<ul>"



print( "Content-Type: text/html; charset=utf-8" )
print( "" )   # empty line
print( f"""<!doctype html />
<html>
<head>
    <title>Py-191</title>
</head>
<body>
{__name__}
    <h1>Hello CGI World!</h1>
    {envs}
</body>
</html>""" )