from flask import *
import sqlite3

Connection=sqlite3.connect("Hospital.db")
print("Database Hospital Connected");

Connection.execute("CREATE TABLE IF NOT EXISTS PatientDet(ID INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT NOT NULL,Age TEXT NOT NULL,DOB TEXT NOT NULL,Fathers_Name TEXT NOT NULL,Mothers_Name TEXT NOT NULL,Address TEXT NOT NULL,Mobile_No TEXT UNIQUE NOT NULL,Blood_Group TEXT NOT NULL,Allergy TEXT)")
print("Table PatientDet Created")

Connection.execute("CREATE TABLE IF NOT EXISTS LoginDet(ID INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT NOT NULL,Degree TEXT NOT NULL,RegNo TEXT UNIQUE NOT NULL,Age TEXT NOT NULL,DOB TEXT NOT NULL,Email TEXT UNIQUE NOT NULL,Mobile_No TEXT UNIQUE NOT NULL,Username TEXT UNIQUE NOT NULL,Password TEXT NOT NULL)")
print("Table LoginDet Created")

Connection.close()

app=Flask(__name__)
app.secret_key="Harish"

@app.route("/")
@app.route("/login",methods=["GET","POST"])
def login():
    msg=""
    if request.method=="POST" and "Username" in request.form and "Password" in request.form:
        Username=request.form["Username"]
        Password=request.form["Password"]
        Connection=sqlite3.connect("Hospital.db")
        Cursor=Connection.cursor()
        Cursor.execute("SELECT * FROM LoginDet WHERE Username=? AND Password=?",(Username,Password))
        account=Cursor.fetchone()
        if account:
            session["loggedin"]=True
            session["id"]=account[0]
            session["username"]=account[1]
            msg=account[1]
            return render_template("index.html",msg=msg)
        else:
            msg="Incorrect Username or Password!"
            return render_template("login.html",msg=msg)
    else:
        return render_template("login.html",msg=msg)

@app.route("/logout")
def logout():
    session.pop("loggedin",None)
    session.pop("id",None)
    session.pop("username",None)
    return redirect(url_for("login"))

@app.route("/register",methods=["GET","POST"])
def register():
    msg=""
    if request.method=="POST" and "Username" in request.form and "Password" in request.form and "Name" in request.form and "Degree" in request.form and "RegNo" in request.form and "Age" in request.form and "DOB" in request.form and "Email" in request.form and "Mobile_No" in request.form:
        Username=request.form["Username"]
        Password=request.form["Password"]
        Email=request.form["Email"]
        Name=request.form["Name"]
        Degree=request.form["Degree"]
        RegNo=request.form["RegNo"]
        Age=request.form["Age"]
        DOB=request.form["DOB"]
        Mobile_No=request.form["Mobile_No"]
        Connection=sqlite3.connect("Hospital.db")
        Cursor=Connection.cursor()
        Cursor.execute("SELECT * FROM LoginDet WHERE Username=?",(Username,)) 
        account=Cursor.fetchone()
        if account:
            msg="Account already exists!"
        elif not Username or not Password or not Email or not Name or not Degree or not RegNo or not Age or not DOB or not Mobile_No:
            msg="Please fill out the form!"
        else:
            Cursor.execute("INSERT INTO LoginDet(Name,Degree,RegNo,Age,DOB,Email,Mobile_No,Username,Password) VALUES(?,?,?,?,?,?,?,?,?)",(Name,Degree,RegNo,Age,DOB,Email,Mobile_No,Username,Password)) 
            Connection.commit()
            msg="You have successfully registered!"
    #elif request.method=="POST": 
        #msg="Please fill out the form!"
    return render_template("register.html",msg=msg)

@app.route("/index",methods=["GET","POST"])
def index():
    msg=""
    return render_template("index.html",msg=msg)

@app.route("/create",methods=["GET","POST"])
def create():
    msg=""
    if request.method=="POST" and "Name" in request.form and "Age" in request.form and "DOB" in request.form and "Fathers_Name" in request.form and "Mothers_Name" in request.form and "Address" in request.form and "Mobile_No" in request.form and "Blood_Group" in request.form and "Allergy" in request.form:
        Name=request.form["Name"]
        Age=request.form["Age"]
        DOB=request.form["DOB"]
        Fathers_Name=request.form["Fathers_Name"]
        Mothers_Name=request.form["Mothers_Name"]
        Address=request.form["Address"]
        Mobile_No=request.form["Mobile_No"]
        Blood_Group=request.form["Blood_Group"]
        Allergy=request.form["Allergy"]
        Connection=sqlite3.connect("Hospital.db")
        Cursor=Connection.cursor()
        Cursor.execute("SELECT * FROM PatientDet WHERE Name=? AND Fathers_Name=? AND Mothers_Name=? AND DOB=?",(Name,Fathers_Name,Mothers_Name,DOB)) 
        account=Cursor.fetchone()
        if account:
            msg="Record already exists!"
        elif not Name or not Age or not DOB or not Fathers_Name or not Mothers_Name or not Address or not Mobile_No or not Blood_Group:
            msg="Please fill out the form!"
        else:
            Cursor.execute("INSERT INTO PatientDet(Name,Age,DOB,Fathers_Name,Mothers_Name,Address,Mobile_No,Blood_Group,Allergy) VALUES(?,?,?,?,?,?,?,?,?)",(Name,Age,DOB,Fathers_Name,Mothers_Name,Address,Mobile_No,Blood_Group,Allergy)) 
            Connection.commit()
            msg="Record created successfully!"
    return render_template("create.html",msg=msg)

@app.route("/view",methods=["GET","POST"])
def view():
    if request.method=="POST" and "Name" in request.form:
        Name=request.form["Name"]
        Connection=sqlite3.connect("Hospital.db")
        Connection.row_factory=sqlite3.Row
        Cursor=Connection.cursor()
        Cursor.execute("Select * FROM PatientDet WHERE Name=?",(Name,))
        rows=Cursor.fetchall()
        return render_template("view.html",rows=rows)
    else:
        Connection=sqlite3.connect("Hospital.db")
        Connection.row_factory=sqlite3.Row
        Cursor=Connection.cursor()
        Cursor.execute("Select * FROM PatientDet")
        rows=Cursor.fetchall()
        return render_template("view.html",rows=rows)

if __name__=="__main__":
    app.run(debug=True)
