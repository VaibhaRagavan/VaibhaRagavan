from datetime import date,datetime
from flask_sqlalchemy import SQLAlchemy
import pymysql
import smtplib
import datetime

hostname='localhost'
user='root'
database='mydatabase'

db=pymysql.connections.Connection(host=hostname,user=user,database=database)
mycursor=db.cursor()


def construct_sql_query(month, date):
    return "SELECT name,id FROM eventdetails WHERE month(dateofbirth)={} && day(dateofbirth)={}".format(month, date)

def sendwish(name,email):
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("vaibhavijayvidhun@gmail.com","novo gdnp zlvy iaoz")
    message="Wish you a Happy Birthday "+name +"from the Birthday calender site"
    s.sendmail("vaibhavijayvidhun@gmail.com",email,message)
    s.quit()

def sendemailtoothers(l_id,person_name):

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("vaibhavijayvidhun@gmail.com","novo gdnp zlvy iaoz")
    message="This is  the reminder from Birthday calender site . we would like to remind you that today is"+ person_name +" birthday wish him a happy birthday"

    s.sendmail("vaibhavijayvidhun@gmail.com",l_id,message)
    s.quit()

today_month=datetime.datetime.now().month
today_date=datetime.datetime.now().day

mycursor.execute(construct_sql_query(today_month,today_date))
birthday=mycursor.fetchall()
if len(birthday)>0:
    names,ids=zip(*birthday)
    names=list(names)
    ids=list(ids)
    for i in ids:
        mycursor.execute("SELECT userdetails.emailid FROM((favorites INNER JOIN userdetails ON userdetails.userid=favorites.userid)INNER JOIN eventdetails ON eventdetails.id=favorites.u_id)WHERE eventdetails.id=%s",i)    
        sender=mycursor.fetchall()
        mycursor.execute("SELECT name FROM eventdetails WHERE id=%s",i)
        name=mycursor.fetchall()
        send_list=[item for subtuple in sender for item in subtuple]
        name_str=''.join(str(item)for subtuple in name for item in subtuple )
        print(name_str)
        sendemailtoothers(send_list,name_str)
else:  
    mycursor.execute("SELECT user,emailid FROM userdetails where month(DOB)={} && day(DOB)={}".format(today_month,today_date))
    wish=mycursor.fetchall()
    if len(wish)>0:
        birthday_person,email=zip(*wish)
        birthday_person=list(birthday_person)
        email=list(email) 
 
        for mail in email:
            mycursor.execute("SELECT user FROM userdetails WHERE emailid=%s",mail)
            bdperson_name=mycursor.fetchall()
            bdperson_namestr=''.join(str(items)for subtuple in bdperson_name for items in subtuple)
            sendwish(bdperson_namestr,mail)
    else:
        print("No user having birthday today")

log_file_path = "/Users/vaibha/Documents/log_file.txt"

# Get the current time
current_time = datetime.datetime.now()

# Write the current time to the log file
with open(log_file_path, "a") as log_file:
    log_file.write(f"Script ran at: {current_time}\n")
