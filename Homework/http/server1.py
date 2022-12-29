import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
import os, sys

import db, dao
import mysql.connector


class DBService:
    connection: mysql.connector.MySQLConnection = None
    def get_connection(self) -> mysql.connector.MySQLConnection :
        if DBService.connection is None or not DBService.connection.is_connected():
            try:
                DBService.connection = mysql.connector.connect(**db.conf)
            except:
                print("Connection error")
                DBService.connection = None
            else:
                print("Connection success")
        return DBService.connection 
              
db_service: DBService = None

class DbService : 
    __connection:mysql.connector.MySQLConnection = None 
 
    def get_connection( self ) -> mysql.connector.MySQLConnection : 
        if DbService.__connection is None or not DbService.__connection.is_connected() : 
            # print( db.conf ) 
            try : 
                DbService.__connection = mysql.connector.connect( **db.conf ) 
            except mysql.connector.Error as err : 
                print( err ) 
                DbService.__connection = None 
        return DbService.__connection 
 
 
class DAOService : 
 
    def __init__( self, db_service ) -> None: 
        self.__db_service: DbService = db_service 
        self.__user_dao: dao.UserDAO = None                  # угода іменування: до полів з "__" додається назва класу:  
        self.__access_token_dao: dao.AccessTokenDAO = None   # "DaoService._DaoService__user_dao". Це аналог "private" 
        return 
 
    def get_user_dao( self ) -> dao.UserDAO : 
        if self.__user_dao is None : 
            self.__user_dao = dao.UserDAO( self.__db_service.get_connection() ) 
        return self.__user_dao 
 
    def get_access_token_dao( self ) -> dao.AccessTokenDAO : 
        if self.__access_token_dao is None : 
            self.__access_token_dao = dao.AccessTokenDAO( self.__db_service.get_connection() ) 
        return self.__access_token_dao

dao_service : DAOService = None


class MainHandler( BaseHTTPRequestHandler ) :

    def __init__(self, request, client_address, server) -> None:
        super().__init__(request, client_address, server)           # RequestScoped - выполняется при каждом запросе
        # print( 'init', self.command )                             # self.command - метод запроса (GET, POST, ...)


    def do_GET( self ) -> None :
        print( self.path )                        # вывод в консоль (не в ответ сервера)
        path_parts = self.path.split( "/" )       # разделенный на части запрос, path_parts[0] - пустой, т.к. path начинается со "/" 
        # if path_parts[1] == "" :
        #     path_parts[1] = "index.html"
        if self.path == "/" :
            self.path = "/index.html"
        fname = "./Homework/http" + self.path
        if os.path.isfile( fname ) :              # запрос - существующий файл
            #print( fname, "file" )
            self.flush_file( fname )
        elif path_parts[1] == "auth" :            # запрос - /auth
            self.auth()
        else :
            # print( fname, "not file" )
            self.send_response( 200 )
            self.send_header( "Content-Type", "text/html" )
            self.end_headers()
            self.wfile.write( "<h1>404</h1>".encode() )
        return

    def log_request(self, code: int | str = ..., size: int | str = ...) -> None:
        # return super().log_request(code, size)
        return

    def flush_file( self, filename ) -> None :
        # Определить расширение файла filename
        ext = filename.split(".")[-1]

        # Установить Content-Type согласно расширению
        if ext in ('png', 'bmp') :
            content_type = "image/" + ext
        elif ext == 'ico' : 
            content_type = "image/x-icon"
        elif ext == 'html' : 
            content_type = "text/html"
        elif ext == 'css' : 
            content_type = "text/css"
        elif ext == 'js' : 
            content_type = "application/javascript"
        else :
            content_type = "application/octet-stream"

        self.send_response( 200 )
        self.send_header( "Content-Type", content_type )
        self.end_headers()
        # Передать файл в ответ
        with open( filename, "rb" ) as f :
            self.wfile.write( f.read() )
        return

    def auth( self ) :   # API
        # Проверяем наличие заголовка Authorization
        auth_header = self.headers.get( "Authorization" ) 
        if auth_header is None :
            self.send_401( "Authorization header required" )
            return
        # Проверяем схему авторизации Basic
        if not auth_header.startswith( 'Basic' ) :
            self.send_401( "Basic Authorization header required" )
            return
        # декодируем переданную строку
        try :
            cred = base64.b64decode( auth_header[6:], validate=True ).decode( 'utf-8' )
        except :
            self.send_401( "Malformed credentials: Login:Password base64 encoded expected" )
            return        
        # Проверяем формат строки (должен быть ":")
        if not ':' in cred :
            self.send_401( "Malformed credentials: Login:Password base64 encoded required" )
            return

        # Разделяем логин и пароль по первому ":" (в пароле могут быть свои ":")
        user_login, user_password = cred.split( ':', maxsplit = 1 )    

        user_dao = dao_service.get_user_dao()
        user = user_dao.auth_user(user_login,user_password)
        if user is None:
            self.send_401( "Credentials rejected" )
            return

        self.send_200( user.id )
        return

    def send_401( self, message = None ) :
        self.send_response( 401 )
        self.send_header( "Status", "401 Unauthorized" )
        if message : self.send_header( "Content-Type", "text/plain" )
        self.end_headers()
        if message : self.wfile.write( message.encode() )

    def send_200( self, message:str = None, type:str = "text" ) -> None : 
        self.send_response( 200 ) 
        if type == 'json' : 
            content_type = 'application/json; charset=UTF-8' 
        else : 
            content_type = 'text/plain; charset=UTF-8' 
        self.send_header( "Content-Type", content_type ) 
        self.end_headers() 
        if message: 
            self.wfile.write( message.encode() ) 
        return

def main() -> None :
    http_server = HTTPServer( ( '127.0.0.1', 88 ), MainHandler )
    try :
        print( "Server started" )
        dao_service = DAOService( DBService() )
        http_server.serve_forever()
    except :
        print( "Server stopped" )
        excep = sys.exc_info()[1]
        print(excep.args[0])


if __name__ == "__main__" :
    main()
