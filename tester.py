# Just a tester to test the database
from database import Database_Manager

# Create a database manager object
db = Database_Manager()

# Insert a test transaction
db.insert_transactions(100, "Food", "Bought dinner", "2025-03-22")

# Retrieve transactions
transactions = db.get_transactions()
for transaction in transactions:
    print(transaction)

# Close the database connection
db.close_db()    