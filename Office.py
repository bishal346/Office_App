from flask import Flask, render_template, request
app = Flask(__name__)

import psycopg2

hostname = '127.0.0.1'
database = 'Office'
username = 'postgres'
pwd = 'bishal@123'
port_id = 5432
conn = None
cur = None
try :
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    print("HELLO")
    cur = conn.cursor()   
    @app.route("/") 
    def func() : 
        return render_template("home.html")

    @app.route("/boss_signUP") 
    def boss_sign_up() :  
        return render_template("bosssignUp.html", txt = "")   

    @app.route("/boss_signUP", methods = ["POST"]) 
    def boss_sign_up_again() :  
 
        nam = str(request.form['name'] )
        eml = str(request.form['email']).lower() 
        #inst = str(request.form['inst_name'])
        paswd = str(request.form['password'])  
        adres = str(request.form['adress'])
        tx = "Thankyou for Signing UP now please go back and singIn to acess your priviledges" 
        cur.execute('''select * from bosslogin''') 
        don_passwd = cur.fetchall()  
        conn.commit() 
        bulabis = True 
        for tup in don_passwd :
            if(tup[1]==eml) : 
                tx = "Sorry emailId already exists please try another one" 
                bulabis = False 
                break

        if bulabis :
            tuplu = (nam,eml,paswd,adres)   
            cur.execute('''insert into bosslogin values(%s,%s,%s,%s)''',tuplu) 
            conn.commit()
        
        return render_template("bosssignUp.html", txt = tx) 

    #BOSS SIgnIN 
    @app.route("/boss") 
    def boss_sign_in() :  
        return render_template("bossLOGIN.html", xman = "", deptwa = "", holwa = "", lonwa = "", salwa = "", postwa = "", viewa = "")
    
    @app.route("/boss", methods = ["POST"]) 
    def boss_sign_in_again() :  
        eml = str(request.form['email']).lower() 
        paswd = request.form['password']  
        cur.execute('''select * from bosslogin''')
        don_passwd = cur.fetchall()  
        xm = "invalid password or email please refill it again"  
        #ln = "" 
        #ln2 = ""    
        deptwa1 = ""
        holwa1 = ""
        lonwa1 = "" 
        salwa1 = "" 
        postwa1 = "" 
        viewa1 = ""
        for tup in don_passwd :
            if(tup[1]==eml) : 
                if(tup[2]==paswd) :
                    xm = "SUCESS, now please click any of the below link as per your choise" 
                    #ln = "Add Depar"
                    #ln2 = "View food items"
                    deptwa1 = "Click here to visit the Department Section"
                    holwa1 = "Click here to visit the Holiday Section"
                    lonwa1 = "Click here to visit the Loan Section" 
                    salwa1 = "Click here to visit the Salary Section" 
                    postwa1 = "Click here to visit the Posts Section" 
                    viewa1 = "Click here to view the department wise details"
                    break 
                  
        return render_template("bossLOGIN.html", xman = xm, deptwa = deptwa1, holwa = holwa1, lonwa = lonwa1, salwa = salwa1, postwa = postwa1, viewa = viewa1)


    #Boss Department Add
    @app.route("/boss/deparment_ADD") 
    def add_new_deparments() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("departmentadd.html", tup = tups)   
 
    @app.route("/boss/deparment_ADD", methods = ["POST"]) 
    def add_new_deparments_again() :  
        nam = str(request.form['name'] ) 
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        tuplu = (len(tups)+1,nam)   
        cur.execute('''insert into department values(%s,%s)''',tuplu) 
        conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("departmentadd.html", tup = tups)
    
    #Department Update
    @app.route("/boss/departmentUpdate") 
    def department_Update() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("departmentUPDATE.html", tup = tups, mg = "")   

    @app.route("/boss/departmentUpdate", methods = ["POST"]) 
    def department_Update_again() :   
        pid = int(request.form['pid']) 
        name = str(request.form['name'])
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        mesg = "Sucessfully UPDATED "
        cur.execute('''select * from department order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1) : 
            mesg = "Invalid request please try again"
        else :
            cur.execute('''delete from department where pid = {}'''.format(pid)) 
            conn.commit()
            tuplu = (pid,name)   
            cur.execute('''insert into department values(%s,%s)''',tuplu) 
            conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()   
        conn.commit() 
        return render_template("departmentUPDATE.html", tup = tups, mg = mesg)


    #Salary Add 
    @app.route("/boss/salary_ADD") 
    def add_new_salary() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("Salaryadd.html", tup = tups, mg = "")   

    @app.route("/boss/salary_ADD", methods = ["POST"]) 
    def add_new_salary_again() :  
        pid = int(request.form['pid']) 
        salary = request.form['salary']
        cur.execute('''select * from salary''') 
        tups = cur.fetchall()  
        conn.commit() 
        bolta = False
        for tlp in tups :
            if(tlp[0]==pid) : 
                bolta = True
        mesg = "Sucessfully Added"
        cur.execute('''select * from department order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1 or bolta) : 
            mesg = "Invalid request please try again"
        else :
            tuplu = (pid,salary)   
            cur.execute('''insert into salary values(%s,%s)''',tuplu) 
            conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()   
        conn.commit() 
        return render_template("Salaryadd.html", tup = tups, mg = mesg)

    #Update Salary
    @app.route("/boss/salaryUpdate") 
    def salary_Update() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("SalaryUpdate.html", tup = tups, mg = "")   

    @app.route("/boss/salaryUpdate", methods = ["POST"]) 
    def salary_Update_again() :   
        pid = int(request.form['pid']) 
        salary = int(request.form['salary'])
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        mesg = "Sucessfully UPDATED "
        cur.execute('''select * from salary order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1) : 
            mesg = "Invalid request please try again"
        else :
            cur.execute('''delete from salary where pid = {}'''.format(pid)) 
            conn.commit()
            tuplu = (pid,salary)   
            cur.execute('''insert into salary values(%s,%s)''',tuplu) 
            conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()   
        conn.commit() 
        return render_template("SalaryUpdate.html", tup = tups, mg = mesg)

    #Interst Rate ADD  
    @app.route("/boss/loanInterest_ADD") 
    def add_new_loanInterest() :  
        cur.execute('''select * from department''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("loan_interestADD.html", tup = tups, mg = "")   

    @app.route("/boss/loanInterest_ADD", methods = ["POST"]) 
    def add_new_loanInterest_again() :  
        pid = int(request.form['pid']) 
        interst = request.form['interest']
        cur.execute('''select * from loan''') 
        tups = cur.fetchall()    
        conn.commit()   
        
        bolta = False
        for tlp in tups :
            if(tlp[0]==pid) : 
                bolta = True
        mesg = "Sucessfully Added"
        cur.execute('''select * from department order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1 or bolta) : 
            mesg = "Invalid request please try again"
        else :
            tuplu = (pid,interst)   
            cur.execute('''insert into loan values(%s,%s)''',tuplu) 
            conn.commit()
        #tuplu = (pid,interst)   
        #cur.execute('''insert into loan values(%s,%s)''',tuplu) 
        #conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("loan_interestADD.html", tup = tups, mg = mesg)
    
    #UPDATE LOAN Interest RATE 
    @app.route("/boss/loanInterestUpdate") 
    def loanInterest_Update() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("LoanInterest_RateUpdate.html", tup = tups, mg = "")   

    @app.route("/boss/loanInterestUpdate", methods = ["POST"]) 
    def loanInterest_Update_again() :   
        pid = int(request.form['pid']) 
        intrest = int(request.form['interest'])
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        mesg = "Sucessfully UPDATED "
        cur.execute('''select * from loan order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1) : 
            mesg = "Invalid request please try again"
        else :
            cur.execute('''delete from loan where pid = {}'''.format(pid)) 
            conn.commit()
            tuplu = (pid,intrest)   
            cur.execute('''insert into loan values(%s,%s)''',tuplu) 
            conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()   
        conn.commit() 
        return render_template("LoanInterest_RateUpdate.html", tup = tups, mg = mesg)

    #Holidays ADD  
    @app.route("/boss/Holidays_ADD") 
    def add_new_Holiday() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("holidaysAdd.html", tup = tups, mg = "")   

    @app.route("/boss/Holidays_ADD", methods = ["POST"])     
    def add_new_Holiday_again() :  
        pid = int(request.form['pid']) 
        holiday = request.form['holiday']
        cur.execute('''select * from holidays''') 
        tups = cur.fetchall()    
        conn.commit()   
        
        bolta = False
        for tlp in tups :
            if(tlp[0]==pid) : 
                bolta = True
        mesg = "Sucessfully Added"
        cur.execute('''select * from department order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1 or bolta) : 
            mesg = "Invalid request please try again"
        else :
            tuplu = (pid,holiday)   
            cur.execute('''insert into holidays values(%s,%s)''',tuplu) 
            conn.commit() 
        #tuplu = (pid,interst)   
        #cur.execute('''insert into loan values(%s,%s)''',tuplu) 
        #conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("holidaysAdd.html", tup = tups, mg = mesg)
    
    #Holiday Update 
    @app.route("/boss/HolidayUpdate") 
    def holiday_Update() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("Holiday_UPDate.html", tup = tups, mg = "")   
 
    @app.route("/boss/HolidayUpdate", methods = ["POST"]) 
    def holiday_Update_again() :   
        pid = int(request.form['pid']) 
        holiday = int(request.form['holiday'])
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        mesg = "Sucessfully UPDATED "
        cur.execute('''select * from holidays order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1) : 
            mesg = "Invalid request please try again"
        else :
            cur.execute('''delete from holidays where pid = {}'''.format(pid)) 
            conn.commit()
            tuplu = (pid,holiday)   
            cur.execute('''insert into holidays values(%s,%s)''',tuplu) 
            conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()   
        conn.commit() 
        return render_template("Holiday_UPDate.html", tup = tups, mg = mesg)
    
    #Posts Add
    @app.route("/boss/Posts_ADD") 
    def add_new_seats() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("PostsADD.html", tup = tups, mg = "")   

    @app.route("/boss/Posts_ADD", methods = ["POST"])     
    def add_new_seats_again() :  
        pid = int(request.form['pid']) 
        seats = request.form['seats']
        cur.execute('''select * from posts''') 
        tups = cur.fetchall()    
        conn.commit()   
        
        bolta = False
        for tlp in tups :
            if(tlp[0]==pid) : 
                bolta = True
        mesg = "Sucessfully Added"
        cur.execute('''select * from department order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1 or bolta) : 
            mesg = "Invalid request please try again"
        else :
            tuplu = (pid,seats)   
            cur.execute('''insert into posts values(%s,%s)''',tuplu) 
            conn.commit() 
        #tuplu = (pid,interst)   
        #cur.execute('''insert into loan values(%s,%s)''',tuplu) 
        #conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("PostsADD.html", tup = tups, mg = mesg)
    
    #Posts Update 
    @app.route("/boss/PostsUpdate") 
    def Seats_posts_Update() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("PostsUpdate.html", tup = tups, mg = "")   
 
    @app.route("/boss/PostsUpdate", methods = ["POST"])  
    def Seats_posts_Update_again() :   
        pid = int(request.form['pid']) 
        seats = int(request.form['seats'])
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        mesg = "Sucessfully UPDATED "
        cur.execute('''select * from posts order by pid''') 
        if(pid>len(cur.fetchall()) or pid<1) : 
            mesg = "Invalid request please try again"
        else :
            cur.execute('''delete from posts where pid = {}'''.format(pid)) 
            conn.commit()
            tuplu = (pid,seats)   
            cur.execute('''insert into posts values(%s,%s)''',tuplu) 
            conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()   
        conn.commit() 
        return render_template("PostsUpdate.html", tup = tups, mg = mesg)


    @app.route("/boss/View_ALL_Details_PER_DEPARTMENT") 
    def VIEW() :  
        cur.execute('''select department.pid,department.dept,salary.salar,holidays.holydy,loan.intrestrate,posts.seats from department,salary,holidays,loan,posts 
where department.pid = salary.pid and department.pid = holidays.pid and department.pid = loan.pid 
and department.pid = posts.pid order by loan.pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("viewEmployess.html", tup = tups)   

    #Employ SignUP
    @app.route("/employee_signUP") 
    def emp_sign_up() :  
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("empsignUp.html", txt = "", tpl = tups, txe = "")   

    @app.route("/employee_signUP", methods = ["POST"]) 
    def emp_sign_up_again() :  

        pid = int(request.form['inst_name'])
        nam = str(request.form['name'] )
        eml = str(request.form['email']).lower() 
        #inst = str(request.form['inst_name'])
        adres = str(request.form['adress'])
        paswd = str(request.form['password'])  
        tx = "Thankyou for Signing UP now please go back and singIn to acess your priviledges" 
        cur.execute('''select pid,count(*) from emp group by pid having pid = {}'''.format(pid)) 
        bisuvai = cur.fetchall()
        cur.execute('''select * from posts where pid = {}'''.format(pid))  
        biluuvai = cur.fetchall()
        if(len(bisuvai)!=0) :
            if(bisuvai[0][1]==biluuvai[0][1]) :
                tx = "No seats available try next year" 
                cur.execute('''select * from department order by pid''') 
                tups = cur.fetchall()  
                conn.commit() 
                return render_template("empsignUp.html", tpl = tups, txe = tx) 

        cur.execute('''select * from emplogin''') 
        don_passwd = cur.fetchall()  
        conn.commit() 
        bulabis = True 
        for tup in don_passwd :
            if(tup[1]==eml) : 
                tx = "Sorry emailId already exists please try another one" 
                bulabis = False 
                break

        if bulabis :
            tuplu = (nam,eml,paswd)   
            cur.execute('''insert into emplogin values(%s,%s,%s)''',tuplu) 
            conn.commit()
            tuplu = (pid,nam,adres,eml)   
            cur.execute('''insert into emp values(%s,%s,%s,%s)''',tuplu) 
            conn.commit()
        cur.execute('''select * from department order by pid''') 
        tups = cur.fetchall()  
        conn.commit() 
        return render_template("empsignUp.html", tpl = tups, txe = tx) 

    #Employee SigIN   
    @app.route("/emp") 
    def emp_sign_in() :  
        return render_template("empLOGIN.html", xman = "", holwa = "", lonwa = "", viewprof = "")
    
    @app.route("/emp", methods = ["POST"])  
    def emp_sign_in_again() :  
        eml = str(request.form['email']).lower() 
        paswd = request.form['password']  
        cur.execute('''select * from emplogin''') 
        don_passwd = cur.fetchall()  
        xm = "invalid password or email please refill it again"   
        #ln = "" 
        #ln2 = ""    
        holwa1 = ""
        lonwa1 = ""
        viewprof1 = ""
        for tup in don_passwd :
            if(tup[1]==eml) : 
                if(tup[2]==paswd) :
                    xm = "SUCESS, now please click any of the below link as per your choise" 
                    #ln = "Add Depar"
                    #ln2 = "View food items"
                    holwa1 = "Click here to demand holyday"
                    lonwa1 = "Click here to demand loan"
                    viewprof1 = "Click here to view your profile"
                    break 
                  
        return render_template("empLOGIN.html", xman = xm, holwa = holwa1, lonwa = lonwa1, viewprof = viewprof1)
        
    #Employee wanting Holidays 
    @app.route("/emp/HolydayWant") 
    def wanting_Holidays() :  
        return render_template("WantingHolidays.html", xman = "")

    @app.route("/emp/HolydayWant", methods = ["POST"]) 
    def wanting_Holidays_again() :  
        eml = str(request.form['email']).lower() 
        holi = int(request.form['holi']) 
        pdp = 0
        cur.execute('''select emp.pid,emp.nam,emp.adress,emp.email,holidays.holydy from emp,holidays 
where emp.pid = holidays.pid''')
        don_passwd = cur.fetchall()  
        xm = "Sucessfully granted holiday"  
        hol = 0 
        boltu = True
        for tp in don_passwd : 
            if(tp[3]==eml) :
                if holi>tp[4] : 
                    xm = "Nor permisible holiday"  
                    return render_template("WantingHolidays.html", xman = xm)
                pdp = tp[0]
                hol = tp[4]
                boltu = False
                break
        if boltu :
            xm = "Invalid email id please refill it again" 
            return render_template("WantingHolidays.html", xman = xm)
        cur.execute('''select * from holidaystaken''')
        tups = cur.fetchall()  
        biss = 0
        for tp in tups : 
            if(tp[1]==eml) :
                if(tp[2]+holi>hol) : 
                    xm = "Nor permisible holiday"  
                    return render_template("WantingHolidays.html", xman = xm)
                holi = holi + tp[2]
                biss = tp[3]
                cur.execute('''delete from holidaystaken where sln = {}'''.format(biss)) 
                conn.commit()
                break 
        if biss!=0 :
            cur.execute('''insert into holidaystaken values(%s,%s,%s,%s)''',(pdp,eml,holi,biss))  
            conn.commit()
        else : 
            cur.execute('''insert into holidaystaken values(%s,%s,%s,%s)''',(pdp,eml,holi,len(tups)+1)) 
            conn.commit()
        return render_template("WantingHolidays.html", xman = xm)  

    @app.route("/emp/Loan_Want") 
    def wanting_Loan() :  
        return render_template("Want_Loan.html", xman = "")

    @app.route("/emp/Loan_Want", methods = ["POST"]) 
    def wanting_Loan_again() :  
        eml = str(request.form['email']).lower() 
        loan = int(request.form['loan']) 
        pdp = 0
        cur.execute('''select emp.pid,emp.nam,emp.adress,emp.email,loan.intrestrate from emp,loan where emp.pid = loan.pid''')
        don_passwd = cur.fetchall()  
        xm = ""
        boltu = True
        intre = 0
        pdp = 0 
        #biss = 0 
        for tp in don_passwd : 
            if(tp[3]==eml) :
                pdp = tp[0]
                intre = tp[4]
                boltu = False
                break
        if boltu :
            xm = "Invalid email id please refill it again" 
            return render_template("Want_Loan.html", xman = xm)
        cur.execute('''select * from loantaken''')
        tups = cur.fetchall()  
        biss = 0
        amt = 0 
        for tp in tups : 
            if(tp[1]==eml) :
                biss = tp[3]
                amt = tp[2]
                cur.execute('''delete from loantaken where sl = {}'''.format(biss)) 
                conn.commit()
                break 
        if biss!=0 :
            cur.execute('''insert into loantaken values(%s,%s,%s,%s)''',(pdp,eml,amt+loan,biss))  
            conn.commit()
            xm = "An amout of "+str(((amt+loan)*(100+intre))/100)+"will be cut from your this year's salary"
        else : 
            cur.execute('''insert into loantaken values(%s,%s,%s,%s)''',(pdp,eml,loan,len(tups)+1)) 
            conn.commit() 
            xm = "An amout of "+str(((loan)*(100+intre))/100)+"will be cut from your this year's salary"
        return render_template("Want_Loan.html", xman = xm)  

    @app.route("/emp/EmployView") 
    def emp_view() :  
        return render_template("View_OF_Employee.html",xman = "", lst = [])

    @app.route("/emp/EmployView", methods = ["POST"]) 
    def emp_view_again() :  
        eml = str(request.form['email']).lower() 
        paswd = request.form['password']  
        cur.execute('''select emp.pid,emp.nam,emp.adress,emp.email,department.dept,salary.salar,holidays.holydy,loan.intrestrate,emplogin.passwrd from 
emp,department,salary,holidays,loan,emplogin where emp.email = emplogin.email and emp.pid = salary.pid and emp.pid = holidays.pid 
and emp.pid = loan.pid and emp.pid = department.pid''') 
        don_passwd = cur.fetchall()  
        xm = "invalid password or email please refill it again"  
        #ln = "" 
        #ln2 = ""   
        bolubam = True 
        for tup in don_passwd :
            if(tup[3]==eml) : 
                if(tup[8]==paswd) :
                    xm = "SUCESS, now view your profile" 
                    #ln = "Add Depar" 
                    #ln2 = "View food items"
                    don_passwd = tup
                    bolubam = False 
                    break 
        if bolubam : 
            return render_template("View_OF_Employee.html", xman = xm, lst = [])
        cur.execute('''select loantaken.sl,loantaken.pid,loantaken.email,loantaken.amount,loan.intrestrate from loan,loantaken where loan.pid = loantaken.pid''') 
        lon_tup = cur.fetchall() 
        loanAmt = 0
        for tup in lon_tup :
            if(tup[2]==eml) :
                loanAmt = tup[3] 
        cur.execute('''select holidaystaken.sln,holidaystaken.pid,holidaystaken.email,holidaystaken.holiday,holidays.holydy,
(holidays.holydy - holidaystaken.holiday) as holyLeft from holidaystaken,holidays where holidaystaken.pid = holidays.pid;''') 
        holi_tup = cur.fetchall() 
        holTak = 0
        for tup in holi_tup :
            if(tup[2]==eml) :
                holTak = tup[3] 
        holgetting = don_passwd[6]-holTak
        loan_amount_need_to_pay = int((loanAmt*(100+don_passwd[7]))/100)
        arr = [f"Welcome {don_passwd[1]}",f"Your Department Id is : {don_passwd[0]}",f"Your Department is : {don_passwd[4]}",
        f"Your Adress is : {don_passwd[2]}",f"Your Registered Email Id is : {don_passwd[3]}",f"Your Salary(per month) is : {don_passwd[5]}",
        f"Holidays you will get per year (except Saturadya nad Sunday) is : {don_passwd[6]}",
        f"Interest rate you must pay per annum if you take a loan is : {don_passwd[7]}%",f"Your PassWord is : {don_passwd[8]}",
        f"Holidays you have taken in this year is : {holTak}",f"Loan you have taken in this year is : {loanAmt}",
        f"Holidays you you are left with in this year is : {holgetting}",f"loan amount you have to pay in this year is : {loan_amount_need_to_pay}"]
        return render_template("View_OF_Employee.html", xman = xm, lst = arr )
    
    @app.route("/boss/DepartmentSection")  
    def deptComb() : 
        return render_template("Department.html")

    @app.route("/boss/HolidaySection") 
    def HoliComb() : 
        return render_template("Holidayyy.html")

    @app.route("/boss/LoanSection") 
    def LoanComb() : 
        return render_template("Loan.html")

    @app.route("/boss/SalarySection") 
    def SalaryComb() : 
        return render_template("Salary.html")
    
    @app.route("/boss/PostSection") 
    def PostComb() :  
        return render_template("Post.html")

    if __name__ == "__main__" : 
        app.run(debug=True)  
    #truncate_table = '''truncate table emp'''
    #cur.execute(truncate_table)
except Exception as error:
    print('Contains Error! '+str(error))  
finally : 
    if cur is not None : 
        cur.close()
    if conn is not None : 
        conn.close()




