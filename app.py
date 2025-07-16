# ---------------------- app.py ----------------------
from flask import Flask, request, jsonify
import swisseph as swe
from datetime import datetime, timedelta
from bedrock_claude import get_claude_prediction

app = Flask(__name__)

@app.route("/api/kundli", methods=["POST"])
def kundli():
    try:
        data = request.json
        date = data['date']
        time = data['time']
        lat = float(data['latitude'])
        lon = float(data['longitude'])
        tz = float(data['timezone'])

        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        dt_utc = dt - timedelta(hours=tz)

        jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                        dt_utc.hour + dt_utc.minute / 60.0)

        planets = {}
        for pid in range(swe.SUN, swe.PLUTO + 1):
            pos = swe.calc_ut(jd, pid)[0]
            name = swe.get_planet_name(pid)
            planets[name] = round(pos[0], 2)

        # Get AI prediction from Claude
        prediction = get_claude_prediction(data, planets)

        return jsonify({
            "julian_day": jd,
            "planet_positions": planets,
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
