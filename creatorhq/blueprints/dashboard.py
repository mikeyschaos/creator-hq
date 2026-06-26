from flask import Blueprint, render_template

from creatorhq.services.dashboard_service import DashboardService

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def home():

    data = DashboardService.load()

    return render_template(
        "dashboard.html",
        dashboard=data,
    )
