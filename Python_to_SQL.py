import pymysql
import time

mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="Gk5987@6300",
  db= "contact"
)
def intro():
    print("="*32)
    print(" CONTACT BOOK PROJECT")
    print("="*32)
    time.sleep(3)

def create_record():
    name=input("Enter Name:")
    
    address=input("Enter Address:")
    mobile=input("Enter Mobile:")
    email=input("Enter Email:")
    mycursor=mydb.cursor()
    sql = "INSERT INTO book(name, address, mobile, email) VALUES (%s, %s, %s, %s)"
    record = (name, address, mobile, email)
    #sql='''INSERT INTO book(name,address,mobile,email) VALUES("%s,%s,%s,%s")'''
    #record=(name,address,mobile,email)
    mycursor.execute(sql,record)
    mydb.commit()
    mycursor.close()
    print("record inserted successfully!!")

def search(name):
    mycursor=mydb.cursor()
    sql="Select * from book where name=%s"
    value=(name,)
    mycursor.execute(sql,value)
    record=mycursor.fetchone()
    mycursor.close()
    if record==None:
        print("No such record exist")
    else:
        print('Name:',record[0])
        print('Address:',record[1])
        print('Mobile:',record[2])
        print('E-mail:',record[3])
    
def display_all():
    mycursor=mydb.cursor()
    mycursor.execute("select * from book")
    i=1
    for record in mycursor:
        print("Record:",i)
        print('Name:',record[0])
        print('Address:',record[1])
        print('Mobile:',record[2])
        print('E-mail:',record[3],"\n")
        i+=1
    mycursor.close()    

def  delete_book(name):
    mycursor=mydb.cursor()
    sql="Delete from book where name=%s"
    value=(name,)
    mycursor.execute(sql,value)
    mydb.commit()
    if mycursor.rowcount==0:
        print("Record not found")
    else:
        print("Record found Sucessfully")
    mycursor.close()    

def modify_book(name):
    mycursor=mydb.cursor()
    sql="select * from book where name=%s"
    value=(name,)
    mycursor.execute(sql,value)
    record=mycursor.fetchone()
    if record==None:
        print("No such record")
    else:
        while True:
            print("\nPress the option you want:")
            print("1. Name")
            print("2. Address")
            print("3. Mobile")
            print("4. Back")
            print()
            ch=int(input("Enter the number: "))
            if ch==1:
                new_name=input("Enter the new name: ")
                sql='''Update book set name=%s where name=%s'''
                value=(new_name,name)
                mycursor.execute(sql,value)
                mydb.commit()
                print(mycursor.rowcount,"Record Updated")
            elif ch==2:
                new_address=input("Enter the new address: ")
                sql='''Update book set address=%s where name=%s'''
                value=(new_address,name)
                mycursor.execute(sql,value)
                mydb.commit()
                print(mycursor.rowcount,"Record Updated")
            elif ch==3:
                new_mobile=input("Enter the new mobile: ")
                sql='''Update book set mobile=%s where name=%s'''
                value=(new_mobile,name)
                mycursor.execute(sql,value)
                mydb.commit()
                print(mycursor.rowcount,"Record Updated")
            elif ch==4:
                break
            else:
                print("Invalid choice")
            mycursor.close()

                
def main():
    intro()
    while True:
          print("\nMain Menu")
          print("1. ADD NEW RECORD")
          print("2. Search New RECORD")
          print("3. Display all RECORD")
          print("4. DELETE RECORD")
          print("5. MODIFY RECORD")
          print("6. EXIT")
          print()
          ch=int(input("enter your choice:"))
          print()
          if ch==1:
              print("ADD NEW RECORD")
              create_record()
          elif ch==2:
              print("SEARCH RECORD BY NAME")
              name=input("Enter name:")
              search(name)

          elif ch==3:
               print("3. Display all records")
               display_all()

          elif ch==4:
              print("4. DELETE RECORD")
              name=input("enter the name: ")
              delete_book(name)
              
          elif ch==5:
              print("5. MODIFY RECORD")
              name=input("enter the name of Record that you want to modify:")
              modify_book(name)
              
          elif ch==6:
              print("Thanks for choosing contact book")
              mydb.close()
              break
          else:
              print("Invalid choice")
main()