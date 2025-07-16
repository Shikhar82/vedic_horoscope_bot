# ---------------------- horoscope_bot.py ----------------------
import streamlit as st
import requests
import datetime
from fpdf import FPDF
from io import BytesIO
from bedrock_claude import get_claude_prediction
from fpdf.enums import XPos, YPos

FONT_PATH = "NotoSansDevanagari-Regular.ttf"

def get_rashi(degree: float) -> str:
    rashis = [
        "मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)",
        "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)",
        "धनु (Sagittarius)", "मकर (Capricorn)", "कुंभ (Aquarius)", "मीन (Pisces)"
    ]
    return rashis[int(degree // 30)]

def moon_prediction(rashi: str) -> str:
    return {
        "मेष (Aries)":  "आप ऊर्जावान और साहसी हैं। नेतृत्व करना पसंद करते हैं।",
        "वृषभ (Taurus)": "आप व्यावहारिक हैं और सुंदरता पसंद करते हैं।",
        "मिथुन (Gemini)": "आप जिज्ञासु हैं और संवाद प्रिय हैं।",
        "कर्क (Cancer)":  "आप भावनात्मक और परिवार केंद्रित हैं।",
        "सिंह (Leo)":    "आप आत्मविश्वासी हैं और शोप्रिय हैं।",
        "कन्या (Virgo)":  "आप विश्लेषणात्मक और व्यावहारिक हैं।",
        "तुला (Libra)":   "आप संतुलन और न्याय प्रिय हैं।",
        "वृश्चिक (Scorpio)": "आप रहस्यमयी और तीव्र भावनाओं वाले हैं।",
        "धनु (Sagittarius)": "आप स्वतंत्रता प्रिय और दार्शनिक हैं।",
        "मकर (Capricorn)":   "आप जिम्मेदार और परंपरावादी हैं।",
        "कुंभ (Aquarius)":   "आप विचारशील और नवीनता में रुचि रखते हैं।",
        "मीन (Pisces)":      "आप संवेदनशील और कलात्मक हैं।"
    }.get(rashi, "आपमें विशेष गुण हैं।")

def generate_pdf(payload: dict, positions: dict, prediction: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font("Unicode", "", FONT_PATH, uni=True)
    pdf.set_font("Unicode", "", 14)
    pdf.cell(0, 10, "वेदिक कुंडली रिपोर्ट", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)

    pdf.set_font("Unicode", "", 12)
    pdf.cell(0, 10, "जन्म जानकारी:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for key, val in payload.items():
        pdf.cell(0, 8, f"{key.capitalize()}: {val}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)
    pdf.cell(0, 10, "ग्रह स्थिति:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for planet, deg in positions.items():
        rashi = get_rashi(deg)
        pdf.cell(0, 8, f"{planet}: {deg:.2f}° - {rashi}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    if "Moon" in positions:
        moon_rashi = get_rashi(positions["Moon"])
        pdf.ln(6)
        pdf.cell(0, 10, f"चंद्र राशि: {moon_rashi}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.multi_cell(0, 8, f"भविष्यवाणी: {moon_prediction(moon_rashi)}")

    if prediction:
        pdf.ln(6)
        pdf.set_font("Unicode", "", 11)
        pdf.cell(0, 10, "AI आधारित विस्तृत भविष्यवाणी:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.multi_cell(0, 8, prediction)

    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()

# ---------------------------- UI ---------------------------------
st.set_page_config(page_title="Vedic Horoscope Generator", layout="centered")
st.title("Horoscope Generator (वेदिक कुंडली)")

with st.form("form"):
    dob = st.date_input("जन्म तिथि", datetime.date(1990, 1, 1),
                        min_value=datetime.date(1900, 1, 1),
                        max_value=datetime.date.today())
    tob = st.time_input("जन्म समय")
    lat = st.number_input("अक्षांश (Latitude)", value=26.8467, format="%.4f")
    lon = st.number_input("देशांतर (Longitude)", value=80.9462, format="%.4f")
    tz  = st.number_input("समय क्षेत्र (Timezone)", value=5.5, format="%.1f")
    submit = st.form_submit_button("🔮 कुंडली बनाएँ")

if submit:
    payload = {
        "date": str(dob),
        "time": str(tob)[:5],
        "latitude": lat,
        "longitude": lon,
        "timezone": tz
    }

    try:
        res  = requests.post("http://localhost:5001/api/kundli", json=payload)
        data = res.json()

        if "planet_positions" in data:
            positions = data["planet_positions"]

            # Claude Foundation Model Prediction
            prediction = get_claude_prediction(payload, positions)

            st.success("✅ कुंडली सफलतापूर्वक बनाई गई")

            st.subheader("ग्रह स्थिति")
            for planet, deg in positions.items():
                rashi = get_rashi(deg)
                st.write(f"**{planet}**: {deg:.2f}° - {rashi}")

            if "Moon" in positions:
                moon_rashi = get_rashi(positions["Moon"])
                st.subheader("चंद्र राशि")
                st.success(f"आपकी राशि है: **{moon_rashi}**")
                st.markdown(f"**भविष्यवाणी:** {moon_prediction(moon_rashi)}")

            if prediction:
                st.subheader("🤖 Claude AI आधारित भविष्यवाणी")
                st.info(prediction)

            pdf_bytes = generate_pdf(payload, positions, prediction)
            st.download_button(
                label="📥 कुंडली PDF डाउनलोड करें",
                data=pdf_bytes,
                file_name="kundli_report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("❌ कुंडली डेटा नहीं मिला।")

    except Exception as e:
        st.error(f"❌ त्रुटि: {e}")
