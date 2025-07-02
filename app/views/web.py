from flask import Blueprint, redirect, render_template

from app.model import Url
from app.service import update_count

web = Blueprint("web", __name__)


@web.route("/")
def index():
    return render_template("base.html")


@web.route("/<url>")
def redir(url):
    origin = Url.query.filter_by(short_url=url).scalar()
    if origin is None:
        return render_template("not_valid_url.html")
    else:
        update_count(origin)
        return redirect(origin.original_url)
