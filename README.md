**Online Book Store**
Project Overview
This project is an online book store built using Django. It features a robust authentication system, secure data handling, and two types of users: end users and administrators. End users can browse and purchase books, while administrators can manage the application data.

Features
User Authentication: Secure login and registration forms.
User Roles:
End User: Can browse and purchase books.
Admin: Can manage books, orders, and user data.
Security: Implemented using Django tokens (e.g., CSRF tokens).
Database: Uses SQLite for data storage.

Usage
End User
Register/Login: Create an account or log in to purchase books.
Browse Books: View the list of available books.
Purchase Books: Add books to the cart and complete the purchase.
Admin
Manage Books: Add, update, or delete books from the store.
Manage Orders: View and process orders.
Manage Users: View user information and manage user accounts.
Security
CSRF Protection: All forms are protected against Cross-Site Request Forgery (CSRF) using Django's built-in CSRF tokens.
Authentication Tokens: Secure user authentication and session management.
Database
The project uses SQLite as its database. SQLite is a lightweight, file-based database that's easy to set up and perfect for development and testing purposes.

To run the server:
python manage.py runserver
