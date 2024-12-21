from flask import Flask, render_template, request
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load model
model_path = "artifacts/models/trained_model.pkl"
model = joblib.load(model_path)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Collect inputs from the form
            departure_delay = float(request.form["Departure Delay"])
            arrival_delay = float(request.form["Arrival Delay"])
            flight_distance = float(request.form["Flight Distance"])
            
            # Calculate Delay Ratio
            delay_ratio = (departure_delay + arrival_delay) / (flight_distance + 1)
            
            # Prepare input data for the model
            data = [
                delay_ratio,
                flight_distance,
                int(request.form["Online boarding"]),
                int(request.form["Inflight wifi service"]),
                int(request.form["Class"]),
                int(request.form["Type of Travel"]),
                int(request.form["Inflight entertainment"]),
                int(request.form["Seat comfort"]),
                int(request.form["Leg room service"]),
                int(request.form["On-board service"]),
                int(request.form["Cleanliness"]),
                int(request.form["Ease of Online booking"]),
            ]

            # Model prediction
            prediction = model.predict([data])
            output = prediction[0]

            return render_template("index.html", prediction=output)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
