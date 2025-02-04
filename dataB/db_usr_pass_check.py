from mysql.connector import MySQLConnection, Error
#from dbconfig import read_db_config
from dataB.dbconfig import read_db_config

#http://www.mysqltutorial.org/python-mysql-update/
#http://www.mysqltutorial.org/mysql-stored-procedure-tutorial.aspx
#http://www.mysqltutorial.org/mysql-if-statement/

def connect():
    """ Connect to MySQL database """

    db_config = read_db_config()

    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')

    except Error as error:
        print(error)

    finally:
        conn.close()
        print('Connection closed.')


def checkLogin(usr):
        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor(buffered=True)
            usr_query  = "SELECT nUser FROM folha where nUser = %s"
            cursor.execute(usr_query,(usr,) )
        
            data = cursor.fetchone() 
        
            print(data)
     
        except Error as e:
            print(e)
        
        finally:
            cursor.close()
            conn.close()
            print(data)
            return data
    
def checkPass(upass):
        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor(buffered=True)
            pass_query = "SELECT userPasswd FROM folha WHERE userPasswd = %s" 
            cursor.execute(pass_query,(upass,) )
        
            data = cursor.fetchone() 
            print(data)

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

            print(data)
            return data


def get_db_fila(tipo):
    nFila=minhaSenha=mesa=0
    data = []
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(buffered=True)
        if (tipo == "comum"):

            cursor.execute('SELECT id,nFila,minhaSenha,tipo,mesa,amaterasu,rasengan FROM pedra WHERE tipo="comum" ORDER BY id DESC LIMIT 1;')

        if (tipo == "pref"):

            cursor.execute('SELECT id,nFila,minhaSenha,tipo,mesa,amaterasu,rasengan FROM pedra WHERE tipo="pref" ORDER BY id DESC LIMIT 1;')

        row = cursor.fetchone()

        while row is not None:
#            print(row[0]); print(row[1]);print(row[2])
#            print(row[3]); print(row[4]);print(row[5])
#            print(row[6])
            data.append(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

        filaID = data[0][0]
        nFila = data[0][1]
        minhaSenha = data[0][2]
        tipo = data[0][3]
        numeroMesa = data[0][4]
        amaterasu = data[0][5]
        rasengan = data[0][6]

        return filaID,nFila,minhaSenha,tipo,numeroMesa,amaterasu,rasengan


def Many():

    def iter_row(cursor, size):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(buffered=True)

        cursor.execute("SELECT id,minhaSenha,amaterasu FROM pedra")

        for row in iter_row(cursor, 10):
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def insertFila(nFila,tipo):
    query = "INSERT INTO pedra (nFila,tipo) " \
            "VALUES(%s,%s)"
    args = (nFila, tipo)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def update_fila(id,amaterasu,rasengan):
    # read database configuration
    db_config = read_db_config()

    # prepare query and data
    query = "UPDATE pedra SET amaterasu = %s,rasengan = %s WHERE id = %s"

    data = (id,amaterasu,rasengan)

    try:
        conn = MySQLConnection(**db_config)

        # update book title
        cursor = conn.cursor()
        cursor.execute(query, data)

        # accept the changes
        conn.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

#def main():
#    insert_book('A Sudden Light','9781439187036')
#    connect()
#    Many()
#     return get_db_fila("comum")

#if __name__ == '__main__':
#    main()
