import plotly.graph_objects as go
import pandas as pd


def dunya_kuresi_olustur():
    print("Situation Room: Küresel Veriler ve '007 GoldenEye' Arayüzü Yükleniyor...")

    # 1. ADIM: Verileri Çek
    try:
        url = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv'
        df = pd.read_csv(url)
    except Exception as e:
        print(f"Veri hatası: {e}")
        return

    # 2. ADIM: Siber Harita
    fig = go.Figure(data=go.Choropleth(
        locations=df['CODE'],
        z=[1] * len(df),
        text=df['COUNTRY'],
        colorscale=[[0, '#001a2c'], [1, '#00ccff']],
        autocolorscale=False,
        reversescale=False,
        marker_line_color='#00ffff',
        marker_line_width=0.5,
        showscale=False,
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))

    # 3. ADIM: GoldenEye Temalı Arayüz
    # Font ailesine dosya adını ve gerçek font adını ekledik.
    # Tarayıcı sırayla dener: Önce 007 GoldenEye, bulamazsa Courier New.
    font_ailesi = "'007 GoldenEye', '007Goldeneye', 'GoldenEye', 'Courier New', monospace"

    fig.update_layout(
        title={
            'text': "CLASSIFIED: AI GLOBAL INTEL",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 40, 'color': '#00ffff', 'family': font_ailesi}
        },
        paper_bgcolor='black',

        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='orthographic',
            showland=True,
            landcolor="black",
            showocean=True,
            oceancolor="#020408",
            showlakes=False,
            bgcolor='black'
        ),
        margin=dict(r=0, l=0, b=0, t=80),
        height=800,

        # Hover (Üzerine gelince çıkan) Etiket Stili
        hoverlabel=dict(
            bgcolor="black",
            font_size=18,
            font_family=font_ailesi,  # Aynı fontu burada da kullandık
            font_color="#00ffff",
            bordercolor="#00ffff"
        )
    )

    print("Arayüz render ediliyor... Erişim bekleniyor.")
    fig.show()


if __name__ == "__main__":
    dunya_kuresi_olustur()