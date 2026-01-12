## How to create table of selected database
import pymysql
conn=pymysql.connect(host='localhost',user='root',
                     password='Admin')
a=conn.cursor()
a.execute('create database contact')
print("contact Database created")

conn=pymysql.connect(host='localhost',user='root',
            password='Admin',db='contact')

a=conn.cursor()
a.execute('''CREATE TABLE BOOK
       (NAME CHAR(30) PRIMARY KEY NOT NULL,
        ADDRESS CHAR(100),
        MOBILE BIGINT,
        EMAIL CHAR(30))''')
print("Table created successfully")
conn.close()
