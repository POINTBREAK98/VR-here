from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect

import MySQLdb
import random

hostname = 'localhost'
username = 'root'
password = 'bigpika'
database = 'vrhere'


def homepage(request):
    return render(request , 'home_page/home.html')

def login(request):
    return render(request, 'home_page/login.html')
       
"""    if request.method=='POST'
        
        conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
        cur1 = conn.cursor()
        cur2 = conn.cursor()
        cur3 = conn.cursor()
        cur2.execute("select count(*) from customer")
        total_customers = cur2.fetchone()
        reg_no = 'c10' + str((total_customers[0] + 1))
        user={}

        for i in ['fname','lname','doorno']:
            user[i]=request.POST.get(i)
        insertIntoUser = insert into user values()
        cur1.execute()
        
        #cur1.execute('insert into user(Reg_No,Fname,Lname,Door_No) values(reg_no,%s,%s,%s)',{user['fname'],user['lname'],user['doorno']})
        #cur3.execute('insert into customer values(reg_no,:user_id,:password,:aadharnumber)')
        isuser=None
        for i in cur1:
            isuser=i
        if isuser!=None:
            messages.error(request,f'Account Already Exists!')
            return redirect('customerSignIn')
        conn.close()
        messages.success(request,f'Account created for Mr/Ms. {user["fname"]}!')
        return redirect('login')
    else: """


def driverSignIn(request):
    return render(request, 'home_page/driver_signup.html')


