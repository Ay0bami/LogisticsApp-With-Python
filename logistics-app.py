# Logistic APP By Group-5
import sqlite3
import time
import datetime
import csv
import os

class Error(Exception):
    """Base class for other exceptions"""
    pass
class InvalidChoice(Error):
    """Raised when the input value not in the given choice"""
    pass
class Insufficient(Error):
    """Raised when the input quantity not available"""
    pass
class InvalidUserName(Error):
    """Raise when the user name is not correct or invalid"""
    pass
class InvalidPassword(Error):
    """Raise when the password is not correct or invalid"""
    pass
conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()
def encrypt_data(password):         # For encryting and decrypting password
    filename = open('chyper-code.csv', 'r') # file contains the crypt values for all uppercase letters and numbers
    file = csv.DictReader(filename)
    User_type = []
    Sys_type=[]
    enc_password=''
    for col in file:
        User_type.append(col['USER TYPE'])
        Sys_type.append(col['SYSTEM CONVERT'])
    for i in password:
        enc_password=enc_password+Sys_type[User_type.index(i)]
    return(enc_password)
def AdminProductInsert():
    head=True
    while(head==True):
        name=input("Enter the product name\n")
        qty=int(input("Enter the product quantity\n"))
        cursor.execute("insert into product_db (product_Name,Quantity) values (?, ?)",
                    (name, qty ))
        conn.commit()
        if(int(input("Enter 1 to continue inserting and 0 to go back\n"))==0):
            return
        os.system('cls' if os.name == 'nt' else 'clear')
def AdminProductUpdate():
    head=True
    while(head==True):
        id_product=input("Enter the product Id you want to change\n")
        cursor.execute('''SELECT product_Name,Quantity from product_db WHERE product_id= ?;''',(id_product,))
        print(cursor.fetchone())
        if(int(input("press 1 to edit the product name and 2 to add quantity:\n"))==1):
            name=input("Enter the name of the product:\n")
            cursor.execute('''UPDATE product_db SET product_Name = ?  WHERE product_id= ?;''',(name,id_product))
            conn.commit()
        else:
            cursor.execute('''SELECT Quantity from product_db WHERE product_id= ?;''',(id_product,))
            qty=int(input("Enter the quantity to be added to the product\n"))
            row=cursor.fetchone()
            t=0
            for r in row:
                t=r
            qty=t+qty
            cursor.execute('''UPDATE product_db SET Quantity = ?  WHERE product_id= ?;''',(qty,id_product))
            conn.commit()
        if(int(input("Enter 1 to continue update and 0 to go back\n"))==0):
            return
        os.system('cls' if os.name == 'nt' else 'clear')
def AdminProductView():
    print("Product list:\n")
    row=cursor.execute('''SELECT * from product_db ;''')
    for r in row:
        print(r)
    return
