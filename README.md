# NEXUS: Global AI Sentinel 🌍

![Status](https://img.shields.io/badge/Status-Operational-00ffff)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Dash](https://img.shields.io/badge/Framework-Dash-orange)

**NEXUS**, dünya genelindeki yapay zeka (AI) gelişmelerini, askeri ve stratejik hareketlilikleri gerçek zamanlı olarak izleyen, 3 boyutlu interaktif bir istihbarat paneli (dashboard) projesidir.

## 🚀 Özellikler

* **3D İnteraktif Küre:** Plotly altyapısı ile geliştirilmiş, ortografik projeksiyonlu siber dünya haritası.
* **Gerçek Zamanlı İstihbarat:** Google News altyapısı ile seçilen ülkeye dair en güncel AI haberlerinin anlık çekilmesi.
* **Risk Analizi:** Haber metinlerinde geçen kritik kelimelere (military, nuclear, hack, surveillance vb.) göre otomatik **[CRITICAL]** tehdit algılama sistemi.
* **Çoklu Dil Desteği:** Entegre `deep-translator` servisi ile haberleri İngilizce, Türkçe, İspanyolca, Almanca, Rusça ve Fransızca dillerine anlık çevirme.
* **Siber Arayüz (HUD):** "007 GoldenEye" ve Cyberpunk estetiğinden esinlenilmiş, neon renk paletine sahip kullanıcı arayüzü.

## 🛠️ Kurulum (Installation)

Projeyi kendi bilgisayarınızda çalıştırmak için adımları izleyin:

1.  Repoyu klonlayın:
    ```bash
    git clone [https://github.com/yigitbkucuk/nexus-ai-sentinel.git](https://github.com/yigitbkucuk/nexus-ai-sentinel.git)
    cd nexus-ai-sentinel
    ```

2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

3.  Uygulamayı başlatın:
    ```bash
    python app.py
    ```

4.  Tarayıcınızda şu adrese gidin: `http://127.0.0.1:8050/`

## 🏗️ Teknoloji Yığını (Tech Stack)

* **Backend:** Python
* **Frontend:** Dash & CSS (Cyber-themed)
* **Veri Görselleştirme:** Plotly Graph Objects (3D Globe)
* **Veri Kaynağı:** GoogleNews Library (Real-time fetching)
* **NLP & Çeviri:** Deep-Translator & Keyword Matching Algorithm


---
*Developed by Yiğit B. Küçük*