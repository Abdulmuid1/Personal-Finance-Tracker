# Personal Finance Tracker

A lightweight, web-based finance tracker built with Flask that helps users manage their daily expenses. One can add, filter, categorize, and visualize transactions, and also export them as a PDF report.

---

## Features

- Add and view income/expense transactions
- Filter transactions by category and date
- Auto-handle custom categories
- View interactive bar charts of expenses by category
- Download filtered or full transaction history as a PDF
- Simple, mobile-friendly frontend using HTML, CSS, and JavaScript

---

## Project Structure

```
Personal-Finance-Tracker/
├── static/
│   ├── style.css          
│   └── script.js          
├── templates/
│   └── transactions.html  
├── app.py                 
├── database.py            
├── database.db           
├── tester.py             
├── Dockerfile            
├── requirements.txt       
├── README.md             
└── LICENSE               
```

---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/Abdulmuid1/Personal-Finance-Tracker.git
cd Personal-Finance-Tracker
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask app
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

---

## Technologies Used

- **Flask** – lightweight backend
- **SQLite** – for transaction storage
- **pandas** & **matplotlib** – for generating visual charts
- **reportlab** – to export PDF reports
- **HTML/CSS/JS** – for frontend layout and interactivity

---

## Run with Docker

```bash
docker build -t finance-tracker .
docker run -p 5000:5000 finance-tracker
```

---

## Future Improvements

- Add user authentication
- Add pie chart for better visuals
- Include budget tracking and alerts
- Improve mobile responsiveness

---

## Deployment

This app was deployed to **AWS** using the web console to configure and launch the instance. While not deployed through infrastructure as code, this gave me hands-on experience with AWS services and manual configuration, including instance setup, security groups, and hosting a Flask application in the cloud.

## License

Licensed under the [MIT License](LICENSE).
