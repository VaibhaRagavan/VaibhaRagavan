from flask import (
    Flask,
    render_template,
    request,
    url_for,
    jsonify
    
)
import requests
import json
import dict_search

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        word = request.form["keyword"]
        page = dict_search.api_call(word)
        display = dict_search.text_processor(page)
        return render_template("search.html", response1=display)
    else:
        return render_template("index.html")
