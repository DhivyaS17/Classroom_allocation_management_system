import os
import mysql.connector
from prettytable import PrettyTable
import time


# display the periods for class allocation
def display_periods():
    columns=["Timings","Period"]
    myTable=PrettyTable()
    myTable.add_column(columns[0],["8:00am - 9:00am","9:00am - 9:50am","10:10am - 11:00am","11:00am - 11:50am",
    "11:50am - 12:40pm","1:20pm - 2:10pm","2:10pm - 3:00pm"])
    myTable.add_column(columns[1],["1","2","3","4","5","6","7"])
    print(myTable)

# Login credentials
def login_details():
    # establishing sql connection
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhiv@1722")
    
    os.system("cls")
    print("                  Classroom Allocation Managemnt System")
    print("                  -------------------------------------")
    # getting login credentials
    print("\nLogin")
    print("-----")
    print("Name:")
    uname=input()
    print("Password:")
    upwd=input()
    
    # Checking if the user exists
    log_cur=mydb.cursor()
    log_cur.execute("use classroom_allocation;")
    user_not_found=1
    log_cur.execute("select * from users;")
    for(n,p) in log_cur:
        if(n==uname and p==upwd):
            print("Logging in...")
            time.sleep(1)
            user_not_found=0
            # moving on to activity page
            activity_page()
            break
    if(user_not_found):
        print("No such user exists.\nAre you a registered user(y\n):")
        user_choice=input()
        if(user_choice=='y'):
          login_details()
        else:
            registration_details()
    # closing sql connection
    mydb.close()

# activity page that diplays the functionalities of the system
def activity_page():
    os.system("cls")
    print("                  Classroom Allocation Managemnt System")
    print("                  -------------------------------------")
    print("\nWhat would you like to do?")
    print("1 - Schedule Session")
    print("2 - Change Session")
    print("3 - Cancel Session")
    while True:
     print("\nYour choice:")
     ch=int(input())
     #time.sleep(3)
     if(ch==1):
        schedule_session()
        break
     elif(ch==2):
        change_session()
        break
     elif(ch==3):
        cancel_session()
        break
     else:
        print("Enter valid choice!")

# scheduling a session
def schedule_session():
    
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhiv@1722")
    
    os.system("cls")
    print("                  Classroom Allocation Managemnt System")
    print("                  -------------------------------------")
    print("\nSchedule Session")
    print("----------------")
    display_periods()
    print("Enter the session timing according to the periods table")
    print("\n\nStaff Name:")
    sname=input()
    print("Description:")
    sdesc=input()
    print("Date:")
    sdate=input()
    print("From:")
    ftime=input()
    print("To:")
    ttime=input()
    print("Contact Number:")
    phno=input()
    is_empty=0
    
    #validate
    if((not(sname)) or (not(sdesc)) or (not(sdate)) or (ftime=='') or (ttime=='') or (not(phno))):
        is_empty=1
    
    ftime=int(ftime)
    ttime=int(ttime)
    sessid=""
    
    sh_cur=mydb.cursor()
    sh_cur.execute("use classroom_allocation;")
    sql = "insert into session_allocation(StaffName,Description,sessionDate,fperiod,tperiod,PhoneNUmber,SessionID) values(%s, %s,%s,%s,%s,%s,%s)"
    val = (sname,sdesc,sdate,ftime,ttime,phno,sessid)
    sh_cur.execute(sql,val)
    if(is_empty):
        print("Enter all the details")
        time.sleep(1)
        schedule_session()
    
    # get the session id of the user
    sql="Select SessionID,StaffName from session_allocation where StaffName='"+sname+"' and Description='"+sdesc+"';"
    sh_cur.execute(sql)
    for (i,s) in sh_cur:
        sess_id=i
    print("\nYour Session has been Scheduled!\nYour Session Id is",sess_id)
    
    # save the changes to the database
    mydb.commit()
    mydb.close()
   

# check whether a session already exists or not
def check_session(name,sess):
    
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhiv@1722")

    check=0
    check_cur=mydb.cursor()
    check_cur.execute("use classroom_allocation;")
    check_cur.execute("select StaffName,SessionID from session_allocation;")
    for(n,s) in check_cur:
        if(n==name and sess==s):
            check=1
            break
        elif(name!=n and sess==s):
            check=2
            break
        else:
            check=0
    mydb.close()
    return check

# session already exists
def check_session1(name,desc,d,per):
    
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhiv@1722")

    check=0
    check_cur=mydb.cursor()
    check_cur.execute("use classroom_allocation;")
    check_cur.execute("select StaffName,Description,sessionDate,fperiod from session_allocation;")
    for(n,des,da,fp) in check_cur:
        if(n==name and des==desc and da==d):
            check=1
            break
        else:
            check=0
    mydb.close()
    return check


