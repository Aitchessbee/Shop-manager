import tkinter as tk
import mysql.connector
from PIL import ImageTk, Image  # type into terminal: pip install Pillow
import time
from prettytable import PrettyTable
import os,sys
import re
import json
from urllib.request import Request, urlopen

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def error_msg():
    error_win = tk.Toplevel()
    lbl1 = tk.Label(error_win, text="Invalid username or password (sql credentials) or SQL server has not be started", padx=10, pady=10)
    lbl1.grid(row=0, column=0)

    close_but = tk.Button(error_win, text="close", command=error_win.destroy, padx=10, pady=10)
    close_but.grid(row=1, column=0)

def func():
    global database
    try:
        database = mysql.connector.connect(host='localhost', user=user_entry.get(), password=pswd_entry.get())
        root1.destroy()
    except Exception:
        error_msg()

root1 = tk.Tk()
root1.title("Login")
root1.geometry("300x175")

title1 = tk.Label(root1,text="Login (mysql credentials)", padx=10, pady=10)
title1.grid(row=0, column=1)

user_lbl = tk.Label(root1,text="Username", padx=10, pady=10)
user_lbl.grid(row=1, column=0)

pswd_lbl = tk.Label(root1,text="Password", padx=10, pady=10)
pswd_lbl.grid(row=2, column=0)

user_entry = tk.Entry(root1)
user_entry.grid(row=1, column=1, padx=10, pady=10)

pswd_entry = tk.Entry(root1)
pswd_entry.grid(row=2, column=1, padx=10, pady=10)

submit_btn = tk.Button(root1,text="Submit", command=func, padx=10, pady=10)
submit_btn.grid(row=3, column=1)

root1.mainloop()


#def shop_manager():
    # for window 1 - Stock manager
def OnClick1():
    global frame, item_list, ProductName_entry, Quantity_entry, Price_entry

    clear_win()

    root.title("Item List")

    title1 = tk.Label(root, text="Item List")
    title1.grid(row=0, column=1)

    productName_label = tk.Label(root, text="Product Name")
    productName_label.grid(row=1, column=0,pady=4)

    quantity_label = tk.Label(root, text="Quantity")
    quantity_label.grid(row=2, column=0,pady=4)

    price_label = tk.Label(root, text="Price")
    price_label.grid(row=3, column=0,pady=4)

    ProductName_entry = tk.Entry(root, borderwidth=2, width=20)
    ProductName_entry.grid(row=1, column=1,pady=4)

    Quantity_entry = tk.Entry(root, borderwidth=2, width=20)
    Quantity_entry.grid(row=2, column=1,pady=4)

    Price_entry = tk.Entry(root, borderwidth=2, width=20)
    Price_entry.grid(row=3, column=1,pady=4)

    submit = tk.Button(root, text="Submit", padx=12, pady=7, command=SubmitToDB,width=8,relief="groove")
    submit.grid(row=4, column=1,stick="w",pady=10,padx=4)

    frame = tk.LabelFrame(root, text="Delete/update records", padx=10, pady=10)
    frame.grid(row=5, column=0, columnspan=3,pady=10)

    item_list = tk.Listbox(frame, exportselection=False, height=9, width=50)
    item_list.grid(row=0, column=0, columnspan=2)

    # Showing items in items listbox
    c.execute("SELECT ProductName, id FROM STOCK_ITEMS;")
    items = c.fetchall()
    for element in items:
        item_list.insert(tk.END, element[0])

    clear = tk.Button(root, text="Clear input", padx=12, pady=7, command=Clear,width=8,relief="groove")
    clear.grid(row=4, column=0,stick="e",padx=4)

    Back = tk.Button(root, text="Back", padx=12, pady=7, command=back,width=8,relief="groove")
    Back.grid(row=5, column=3,stick="s",pady=10,padx=4)

    del_but = tk.Button(frame, text="Delete a record", command=Delete,width=15,relief="groove")
    del_but.grid(row=1, column=0)

    upd_but = tk.Button(frame, text="Update a record", command=Update,width=15,relief="groove")
    upd_but.grid(row=1, column=1)

    # This is to show the price, name and quantity of selected item in the text boxes.
    def select_item(event):
        global selected_item, item_list
        index = item_list.curselection()
        selected_item = item_list.get(index)
        product = index[0]

        ProductName_entry.delete(0, tk.END)
        Quantity_entry.delete(0, tk.END)
        Price_entry.delete(0, tk.END)

        ProductName_entry.insert(0, Fetch_From_DB(product, 0))
        Quantity_entry.insert(0, Fetch_From_DB(product, 1))
        Price_entry.insert(0, Fetch_From_DB(product, 2))

    item_list.bind('<<ListboxSelect>>', select_item)

