from flask import Flask, render_template, request,session,redirect,flash
import psycopg2
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


app=Flask(__name__)  
app.secret_key="hello123"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register")
def register_func():
    return render_template("register.html")

@app.route("/login")
def login_func():
    return render_template("login.html")


@app.route("/logindata", methods=["POST"])
def logindata():
    user=request.form["user"]
    password=request.form["pass"]
    conn=psycopg2.connect(host="localhost",database="flask1stDB",user="postgres",password="vidhu")
    cur=conn.cursor()
    cur.execute('select * from "User" where name=%s',(user,))
    d=cur.fetchone()

    if(d):
        st=d[2]
        if check_password_hash(st,password):
            session["user"]=user
            
            return redirect("/dashboard")

        else:
            flash("wrong Password-Check Password Again")
            return redirect('/login')
             
    else:
        flash("No User Exist")
        return redirect('/login')

    conn.commit()
    conn.close()
    cur.close()
    
    
@app.route("/registerdata", methods=["POST"])
def registerdata():
    user=request.form["user"]
    password=request.form["pass"]
    conn=psycopg2.connect(host="localhost",database="flask1stDB",user="postgres",password="vidhu")
    cur=conn.cursor()
    hashed=generate_password_hash(password)
    cur.execute('select * from "User" where name =%s',(user,))
    d=cur.fetchone()
    if d:
        flash("User already exist ")
        return redirect('/register')
    else:
        cur.execute('Insert into "User" (name,password) values(%s,%s)',(user,hashed))
        conn.commit()
        cur.close()
        conn.close()
        flash("Registered User Successfully Login Now")
        return redirect('/login')

@app.route("/dashboard")
def dashboard_page():
    if "user" in session:
        user=session["user"]
        conn=psycopg2.connect(host="localhost",database="flask1stDB",user="postgres",password="vidhu")
        cur=conn.cursor()
        cur.execute("select * from tasks where name =%s",(user,))
        d=cur.fetchall()
        c=0
        p=0
        for i in d:
            if i[3]:
                c+=1
            else:
                p+=1

        conn.commit()
        cur.close()
        conn.close()


        return render_template("dashboard.html",user=user,tasks=d,p=p,c=c)
    else:
        return redirect("/login")


@app.route("/addpopuptask",methods=["POST"])
def pop_up():
    if "user" in session:    
        user=session["user"] 
    else:
        return redirect("/login")
    task=request.form["task"]
    conn=psycopg2.connect(host="localhost",database="flask1stDB",user="postgres",password="vidhu")
    cur=conn.cursor()
    cur.execute('insert into tasks(name,t_name,status) values(%s,%s,%s)',(user,task,False))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/dashboard")

@app.route("/done/<int:id>")
def done(id):
    conn=psycopg2.connect(host="localhost",database="flask1stDB",user="postgres",password="vidhu")
    cur=conn.cursor()
    cur.execute("update tasks set status=NOT status where t_id=%s",(id,))

    conn.commit()
    cur.close()
    conn.close()
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id):
    conn=psycopg2.connect(host="localhost",database="flask1stDB",user="postgres",password="vidhu")
    cur=conn.cursor()
    cur.execute("delete from tasks where t_id=%s",(id,))

    conn.commit()
    cur.close()
    conn.close()
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/login")

app.run(debug=True)