# change the scheduled session
def change_session():
    
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhiv@1722")

    os.system("cls")
    print("                  Classroom Allocation Managemnt System")
    print("                  -------------------------------------")
    print("\nChange the Scheduled Session")
    print("----------------------------")
    session_sched=0
    while(True):
     print("\nEnter the details of scheduled session")
     print("Staff Name:")
     fsname=input()
     print("Session Id:")
     session_id=input()
     
     session_exits=check_session(fsname,session_id)
     print("\nThe result is",session_exits)
     if(session_exits==0):
         print("No such session has been scheduled, enter correct details")
         print("Do you want to quit(yes/no):")
         to_quit=input()
         if(to_quit=="yes"):
             print("Logging out..")
             break
         else:
             change_session()
     else:
         while(True):
          print("\n\nEnter the details of the new session")
          display_periods()
          print("Enter the session timing according to the periods table")
          print("\n\nStaff Name:")
          sname=input()
          print("Description:")
          sdesc=input()
          print("Date")
          sdate=input()
          print("From:")
          ftime=int(input())
          print("To:")
          ttime=int(input())
          print("Contact Number:")
          phno=int(input())
          
          if(check_session1(sname,sdesc,sdate,ftime)==1):
             print("Sorry! Session has been scheduled already")
             print("1 - schedule with different timing")
             print("2 - quit\nYour choice:")
             c=int(input())
             if(c==2):
                 print("Logging out...")
                 break
          
          cur=mydb.cursor()
          cur.execute("use classroom_allocation;")
          sql = "insert into session_allocation(StaffName,Description,sessionDate,fperiod,tperiod,PhoneNUmber) values(%s, %s,%s,%s,%s,%s)"
          val = (sname,sdesc,sdate,ftime,ttime,phno)
          cur.execute(sql,val)
          sql="delete from session_allocation where StaffName='"+fsname+"' and SessionID='"+session_id+"';"
          cur.execute(sql)
          mydb.commit()
          
          session_sched=1
          sql="Select SessionID,StaffName from session_allocation where StaffName='"+sname+"' and Description='"+sdesc+"';"
          cur.execute(sql)
          for (i,s) in cur:
            sess_id=i
          print("\nYour Session has been Scheduled!\nYour New Session Id is",sess_id)
          if(session_sched):
             break
     
     if(session_sched):
             break
    mydb.close()

# cancel schedule
def cancel_session():
    
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhiv@1722")

    os.system("cls")
    print("                  Classroom Allocation Managemnt System")
    print("                  -------------------------------------")
    print("\nCancel Session")
    print("--------------")
    print("Enter the details of the session")
    print("Staff Name:")
    del_name=input()
    print("Session id:")
    del_sessid=input()
    
    # checks whether the session already exists
    check_session_exits=0
    check_session_exits=check_session(del_name,del_sessid)
    if(not(check_session_exits)):
        print("Session does not exits!\nDo you have the session scheduled(y/n):")
        ch=input()
        if(ch=='y'):
            cancel_session()
        else:
            print("Exiting..")
            time.sleep(1)
    else:
       cur=mydb.cursor()
       cur.execute("use classroom_allocation;")
       sql="delete from session_allocation where StaffName='"+del_name+"' and SessionID='"+del_sessid+"';"
       cur.execute(sql)
       mydb.commit()
       mydb.close()
       print("\nSession Cancelled!")

# Registration credentials
def registration_details():
    
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhiv@1722")

    os.system("cls")
    print("                  Classroom Allocation Managemnt System")
    print("                  -------------------------------------")
    
    #get the user details
    print("\nRegister")
    print("--------")
    print("Name:")
    is_empty=0
    uname=input()
    if(not(uname)):
       is_empty=1
    print("Password:")
    upwd=input()
    if(not(upwd)):
        is_empty=1
    
    #insert it into the database
    cur=mydb.cursor()
    cur.execute("use classroom_allocation;")
    sql = "insert into users(UName,UPassword) values(%s, %s)"
    val = (uname,upwd)
    cur.execute(sql,val)
    if(is_empty):
        print("Enter all the details!")
        registration_details()
    mydb.commit()
    mydb.close()
    print("Registration successful")
    time.sleep(1)
    #move onto login page
    login_details()

#main program
while True:
 os.system("cls")
 print("                  Classroom Allocation Managemnt System")
 print("                  -------------------------------------")
 print("1 - Register\n2 - Login")
 while True:
  print("\nYour choice:")
  choice=int(input())
  if(choice==1):
    registration_details()
    break
  elif(choice==2):
    login_details()
    break
  else:
    print("Enter etheir 1 or 2")
 print("\nDo you want to continue(yes/no):")
 choice=input()
 
 if(choice=="no"):
     print("Exiting..")
     break