# for window - Purchase items
def OnClick2():
    global database, c, item_list1, root, quantity_order, order_items, check, items

    clear_win()
    
    root.title("Purchase Items")

    productName_label = tk.Label(root, text="Product Name")
    productName_label.grid(row=0, column=0)

    # Creating list box menu of products
    item_list1 = tk.Listbox(root, exportselection=False, height=10, width=40)
    item_list1.grid(row=1, column=0)

    c.execute("SELECT ProductName, id FROM STOCK_ITEMS;")
    items = c.fetchall()
    for element in items:
        item_list1.insert(tk.END, element[0])

    Quantity_label = tk.Label(root, text="Quantity")
    Quantity_label.grid(row=0, column=1)

    quantity_order = tk.Entry(root)
    quantity_order.grid(row=1, column=1,stick="n")

    orderB = tk.Button(root, text="Place order", command=order,width=14,relief="groove")
    orderB.grid(row=3, column=1,stick="s")

    cart = tk.Label(root,text=" Shopping Cart")
    cart.grid(row=2,column=0)

    items = list()  # items is the list of items price

    order_items = tk.Listbox(root, exportselection=False, height=10, width=40)
    order_items.grid(row=3, column=0, rowspan=2)
    
    # print the quantity of the selected item in the text box
    def select_item_order(event):
        global selected_item, item_list
        index = item_list1.curselection()
        selected_item = item_list1.get(index)
        product = index[0]

        quantity_order.delete(0, tk.END)
        quantity_order.insert(0, Fetch_From_DB(product, 1))

    item_list1.bind('<<ListboxSelect>>', select_item_order)

    rem = tk.Button(root, text="Remove from Cart",command=Remove_from_Cart,width=14,relief="groove")
    rem.grid(row=3, column=1, stick="N")

    check = tk.IntVar()

    bill = tk.Checkbutton(root, text="Generate bill", variable = check)
    bill.grid(row=4, column=1)

    cart_but = tk.Button(root, text="Add to cart", command=Add_to_Cart,width=14,relief="groove")
    cart_but.grid(row=1, column=1)

    Back = tk.Button(root, text="Back", command=back,width=14,relief="groove",)
    Back.grid(row=4, column=1,stick="s",pady=4)

# For purchase history window
def onClick3():

    clear_win()
    root.title("Purchase History")


    c.execute("SELECT * FROM PURCHASE_HIST;")
    item = c.fetchall()    # extracts all data from purchase history database

    pur_items = tk.Text(root,width=55,height=20) 
    pur_items.grid(row=0, column=0,)
    pur_items.config(state="normal")
    for i in item:
        pur_items.insert(1.0,(f"{i[0]} \t \t {i[1]} \t{i[2]} \t{i[3]}\n"))  # inserts data into the listbox
    pur_items.config(state="disabled")
    database.commit()    

    Back = tk.Button(root, text="Back", command=back,width=15,relief="groove",)
    Back.grid(row=1, column=0,pady=4,stick="e")


