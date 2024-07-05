Banking and Exchange Web Application

Overview A Django-based app for banking and exchange, allowing users to manage accounts, perform transactions, and handle foreign exchange.

Features User Authentication, Account Management, Money Transfer, Foreign Exchange, Notifications, KYC Verification, Admin Dashboard,

Technologies Backend: Django, Frontend: HTML, CSS, JavaScript Database: db.sqlite3

Login Details: email:tobemarizu@gmail.com password:12345

Setup 1)Clone the Repo:git clone https://github.com/yourusername/banking-exchange-app.git cd banking-exchange-app

2)Virtual Environment:python -m venv env source env/bin/activate # Windows: env\Scripts\activate

3)Install Dependencies:pip install -r requirements.txt

4)Run Migrations:python manage.py makemigrations python manage.py migrate

5)Create Superuser:python manage.py createsuperuser

6)Collect Static Files:python manage.py collectstatic

7)Run Server:python manage.py runserver

Usage Register/Login: Access user dashboard. Manage Accounts: View and transfer funds. Currency Exchange: Perform exchanges, view rates. Admin: Manage users, accounts, transactions. Admin Dashboard:

Admins can manage users, accounts, and transactions through the admin interface. Access the admin interface at http://127.0.0.1:8000/admin/ and log in with superuser credentials.

Contributing Fork the repo. Create a branch: git checkout -b feature-name. Commit changes: git commit -m 'Add feature'. Push: git push origin feature-name. Submit a pull request.

License MIT License. See LICENSE.

Contact For support, contact tobemarizu@gmail.com