def create_order(user_name): # Order function to get and enter details of customer order
    product=[]    # product list contains list of all the products available
    cursor.execute('''SELECT product_Name from product_db ;''')
    product=list(cursor.fetchall())
    qty=[]
    cursor.execute('''SELECT Quantity from product_db ;''')
    qty=list(cursor.fetchall())
    
    shipment=["flight","ship","truck","train"] # shipment list contains all the possible shipments available
    country=["Canada","USA","UK","Mexico","India"]
    while True:
        try:
            print("List of products available are: \n")
            i=1
            for r,qt in zip(product, qty):
                print(f'{i}.{r[0]}-{qt[0]}')
                i=i+1
            p= int(input("Enter the product number of the product you want to ship from above: \n"))# getting product from customer
            if(p not in range(1,(len(product)+1))):
                raise InvalidChoice
            q= int(input("Enter the quantity of the product:\n"))
            if(q<0 or q>qty[p-1][0]):
                raise Insufficient
            print("List of shipment methods available are:\n1.Flight\n2.ship\n3.truck\n4.Train\n")# getting shipment method from the user
            s=int(input("Choose the shipment method from above list:\t"))
            if(s not in [1,2,3,4]):
                raise InvalidChoice
            print("List of shipment country available are:\n")
            i=1
            for r in country:
                print(f'{i}.{r}')
                i=i+1
            
            f=int(input("Enter the country number it should be picked up from:\n"))
            if(f not in range(1,len(country))):
                raise InvalidChoice
            t=int(input("Enter the destination country number:\n"))
            if(t not in range(1,len(country))):
                raise InvalidChoice
            d=int(input(f"Enter how many days from now on the shipment should take place:\nTodays date: {datetime.date.today()}\t"))
            if(d<0 and d>100):
                raise InvalidChoice
            shipdate=datetime.date.today()
            shipdate=shipdate+datetime.timedelta(days=d)
            print(f"Your order will be shipped on : {shipdate}")
            cursor.execute("insert into order_db (User_Name,Product,Quantity,Shipment,Pick_from,Destination,Ship_date,Created_at) values (?, ?, ?, ?, ?, ?, ?,?)",
                    (user_name, product[p-1][0],q,shipment[s-1],country[f-1],country[t-1],shipdate,datetime.date.today() ))
            cursor.execute('''UPDATE product_db SET Quantity = ?  WHERE product_id= ?;''',(qty[p-1][0]-q,p))
            conn.commit()
            print("Order entered succesfully!!\n")
            break
        except InvalidChoice:
            print("Select from the above given choice only!!!")
        except Insufficient:
            print("Sorry,Given quantity is not available/correct!!\n")
        except ValueError:
            print("Enter only numbers")
def show_order(user_name):
    print("List of all orders:\n")
    cursor.execute('''SELECT * from order_db WHERE User_Name=?;''',(user_name,))
    records = cursor.fetchall()
    for r in records:
        print(r)

    
