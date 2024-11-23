from flask import Flask, render_template, request, redirect
import flask
import requests
import json
import loc

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
