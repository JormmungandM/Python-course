from datetime import datetime, timedelta
import mysql.connector
import hashlib
import random
import uuid

class User : 
    def __init__( self, row = None ) -> None:
        if row == None:
            self.id                  = None
            self.login               = None
            self.passw               = None
            self.name                = None
            self.salt                = None
            self.avatar              = None
            self.email               = None
            self.email_code          = None
            self.email_code_attempts = None
            self.del_dt              = None
        else :
            if row :
                self.id                  = row[0]
                self.login               = row[1]
                self.passw               = row[2]
                self.name                = row[3]
                self.salt                = row[4]
                self.avatar              = row[5]
                self.email               = row[6]
                self.email_code          = row[7]
                self.email_code_attempts = row[8]
                self.del_dt              = row[9]

    def __str__ (self) -> str :
        return str(self.__dict__)

    def print( self ):
        print ( 
        f"Id:                   {self.id}\n" + 
        f"Login:                {self.login}\n" + 
        f"Password:             {self.passw}\n" + 
        f"Name:                 {self.name}\n" + 
        f"Salt:                 {self.salt}\n" + 
        f"Avatar:               {self.avatar}\n" + 
        f"Email:                {self.email}\n" + 
        f"Email code:           {self.email_code}\n" + 
        f"Email code attempts:  {self.email_code_attempts}\n" +
        f"Removal time:         {self.del_dt}\n")

class UserDAO:

    def __init__( self, db: mysql.connector.MySQLConnection ) -> None:
        self.db = db


    def add_user( self, user : User) -> bool :

        user.salt = random.randbytes(20).hex()
        user.passw = hashlib.sha1((user.salt + user.passw).encode()).hexdigest()
        user.email_code = random.randbytes(3).hex()

        user.id = str(uuid.uuid4())
        user.email_code_attempts = 0
        
        names = user.__dict__.keys()
        fields = ','.join( f"`{name}`" for name in names ).replace( 'passw', 'pass' ) #`id`, `login`, `name`;
        placeholders = ','.join( f"%({name})s" for name in names )
        sql = f"INSERT INTO Users({fields}) VALUES({placeholders})"
        print(fields)
        print(placeholders)
        # sql = f"INSERT INTO Users VALUES(UUID(), %s, '{user.passw}', %s, '{user.salt}', %s, %s, '{user.email_code}', 0)"
        try:
            cursor = self.db.cursor()
            cursor.execute( sql, user.__dict__ )
            self.db.commit()
        except mysql.connector.Error as err :
            print( "UserDAO: add_user -> " + err )
            return False
        finally:
            cursor.close()
        return True

    def get_users( self, ignore_deleted = True ) -> tuple | None:
        sql = "SELECT * FROM users"
        if ignore_deleted :
            sql += " WHERE del_dt IS NULL"

        try:
            cursor = self.db.cursor()
            cursor.execute (sql)
        except mysql.connector.Error as err:
            print("UserDAO: get_user -> " + err)
            return None
        else:
            return tuple( User(row).print() for row in cursor)
        finally:
            cursor.close()
        return

    def get_user( self, id = None, login = None, ignore_deleted=True) -> User | None:

        sql = "SELECT u.* FROM Users u WHERE "
        if ignore_deleted :
            sql = "SELECT u.* FROM Users u WHERE del_dt IS NULL AND "

        params = []
        if id:
            sql += "u.id = %s "
            params.append(id)
        if login:
            sql += ( "AND " if id else "" ) + "u.login = %s"
            params.append( login )
        if len( params ) == 0:
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute( sql, params)
            row = cursor.fetchone()
            if row:
                User(row)
                return User(row)
            else:
                print("User has been deleted")
        except mysql.connector.Error as err:
            print( "UserDAO: get_user -> " + err)
        finally:
            try: cursor.close()
            except : pass
        return None

    def update(self, user : User) -> bool:
        sql = "UPDATE users u SET " + \
            ','.join(f"u.`{x.replace('passw','pass')}`=%({x})s" for x in user.__dict__.keys() if x != 'id') + \
            ' WHERE u.`id`=%(id)s'
        print(sql)
        try :
            cursor = self.db.cursor()
            cursor.execute(sql, user.__dict__)
            self.db.commit()
        except mysql.connector.Error as err:
            print("UserDAO: update -> " + err)
            return False
        else:
            return True
        finally:
            try : cursor.close()
            except: pass

    def delete(self, user : User ) -> bool:
        if not user : return False
        try:
            cursor = self.db.cursor()
            cursor.execute( "UPDATE users u SET u.del_dt = CURRENT_TIMESTAMP WHERE u.id = %s", (user.id,) )
            self.db.commit()
        except mysql.connector.Error as err:
            print("UserDAO: delete -> " + err)
            return False
        else:
            return True
        finally:
            try: cursor.close()
            except: pass
      
    def is_login_free(self, login:str) -> bool:
        return self.get_user(login=login) != None

    def auth_user(self, login:str, passw:str) -> User | None:
        user = self.get_user( login = login )
        if user:
            if hashlib.sha1((user.salt + passw).encode()).hexdigest() == user.passw:
                return user
        return None

