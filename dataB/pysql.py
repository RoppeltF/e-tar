from mysql.connector import MySQLConnection, Error
#from dbconfig import read_db_config
from dataB.dbconfig import read_db_config


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

    return 0

# def get_lista(id,amaterasu,rasengan):
#     # read database configuration
#     db_config = read_db_config()

#     # prepare query and data
#     query = "UPDATE pedra SET amaterasu = %s,rasengan = %s WHERE id = %s"

#     data = (id,amaterasu,rasengan)

#     try:
#         conn = MySQLConnection(**db_config)

#         # update book title
#         cursor = conn.cursor()
#         cursor.execute(query, data)

#         # accept the changes
#         conn.commit()

#     except Error as error:
#         print(error)

#     finally:
#         cursor.close()
#         conn.close()

def update_lista(link,nomes,datas):
    # read database configuration
    db_config = read_db_config()

    link = (*link,)
    nomes = (*nomes,)
    datas = (*datas,)

    # prepare query and data
    query = "INSERT INTO listas (nomes,link,data) VALUES (%s,%s,%s)"

    data = zip(nomes,link,datas)
    data = tuple(data)

    try:
        conn = MySQLConnection(**db_config)

        # update book title
        cursor = conn.cursor()
        cursor.executemany( query, data )

        # accept the changes
        conn.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

#Function to check the last data in the database
def checkDados():

    # read database configuration
    db_config = read_db_config()

    # prepare query and data
    query = "SELECT link FROM listas ORDER BY id DESC LIMIT 1;"

    try:
        conn = MySQLConnection(**db_config)

        # update book title
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

    return result



# def main():
#     connect()
#     print( checkDados() )

#     link = ["agsd3gqr38f0sdfj2k3r23f","22agsd3gqr38f0sdfj2k3r23f","33434agsd3gqr38f0sdfj2k3r23f"]
#     nomes = ["nome6","nome7","nome8"]
#     datas = ["2020-01-01","2020-01-02","2020-01-03"]

#     print( update_lista(link,nomes,datas) )

# if __name__ == '__main__':
#    main()
