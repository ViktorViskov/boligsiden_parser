# 
# class for open connection to mysql
# 

# libs
import mysql.connector

class Mysql_Connect:

    # constructor
    def __init__(self, host, user, password, db):

        self.host = host
        self.user = user
        self.password = password
        self.db = db

        # Create connection 
        try:
            self.Connect()
        except:
            print("DB connection error")

    # create connection
    def Connect(self):
        # connection
        self.connection = mysql.connector.connect(host = self.host, user = self.user, passwd = self.password, database = self.db)

        # io buffer cursor
        self.cursor = self.connection.cursor()

    # Input (not read server ansver)
    def I(self, sql_command):

        self.cursor.execute(sql_command)
        self.connection.commit()

    
    # Input and Outpur
    def IO(self, sql_command):

        self.cursor.execute(sql_command)

        return self.cursor.fetchall()