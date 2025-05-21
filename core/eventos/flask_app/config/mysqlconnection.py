## Coding Dojo - Python Bootcamp Jan 2025
## Eventos
## Roberto Alvarez, 2025
 
import pymysql.cursors 
import os

class MySQLConnection: 
    def __init__(self, db=None):
        print("USER ", os.getenv("USER"))
        connection = pymysql.connect(
            host=os.getenv("HOST_DATABASE", "localhost"),
            user=os.getenv("USER_DATABASE"),
            password=os.getenv("PASSWORD"),
            db=db if db else os.getenv("DATABASE"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        self.connection = connection 
        
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                # Print query for debugging
                print("Running Query:", query)
                
                if data:
                    executable = cursor.execute(query, data)
                else:
                    executable = cursor.execute(query)
                    
                if query.lower().find("insert") >= 0:
                    # If INSERT, return the ID of the last inserted row
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # If SELECT, return the results as a dictionary
                    result = cursor.fetchall()
                    return result
                else:
                    # If UPDATE or DELETE, return nothing
                    self.connection.commit()
            except Exception as e:
                # If the query fails, print error and return False
                print("Something went wrong", e)
                return False
            finally:
                # Close the connection
                self.connection.close()

def connectToMySQL(db=None):
    # Function to create an instance of the connection
    return MySQLConnection(db)