def main():
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS User_db (User_id integer PRIMARY KEY,User_Name text NOT NULL,Password text NOT NULL,Count integer NOT NULL);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_db (order_id integer PRIMARY KEY,User_Name text NOT NULL,Product text NOT NULL,Quantity integer NOT NULL,Shipment text NOT NULL,Pick_from text NOT NULL,Destination text NOT NULL,Ship_date date NOT NULL,Created_at date NOT NULL);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS product_db (product_id integer PRIMARY KEY,product_Name text NOT NULL,Quantity integer NOT NULL);''')
    records = cursor.fetchall()
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        try:
            log_del=input("If you are a new user enter 'Y'.   If not enter 'N',\nIf your are admin user enter A:\n")
            type(log_del)
            if(log_del not in 'YNA'):
                raise InvalidChoice
            if(log_del=='Y'):
                while True:
                    try:
                        user_name=input("Enter your user name\n")
                        if(user_name.isalpha()==False):
                            raise InvalidUserName
                        message=input("enter your password\n")
                        count=0
                        encMessage = encrypt_data(message)
                        cursor.execute('''SELECT User_Name from User_db WHERE User_Name= ?;''',(user_name,))
                        if(cursor.fetchone() is None):
                            cursor.execute("insert into User_db (User_Name,Password,Count) values (?, ?, ?)",
                                    (user_name, encMessage,count ))
                            conn.commit()
                            print("user account created successfully!!")
                            head=True
                            while(head==True):
                                while True:
                                    try:
                                        print(" Press 1 - to make order\n Press 2- to view your order history\n")
                                        t=int(input("enter your choice\n"))
                                        if(t not in [1,2]):
                                            raise InvalidChoice
                                        if(t==1):
                                            create_order(user_name)
                                            show_order(user_name)
                                            if(int(input("To exit user application press 0 \t to continue press 1\n"))==0):
                                                head= False
                                            os.system('cls' if os.name == 'nt' else 'clear')
                                        else:
                                            show_order(user_name)
                                            if(int(input("To exit user application press 0 \t to continue press 1\n"))==0):
                                                head= False
                                            os.system('cls' if os.name == 'nt' else 'clear')
                                        break
                                    except InvalidChoice:
                                            print("Select from the above given choice only!!!")
                                    except ValueError:
                                            print("Enter only numbers")
                        
                        else:
                            print("the username exists")
                        break 
                    except InvalidUserName:
                        print("User name should only contain  letters!!")
                    except ValueError:
                        print("Password should only contain Uppercase letters and numbers!!")
                    


            elif(log_del=='N'):
                while True:
                    try:

                        user_name=input("Enter your user name\n")
                        if(user_name.isalpha()==False):
                            raise InvalidUserName
                        message=input("Enter your password\n")
                        message=encrypt_data(message)
                        cursor.execute('''SELECT Password from User_db WHERE User_Name= ?;''',(user_name,))
                        check_message = cursor.fetchone()[0]
                        if  message == check_message:
                            cursor.execute('''UPDATE User_db SET Count = Count+1 WHERE  User_Name= ? and Password=?;''',(user_name,message))
                            conn.commit()
                            with open("Logdata.txt", "a") as file:
                                cursor.execute('''SELECT User_id,Password,Count from User_db WHERE User_Name=?  and Password=?;''',(user_name,message))
                                records = cursor.fetchall()
                                file.write(f'{user_name},{message},{records[0][2]+1},{datetime.datetime.now()}\n')                
                            head=True
                            while(head==True):
                                while True:
                                    try:
                                        print("Press 1 - to make order\n Press 2- to view your order history\n")
                                        t=int(input("Enter your choice\n"))
                                        if(t not in [1,2]):
                                            raise InvalidChoice
                                        if(t==1):
                                            create_order(user_name)
                                            if(int(input("To exit user application press 0 \t to continue press 1\n"))==0):
                                                head= False
                                            os.system('cls' if os.name == 'nt' else 'clear')
                                        else:
                                            show_order(user_name)
                                            if(int(input("To exit user application press 0 \t to continue press 1\n"))==0):
                                                head= False
                                            os.system('cls' if os.name == 'nt' else 'clear')
                                        break
                                    except InvalidChoice:
                                            print("Select from the above given choice only!!!")  
                                    except ValueError:
                                            print("Enter only numbers")                             
                        else:
                            print("Please input the right password")
                        break 
                    except InvalidUserName:
                        print("User name should only contain  letters!!")
                    except ValueError:
                        print("Password should only contain Uppercase letters and numbers!!")
            else:
                while True:
                    try:

                        user_name="Admin"
                        message=input("Enter your Admin password (Password should be uppercase and/or number)\n")
                        message=encrypt_data(message)
                        cursor.execute('''SELECT Password from User_db WHERE User_Name= ?;''',(user_name,))
                        check_message = cursor.fetchone()[0]
                        if  message == check_message:
                            cursor.execute('''UPDATE User_db SET Count = Count+1 WHERE  User_Name= ? and Password=?;''',(user_name,message))
                            conn.commit()
                            with open("Logdata.txt", "a") as file:
                                cursor.execute('''SELECT User_id,Password,Count from User_db WHERE User_Name=?  and Password=?;''',(user_name,message))
                                records = cursor.fetchall()
                                for item in records:
                                    print(item)
                                file.write(f'{user_name},{message},{records[0][2]+1},{datetime.datetime.now()}\n')
                        head=True        
                        while(head==True):
                            c=int(input(" Press 1 to view product\n Press 2 to insert product\n Press 3 to Update product\n"))
                            if(t not in [1,2,3]):
                                    raise InvalidChoice
                            if(c==1):
                                AdminProductView()
                                if(int(input("Press 0 to exist admin view and 1 to continue admin view\n"))==0):
                                    break
                                os.system('cls' if os.name == 'nt' else 'clear')
                            elif(c==2):
                                AdminProductInsert()
                                if(int(input("Press 0 to exist admin view and 1 to continue admin view\n"))==0):
                                    break
                                os.system('cls' if os.name == 'nt' else 'clear')
                            else:
                                AdminProductUpdate()
                                if(int(input("Press 0 to exist admin view and 1 to continue admin view\n"))==0):
                                    break
                                os.system('cls' if os.name == 'nt' else 'clear')
                        break
                    except InvalidUserName:
                        print("User name should only contain  letters!!")
                    except ValueError:
                        print("Password should only contain Uppercase letters and numbers!!")
            break
        except InvalidChoice:
            print("Select from the above given choice only!!!")   
if __name__ == '__main__':
    main()