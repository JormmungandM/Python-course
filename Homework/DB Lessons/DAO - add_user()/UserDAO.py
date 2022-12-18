import mysql.connector
import hashlib
import random

class User : 
    def __intit__( self, cursor = None ) -> None:
        if cursor == None:
            self.id                  = ''
            self.login               = ''
            self.passw               = ''
            self.name                = ''
            self.salt                = ''
            self.avatar              = ''
            self.email               = ''
            self.email_code          = ''
            self.email_code_attempts = ''
        else :
            row = cursor.fetchone()
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

class UserDAO:

    def __init__( self, db: mysql.connector.MySQLConnection ) -> None:
        self.db = db


    def add_user( self, user : User) -> bool :
        user.salt = random.randbytes(20).hex()
        user.passw = hashlib.sha1((user.salt + user.passw).encode()).hexdigest()
        user.email_code = random.randbytes(3).hex()
        sql = f"INSERT INTO Users VALUES(UUID(), %s, '{user.passw}', %s, '{user.salt}', %s, %s, '{user.email_code}', 0)"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (user.login, user.name, user.avatar, user.email) )
            self.db.commit()
        except mysql.connector.Error as err :
            print( "add_user:", err )
            return False
        finally:
            cursor.close()
        return True



def main(connection, userDao) -> None :
    user = User()
    user.login  = "admin"
    user.passw  = "123"
    user.name   = "Root Administrator"
    user.avatar = None
    user.email  = "admin@urk.net"
    
    print(userDao.add_user (user) )
    
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
    else:
        print("Connection OK")

    userDao = UserDAO(connection)

    main(connection, userDao)
    