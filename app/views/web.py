import json

import requests
from flask import Blueprint, redirect, render_template, request, url_for

from app import Config
from app.model import Url
from app.service import update_count

web = Blueprint("web", __name__)


@web.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        response = requests.post(
            url=Config.DOMAIN_URL + url_for("api.create_url"),
            data=json.dumps(request.form),
        )
        if response.status_code == 200:
            return render_template("modules/short_url.html", response=response.json())
        else:
            return response.text, response.status_code

    return render_template("modules/index.html")


@web.route("/<url>")
def redir(url):
    origin = Url.query.filter_by(short_url=url).scalar()
    if origin is None:
        return render_template("modules/index.html", error="this url does not exist")
    else:
        update_count(origin)
        return redirect(origin.original_url)
