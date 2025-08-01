from tkinter import *
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from tkinter import messagebox, Toplevel, Label, LabelFrame
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os  # Importing os to execute another Python script

frame = Tk()
frame.geometry("1200x780")
frame.title("Bill Generate")


def open_Customer_Page():
    try:
        # Execute the Customer_Product.py script
        os.system("python Customer.py")  # Ensure the file is in the same directory
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Customer Page: {e}")


def open_Product_Page():
    try:
        # Execute the Customer_Product.py script
        os.system("python Product.py")  # Ensure the file is in the same directory
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Customer Page: {e}")


# Code for the Generate Bill No

billl = Label(frame, text="Bill No.", font=("Arial", 14))
billl.place(x=30, y=40)
bille = Entry(frame, font=("Arial", 14), width=13, state="readonly", bg="#FFFF00")
bille.place(x=170, y=40)

billno = 1


def newbill():
    bille.config(state="normal")
    global billno
    bille.delete(0, "end")

    con = mysql.connector.connect(
        host="localhost", database="python_pro_shopping", user="root", password=""
    )
    cmd = con.cursor()
    cmd.execute("select max(BillNo) from orders")
    data = cmd.fetchall()

    for row in data:
        billnodata = int("%s" % (row[0]))
    #     bill = bille.get()
    #     if int(float(billno)) == billnotabledata:
    #         billno = billno + 1
    #     else:
    #         billno = bille.get()
    billnodata = billnodata + 1
    bille.insert(0, billnodata)
    # con.commit()
    # con.close()
    bille.config(state="readonly")


b1 = Button(frame, text="New", command=newbill, font=("Arial", 13), width=14)
b1.place(x=400, y=37)


# Customer Id Dropdown,Label
l1 = Label(frame, text="Customer Id", font=("Arial", 14))
l1.place(x=30, y=105)

con = mysql.connector.connect(
    host="localhost", database="python_pro_shopping", user="root", password=""
)
cmd = con.cursor()

clicked1 = StringVar()

cmd.execute("select * from customer")
data = cmd.fetchall()
cid = []

for row in data:
    cid.append("%s,%s" % (row[0], row[1]))

clicked1.set("Select")
drop1 = OptionMenu(
    frame,
    clicked1,
    *cid,
)
drop1.place(x=170, y=103, height=32, width=150)

con.commit()
con.close()


# Button


# Function to connect MySQL and Search the Customer Data From the customer Table By Selected CID
def btnsearch1():
    e1.delete(0, "end")
    e2.delete(0, "end")
    e3.delete(0, "end")
    e4.delete(0, "end")
    cid = clicked1.get()
    cid = cid[0]
    if cid == "Select" or cid == "":
        messagebox.showwarning("Input Error", "First Select the Customer Name or Id.")
    else:
        try:
            con = mysql.connector.connect(
                host="localhost",
                database="python_pro_shopping",
                user="root",
                password="",
            )
            cmd = con.cursor()

            cmd.execute("select * from customer where Cid=%s" % cid)
            data = cmd.fetchall()
            cname = ""
            caddress = ""
            cphone = ""
            cdeliveryadd = ""

            for row in data:
                cname = "%s" % (row[1])
                caddress = "%s" % (row[2])
                cphone = "%s" % (row[3])
                cdeliveryadd = "%s" % (row[4])
            e1.insert(0, cname)
            e2.insert(0, caddress)
            e3.insert(0, cphone)
            e4.insert(0, cdeliveryadd)

            con.commit()
            con.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")


b1 = Button(frame, text="Search", command=btnsearch1, font=("Arial", 13), width=14)
b1.place(x=400, y=101)

Button(
    frame, text="Open Customer Page", font=("Arial", 14), command=open_Customer_Page
).place(x=600, y=97, width=220)

# Customer Name

l2 = Label(frame, text="Customer Name", font=("Arial", 13))
l2.place(x=80, y=180)
e1 = Entry(frame, font=("Arial", 14), width=16)
e1.place(x=83, y=210)


# Address

l3 = Label(frame, text="Address", font=("Arial", 13))
l3.place(x=330, y=180)
e2 = Entry(frame, font=("Arial", 14), width=16)
e2.place(x=331, y=210)


# Phone

l4 = Label(frame, text="Phone", font=("Arial", 13))
l4.place(x=578, y=180)
e3 = Entry(frame, font=("Arial", 14), width=16)
e3.place(x=580, y=210)


# Delivery Add.

l5 = Label(frame, text="Delivery Add.", font=("Arial", 13))
l5.place(x=827, y=180)
e4 = Entry(frame, font=("Arial", 14), width=16)
e4.place(x=830, y=210)

# Product Name

l6 = Label(frame, text="Product Name", font=("Arial", 14))
l6.place(x=30, y=298)

