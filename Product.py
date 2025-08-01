from tkinter import *
import mysql.connector
from tkinter import messagebox
import os
from tkinter import filedialog
from PIL import Image, ImageTk  # Importing Pillow for image handling
import shutil


# Initialize the main Tkinter frame
frame = Tk()
frame.geometry("800x600")
frame.title("Product Management System")

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
header_label.place(relx=0.5, y=25, anchor="center")

# Insert the header text
header_label.insert("1.0", "Add Product")

header_label.tag_add("underline", "1.0", "end")
header_label.tag_configure("underline", underline=True)

header_label.config(state="disabled")

# UI Components for Product and Rate
Label(frame, text="Product:", font=("Arial", 14)).place(x=30, y=148)
product_entry = Entry(frame, font=("Arial", 14), width=16)
product_entry.place(x=120, y=150)

Label(frame, text="Rate:", font=("Arial", 14)).place(x=30, y=248)
rate_entry = Entry(frame, font=("Arial", 14), width=16)
rate_entry.place(x=120, y=250)


# Function to open Customer_Product.py page
def open_Final_Page():
    try:
        # Execute the Customer_Product.py script
        os.system(
            "python Customer_Product.py"
        )  # Ensure the file is in the same directory
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Customer Page: {e}")


# Variable to store image path and Tkinter Image object
product_image_path = None
product_image_label = None  # Initialize a label to display the image

# Folder to save product images
IMAGE_FOLDER = "product_images"

# Ensure that the folder exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)


