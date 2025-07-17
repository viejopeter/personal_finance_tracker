# Personal Finance Tracker

A web-based application to track personal finances, manage income, expenses, and set up budgets. Built using Django and Django ORM to practice working with models, relationships, and querying data.

---

## Features

    User Authentication: Users can create accounts and log in to manage their finances.

    Income & Expense Tracking: Users can add, categorize, and track their financial transactions.

    Budget Management: Users can set monthly budgets and track their spending against it.

    Recurring Transactions: Support for recurring expenses like rent or subscriptions.

    Transaction Categories: Categorize transactions (e.g., food, rent, entertainment).

    Reports: View detailed financial reports for each month, including total expenses, income, and categories.

    Graphical Insights: Visualize spending trends and compare against set budgets.

## Tech Stack

    Django: Web framework for Python.

    PostgreSQL: Database (can be replaced with SQLite or MySQL).

    Django ORM: Object-Relational Mapping for interacting with the database.

    Bootstrap: For basic front-end design (optional).

## Setup Instructions

1. Clone the Repository
   Clone the repository to your local machine:
    ```
    git clone https://github.com/yourusername/personal_finance_tracker.git
    cd personal_finance_tracker
    ```
   
2. Set up the Virtual Environment

   It’s a good practice to use a virtual environment. To create one:
     ```
     python -m venv .venv
     ```
    Activate the virtual environment:
    On Windows: 
     ```
    .venv\Scripts\activate
     ```
    On macOS/Linux:
     ```
    source .venv/bin/activate
     ```
   
3. Install Dependencies

    Install the required dependencies using pip:
    ```
    pip install -r requirements.txt
    ```
   
4. Set up the Database using .env file
    ```
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=5432
    ```
   Run migrations to set up the database:
    ```
    python manage.py migrate
    ```

5. Create a Superuser

   Create a superuser to access the Django admin panel:
    ```
    python manage.py createsuperuser
    ```
   Follow the prompts to create a superuser.

6. Run the Development Server

   Start the Django development server:
    ```
    python manage.py runserver
    ```
    You can now access the application at http://127.0.0.1:8000/.

7. Access the Admin Panel

    To manage users, transactions, and other data, go to http://127.0.0.1:8000/admin/ and log in with the superuser credentials.