def onClick4():
    global name_entry, sal_entry, phone_entry, dob_entry, employ, id_label2

    clear_win()
    root.title("Employee database")

    id_Label = tk.Label(root, text="Employee id")
    id_Label.grid(row=0, column=0,pady=4)

    name_label = tk.Label(root, text="Name")
    name_label.grid(row=1, column=0,pady=4)

    phone_label = tk.Label(root, text="Mobile no.")
    phone_label.grid(row=2, column=0,pady=4)

    dob_label = tk.Label(root, text="DOB")
    dob_label.grid(row=3, column=0,pady=4)

    sal_label = tk.Label(root, text="Salary")
    sal_label.grid(row=4, column=0,pady=4)

    id_label2 = tk.Label(root)
    id_label2.grid(row=0, column=1,pady=4)

    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1,pady=4)

    phone_entry = tk.Entry(root)
    phone_entry.grid(row=2, column=1,pady=4)

    dob_entry = tk.Entry(root)
    dob_entry.grid(row=3, column=1,pady=4)

    sal_entry = tk.Entry(root)
    sal_entry.grid(row=4, column=1,pady=4)

    add = tk.Button(root, text="Add record", command=add_emp,width=13,relief="groove")
    add.grid(row=5, column=0, pady=4)

    updt = tk.Button(root, text="Update record", command=update_emp,width=13,relief="groove")
    updt.grid(row=5, column=1, pady=4)

    delt = tk.Button(root, text="Delete record", command=del_emp,width=13,relief="groove")
    delt.grid(row=5, column=2, pady=4)

    clear_text = tk.Button(root, text="Clear text boxes", command=Clear_emp,width=13,relief="groove")
    clear_text.grid(row=4, column=2, padx=10)

    employ = tk.Listbox(root, exportselection=False,width=38,height=12)
    employ.grid(row=6, column=0, columnspan=2)

    c.execute("SELECT emp_id,name from employee;")
    names = c.fetchall()

    for i in names:
        employ.insert(tk.END, (i[0],i[1]))

    def sel_emp(event):

        index = employ.curselection()
        employee = index[0]

        Clear_emp()

        id_label2.config(text=fetch_emp(employee,0))
        name_entry.insert(0, fetch_emp(employee,1))
        phone_entry.insert(0, fetch_emp(employee,2))
        dob_entry.insert(0, fetch_emp(employee,3))
        sal_entry.insert(0, fetch_emp(employee,4))

    employ.bind('<<ListboxSelect>>', sel_emp)

    Back = tk.Button(root, text="Back", command=back,width=12,relief="groove",)
    Back.grid(row=6, column=2, stick="s")


def Calculator():
    clear_win()
    root.title("Calculator")

    def button_click(number):
        current = e.get()
        e.delete(0, tk.END)
        e.insert(0, str(current) + str(number))

    def button_clear():
        e.delete(0, tk.END)

    def button_add():
        first_number = e.get()
        global f_num
        global math
        math = "add"
        f_num = int(first_number)
        e.delete(0, tk.END)

    def button_subtract():
        first_number = e.get()
        global f_num
        global math
        math = "subtract"
        f_num = int(first_number)
        e.delete(0, tk.END)

    def button_multiply():
        first_number = e.get()
        global f_num
        global math
        math = "multiply"
        f_num = int(first_number)
        e.delete(0, tk.END)

    def button_divide():
        first_number = e.get()
        global f_num
        global math
        math = "divide"
        f_num = int(first_number)
        e.delete(0, tk.END)

    def button_equal():
        second_number = e.get()
        e.delete(0, tk.END)

        if math == "add":
            e.insert(0, f_num + int(second_number))

        if math == "subtract":
            e.insert(0, f_num - int(second_number))

        if math == "multiply":
            e.insert(0, f_num * int(second_number))

        if math == "divide":
            e.insert(0, f_num / int(second_number))

    # e box in which no. wil be displayed
    e = tk.Entry(root,borderwidth=2,width=40,)
    e.grid(row=0, column=0, columnspan=4, padx=10, pady=10,rowspan=2)

    # Define buttons

    button_1 = tk.Button(root, text="1", padx=20, pady=20,width=5, command=lambda: button_click(1))
    button_2 = tk.Button(root, text="2", padx=20, pady=20,width=5, command=lambda: button_click(2))
    button_3 = tk.Button(root, text="3", padx=20, pady=20,width=5, command=lambda: button_click(3))
    button_4 = tk.Button(root, text="4", padx=20, pady=20,width=5, command=lambda: button_click(4))
    button_5 = tk.Button(root, text="5", padx=20, pady=20,width=5, command=lambda: button_click(5))
    button_6 = tk.Button(root, text="6", padx=20, pady=20,width=5, command=lambda: button_click(6))
    button_7 = tk.Button(root, text="7", padx=20, pady=20,width=5, command=lambda: button_click(7))
    button_8 = tk.Button(root, text="8", padx=20, pady=20,width=5, command=lambda: button_click(8))
    button_9 = tk.Button(root, text="9", padx=20, pady=20,width=5, command=lambda: button_click(9))
    button_0 = tk.Button(root, text="0", padx=20, pady=20,width=29, command=lambda: button_click(0))

    button_add = tk.Button(root, text="+", padx=20, pady=20,width=5, command=button_add)
    button_equal = tk.Button(root, text="=", padx=20, pady=20,width=17, command=button_equal)
    button_clear = tk.Button(root, text="C", padx=20, pady=20,width=17, command=button_clear)

    button_subtract = tk.Button(root, text="-", padx=20, pady=20,width=5, command=button_subtract)
    button_multiply = tk.Button(root, text="x", padx=20, pady=20,width=5, command=button_multiply)
    button_divide = tk.Button(root, text="/", padx=20, pady=20,width=5, command=button_divide)

    # Place buttons on-screen

    button_1.grid(row=5, column=0)
    button_2.grid(row=5, column=1)
    button_3.grid(row=5, column=2)

    button_4.grid(row=4, column=0)
    button_5.grid(row=4, column=1)
    button_6.grid(row=4, column=2)

    button_7.grid(row=3, column=0)
    button_8.grid(row=3, column=1)
    button_9.grid(row=3, column=2)

    button_0.grid(row=6, column=0,columnspan=3)

    button_clear.grid(row=2, column=0,columnspan=2)

    button_add.grid(row=3, column=3)
    button_multiply.grid(row=5, column=3)
    button_divide.grid(row=6, column=3)
    button_subtract.grid(row=4, column=3)

    button_equal.grid(row=2, column=2,columnspan=2)

    Back = tk.Button(root, text="Back", command=back,width=12,relief="groove",height=2)
    Back.grid(row=6, column=4, columnspan=2, stick="s")