con = mysql.connector.connect(
    host="localhost", database="python_pro_shopping", user="root", password=""
)
cmd = con.cursor()

clicked2 = StringVar()

cmd.execute("select * from product")
data = cmd.fetchall()
pname = []

for row in data:
    pname.append("%s" % (row[1]))

clicked2.set("Select")
drop2 = OptionMenu(frame, clicked2, *pname)
drop2.place(x=170, y=298, height=32, width=150)

con.commit()
con.close()

# Button


# Function to connect MySQL and Search the Product Data By the Product Name
def btnsearch2():
    e5.delete(0, "end")
    e6.delete(0, "end")
    e7.delete(0, "end")
    pname = clicked2.get()

    if pname == "Select" or pname == "":
        messagebox.showwarning("Input Error", "First Select the Product.")
    else:
        try:
            con = mysql.connector.connect(
                host="localhost",
                database="python_pro_shopping",
                user="root",
                password="",
            )
            cmd = con.cursor()

            cmd.execute("select * from product where Pname='" + pname + "'")
            data = cmd.fetchall()

            quentity = ""
            total = ""

            for row in data:
                prate = float("%s" % (row[2]))
            e5.insert(0, prate)

            e6.insert(0, 1)
            quentity = 1
            total = quentity * prate
            e7.insert(0, total)

            con.commit()
            con.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")


b2 = Button(frame, text="Search", command=btnsearch2, font=("Arial", 13), width=14)
b2.place(x=400, y=297)

Button(
    frame, text="Open Product Page", font=("Arial", 14), command=open_Product_Page
).place(x=600, y=294, width=220)


# Rate

l7 = Label(frame, text="Rate", font=("Arial", 13))
l7.place(x=80, y=370)
e5 = Entry(frame, font=("Arial", 14), width=16)
e5.place(x=83, y=400)


# Quantity

l8 = Label(frame, text="Quantity", font=("Arial", 13))
l8.place(x=330, y=370)
e6 = Entry(frame, font=("Arial", 14), width=16)
e6.place(x=331, y=400)

# Total Amount

l9 = Label(frame, text="Total Amount", font=("Arial", 13))
l9.place(x=578, y=370)
e7 = Entry(frame, font=("Arial", 14), width=16)
e7.place(x=580, y=400)


# Calculation of net-amount
def btncalculation():
    pquentity = e6.get()

    e5.delete(0, "end")
    e6.delete(0, "end")
    e7.delete(0, "end")
    pname = clicked2.get()

    if pname == "Select" or pname == "" or pquentity == "":
        messagebox.showwarning("Input Error", "Select Product.")
    else:
        try:
            con = mysql.connector.connect(
                host="localhost",
                database="python_pro_shopping",
                user="root",
                password="",
            )
            cmd = con.cursor()

            cmd.execute("select * from product where Pname='" + pname + "'")
            data = cmd.fetchall()

            prate = ""
            total = ""

            for row in data:
                prate = "%s" % (row[2])

            quentity = pquentity
            e5.insert(0, prate)
            e6.insert(0, quentity)

            total = float(quentity) * float(prate)
            e7.insert(0, total)

            con.commit()
            con.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")


b3 = Button(
    frame, text="Get Total", command=btncalculation, font=("Arial", 13), width=14
)
b3.place(x=825, y=396)

# Code for Items Show in to Cart

bill_frame = Frame(frame, height=1000, width=1000)
bill_frame.place(x=320, y=500)

bill_scroll = Scrollbar(bill_frame)
bill_scroll.pack(side=RIGHT, fill=Y)
bill_scroll = Scrollbar(bill_frame, orient="horizontal")
bill_scroll.pack(side=BOTTOM, fill=X)
my_bill = ttk.Treeview(
    bill_frame, yscrollcommand=bill_scroll.set, xscrollcommand=bill_scroll.set
)
my_bill.pack()
bill_scroll.config(command=my_bill.yview)
bill_scroll.config(command=my_bill.xview)


my_bill["columns"] = (
    "product_id",
    "product_name",
    "product_rate",
    "product_quntity",
    "product_totalamount",
)

my_bill.column("#0", width=0, stretch=NO)
my_bill.column("product_id", anchor=CENTER, width=75)
my_bill.column("product_name", anchor=CENTER, width=120)
my_bill.column("product_rate", anchor=CENTER, width=120)
my_bill.column("product_quntity", anchor=CENTER, width=120)
my_bill.column("product_totalamount", anchor=CENTER, width=120)


my_bill.heading("#0", text="", anchor=CENTER)
my_bill.heading("product_id", text="Sr", anchor=CENTER)
my_bill.heading("product_name", text="Name", anchor=CENTER)
my_bill.heading("product_rate", text="Rate", anchor=CENTER)
my_bill.heading("product_quntity", text="Quntity", anchor=CENTER)
my_bill.heading("product_totalamount", text="Net-Price", anchor=CENTER)