class AccessToken :
    def __init__( self, row = None ) -> None :
        if row == None :
            self.token   = None
            self.user_id = None 
            self.expires = None 
        elif isinstance( row, tuple ) or isinstance( row, list ) :
            self.token   = row[0]
            self.user_id = row[1] 
            self.expires = row[2] 
        elif isinstance( row, dict ) :
            self.token   = row["token"  ]
            self.user_id = row["user_id"] 
            self.expires = row["expires"] 



class AccessTokenDAO :
    def __init__( self, db: mysql.connector.MySQLConnection ) -> None :
        self.db = db

    def checkActiveToken( self, user: str|User ) -> AccessToken|None :
        user_id = None
        token = None
        if isinstance( user, str ) :   # str - user_id only
            user_id = user
        elif isinstance( user, User )  :
            user_id = user.id

        if not user_id : return None
        sql = "SELECT * FROM access_tokens WHERE user_id=%s"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, ( user_id, ))
            row = cursor.fetchone()
            if row:                                     # если токен есть, то проверяем сроки
                token = AccessToken(row)
                if token.expires < datetime.now() or ((token.expires - datetime.now()).total_seconds() / 60) < 10:      # если вышел срок токена или если до конца срока осталось менее 10 минут
                    token = self.miniUpdate(user_id)
            else:                                       # если токена нету, то создаем новый
                token = self.create(user_id)
        except :
            return None
        else :
            return token
        finally :
            try : cursor.close()
            except : pass

    # 
    def miniUpdate(self, user_id : str) -> AccessToken:
        if  self.delete(user_id):           # удаляем токен
            return self.create(user_id)     # создаем новый и возвращаем

    def create( self, user_id: str ) -> AccessToken|None :
        access_token = AccessToken()
        access_token.token   = random.randbytes(20).hex()  # 20 bytes = 40 hex-digits = 160 bit
        access_token.user_id = user_id
        access_token.expires = ( datetime.now() + timedelta( days = 1 )  # 1 day from now
            ).strftime( "%Y-%m-%d %H:%M:%S" ) # SQL-format
        sql = "INSERT INTO access_tokens VALUES( %(token)s, %(user_id)s, %(expires)s )"
        try :
            cursor = self.db.cursor()
            cursor.execute( sql, access_token.__dict__ )
            self.db.commit()
        except :
            return None
        else :
            return access_token
        finally :
            try : cursor.close()
            except : pass

    def delete(self, user_id: str) -> bool:                 # удаляем токин по user_id
        sql = "DELETE FROM access_tokens WHERE user_id=%s"
        try :
            cursor = self.db.cursor()
            cursor.execute(sql, ( user_id, ))
            self.db.commit()
        except :
            return False
        else :
            return True
        finally :
            try : cursor.close()
            except : pass

    def get( self, access_token: str ) -> AccessToken|None :
        sql = "SELECT * FROM access_tokens WHERE token = %s"
        try :
            cursor = self.db.cursor( dictionary = True )
            cursor.execute( sql, ( access_token, ) ) 
            row = cursor.fetchone()
            if row : return AccessToken( row )
        except :
            pass
        finally :
            try : cursor.close()
            except : pass
        return None