def SubmitToDB():
    global database, c, item_list
    c.execute(f"INSERT INTO STOCK_ITEMS(ProductName, Quantity, Price) VALUES('{ProductName_entry.get()}', {Quantity_entry.get()}, {Price_entry.get()});")
    database.commit()

    item_list.insert(tk.END, ProductName_entry.get())
    Clear()


def Fetch_From_DB(index, req):  # req is required item
    global database, c
    # ProductName = 0, quantity = 1, price = 2, id = 3

    c.execute("SELECT * FROM STOCK_ITEMS;")
    all_records = c.fetchall()
    req_data = all_records[index][req]

    database.commit()

    return req_data


def Add_to_Cart():
    global database, c, items, quantity_order, order_items

    index = item_list1.curselection()   # gets the position of selected item from the list in the form of a tuple
    selected_item = item_list1.get(index)   # gets the item from the item list using the position
    product = index[0]  # gets the item index in the list
    
    max_quantity = Fetch_From_DB(product, 1)
    selected_quantity = quantity_order.get()

    if max_quantity >= int(selected_quantity):
        price = int(Fetch_From_DB(product, 2)) * int(quantity_order.get())
        items.append(price)
        order_items.insert(tk.END, (selected_item, str(selected_quantity), price)) # inserts the item name, quantity and price in the listbox

        new_quantity = max_quantity - int(selected_quantity)
        Modify_quantity(product, new_quantity) 
        quantity_order.delete(0, tk.END)
    # if items added to cart is more than items in database, displays message
    else:
        display = tk.Label(root, text=f"Max quantity is {max_quantity}")
        display.grid(row=0, column=5)
        quantity_order.delete(0, tk.END)


def Remove_from_Cart():
    global root, items, order_items, c

    product = order_items.curselection()[0] # returns index in the form of tuple
    selection = order_items.get(product)[0] # gets name of product from the listbox using the index
    
    quantity = int(order_items.get(product)[1])
    
    order_items.delete(product)
    items.pop(product)

    c.execute(f"SELECT Quantity FROM STOCK_ITEMS WHERE ProductName = '{selection}';")  # Extracts present quantity from the database
    old_quantity = int(c.fetchall()[0][0])
    new_quantity = old_quantity + quantity # adds the quantity in cart to the quantity in database to get quantity before placing order

    c.execute(f"UPDATE STOCK_ITEMS SET Quantity = {new_quantity} WHERE ProductName = '{selection}';")

    database.commit()


