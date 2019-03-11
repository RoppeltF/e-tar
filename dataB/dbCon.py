import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='K0di123$',
    database='etar'
)

dBase = mydb.cursor()

def dBaseClose():
    mydb.commit()
    dBase.close()
    mydb.close()
