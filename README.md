# ☀️ Solar Rooftop AI Assistant

A Streamlit web app that analyzes satellite rooftop images to estimate solar panel installation potential, calculate ROI, and provide AI-driven recommendations.

---

## 🚀 Features

- **Rooftop segmentation** from uploaded satellite images using TensorFlow model.
- **Solar panel estimation** based on rooftop area and panel specs.
- **ROI calculation** considering installation cost, electricity rates, and sunlight hours.
- **AI-generated recommendations** using an LLM for personalized advice.
- **Downloadable report** summarizing analysis and recommendations.

---

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning repo)
- Virtual environment tool (recommended)

---

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/inferno-0709/solar-ai-assistant.git
cd solar-ai-assistant
```

2. **Create and activate virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## ⚙️ Running the App

Start the Streamlit app by running:

```bash
streamlit run app.py
```

Open the URL provided in your browser (usually `http://localhost`).

---

## 📋 Usage Guide

1. Upload a satellite image of the rooftop (`.jpg`, `.jpeg`, `.png`).
2. Enter solar panel specifications:
   - Wattage of one panel (100W–600W)
   - Area of one panel (1.0–40.0 sq.m)
3. Click **Analyze rooftop** to perform rooftop segmentation and get area estimates.
4. Enter ROI parameters:
   - Installation cost per watt
   - Electricity rate (₹ per kWh)
   - Average sunlight hours per day
5. View ROI estimate and payback period.
6. Click **Generate Recommendation** to get AI-driven advice.
7. Download the full report with analysis and recommendations.

---

## 🗂️ Project Structure

```
solar-ai-assistant/
├── app.py           # Main Streamlit app
├── model.py         # TensorFlow rooftop segmentation model loader
├── area.py          # Rooftop area and panel estimation logic
├── cost.py          # ROI calculation functions
├── summary.py       # Summary prompt generation
├── llm.py           # AI model (LLM) integration for recommendations
├── requirements.txt # Python dependencies
```

---

## ⚠️ Notes

- Ensure the pretrained segmentation model files are properly set up in `model.py`.
- The AI recommendation feature requires API access (Hugging face already provided with the api key) configured in `llm.py`.
- Adjust parameters according to your local energy and installation cost data for accurate ROI estimates.