def check(request):
    # input get
    if request.method == "GET":  
        if request.GET.get('dri_activate')=='activate': #driver
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            query1 = """update driver_log set Status = %s,activation_time = CURTIME(),Date = CURDATE() where Driver_id = %s"""
            prep1 = ('available',request.GET.get('username'))
            c.execute(query1,prep1)
            conn.commit()
            conn.close()
            return render(request, 'home_page/driver.html', Driver_login(request))
        if request.GET.get('dri_deactivate')=='deactivate': #driver
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            query1 = """update driver_log set Status = %s,activation_time = CURTIME(),Date = CURDATE() where Driver_id = %s"""
            prep1 = ('not_avail',request.GET.get('username'))
            c.execute(query1,prep1)
            conn.commit()
            conn.close()
            return render(request, 'home_page/driver.html', Driver_login(request))
        if request.GET.get('update_loc')=='update': #driver
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            query1 = """update driver_log set Area = %s where Driver_id = %s"""
            prep1 = (request.GET.get('activate_area'),request.GET.get('username'))
            c.execute(query1,prep1)
            conn.commit()
            conn.close()
            return render(request, 'home_page/driver.html', Driver_login(request))
        if request.GET.get('dri_refresh')=='refresh': #driver
            return render(request, 'home_page/driver.html', Driver_login(request))
        if request.GET.get('cus_accept')!=None: #driver
            trip_history = {}
            trip_history["Customer_id"] = request.GET.get('cus_accept')
            trip_history["driver_id"] = request.GET.get('username')
            trip_history["from"] = request.GET.get('from')
            trip_history["to"] = request.GET.get('to')

            #check for driver is busy
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select count(Driver_id) from CURRENT_RIDES where Driver_id = %s", [trip_history["driver_id"]] )
            conn.close()
            busy = None
            for i in c:
                busy = i[0]
            if busy > 0:
                messages.error(request,f'You can Accept only one ride at a time!')
                return render(request, 'home_page/driver.html', Driver_login(request))

            #accept the ride
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            query1 = """insert into CURRENT_RIDES values(%s,%s,%s,%s,CURTIME(),CURDATE())"""
            prep1 = (trip_history["Customer_id"],trip_history["driver_id"],trip_history["from"],trip_history["to"])
            c.execute(query1,prep1)
            conn.commit()
            conn.close()

            #delete customer from customer log
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "delete from CUSTOMER_LOG where Customer_id = %s", [trip_history["Customer_id"]] )
            conn.commit()
            conn.close()

            return render(request, 'home_page/driver.html', Driver_login(request))

        if request.GET.get('End_trip')!=None: #driver
            end_trip_update ={}
            end_trip_update["S_no"] = random.randint(1000000, 9999999)
            end_trip_update["Customer_id"] = request.GET.get("End_trip")
            end_trip_update["driver_id"] = request.GET.get("username")
            end_trip_update["from"] = request.GET.get("from")
            end_trip_update["to"] = request.GET.get("to")
            end_trip_update["from_time"] = request.GET.get("from_time")
            end_trip_update["trip_date"] = request.GET.get("date")
            end_trip_update["Amount"] = random.randint(100, 500)

            #end trip
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            query1 = """insert into TRIP_HISTORY(S_no,customer_id,driver_id,from_location,to_location,from_time,To_time,trip_date,Amount) values(%s,%s,%s,%s,%s,%s,CURTIME(),CURDATE(),%s)"""
            prep1 = (end_trip_update['S_no'],end_trip_update['Customer_id'],end_trip_update["driver_id"],end_trip_update["from"],end_trip_update["to"],end_trip_update["from_time"],end_trip_update["Amount"])
            c.execute(query1,prep1)
            conn.commit()
            conn.close()

            #delete driver from current rides
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "delete from CURRENT_RIDES where Driver_id = %s", [end_trip_update["driver_id"]] )
            conn.commit()
            conn.close()

            return render(request, 'home_page/driver.html', Driver_login(request))
        if request.GET.get('cus_refresh')=='refresh': #customer
            return render(request, 'home_page/customer.html', Cust_login(request))
        if request.GET.get('BOOK_A_RIDE')=='book': #customer
            #check for before request
            customer_src_dest = {}
            for i in ['username','source', 'destination']:
                customer_src_dest[i] = request.GET.get(i)
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select count(*) from CUSTOMER_LOG where Customer_id = %s", [customer_src_dest['username']] )
            conn.close()
            already_req = None
            for i in c:
                already_req = i[0]
            if already_req != 0:
                messages.error(request,f'We Already have a request from you! Please wait until the current request is confirmed')
                return render(request, 'home_page/customer.html',Cust_login(request))
            #check for driver
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            query1 = """select count(*) from DRIVER_LOG where area = %s and status = %s """
            prep1 = (customer_src_dest['source'],'available')
            c.execute(query1,prep1)
            conn.close()
            ava_driv = None
            for i in c:
                ava_driv = i[0]
            if ava_driv > 0: #book the ride
                conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
                c = conn.cursor()
                query1 = """insert into customer_log values(%s,%s,%s)"""
                prep1 = (customer_src_dest['username'],customer_src_dest['source'],customer_src_dest['destination'])
                c.execute(query1,prep1)
                conn.commit()
                conn.close()
                messages.success(request,f'Drivers are available wait for confirmation')
                return render(request, 'home_page/customer.html',Cust_login(request))
            else : #error msg
                messages.error(request,f'No drivers available!')
                return render(request, 'home_page/customer.html',Cust_login(request))
        else:
            return render(request, 'home_page/login.html')
    else:
        conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
        c = conn.cursor()
        d = {}
        for i in ['userid', 'password']:
            d[i] = request.POST.get(i)
        
        option = None
        # check for admin
        c.execute('select user_id,password from ADMINISTRATOR')
        admin = []
        for i in c:
            admin.append(i)
        for i in admin:
            if(i[0] == d["userid"] and i[1] == d["password"]):
                option = 1 #admin

        # check for customer
        c.execute('select user_id,password from CUSTOMER')
        customer = []
        for i in c:
            customer.append(i)
        for i in customer:
            if(i[0] == d["userid"] and i[1] == d["password"]):
                option = 2 #customer

        # check for driver
        c.execute('select user_id,password from DRIVER')
        driver = []
        for i in c:
            driver.append(i)
        for i in driver:
            if(i[0] == d["userid"] and i[1] == d["password"]):
                option = 3 #driver

        #login
        if option == 1: #admin
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute('select count(user_id) from CUSTOMER')
            for i in c:
                custo = i[0]
            c.execute('select count(user_id) from DRIVER')
            for i in c:
                driv = i[0]
            return render(request, 'home_page/admin.html', {'username':d["userid"],'customer':custo,'driver':driv})
        elif option == 2: #customer
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from CUSTOMER_LOG where Customer_id = %s", [d["userid"]] )
            conn.close()
            cur_ride = []
            for i in c:
                cur_ride.append(i)

            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from CURRENT_RIDES where Customer_id = %s", [d["userid"]] )
            conn.close()
            now_riding = []
            for i in c:
                now_riding.append(i)

            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from TRIP_HISTORY where Customer_id = %s", [d["userid"]] )
            conn.close()
            history = []
            for i in c:
                history.append(i)
            return render(request, 'home_page/customer.html',{'username':d["userid"],'xpas':d["password"],'rides':cur_ride,'now_riding':now_riding,'history':history})
        elif option == 3: #driver
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from DRIVER_LOG where Driver_id = %s", [d["userid"]] )
            conn.close()
            dri_ride = []
            for i in c:
                dri_ride.append(i)

            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from CUSTOMER_LOG where From_location = (select Area from DRIVER_LOG where Driver_id = %s)", [d["userid"]] )
            conn.close()
            cus_ride = []
            for i in c:
                cus_ride.append(i)

            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from CURRENT_RIDES where Driver_id = %s", [d["userid"]] )
            conn.close()
            now_riding = []
            for i in c:
                now_riding.append(i)

            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from TRIP_HISTORY where Driver_id = %s", [d["userid"]] )
            conn.close()
            history = []
            for i in c:
                history.append(i)     
            return render(request, 'home_page/driver.html', {'username':d["userid"],'xpas':d["password"],'dri_ride':dri_ride,'cus_ride':cus_ride,'now_riding':now_riding,'history':history})
        else:
            messages.error(request,f'Username or Password is incorrect!')
            return redirect('login')

