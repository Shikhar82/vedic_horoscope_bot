# 🔮 Vedic Horoscope Generator (वेदिक कुंडली)

A modern Python-powered web app to generate detailed Vedic horoscope (कुंडली) using:
- 📍 User birth details (date, time, location)
- 🌌 Swiss Ephemeris (swisseph) for planetary positions
- 🤖 Claude AI (Amazon Bedrock) for astrology predictions in Hindi
- 📄 Downloadable PDF horoscope reports with Unicode Hindi font
- 🖥️ Streamlit-based frontend + Flask API backend

---

## 🚀 Live Demo (if hosted)

👉 [http://your-ec2-ip:8501](http://your-ec2-ip:8501)

---

## 🧠 Features

- Input form for DOB, TOB, Latitude, Longitude, Timezone
- Fetches planet positions using Swiss Ephemeris
- Generates Hindi prediction using Claude AI (`bedrock.claude-3-sonnet`)
- Shows Rashi (Moon Sign) with personality description
- Generates downloadable PDF in Hindi
- Modular code with separate frontend/backend/Claude integration

---

## 📦 Project Structure

vedic_horoscope_bot/
├── app.py # Flask backend for API
├── bedrock_claude.py # Claude API integration
├── horoscope_bot.py # Streamlit UI
├── NotoSansDevanagari-Regular.ttf # Font for PDF
├── requirements.txt
├── .gitignore
└── README.md


---

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/vedic_horoscope_bot.git
cd vedic_horoscope_bot

2. Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate
3. Install dependencies

pip install -r requirements.txt
4. Set up Amazon Bedrock access
Ensure your AWS credentials are configured properly to access Bedrock via Boto3:

=
aws configure
5. Run Flask API (Backend)

python app.py
6. In a new terminal, run Streamlit (Frontend)

streamlit run horoscope_bot.py
Access at: http://localhost:8501

🖼️ Screenshot

📤 API Example (Optional)

curl -X POST http://localhost:5001/api/kundli \
-H "Content-Type: application/json" \
-d '{
  "date": "1990-01-01",
  "time": "11:17",
  "latitude": 26.8467,
  "longitude": 80.9462,
  "timezone": 5.5
}'
📚 Technologies Used
Python 3

Flask

Streamlit

Boto3 + Amazon Bedrock (Claude 3)

Swiss Ephemeris (swisseph)

fpdf (for PDF generation)

Noto Sans Devanagari Font (Unicode Hindi)

✨ Credits
Developed by Your Name

📃 License
MIT License (optional)



---

## ✅ 4. Final Push to GitHub

```bash
git add .
git commit -m "🎉 Initial commit - Vedic Horoscope Generator with Claude AI"
git branch -M main
git remote add origin https://github.com/<your-username>/vedic_horoscope_bot.git
git push -u origin main

Make it run as background services (Flask + Streamlit) with systemd
