# NEXUS: Global AI Sentinel 🌍

![Status](https://img.shields.io/badge/Status-Operational-00ffff)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Dash](https://img.shields.io/badge/Framework-Dash-orange)

**NEXUS** is a real-time, 3D interactive intelligence dashboard designed to monitor global Artificial Intelligence (AI) developments, military activities, and strategic movements. It aggregates scattered data into a unified "Situation Room" interface for strategic decision-making.

## 🚀 Features

* **3D Interactive Globe:** A fully interactive cyber-globe built with Plotly using orthographic projection for a realistic "command center" experience.
* **Real-Time Intelligence:** Instantly fetches the latest AI-related news for any selected country using the Google News infrastructure.
* **Automated Risk Analysis:** Scans news content for critical keywords (e.g., *military, nuclear, hack, surveillance, bioweapon*) and automatically flags threats as **[CRITICAL]** in red.
* **Multi-Language Support:** Breaks language barriers with integrated `deep-translator` support. Instantly translates global news into **English, Turkish, Spanish, German, Russian, and French**.
* **Cyber Interface (HUD):** A sleek, dark-mode UI inspired by "007 GoldenEye" and Cyberpunk aesthetics, featuring neon visuals and custom typography.

## 🛠️ Installation

Follow these steps to deploy NEXUS on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yigitbkucuk/nexus-ai-sentinel.git](https://github.com/yigitbkucuk/nexus-ai-sentinel.git)
    cd nexus-ai-sentinel
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python app.py
    ```

4.  **Access the Dashboard:**
    Open your browser and navigate to: `http://127.0.0.1:8050/`

## 🏗️ Tech Stack

* **Backend:** Python
* **Frontend:** Dash & CSS (Cyber-themed styling)
* **Visualization:** Plotly Graph Objects (3D Orthographic Globe)
* **Data Source:** GoogleNews Library (Real-time scraping & fetching)
* **NLP & Translation:** Deep-Translator & Custom Keyword Matching Algorithm

---
*Developed by Yiğit Buğra Küçük*