# Function to select the image but not save until Insert
def select_image():
    global product_image_path, product_image_label
    file_path = filedialog.askopenfilename(
        title="Select Product Image",
        filetypes=(("Image Files", "*.jpg;*.jpeg;*.png;*.gif"), ("All Files", "*.*")),
    )
    if file_path:
        # Get the product name entered by the user
        product_name = product_entry.get()
        if not product_name:
            messagebox.showwarning(
                "Input Error", "Please enter the product name first."
            )
            return

        # Store the file path (but don't copy yet)
        product_image_path = file_path

        # Open and display the image in the Tkinter window
        img = Image.open(file_path)  # Open the image using PIL
        img = img.resize((350, 300), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        if product_image_label:
            product_image_label.config(image=img_tk)
            product_image_label.image = img_tk
        else:
            product_image_label = Label(frame, image=img_tk)
            product_image_label.place(x=380, y=75)  # Adjust position of image
            product_image_label.image = img_tk

        messagebox.showinfo("Image Selected", "Product image selected successfully!")


# MySQL Connection Helper Function
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost", database="python_pro_shopping", user="root", password=""
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None


# Modify the insert_product function to store image in folder after the "Insert" button is clicked
def insert_product():
    name = product_entry.get()
    rate = rate_entry.get()

    if not name or not rate:
        messagebox.showwarning("Input Error", "All fields are required")
        return

    if not product_image_path:
        messagebox.showwarning("Input Error", "Please select a product image.")
        return

    try:

        # Now insert the product data into the database, including the image path
        con = connect_db()
        if con is None:
            return
        cursor = con.cursor()
        cursor.execute("SELECT * FROM product WHERE Pname=%s", (name,))
        if cursor.fetchone():
            messagebox.showerror("Error", "This Product Already Exists in Database.")
        else:
            # Move the image to the designated folder and give it a new name
            new_image_path = os.path.join(IMAGE_FOLDER, f"{name}.jpg")
            shutil.copy(product_image_path, new_image_path)
            cursor.execute(
                "INSERT INTO product (Pname, Prate, Pimage, DateTime) VALUES (%s, %s, %s, CURDATE())",
                (name, rate, new_image_path),
            )
            con.commit()
            messagebox.showinfo("Success", "Data Successfully Inserted.")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")
    finally:
        if con:
            con.close()
        clear_inputs()


from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import shutil
import mysql.connector


# Function to connect to the database
def connect_db():
    try:
        # Update connection parameters as per your setup
        con = mysql.connector.connect(
            host="localhost", user="root", password="", database="python_pro_shopping"
        )
        return con
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None


# Function to edit a product
def edit_product():
    selected_product = clicked1.get()
    if selected_product == "Select":
        messagebox.showwarning(
            "Input Error", "Please select a product from the dropdown."
        )
        return

    try:
        con = connect_db()
        if con is None:
            return
        cursor = con.cursor()

        # Fetch product details
        cursor.execute(
            "SELECT Prate, Pimage FROM product WHERE Pname=%s", (selected_product,)
        )
        result = cursor.fetchone()

        if result:
            product_rate = result[0]
            product_image_path = result[1]

            if not product_image_path:
                messagebox.showerror("Error", "Image not available for this product.")
                return
        else:
            messagebox.showerror("Error", "Product not found in the database.")
            return
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return
    finally:
        if con:
            con.close()

    def update_product():
        updated_name = update_product_entry.get()
        updated_rate = update_rate_entry.get()

        if not updated_name or not updated_rate:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        new_image_path = image_path_var.get()

        try:
            con = connect_db()
            if con is None:
                return
            cursor = con.cursor()

            if new_image_path:
                new_image_filename = os.path.basename(new_image_path)
                image_save_path = os.path.join("product_images", new_image_filename)

                # Create directory if not exists
                if not os.path.exists("product_images"):
                    os.makedirs("product_images")

                shutil.copy(new_image_path, image_save_path)

                # Remove old image if exists
                old_image_path = os.path.join("product_images", product_image_path)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

                cursor.execute(
                    "UPDATE product SET Pname=%s, Prate=%s, Pimage=%s WHERE Pname=%s",
                    (updated_name, updated_rate, image_save_path, selected_product),
                )
            else:
                cursor.execute(
                    "UPDATE product SET Pname=%s, Prate=%s WHERE Pname=%s",
                    (updated_name, updated_rate, selected_product),
                )

            con.commit()
            messagebox.showinfo("Success", "Product updated successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if con:
                con.close()
            update_window.destroy()
            refresh_dropdown()

    update_window = Toplevel(frame)
    update_window.title("Update Product")
    update_window.geometry("600x800")

    # Create a canvas to add scrolling
    canvas = Canvas(update_window)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = Scrollbar(update_window, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold all the widgets
    scrollable_frame = Frame(canvas)

    # Create a window inside the canvas to place the scrollable frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configure the frame to be scrollable
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        ),  # Update scroll region
    )

    Label(scrollable_frame, text="Update Product", font=("Arial 16 underline")).pack(
        pady=10
    )

    # Center the frame contents
    center_frame = Frame(scrollable_frame)
    center_frame.pack(expand=True)

    Label(center_frame, text="Product:", font=("Arial", 14)).pack()
    update_product_entry = Entry(center_frame, font=("Arial", 14), width=20)
    update_product_entry.pack(pady=5)
    update_product_entry.insert(0, selected_product)

    Label(center_frame, text="Rate:", font=("Arial", 14)).pack()
    update_rate_entry = Entry(center_frame, font=("Arial", 14), width=20)
    update_rate_entry.pack(pady=5)
    update_rate_entry.insert(0, product_rate)

    if product_image_path:
        image_file_path = product_image_path
        if os.path.exists(image_file_path):
            img = Image.open(image_file_path)
            img = img.resize((350, 300), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            # Title for the old image
            Label(center_frame, text="Old Image", font=("Arial", 14, "underline")).pack(
                pady=5
            )
            img_label = Label(center_frame, image=img_tk)
            img_label.pack(pady=10)
            img_label.image = img_tk
        else:
            messagebox.showerror("Error", "Image file not found: " + image_file_path)

    # Entry for selecting new image
    image_path_var = StringVar()

    def browse_image():
        global new_img_label  # Declare global before usage

        new_image_path = filedialog.askopenfilename(
            initialdir=".",
            title="Select Image",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("all files", "*.*")),
        )
        if new_image_path:
            image_path_var.set(new_image_path)  # Set the path in the variable

            # Load and display the selected image
            try:
                img = Image.open(new_image_path)  # Open the selected image
                img = img.resize(
                    (350, 300), Image.Resampling.LANCZOS
                )  # Resize the image
                img_tk = ImageTk.PhotoImage(img)

                if "new_img_label" in globals() and new_img_label.winfo_exists():
                    # If label exists, update its image
                    new_img_label.config(image=img_tk)
                    new_img_label.image = (
                        img_tk  # Keep reference to prevent garbage collection
                    )
                else:
                    # Create the label if it doesn't exist
                    new_img_label = Label(center_frame, image=img_tk)
                    new_img_label.pack(pady=10)
                    new_img_label.image = (
                        img_tk  # Keep reference to prevent garbage collection
                    )

            except Exception as e:
                messagebox.showerror("Image Error", f"Unable to load image: {e}")

    # Browse button
    browse_button = Button(
        center_frame, text="Browse", font=("Arial", 14), command=browse_image
    )
    browse_button.pack(pady=10)

    # Title for the new image
    Label(center_frame, text="New Image", font=("Arial", 14, "underline")).pack(pady=10)

    # Update button at the bottom
    Button(
        center_frame, text="Update", font=("Arial", 14), command=update_product
    ).pack(pady=20, side=BOTTOM)

    update_window.mainloop()


# Delete Product Function
def delete_product():
    selected_product = clicked1.get()
    if selected_product == "Select":
        messagebox.showwarning("Input Error", "Please select a product.")
        return

    try:
        con = connect_db()
        if con is None:
            return
        cursor = con.cursor()
        cursor.execute("DELETE FROM product WHERE Pname=%s", (selected_product,))
        con.commit()
        messagebox.showinfo("Success", "Product deleted successfully.")
        refresh_dropdown()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        if con:
            con.close()


# Clear Inputs
def clear_inputs():
    product_entry.delete(0, END)
    rate_entry.delete(0, END)
    global product_image_path
    product_image_path = None
    if product_image_label:
        product_image_label.config(image=None)
        product_image_label.image = None


# Refresh Dropdown
def refresh_dropdown():
    try:
        con = connect_db()
        if con is None:
            return
        cursor = con.cursor()
        cursor.execute("SELECT Pname FROM product")
        products = [row[0] for row in cursor.fetchall()]
        clicked1.set("Select")
        dropdown["menu"].delete(0, "end")
        for product in products:
            dropdown["menu"].add_command(
                label=product, command=lambda value=product: clicked1.set(value)
            )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        if con:
            con.close()


# Dropdown for Products
Label(frame, text="Product Name:", font=("Arial", 14)).place(x=30, y=550)
clicked1 = StringVar()
clicked1.set("Select")
dropdown = OptionMenu(frame, clicked1, "Select")
dropdown.place(x=170, y=550, height=32, width=150)
refresh_dropdown()


# Buttons Row 1 (Insert, Edit, Delete)
Button(frame, text="Insert", font=("Arial", 14), command=insert_product).place(
    x=120, y=400, width=120, height=40
)
Button(frame, text="Edit", font=("Arial", 14), command=edit_product).place(
    x=350, y=400, width=120, height=40
)
Button(frame, text="Delete", font=("Arial", 14), command=delete_product).place(
    x=550, y=400, width=120, height=40
)

# Buttons Row 2 (Open Customer Page, Clear, Exit)
Button(
    frame, text="Open Final Page", font=("Arial", 14), command=open_Final_Page
).place(x=120, y=460, width=190, height=40)
Button(frame, text="Clear", font=("Arial", 14), command=clear_inputs).place(
    x=350, y=460, width=120, height=40
)
Button(frame, text="Exit", font=("Arial", 14), command=frame.quit).place(
    x=550, y=460, width=120, height=40
)

# Add a button to select an image
Button(
    frame, text="Select Product Image", font=("Arial", 14), command=select_image
).place(x=120, y=300, width=120, height=40)


frame.mainloop()