l10 = Label(frame, text="Net-Amount", font=("Arial", 13))
l10.place(x=600, y=745)
e8 = Entry(frame, font=("Arial", 14), width=16)
e8.place(x=700, y=745)

# selected items add into cart table and show in to cart

nettotal = 0
p = 1


def btnaddtocart():
    e8.delete(0, "end")
    pname = clicked2.get()

    if pname == "Select" or pname == "":
        messagebox.showwarning("Input Error", "First Select Product.")
    else:
        try:
            # Show Data into Text Area contol
            global p
            my_bill.insert(
                parent="",
                index="end",
                text="",
                values=(p, pname, e5.get(), e6.get(), e7.get()),
            )
            p = p + 1

            # Insert Data into cart
            con = mysql.connector.connect(
                host="localhost",
                database="python_pro_shopping",
                user="root",
                password="",
            )
            cmd = con.cursor()

            cmd.execute("select * from product where Pname='" + pname + "'")
            data = cmd.fetchall()

            for row in data:
                pid = float("%s" % (row[0]))

            cid = clicked1.get()
            cid = cid[0]
            prate = e5.get()
            pquantity = e6.get()
            ptotalamount = e7.get()
            billno = bille.get()

            cmd.execute(
                "insert into cart values(NULL,%s,%s,%s,%s,%s,%s,%s,CURDATE())",
                (pid, cid, billno, pname, prate, pquantity, ptotalamount),
            )

            con.commit()
            con.close()

            # Code for the find Net-Amount
            global nettotal
            nettotal = nettotal + float(e7.get())
            e8.insert(0, nettotal)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")


def fetch_data(query, params=()):
    con = mysql.connector.connect(
        host="localhost",
        database="python_pro_shopping",
        user="root",
        password="",
    )
    cmd = con.cursor()
    cmd.execute(query, params)
    data = cmd.fetchall()
    con.close()
    return data


def send_email(to_email, bill_no, products):
    sender_email = "pateljeet0003@gmail.com"
    sender_password = (
        "fukncfprbahzujzw"  # Consider using environment variables for security
    )
    subject = f"Your Bill No: {bill_no}"
    net = 0

    # Construct the HTML table for the email
    body = f"""
    <html>
        <body>
            <h2>Dear Customer 😊,</h2>
            <p>Thank you for shopping with us at ASP Infotech! 🛍️ We are pleased to share your bill details for your recent purchase. 💳</p>
            <p>Below are the details for your Bill No: {bill_no}:</p>
            <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th>Product</th>
                        <th>Rate</th>
                        <th>Quantity</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
    """
    for product in products:
        body += f"""
        <tr>
            <td>{product[5]}</td>
            <td>{product[6]}</td>
            <td>{product[7]}</td>
            <td>{product[8]}</td>
        </tr>
        """
        net += product[8]

    body += f"""
                </tbody>
            </table>
            <h3 style="text-align: right;">Net Total: {net} 💰</h3>
            <p>If you have any questions or need assistance, feel free to contact us. 📞</p>
            <p>Thank you for choosing ASP Infotech! 🙏</p>
        </body>
    </html>
    """

    # Prepare the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))  # Use "html" for HTML content

    # Send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        messagebox.showinfo("Email Sent", f"Bill No: {bill_no} sent to {to_email}")
    except Exception as e:
        messagebox.showerror("Email Error", f"Error sending email: {str(e)}")


