---> Python-based shopping management system with customer/product management, billing, and email notifications. Built with Tkinter (GUI), MySQL (database), and SMTP (email). Features CRUD operations, cart functionality, and printable bills.


# Shopping Management System
A Python-based shopping management system with customer and product management, billing, and email notification features.

## Features
- **Customer Management**:
  - Add, edit, update, and delete customer records
  - Store customer details (name, address, phone, delivery address, email)

- **Product Management**:
  - Add, edit, update, and delete product records
  - Upload product images
  - Manage product rates

- **Billing System**:
  - Generate bills with automatic numbering
  - Add multiple products to cart
  - Calculate total amounts
  - Print bills

- **Email Notifications**:
  - Send formatted bill emails to customers
  - HTML formatted emails with product details

## Prerequisites
- Python 3.x
- MySQL Database
- Required Python packages:
    - tkinter
    - mysql-connector-python
    - pillow (PIL)
    - smtplib (for email functionality)
    - 
## Installation
1. Clone the repository:
 git clone https://github.com/jeet002/shopping-management-system.git
 cd shopping-management-system

2. Set up MySQL database:
Create a database named python_pro_shopping

Create the following tables:
CREATE TABLE customer (
    Cid INT AUTO_INCREMENT PRIMARY KEY,
    Cname VARCHAR(100),
    Caddress VARCHAR(200),
    Cphone VARCHAR(15),
    Cdeliveryadd VARCHAR(200),
    Cemail VARCHAR(100),
    DateTime DATE
);

CREATE TABLE product (
    Pid INT AUTO_INCREMENT PRIMARY KEY,
    Pname VARCHAR(100),
    Prate DECIMAL(10,2),
    Pimage VARCHAR(255),
    DateTime DATE
);

CREATE TABLE cart (
    Cartid INT AUTO_INCREMENT PRIMARY KEY,
    Pid INT,
    Cid INT,
    BillNo INT,
    Pname VARCHAR(100),
    Prate DECIMAL(10,2),
    Pquantity INT,
    Ptotalamount DECIMAL(10,2),
    DateTime DATE
);

CREATE TABLE orders (
    Oid INT AUTO_INCREMENT PRIMARY KEY,
    Pid INT,
    Cid INT,
    BillNo INT,
    Pname VARCHAR(100),
    Prate DECIMAL(10,2),
    Pquantity INT,
    Ptotalamount DECIMAL(10,2),
    DateTime DATE
);

OR

## Use .sql file which is given in files section and import in your MYSQL Database

3. Configure database connection:
Update the MySQL connection details in all three Python files:

mysql.connector.connect(
    host="localhost",
    database="python_pro_shopping",
    user="root",
    password="yourpassword"
)

4. For email functionality:
Update the email credentials in Customer_Product.py:

sender_email = "your_email@gmail.com"
sender_password = "your_app_password"  # Use app-specific password for Gmail

## Usage
Run the application by executing any of the three main files:

Customer Management:
python Customer.py

Product Management:
python Product.py

Billing System:
python Customer_Product.py
The files are interconnected with buttons to navigate between different modules.

## Screenshots
![image alt](https://github.com/jeet002/shopping-management-system/blob/a411bab4f37fefba01488d81c485f0403379dc00/Main_Blank_Page.png)

## File Structure
Customer.py: Customer management module
Product.py: Product management module
Customer_Product.py: Billing system and main interface
product_images/: Directory for storing product images (created automatically)

## Notes
The system uses a local MySQL database by default
For production use, consider:
  Securing database credentials
  Using environment variables for sensitive information
  Implementing proper error handling
  Adding user authentication# shopping-management-system
