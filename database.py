'''
Author - Abdulmuid Olaniyan
Purpose - A database that stores every transaction information
'''
import sqlite3

class Database_Manager():
    def __init__(self, db_name="database.db"):
        '''
        Initialize the database connection
        '''
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name, check_same_thread=False)
        self._cursor = self._connection.cursor() 
        self.create_table()

    def create_table(self):
        '''
        Creates transaction table if it doesn't exist which will prevent duplicate tables
        Implements a SQL command that tells SQLite to create the table
        '''    
        #id serves as a unique identifier for each row and will increment(e.g. 1, 2, 3...)
        #REAL for amount will allow decimal inputs and NULL doesn't allow an empty field
        #category to store whatever the money was used for as a string   
        #description is optional
        #dates will be stored as a string
        query = """
        CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
        )
        """
        self._cursor.execute(query)
        self._connection.commit()

    def insert_transactions(self, amount, category, description, date):
        '''
        Inserts a new transaction into the database
        '''    
        query = "INSERT INTO transactions(amount, category, description, date) VALUES (?, ?, ?, ?)"
        self._cursor.execute(query, (amount, category, description, date))
        self._connection.commit()

    def get_transactions(self):
        '''
        Retrieves all transactions from the database
        '''    
        query = "SELECT * FROM transactions"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def get_transactions_by_date(self, start_date, end_date):
        '''
        Retrieve transactions within a specific date range
        '''
        query = "SELECT * FROM transactions WHERE date BETWEEN ? AND ?"
        self._cursor.execute(query, (start_date, end_date))
        return self._cursor.fetchall()
    
    def get_transactions_by_category(self, category):
        '''
        Retrieve transactions for a specific category
        '''
        query = "SELECT * FROM transactions WHERE category = ?"
        self._cursor.execute(query, (category,))
        return self._cursor.fetchall()
    
    def close_db(self):
        '''
        Closes the database connection
        '''
        self._connection.close()

    



