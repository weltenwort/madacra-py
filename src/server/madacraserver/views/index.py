# vim: set fileencoding=utf-8 :
from flask import (
        Blueprint,
        render_template,
        )

index_blueprint = Blueprint("index", __name__, template_folder="templates")


@index_blueprint.route("/")
def view_index():
    return render_template("index.jade")
