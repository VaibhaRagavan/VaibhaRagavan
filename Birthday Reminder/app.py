import uuid
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    jsonify
    
)
import flask
import requests
import json
import dict_search
import dayscalculator
import loc
import pymysql
import datetime
import re
from flask_sqlalchemy import SQLAlchemy
import random
import smtplib

from sqlentry import fav_details, getu_id

hostname = "localhost"
user = "root"
database = "mydatabase"

db = pymysql.connections.Connection(host=hostname, user=user, database=database)
mycursor = db.cursor()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/mydatabase"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "abcde"
db = SQLAlchemy(app)


@app.route("/dblinkjs", methods=["GET"])
def dbjs():
    mycursor.execute("SELECT name FROM eventdetails")
    data = mycursor.fetchall()
    return jsonify(data)


@app.route("/favdb", methods=["GET"])
def favdb():
    u1_name = session["user"]
    mycursor.execute(
        "SELECT eventdetails.name FROM((favorites INNER JOIN userdetails ON userdetails.userid=favorites.userid)INNER JOIN eventdetails ON eventdetails.id=favorites.u_id)WHERE userdetails.user=%s",
        u1_name,
    )
    fv_name = mycursor.fetchall()
    return jsonify(fv_name)


@app.route("/homepage")
def Home_page():
    return render_template("home.html")


@app.route("/homedb", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["passwd"]

        mycursor.execute(
            "SELECT * FROM userdetails  WHERE emailid = %s AND password = %s",
            (email, pwd),
        )
        out = mycursor.fetchone()
        if out:
            email == out[1]
            session["loggedin"] = True
            session["user"] = out[0]
            session["userid"] = out[3]
            session["emailid"] = out[1]
            session["password"] = out[4]

            return redirect(url_for("mainpage"))
        else:
            return "Incorrect id/password"


@app.route("/mainpage")
def mainpage():

    return render_template("mainpage.html", out=session["user"])


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    return render_template("login.html")


@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    if request.method == "GET":
        mycursor.execute("SELECT name FROM eventdetails")
        n_list = mycursor.fetchall()
        u1_name = session["user"]
        mycursor.execute(
            "SELECT eventdetails.name FROM((favorites INNER JOIN userdetails ON userdetails.userid=favorites.userid)INNER JOIN eventdetails ON eventdetails.id=favorites.u_id)WHERE userdetails.user=%s",
            u1_name,
        )
        fv_name = mycursor.fetchall()

        return render_template("subscriptionlist.html", n_list=n_list, fv_name=fv_name)


@app.route("/newaccount", methods=["POST", "GET"])
def newaccount():
    if request.method == "POST":
        username = request.form["key"]
        email_id = request.form["em"]
        phoneno = request.form["phn"]
        pswd = request.form["pwd"]

        mycursor.execute(
            "INSERT INTO userdetails (name,emailid,phonenumber,password) values(%s,%s,%s,%s)",
            (username, email_id, phoneno, pswd),
        )
        mycursor.connection.commit()

        return render_template("login.html")
    else:
        return render_template("reg.html")


@app.route("/entry", methods=["POST", "GET"])
def display():
    if request.method == "POST":
        name_1 = request.form["name"]
        dob_1 = request.form["dob"]
        value = request.form["genderbox"]
        if value == "F":
            gender_1 = "F"
        else:
            gender_1 = "M"
        id_1 = uuid.uuid4()

        def entered(n, g, d, id):
            {
                mycursor.execute(
                    "INSERT INTO eventdetails (name,gender,dateofbirth,id) values(%s,%s,%s,%s)",
                    (n, g, d, id),
                )
            }

        entered(name_1, gender_1, dob_1, id_1)
        mycursor.connection.commit()
        res = mycursor.fetchall()
        data = list(res)

        return render_template("entry.html", data=data)
    else:
        return render_template("entry.html")


@app.route("/sendemailverfication", methods=["POST", "GET"])
def verfication():
    if request.method == "POST":
        emailid = request.form["email"]

        rn = random.randint(1000, 9999)
        code = str(rn)

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login("vaibhavijayvidhun@gmail.com", "novo gdnp zlvy iaoz")
        msg = "The verfication code to change pasword for birthday calender is" + code

        s.sendmail("vaibhavijayvidhun@gmail.com", emailid, msg)
        s.quit()
        return redirect(url_for("update", code=code))
    else:
        return render_template("sendverfication.html")


@app.route("/update", methods=["POST", "GET"])
def update():

    if request.method == "POST":
        id = request.form["regemail"]
        otp = request.form["otp"]
        keyword = request.form["newpwd"]
        code = session.get("value")
        if otp == code:
            mycursor.execute(
                "UPDATE userdetails SET password=%s where emailid=%s", (keyword, id)
            )
            mycursor.connection.commit()
        return render_template("login.html")

    else:
        data = request.args.get("code")
        session["value"] = data
        return render_template("update.html")


@app.route("/view", methods=["GET", "POST"])
def finding():
    if request.method == "POST":
        keyword_name = request.form["enter"]
        keyword_month = request.form["month"]
        keyword_date = request.form["date"]

        mycursor.execute(
            "SELECT name,gender,dateofbirth FROM eventdetails WHERE name=%s OR month(dateofbirth)=%s OR day(dateofbirth)=%s",
            (keyword_name, keyword_month, keyword_date),
        )
        view = mycursor.fetchall()
        return render_template("find.html", view=view)
    else:
        return render_template("find.html")


@app.route("/favorite", methods=["POST", "GET"])
def fav():
    if request.method == "GET":
        u_name = session["user"]
        mycursor.execute(
            "SELECT eventdetails.name FROM((favorites INNER JOIN userdetails ON userdetails.userid=favorites.userid)INNER JOIN eventdetails ON eventdetails.id=favorites.u_id)WHERE userdetails.user=%s",
            u_name,
        )
        f_name = mycursor.fetchall()
        return render_template("fav.html", f_name=f_name)
    else:
        data = request.get_json()
        mycursor.execute("SELECT id FROM eventdetails WHERE name=%s", data)
        get_id = mycursor.fetchone()
        us_id = session["userid"]
        mycursor.execute(
            "INSERT INTO favorites(u_id,userid) values(%s,%s)", (get_id, us_id)
        )
        mycursor.connection.commit()
    return render_template("fav.html")


@app.route("/longlat", methods=["POST", "GET"])
def longlat():
    if request.method == "POST":
        area = request.form["area"]
        locationcoor = loc.location(area)
        locationcoor_list = list(locationcoor)
        return render_template(
            "locres.html",
            locationcoor1=locationcoor_list,
            lat=locationcoor[2],
            long=locationcoor[1],
        )
    else:
        return render_template("loc.html")


@app.route("/calculator", methods=["POST", "GET"])
def res():
    if request.method == "POST":
        date1 = request.form["first date"]
        date2 = request.form["second date"]
        enterdate1 = dayscalculator.date_fun(date1)
        enterdate2 = dayscalculator.date_fun(date2)
        result = dayscalculator.res_days(enterdate1, enterdate2)
        return render_template("date.html", calculator=result, date1=date1, date2=date2)
    else:
        return render_template("date.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        word = request.form["keyword"]
        page = dict_search.api_call(word)
        display = dict_search.text_processor(page)
        return render_template("search.html", response1=display)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)
