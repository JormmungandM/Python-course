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
        if  user != None:
            # Хешируем входящий пароль и сравниваем с пользовательским
            return hashlib.sha1((user.salt + passw).encode()).hexdigest() == user.passw
        else:
            return False

def main(connection : mysql.connector.MySQLConnection, userDao : UserDAO) -> None :
    #region Creating and updating users

    # user = User()
    # # First
    # user.login  = "moder"
    # user.passw  = "123"
    # user.name   = "Post Moderator"
    # user.avatar = None
    # user.email  = "moder@urk.net"

    # Second
    # user.login  = "user"
    # user.passw  = "123"
    # user.name   = "Experienced User"
    # user.avatar = None
    # user.email  = "user@urk.net"
    # print(userDao.add_user (user) )

    # print (userDao.get_users())
    # print(userDao.get_user( id = "1e60564a-7ee9-11ed-ae3f-e4a8dfe36290" ))
    # print(userDao.is_login_free( login = "moder" ))
    # user.email  = "admin@gmail.net"
    # print(userDao.update(user))

    #endregion    
    #region is_lree_login()
    # user = userDao.get_user(login = "moder") ; print (user)
    # print(userDao.delete(user))
    # print("admin -", userDao.is_login_free( login = "admin" ))
    # print("user  -", userDao.is_login_free( login = "user"  ))
    # print("moder -", userDao.is_login_free( login = "moder" ))
    #endregion
    
    print(userDao.auth_user(login = "admin", passw = "123"))
    print(userDao.auth_user(login = "user", passw = "123"))
    print(userDao.auth_user(login = "user", passw = "125"))


    

if __name__ == "__main__":
    params = {
        "host":"localhost",
        "port":3306,
        "database":"py191",
        "user":"py191_user",
        "password":"pass_191",
        "charset":"utf8mb4",
        "use_unicode":True,
        "collation":"utf8mb4_general_ci"
    }
    try:
        connection = mysql.connector.connect(**params)
    except mysql.connector.Error as err:
        print("Main: connection -> ", err)
        exit()
    else:
        print("Connection OK")
        userDao = UserDAO(connection)
        main(connection, userDao)
    finally:
        connection.close()


   
   