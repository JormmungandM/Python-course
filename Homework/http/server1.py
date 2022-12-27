from http.server import HTTPServer, BaseHTTPRequestHandler

class MinHandler(BaseHTTPRequestHandler):
    def do_GET( self ) -> None:
        print( "Hello" ) # вывод в консоль (не в ответ сервера)
        self.send_response( 200 )
        self.send_header( "Content-Type", "text/html" )
        self.end_headers()
        self.wfile.write( "<h1>Hello</h1>".encode() )
        return

def main() -> None:
    http_server = HTTPServer(('127.0.0.1', 88), MinHandler )
    try:
        print( "Server started" )
        http_server.serve_forever()
    except:
        print( "Server stopped" )

if __name__ == "__main__":
    main()