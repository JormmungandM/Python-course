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

    def print( self ):
        print ( f"Id: {self.id}\n" + 
        f"Login: {self.login}\n" + 
        f"Password: {self.passw}\n" + 
        f"Name: {self.name}\n" + 
        f"Salt: {self.salt}\n" + 
        f"Avatar: {self.avatar}\n" + 
        f"Email: {self.email}\n" + 
        f"Email code: {self.email_code}\n" + 
        f"Email code attempts: {self.email_code_attempts}\n")

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
            print( "add_user:", err )
            return False
        finally:
            cursor.close()
        return True

    def get_users( self ) -> tuple | None:
        try:
            cursor = self.db.cursor()
            cursor.execute ("SELECT * FROM users")
        except mysql.connector.Error as err:
            print("UserDAO: get_user -> " + err)
            return None
        else:
            return tuple( User(row).print() for row in cursor)
        finally:
            cursor.close()
        return


def main(connection : mysql.connector.MySQLConnection, userDao : UserDAO) -> None :
    # user = User()
    # First
    # user.login  = "admin"
    # user.passw  = "123"
    # user.name   = "Root Administrator"
    # user.avatar = None
    # user.email  = "admin@urk.net"

    # Second
    # user.login  = "user"
    # user.passw  = "123"
    # user.name   = "Experienced User"
    # user.avatar = None
    # user.email  = "user@urk.net"
    # print(userDao.add_user (user) )

    print (userDao.get_users())
    
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


   
   