def Modify_quantity(product, new_quantity):  # argument(Product Name, new quantity)
    global database, c
    record_id = Fetch_From_DB(product, 3)
    c.execute(f"UPDATE Stock_items SET Quantity = {new_quantity} WHERE id = {record_id};")
    database.commit()


def add_emp():
    c.execute(f"INSERT INTO EMPLOYEE(name, mobile, dob, salary) VALUES('{name_entry.get()}','{phone_entry.get()}','{dob_entry.get()}',{sal_entry.get()})")
    c.execute(f"SELECT emp_id from employee where name = '{name_entry.get()}' and mobile='{phone_entry.get()}'")
    x = c.fetchall()
    employ.insert(tk.END, (x[0],name_entry.get()))

    Clear_emp()
    database.commit()


def update_emp():
    index = employ.curselection()
    employ_name = index[0]
    record_id = fetch_emp(employ_name, 0)
    c.execute(f"UPDATE employee SET name = '{name_entry.get()}', mobile = '{phone_entry.get()}', dob = '{dob_entry.get()}', salary = {sal_entry.get()} WHERE emp_id = {record_id};")
    database.commit()
    Clear_emp()


def del_emp():
    index = employ.curselection()
    selected_item = employ.get(index)[1]
    c.execute(f"DELETE FROM employee WHERE name = '{selected_item}';")
    employ.delete(index)
    database.commit()
    Clear_emp()


def fetch_emp(id,req): # req is required item
    c.execute("SELECT * FROM employee;")
    all_records = c.fetchall()
    req_data = all_records[id][req]

    database.commit()

    return req_data


def Clear_emp():
    id_label2.config(text="")
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    sal_entry.delete(0, tk.END)

# Sums up total price of items added to cart when purchased
def order():

    # For purchase history
    x = order_items.get(0,tk.END)
    
    purch_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    p = PrettyTable()
    p.field_names = ["Item no", "Item ID", "Item name", "Rate", "Qty", "Amount"]
    
    total = 0
    for i in items:
        total += i

    item_no = 1
    # Adds time of purchase to purch_hist table
    for i in x: 
        c.execute(f"INSERT INTO PURCHASE_HIST VALUES('{i[0]}',{i[1]}, {i[2]},'{purch_time}')")
        
    if check.get() == 1:
        f = open("file1.txt","w")
        for i in x:
            c.execute(f"SELECT id, price from Stock_items where productname = '{i[0]}'")
            data = c.fetchall()[0]
            p.add_row([item_no, data[0], i[0], data[1], i[1], i[2]])
            item_no += 1
        f.write(f"APS general store \t {purch_time} \n \n")
        f.write(str(p))
        f.write("\n \n")
        f.write(f"Total: {total}")
        f.close()
        os.startfile("file1.txt")


    message = "You have to pay " + "₹" + str(total)
    display = tk.Label(root, text=message)
    display.grid(row=2, column=1)
    database.commit()

# Deletes record from database
def Delete():
    global database, c, item_list
    index = item_list.curselection()
    selected_item = item_list.get(index)
    c.execute(f"DELETE FROM STOCK_ITEMS WHERE ProductName = '{selected_item}';")
    item_list.delete(index)
    database.commit()
    Clear()

# updates database in case of change in any value
def Update():
    global database, c
    index = item_list.curselection()
    product = index[0]
    record_id = Fetch_From_DB(product, 3)
    c.execute(f"UPDATE Stock_items SET ProductName = '{ProductName_entry.get()}', Quantity = {Quantity_entry.get()}, Price = {Price_entry.get()} WHERE id = {record_id};")
    database.commit()
    Clear()

# Clears text in entry widgets
def Clear():
    global ProductName_entry, Quantity_entry, Price_entry
    ProductName_entry.delete(0, tk.END)
    Quantity_entry.delete(0, tk.END)
    Price_entry.delete(0, tk.END)


def clear_win():
    for widget in root.winfo_children():
        widget.destroy()