def Driver_login(request):
    conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
    c = conn.cursor()
    d = {}
    for i in ['username', 'xpas']:
        d[i] = request.GET.get(i)
    c.execute('select user_id,password from DRIVER')
    conn.close()
    customer = []
    for i in c:
        customer.append(i)
    for i in customer:
        if(i[0] == d["username"] and i[1] == d["xpas"]):
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from DRIVER_LOG where Driver_id = %s", [d["username"]] )
            conn.close()
            dri_ride = []
            for i in c:
                dri_ride.append(i)
            
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from CUSTOMER_LOG where From_location = (select Area from DRIVER_LOG where Driver_id = %s)", [d["username"]] )
            conn.close()
            cus_ride = []
            for i in c:
                cus_ride.append(i)
            
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from CURRENT_RIDES where Driver_id = %s", [d["username"]] )
            conn.close()
            now_riding = []
            for i in c:
                now_riding.append(i)

            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from TRIP_HISTORY where Driver_id = %s", [d["username"]] )
            conn.close()
            history = []
            for i in c:
                history.append(i)
            return {'username':d["username"],'xpas':d["xpas"],'dri_ride':dri_ride,'cus_ride':cus_ride,'now_riding':now_riding,'history':history}

def Cust_login(request):
    conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
    c = conn.cursor()
    d = {}
    for i in ['username', 'xpas']:
        d[i] = request.GET.get(i)
    c.execute('select user_id,password from CUSTOMER')
    conn.close()
    customer = []
    for i in c:
        customer.append(i)
    for i in customer:
        if(i[0] == d["username"] and i[1] == d["xpas"]):
            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from CUSTOMER_LOG where Customer_id = %s", [d["username"]] )
            conn.close()
            cur_ride = []
            for i in c:
                cur_ride.append(i)

            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from CURRENT_RIDES where Customer_id = %s", [d["username"]] )
            conn.close()
            now_riding = []
            for i in c:
                now_riding.append(i)

            conn = MySQLdb.connect(host = hostname, user = username , passwd = password , db = database)
            c = conn.cursor()
            c.execute( "select * from TRIP_HISTORY where Customer_id = %s", [d["username"]] )
            conn.close()
            history = []
            for i in c:
                history.append(i)
            return {'username':d["username"],'xpas':d["xpas"],'rides':cur_ride,'now_riding':now_riding,'history':history}