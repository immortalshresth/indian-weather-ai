# 🇮🇳 Pan-India Airport Weather AI 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://indian-weather-ai-gaaxx7atpvqxf6btm2uyer.streamlit.app/)

A full-stack machine learning web application that predicts localized T+2 hour weather conditions across 18 major Indian airports. It fetches live meteorological data directly from the US Government's Aviation Weather API and feeds it into highly compressed, pre-trained Random Forest models.

## 🌟 Features
* **Live Telemetry:** Bypasses web scraping by using a REST API to fetch real-time METAR data (Temperature, Wind, Altimeter) in milliseconds.
* **Localized AI Brains:** Utilizes 18 distinct Random Forest Regressors, trained on decades of Iowa Mesonet historical data, to account for highly specific regional weather patterns.
* **Optimized Architecture:** Models are compressed via `joblib` and pruned (`max_depth=10`, `n_estimators=30`) to reduce file size by 90% without sacrificing predictive accuracy, enabling seamless cloud deployment.
* **Cinematic UI:** Built with Streamlit, featuring dynamic model auto-detection, custom CSS injection, and base64-encoded video backgrounds.

## 🛠️ Tech Stack
* **Frontend:** Streamlit, HTML5/CSS3
* **Backend:** Python, `requests`
* **Machine Learning:** Scikit-Learn (Random Forest Regressor), `joblib`
* **Data Engineering:** Pandas, Numpy

## 🚀 How to Run Locally

1. Clone this repository:
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/pan-india-weather-ai.git](https://github.com/YOUR_GITHUB_USERNAME/pan-india-weather-ai.git)
