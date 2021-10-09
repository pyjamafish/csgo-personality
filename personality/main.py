from flask import Flask, render_template, url_for, request, redirect
import csv
from dataclasses import dataclass

app = Flask(__name__)


@dataclass
class Option:
    name: str
    value: int
    image: str


maps = [
    Option("Ancient", 3, "/static/img/maps/de_ancient.png"),
    Option("Dust II", 1, "/static/img/maps/de_dust2.png"),
    Option("Inferno", 3, "/static/img/maps/de_inferno.png"),
    Option("Mirage", 1, "/static/img/maps/de_mirage.png"),
    Option("Nuke", 2, "/static/img/maps/de_nuke.png"),
    Option("Overpass", 2, "/static/img/maps/de_overpass.png"),
    Option("Vertigo", 3, "/static/img/maps/de_vertigo.png")
]
utilities = [
    Option("Flashbang", 3, "/static/img/utility/flash.png"),
    Option("HE Grenade", 4, "/static/img/utility/he.png"),
    Option("Molotov", 1, "/static/img/utility/molotov.png"),
    Option("Smoke Grenade", 2, "/static/img/utility/smoke.png")
]
ecos = [
    Option("Negev", 4, "/static/img/eco/negev.png"),
    Option("Pistol", 2, "/static/img/eco/pistol.png"),
    Option("Shotgun", 3, "/static/img/eco/shotgun.png"),
    Option("SMG", 1, "/static/img/eco/smg.png")
]
buys = [
    Option("AK-47", 3, "/static/img/buy/ak.png"),
    Option("M4A4/M4A1-S", 2, "/static/img/buy/m4.png"),
    Option("AUG/SSG", 1, "/static/img/buy/aug.png"),
    Option("AWP", 4, "/static/img/buy/awp.png"),
]


def calculate_color(quiz_sum: int) -> str:
    if quiz_sum <= 4:
        result = "Orange"
    elif quiz_sum <= 8:
        result = "Green"
    elif quiz_sum <= 16:
        result = "Blue"
    elif quiz_sum <= 20:
        result = "Yellow"
    else:
        result = "Purple"
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")

        quiz_sum = sum([
            sum(int(s) for s in request.form.getlist("map")),
            int(request.form.get("utility")),
            int(request.form.get("eco")),
            int(request.form.get("buy")),
        ])
        result = calculate_color(quiz_sum)

        with open("data.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([name, quiz_sum, result])

        return render_template(
            "result.html",
            name=name,
            result=result
        )
    else:
        return render_template(
            "index.html",
            maps=maps,
            utilities=utilities,
            ecos=ecos,
            buys=buys
        )
