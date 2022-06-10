import mysql.connector
# from constants import PORT, SERVER_ADDRESS
dbHost = ""
dbUser = ""
dbPassword = ""
dbName = ""
dbConn = ""

def openDb():
    # Open database connection
    dbConn = mysql.connector.connect(host=dbHost, user=dbUser, passwd=dbPassword, database=dbName)
    return dbConn


def closeDb():
    print()
    # dbConn.close()

