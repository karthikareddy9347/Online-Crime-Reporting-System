from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

CSV_PATH = "homicide_crimes_1000.csv"

# Create CSV if missing
if not os.path.exists(CSV_PATH):
    df = pd.DataFrame(columns=[
        "Date", "City", "State", "Offense_Type", "Weapon",
        "Victim_Gender", "Arrest", "Domestic"
    ])
    df.to_csv(CSV_PATH, index=False)

@app.route("/")
def index():
    return render_template("index.html")

# ---------------- POLICE LOGIN --------------------
@app.route("/login_police", methods=["POST"])
def login_police():
    username = request.form["username"]
    password = request.form["password"]

    if username == "akshaya@crime" and password == "admin123":
        return render_template("dashboard_police.html")
    else:
        return render_template("index.html", error="Invalid police login")

# ---------------- CITIZEN LOGIN --------------------
@app.route("/login_citizen", methods=["POST"])
def login_citizen():
    name = request.form["name"]
    password = request.form["password"]

    if name.strip() and password.strip():
        return render_template("dashboard_citizen.html", user=name)
    else:
        return render_template("index.html", error="Enter valid citizen login")

# ---------------- ADD CRIME --------------------
@app.route("/add_crime", methods=["POST"])
def add_crime():
    data = request.form.to_dict()
    df = pd.read_csv(CSV_PATH)

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

    return jsonify({"message": "Crime added successfully!"})

# ---------------- GET ALL CRIMES --------------------
@app.route("/get_all_crimes")
def get_all_crimes():
    df = pd.read_csv(CSV_PATH)
    return df.to_json(orient="records")

# ---------------- SEARCH CRIMES --------------------
@app.route("/search_crimes")
def search_crimes():
    df = pd.read_csv(CSV_PATH)
    q = request.args.get("query", "").lower()

    if q.strip() == "":
        return df.to_json(orient="records")

    filtered = df[df.apply(lambda row: q in str(row.values).lower(), axis=1)]
    return filtered.to_json(orient="records")

if __name__ == "__main__":
    app.run(debug=True)