def btngetbill():
    cid = clicked1.get()[0]

    if cid == "Select" or cid == "":
        messagebox.showwarning("Input Error", "First Select Customer Name Or Id.")
        return
    try:
        bill_no = str(bille.get())

        # Fetch cart data
        cart_data = fetch_data("SELECT * FROM cart WHERE BillNo=%s", (bill_no,))

        # Insert data into Orders table
        con = mysql.connector.connect(
            host="localhost",
            database="python_pro_shopping",
            user="root",
            password="",
        )
        cmd = con.cursor()
        for row in cart_data:
            cmd.execute(
                "INSERT INTO orders VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())",
                (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
            )

        # Delete from cart
        cmd.execute("DELETE FROM cart WHERE BillNo=%s", (bill_no,))

        # Fetch customer email
        email_data = fetch_data("SELECT Cemail FROM customer WHERE Cid=%s", (cid,))
        customer_email = email_data[0][0] if email_data else None

        # Fetch customer name
        name_data = fetch_data("SELECT Cname FROM customer WHERE Cid=%s", (cid,))
        customer_name = name_data[0][0] if name_data else "Unknown"

        # Fetch order data for email
        order_data = fetch_data("SELECT * FROM orders WHERE BillNo=%s", (bill_no,))

        con.commit()
        con.close()

        # Generate Bill
        printbill = Toplevel(frame)
        frame.iconify()
        printbill.geometry("700x670")
        printbill.title("FinalBill")
        printbill.configure(bg="#A9A9A9")

        lbf1 = LabelFrame(printbill, bg="white", width=400, height=600)
        lbf1.pack(pady=20)

        Label(
            lbf1,
            bg="white",
            text="-----------------------------------------------\nASP INFOTECH",
            font=("Arial", 15),
        ).place(x=30, y=30)
        Label(
            lbf1,
            bg="white",
            text="\t       Add:- Mahavirnagar\n\t       Himatnagar, Gujarat 383001\n",
            font=("Arial", 10),
        ).place(x=30, y=85)
        Label(
            lbf1,
            bg="white",
            text="-----------------------------------------------",
            font=("Arial", 15),
        ).place(x=30, y=120)

        Label(lbf1, bg="white", font=("Arial", 11), text="Name :-").place(x=30, y=175)
        Label(lbf1, bg="white", font=("Arial", 11), text=customer_name).place(
            x=90, y=177
        )

        Label(lbf1, bg="white", font=("Arial", 11), text="Bill No. :-").place(
            x=30, y=150
        )
        Label(lbf1, bg="white", font=("Arial", 11), text=bill_no).place(x=95, y=152)

        # Add table headers
        table_y = 210
        Label(
            lbf1,
            bg="white",
            font=("Arial", 10, "bold"),
            text="Sr",
            width=5,
            anchor="center",
        ).place(x=30, y=table_y)
        Label(
            lbf1,
            bg="white",
            font=("Arial", 10, "bold"),
            text="Product",
            width=15,
            anchor="center",
        ).place(x=70, y=table_y)
        Label(
            lbf1,
            bg="white",
            font=("Arial", 10, "bold"),
            text="Rate",
            width=10,
            anchor="center",
        ).place(x=200, y=table_y)
        Label(
            lbf1,
            bg="white",
            font=("Arial", 10, "bold"),
            text="Qty",
            width=5,
            anchor="center",
        ).place(x=280, y=table_y)
        Label(
            lbf1,
            bg="white",
            font=("Arial", 10, "bold"),
            text="Net",
            width=10,
            anchor="center",
        ).place(x=330, y=table_y)

        # Add table data
        for i, row in enumerate(order_data):
            table_y += 25
            Label(
                lbf1,
                bg="white",
                font=("Arial", 10),
                text=f"{i+1}",
                width=5,
                anchor="center",
            ).place(x=30, y=table_y)
            Label(
                lbf1,
                bg="white",
                font=("Arial", 10),
                text=f"{row[5]}",
                width=15,
                anchor="w",
            ).place(x=70, y=table_y)
            Label(
                lbf1,
                bg="white",
                font=("Arial", 10),
                text=f"{row[6]}",
                width=10,
                anchor="center",
            ).place(x=200, y=table_y)
            Label(
                lbf1,
                bg="white",
                font=("Arial", 10),
                text=f"{row[7]}",
                width=5,
                anchor="center",
            ).place(x=280, y=table_y)
            Label(
                lbf1,
                bg="white",
                font=("Arial", 10),
                text=f"{row[8]}",
                width=10,
                anchor="center",
            ).place(x=330, y=table_y)

        total_amount = fetch_data(
            "SELECT SUM(Ptotalamount) FROM orders WHERE BillNo=%s", (bill_no,)
        )[0][0]
        Label(
            lbf1, bg="white", font=("Arial", 11), text="Payable Bill Amount  : "
        ).place(x=32, y=table_y + 30)
        Label(lbf1, bg="white", font=("Arial", 11), text=total_amount).place(
            x=210, y=table_y + 30
        )

        Label(
            lbf1,
            bg="white",
            text="---------------------------------------------\nThank You\n---------------------------------------------",
            font=("Arial", 14),
        ).place(x=58, y=table_y + 60)

        # Send email
        if customer_email:
            send_email(customer_email, bill_no, order_data)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")


# Button

b4 = Button(
    frame, text="Add Item To Cart", command=btnaddtocart, font=("Arial", 13), width=14
)
b4.place(x=83, y=510)

b6 = Button(
    frame, text="Generate Bill", command=btngetbill, font=("Arial", 13), width=14
)
b6.place(x=83, y=620)


def btnclear():
    e1.delete(0, "end")
    e2.delete(0, "end")
    e3.delete(0, "end")
    e4.delete(0, "end")
    e5.delete(0, "end")
    e6.delete(0, "end")
    e7.delete(0, "end")
    e8.delete(0, "end")


def btnexit():
    exit()


# Button

b7 = Button(frame, text="Clear", command=btnclear, font=("Arial", 13), width=14)
b7.place(x=980, y=510)

b8 = Button(frame, text="Exit", command=btnexit, font=("Arial", 13), width=14)
b8.place(x=980, y=620)

frame.mainloop()
