"""
Creator HQ Control Center Blueprint
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from creatorhq.services.settings_service import SettingsService

control = Blueprint("control", __name__)


@control.route("/control")
def index():
    return render_template(
        "control/index.html",
        active_page="overview",
    )


@control.route("/control/goals", methods=["GET", "POST"])
def goals():

    if request.method == "POST":

        goals = {}

        settings = SettingsService.get_goals()

        for channel in settings["goals"]:

            value = request.form.get(channel)

            try:
                goals[channel] = int(value)
            except (TypeError, ValueError):
                goals[channel] = settings["goals"][channel]

        network_goal = request.form.get(
            "networkGoal",
            settings["networkGoal"]
        )

        SettingsService.save_goals(
            goals,
            network_goal,
        )

        return redirect(
            url_for(
                "control.goals",
                saved="true"
            )
        )

    settings = SettingsService.get_goals()

    saved = request.args.get("saved") == "true"

    return render_template(
        "control/goals.html",
        settings=settings,
        saved=saved,
        active_page="goals",
    )


@control.route("/control/tips", methods=["GET", "POST"])
def tips():

    if request.method == "POST":

        tips = request.form.getlist("tip")

        SettingsService.save_tips(tips)

        return redirect(
            url_for(
                "control.tips",
                saved="true"
            )
        )

    tips = SettingsService.get_tips()

    saved = request.args.get("saved") == "true"

    return render_template(
        "control/tips.html",
        tips=tips,
        saved=saved,
        active_page="tips",
    )
