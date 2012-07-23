from flask import (
        Blueprint,
        render_template,
        )

tests_blueprint = Blueprint("tests", __name__, template_folder="templates")


@tests_blueprint.route("/e2e")
def view_e2e():
    return render_template("e2e_tests.jade")


@tests_blueprint.route("/unit")
def view_unit():
    return render_template("unit_tests.jade")
