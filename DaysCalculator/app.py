from flask import Flask,request,rendertemplate
import datetime
import dayscalculator

@app.route("/calculator", methods=["POST", "GET"])
def res():
    if request.method == "POST":
        date1 = request.form["first date"]
        date2 = request.form["second date"]
        enterdate1 = dayscalculator.date_fin(date1)
        enterdate2 = dayscalculator.date_fin(date2)
        result = dayscalculator.res_days(enterdate1, enterdate2)
        return render_template("date.html", calculator=result, date1=date1, date2=date2)
    else:
        return render_template("date.html")
