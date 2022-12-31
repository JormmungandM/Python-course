# MySQL
import mysql.connector


import random

def insert_data( connection: mysql.connector.MySQLConnection ) :
    sql = "INSERT INTO tests(num, ukr, str) VALUES(%s, %s, %s)"
    alf = "абвгдеєжзиіїклмнопрстуфхцчшщьюя" 
    str = ''.join( [ random.choice(alf) for i in range( random.choice([3,4]) ) ] )
    cursor = connection.cursor() 
    try :
        # cursor.execute( (sql), ( ( random.randint(10, 20), "їжак", "їжак" ) ) )
        cursor.execute( (sql), ( ( random.randint(10, 20), str, str ) ) )
        connection.commit()   # буферизация запросов / транзакция -- отправка накопленных изменений (~flush)
    except  mysql.connector.Error as err :
        print( "INSERT:", err )
    else :
        print( "INSERT OK" )
    finally :
        cursor.close()
    return


def show_data( connection: mysql.connector.MySQLConnection, order="G" ) -> None :
    ''' Shows data from 'tests' table ordering by 'order' value: 'G' - general (default), 'U' - unicode '''
    sql = "SELECT * FROM tests t ORDER BY " + ( 't.ukr' if order == 'U' else 't.str' )
    try :
        cursor = connection.cursor()
        cursor.execute( sql )         # выполнение команды создает в БД правило получения данных, но сами данные не передает
    except mysql.connector.Error as err :
        print( err )
    else :                            # передача данных из БД происходит по командам чтения (fetch) либо итерирования cursor
        # for row in cursor :         # после читающего запроса сам cursor становится итерируемым
        #     print( row )  
        print( cursor.column_names )  # данные об именах полей
        while True :                  # аналог предыдущего цикла в раскрытой форме
            row = cursor.fetchone()   # явная команда чтения одной записи (строки результата запроса)
            if row == None :
                break
            print( row )        
    finally :
        try : cursor.close()          # возможно исключение "Unread result found" если не все данные будут запрошены
        except : pass
    return


def main( pars ) :
    try :
        connection = mysql.connector.connect( **pars )
    except mysql.connector.Error as err :
        print( "Connection:", err )
        return
    else :
        print( "Connection OK" )

    # insert_data( connection )
    show_data( connection )
    return

if __name__ == "__main__":
    pars = {
        "host":     "localhost",
        "port":     3306,
        "database": "py191",
        "user":     "py191_user",
        "password": "pass_191",
        
        "charset":  "utf8mb4",
        "use_unicode": True,
        "collation": "utf8mb4_general_ci"
    }
    main( pars ) 
