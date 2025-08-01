from tkinter import *
import mysql.connector
from tkinter import messagebox
import os  # Importing os to execute another Python script

# Initialize the main window
frame = Tk()
frame.geometry("800x670")
frame.title("Customer")


# Function to open Customer_Product.py page
def open_Final_Page():
    try:
        # Execute the Customer_Product.py script
        os.system(
            "python Customer_Product.py"
        )  # Ensure the file is in the same directory
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Customer Page: {e}")


# Header label
header_label = Text(
    frame,
    font=("Arial", 24, "bold"),
    height=1,
    width=15,
    bd=0,
    fg="black",
    bg=frame.cget("bg"),
)
header_label.place(relx=0.5, y=35, anchor="center")

# Insert the header text
header_label.insert("1.0", "Add Customer")

header_label.tag_add("underline", "1.0", "end")
header_label.tag_configure("underline", underline=True)

header_label.config(state="disabled")

# Customer Details Id,Name,Address,Phone,Delivery Add..
l1 = Label(frame, text="Customer Id :", font=("Arial", 14))
l1.place(x=50, y=108)
e1 = Entry(frame, font=("Arial", 14), width=25)
e1.place(x=250, y=110)

l2 = Label(frame, text="Customer Name :", font=("Arial", 14))
l2.place(x=50, y=158)
e2 = Entry(frame, font=("Arial", 14), width=25)
e2.place(x=250, y=160)

l3 = Label(frame, text="Address :", font=("Arial", 14))
l3.place(x=50, y=208)
e3 = Entry(frame, font=("Arial", 14), width=25)
e3.place(x=250, y=210)

l4 = Label(frame, text="Phone :", font=("Arial", 14))
l4.place(x=50, y=258)
e4 = Entry(frame, font=("Arial", 14), width=25)
e4.place(x=250, y=260)

l5 = Label(frame, text="Delivery Add :", font=("Arial", 14))
l5.place(x=50, y=308)
e5 = Entry(frame, font=("Arial", 14), width=25)
e5.place(x=250, y=310)

l6 = Label(frame, text="Email id :", font=("Arial", 14))
l6.place(x=50, y=358)
e6 = Entry(frame, font=("Arial", 14), width=25)
e6.place(x=250, y=360)
# # Image
# l7 = Label(frame, bg="skyblue", width=42, height=15)
# l7.place(x=450, y=108)


# Function to connect MySQL and Insert data into customer Table
def btninsert():
    cname = e2.get()
    caddress = e3.get()
    cphone = e4.get()
    cdeliveryadd = e5.get()
    cemail = e6.get()

    if (
        cname == ""
        or caddress == ""
        or cphone == ""
        or cdeliveryadd == ""
        or cemail == ""
    ):
        messagebox.showwarning("Input Error", "All fields are required")
    else:
        try:
            con = mysql.connector.connect(
                host="localhost",  # Replace with your MySQL host
                database="python_pro_shopping",  # Replace with your MySQL database name
                user="root",  # Replace with your MySQL username
                password="",  # Replace with your MySQL password
            )
            cmd = con.cursor()

            cmd.execute(
                "insert into customer values(NULL,%s,%s,%s,%s,%s,CURDATE())",
                (cname, caddress, cphone, cdeliveryadd, cemail),
            )

            con.commit()
            messagebox.showinfo("Message", "Your data successfully saved...")
            con.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            e1.delete(0, "end")
            e2.delete(0, "end")
            e3.delete(0, "end")
            e4.delete(0, "end")
            e5.delete(0, "end")
            e1.focus()


# Function to connect to MySQL and Featch Data From table by Given CID
def btnedit():
    cid = e1.get()
    if cid == "":
        messagebox.showwarning("Input Error", "All fields are required")
    else:
        try:
            con = mysql.connector.connect(
                host="localhost",
                database="python_pro_shopping",
                user="root",
                password="",
            )
            cmd = con.cursor()
            cmd.execute("select * from customer where Cid=%s", (cid))
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
            e2.insert(0, cname)
            e3.insert(0, caddress)
            e4.insert(0, cphone)
            e5.insert(0, cdeliveryadd)
            con.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error{e}")


# Function to connect MySQL and Update the Data of perticular customer
def btnupdate():
    cname = e2.get()
    caddress = e3.get()
    cphone = e4.get()
    cdeliveryadd = e5.get()
    datashowid = e1.get()
    if (
        cname == ""
        or caddress == ""
        or cphone == ""
        or cdeliveryadd == ""
        or datashowid == ""
    ):
        messagebox.showwarning("Input Error", "All fields are required")
    else:
        try:
            con = mysql.connector.connect(
                host="localhost",
                database="python_pro_shopping",
                user="root",
                password="",
            )
            cmd = con.cursor()

            cmd.execute(
                "update customer set Cname=%s,Caddress=%s,Cphone=%s,Cdeliveryadd=%s where Cid=%s",
                (cname, caddress, cphone, cdeliveryadd, datashowid),
            )
            con.commit()
            messagebox.showinfo(
                "Message", "Your selected record successfully updated..."
            )
            con.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error:{e}")
        finally:
            e1.delete(0, "end")
            e2.delete(0, "end")
            e3.delete(0, "end")
            e4.delete(0, "end")
            e5.delete(0, "end")
            e1.focus()


# Function to connect MySQL and Delete selected record
def btndelete():
    cid = e1.get()
    if cid == "":
        messagebox.showwarning("Input Error", "All fields are required")
    else:
        try:
            con = mysql.connector.connect(
                host="localhost",
                database="python_pro_shopping",
                user="root",
                password="",
            )
            cmd = con.cursor()

            cmd.execute("delete from customer where Cid=%s", (cid))
            con.commit()
            messagebox.showinfo(
                "Message", "Your selected record successfully deleted..."
            )
            con.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error:{e}")
        finally:
            e1.delete(0, "end")
            e2.delete(0, "end")
            e3.delete(0, "end")
            e4.delete(0, "end")
            e5.delete(0, "end")
            e6.delete(0, "end")
            e1.focus()


def btnclear():
    e1.delete(0, "end")
    e2.delete(0, "end")
    e3.delete(0, "end")
    e4.delete(0, "end")
    e5.delete(0, "end")
    e6.delete(0, "end")
    e1.focus()


def btnexit():
    exit()


# Buttons

b1 = Button(frame, text="Insert", command=btninsert, font=("Arial", 14), width=12)
b1.place(x=120, y=450)

b2 = Button(frame, text="Update", command=btnupdate, font=("Arial", 14), width=12)
b2.place(x=330, y=450)

b3 = Button(frame, text="Edit", command=btnedit, font=("Arial", 14), width=12)
b3.place(x=550, y=450)

b4 = Button(frame, text="Delete", command=btndelete, font=("Arial", 14), width=12)
b4.place(x=120, y=520)

b5 = Button(frame, text="Clear", command=btnclear, font=("Arial", 14), width=12)
b5.place(x=330, y=520)

b6 = Button(frame, text="Exit", command=btnexit, font=("Arial", 14), width=12)
b6.place(x=550, y=520)
# New Button to Open Customer_Product Page
Button(
    frame, text="Open Final Page", font=("Arial", 14), command=open_Final_Page
).place(x=300, y=590, width=190)


frame.mainloop()