def back():
    global my_img, clock, date, logo_img
    clear_win()
    root.title("CS-Project")

    logo = tk.Label(root, image=logo_img)
    logo.grid(row=0, column=0)

    title = tk.Label(root, text="APS GENERAL STORE", padx=10, pady=15)
    title.grid(row=0, column=1,columnspan=2)

    # Prints todays  date
    date = tk.Label(root)
    date.grid(row=1, column=0,stick="w",padx=40)

    # Prints current time
    clock = tk.Label(root, padx=10, pady=5)
    clock.grid(row=1, column=2,stick="E")

    # Opens Manage stock items window
    button1 = tk.Button(root, text="Manage stock items",command=OnClick1, padx=20, pady=20,relief="groove",width=15)
    button1.grid(row=2, column=0,padx=40)

    # Opens Purchase item window
    button2 = tk.Button(root, text="Purchase Items",command=OnClick2, padx=20, pady=20,relief="groove",width=15)
    button2.grid(row=3, column=0,padx=40)

    # Opens Purchase History window
    button3 = tk.Button(root, text="Purchase History",command=onClick3,padx=20, pady=20,relief="groove",width=15)
    button3.grid(row=4, column=0,padx=40)

    # Opens employee data
    button4 = tk.Button(root, text="Employee data",command=onClick4,padx=20, pady=20,relief="groove",width=15)
    button4.grid(row=5, column=0,padx=40)

    button5 = tk.Button(root,image=my_img, command=Calculator, relief="groove")
    button5.grid(row=2, column=2)

    current_time = time.strftime("%H:%M")
    current_date = time.strftime("%D")
    clock.config(text=current_time)
    date.config(text=current_date)

# Function to display and update time
def Time():
    global clock, date
    current_time = time.strftime("%H:%M")
    current_date = time.strftime("%D")
    clock.config(text=current_time)
    date.config(text=current_date)

    # Function calls itself after 1 min
    root.after(60000, Time)

root = tk.Tk()
root.title("CS-Project")
root.geometry("450x400+150+50")

logo_img = ImageTk.PhotoImage(Image.open(resource_path("logo2.png")))
logo = tk.Label(root, image=logo_img)
logo.grid(row=0, column=0)

title = tk.Label(root, text="APS GENERAL STORE", padx=10, pady=15)
title.grid(row=0, column=1,columnspan=2)

# Prints todays  date
date = tk.Label(root)
date.grid(row=1, column=0,stick="w",padx=40)

# Prints current time
clock = tk.Label(root, padx=10, pady=5)
clock.grid(row=1, column=2,stick="E")

# Opens Manage stock items window
button1 = tk.Button(root, text="Manage stock items",command=OnClick1, padx=20, pady=20,relief="groove",width=15)
button1.grid(row=2, column=0,padx=40)

# Opens Purchase item window
button2 = tk.Button(root, text="Purchase Items",command=OnClick2, padx=20, pady=20,relief="groove",width=15)
button2.grid(row=3, column=0,padx=40)

# Opens Purchase History window
button3 = tk.Button(root, text="Purchase History",command=onClick3,padx=20, pady=20,relief="groove",width=15)
button3.grid(row=4, column=0,padx=40)

# Opens employee data
button4 = tk.Button(root, text="Employee data",command=onClick4,padx=20, pady=20,relief="groove",width=15)
button4.grid(row=5, column=0,padx=40)

# Adds image from given path to button
my_img = ImageTk.PhotoImage(Image.open(resource_path("calc.jpg")))

button5 = tk.Button(root,image=my_img, command=Calculator, relief="groove")
button5.grid(row=2, column=2)


# Connects file to database
#database = mysql.connector.connect(host='localhost', user=user, password=password)
c = database.cursor()

c.execute("CREATE DATABASE IF NOT EXISTS SHOP_MANAGER;")
c.execute("use SHOP_MANAGER;")
c.execute("CREATE TABLE IF NOT EXISTS STOCK_ITEMS(ProductName varchar(15), Quantity int, Price int, id int primary key auto_increment) auto_increment=0;")
c.execute("CREATE TABLE IF NOT EXISTS PURCHASE_HIST(ProductName varchar(15), Quantity int, Price int, Purch_time datetime);") 
c.execute("CREATE TABLE IF NOT EXISTS EMPLOYEE(emp_id int primary key auto_increment, Name varchar(20), mobile char(10),  DOB DATE, salary int)")

database.commit()

Time()

root.mainloop()