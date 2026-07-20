from flask import Flask, render_template, request, redirect
import sqlite3
import joblib
import os

app = Flask(__name__)

# ----------------------------
# Create Database if Not Exists
# ----------------------------
def create_database():
    conn = sqlite3.connect("medicine.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dosage TEXT,
            time TEXT
        )
    """)

    conn.commit()
    conn.close()

create_database()

# ----------------------------
# Load AI Model
# ----------------------------
model = None

if os.path.exists("health_model.pkl"):
    model = joblib.load("health_model.pkl")

# ----------------------------
# Home Page
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------
# Medicine Page
# ----------------------------
@app.route("/medicine", methods=["GET", "POST"])
def medicine():

    if request.method == "POST":

        name = request.form["name"]
        dosage = request.form["dosage"]
        time = request.form["time"]

        conn = sqlite3.connect("medicine.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO medicines(name,dosage,time) VALUES(?,?,?)",
            (name, dosage, time)
        )

        conn.commit()
        conn.close()

        return redirect("/medicine")

    conn = sqlite3.connect("medicine.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM medicines")

    medicines = cur.fetchall()

    conn.close()

    return render_template(
        "medicines.html",
        medicines=medicines
    )

# ----------------------------
# Delete Medicine
# ----------------------------
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("medicine.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM medicines WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/medicine")

# ----------------------------
# Predictor Page
# ----------------------------
@app.route("/predictor")
def predictor():
    return render_template("predictor.html")

# ----------------------------
# Predict Health Risk
# ----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    age = float(request.form["age"])
    bp = float(request.form["bp"])
    sugar = float(request.form["sugar"])
    bmi = float(request.form["bmi"])

    if model is None:
        return "Model not found! Run train_model.py first."

    prediction = model.predict([[age, bp, sugar, bmi]])[0]

    if prediction == 0:
        risk = "Low Risk"
        suggestion = "Maintain a healthy lifestyle."

    elif prediction == 1:
        risk = "Medium Risk"
        suggestion = "Exercise regularly and monitor your health."

    else:
        risk = "High Risk"
        suggestion = "Consult a healthcare professional."

    return render_template(
        "result.html",
        risk=risk,
        suggestion=suggestion
    )

# ----------------------------
# Run Website
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)s