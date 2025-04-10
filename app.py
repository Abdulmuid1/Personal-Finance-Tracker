import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 
from flask import Flask, render_template, request, redirect, url_for, Response
from database import Database_Manager

app = Flask(__name__)
db = Database_Manager()

@app.route('/transactions', methods=['GET'])
def show_transactions():
    '''
    This function handles filtering transactions by category or a date range.
    '''
    category = request.args.get('category')  # Get category from URL (if provided)
    start_date = request.args.get('start_date')  # Get start date from URL
    end_date = request.args.get('end_date')  # Get end date from URL

    if category:  
        transactions = db.get_transactions_by_category(category)
    elif start_date and end_date:  # Only filter by date if both are provided
        transactions = db.get_transactions_by_date(start_date, end_date)
    else:  
        transactions = db.get_transactions()  # If no filters, show all transactions.

    return render_template('transactions.html', transactions=transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    '''
    This function adds a new transaction to the database.
    '''
    amount = request.form["amount"]
    category = request.form["category"]
    description = request.form["description"]
    date = request.form["date"]

    # Handle custom category if provided
    if category == "Others":
        category = request.form["custom_category"]

    # Insert the new transaction into the database
    db.insert_transactions(amount, category, description, date)

    # Redirect back to the transaction list page
    return redirect(url_for('show_transactions'))  # This will call show_transactions() to refresh the page

@app.route('/charts')
def show_charts():
    '''
    This function generates a bar chart of expenses by category.
    - It retrieves all transactions from the database.
    - It creates a bar chart and returns it as an image.
    '''
    # Get all transactions
    transactions = db.get_transactions()

    # Convert transactions into a pandas DataFrame for easy manipulation
    df = pd.DataFrame(transactions, columns=['id', 'amount', 'category', 'description', 'date'])

    # Group by category and sum the amounts
    category_expenses = df.groupby('category')['amount'].sum()

    plt.figure(figsize=(10, 6))
    category_expenses.plot(kind='bar', color='skyblue')

    plt.title('Expenses by Category', fontsize=14, fontweight='bold')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Amount', fontsize=12)

    # Rotate the x-axis labels to prevent cropping
    plt.xticks(rotation=30, ha='right')  

    # Adjust layout to prevent text from getting cut off
    plt.tight_layout()  

    # Grid lines for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add value labels on top of bars
    for i, value in enumerate(category_expenses):
        plt.text(i, value + 1, str(round(value, 2)), ha='center', fontsize=10, fontweight='bold')


    # Save the plot to a BytesIO object and send it as a response
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    return Response(img, mimetype='image/png')

@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    '''
    This function generates a PDF of the transaction history.
    '''
    category = request.args.get('category')  # Get category from URL (if provided)
    start_date = request.args.get('start_date')  # Get start date from URL
    end_date = request.args.get('end_date')  # Get end date from URL

    if category:
        transactions = db.get_transactions_by_category(category)
    elif start_date and end_date:  # Only filter by date if both are provided
        transactions = db.get_transactions_by_date(start_date, end_date)
    else:
        transactions = db.get_transactions()  # If no filters, show all transactions.

    # Create a PDF in memory
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    # Add a title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Transaction History")

    # Add the table headers
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "ID")
    c.drawString(100, height - 100, "Amount")
    c.drawString(200, height - 100, "Category")
    c.drawString(350, height - 100, "Description")
    c.drawString(500, height - 100, "Date")

    # Add the transaction rows
    c.setFont("Helvetica", 10)
    y_position = height - 120
    for transaction in transactions:
        c.drawString(50, y_position, str(transaction[0]))
        c.drawString(100, y_position, str(transaction[1]))
        c.drawString(200, y_position, transaction[2])
        c.drawString(350, y_position, transaction[3])
        c.drawString(500, y_position, transaction[4])
        y_position -= 20

    # Save the PDF
    c.save()

    # Get the value of the PDF and return it as a download
    pdf_buffer.seek(0)
    return Response(pdf_buffer, mimetype='application/pdf', headers={
        "Content-Disposition": "attachment; filename=transaction_history.pdf"
    })

if __name__ == "__main__":
    app.run(debug=True)
