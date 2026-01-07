import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from GoogleNews import GoogleNews
import datetime

# --- 1. AYARLAR VE VERİ HAZIRLIĞI ---
# Google News servisini başlat
googlenews = GoogleNews(lang='en', period='7d')  # Son 7 gün, İngilizce sonuçlar

# Ülke verilerini çek
url = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv'
try:
    df_geo = pd.read_csv(url)
except:
    # İnternet yoksa dummy data
    df_geo = pd.DataFrame({'CODE': ['TUR', 'USA'], 'COUNTRY': ['Turkey', 'United States']})

# Dash Uygulamasını Başlat
app = dash.Dash(__name__)
server = app.server


# --- 2. FONKSİYONLAR ---

def get_news_for_country(country_name):
    """Seçilen ülke için son 7 günün AI haberlerini getirir."""
    try:
        googlenews.clear()
        # Arama sorgusu: "Artificial Intelligence" + Ülke Adı
        googlenews.search(f'Artificial Intelligence {country_name}')
        results = googlenews.result()

        if not results:
            return None

        # İlk 5 haberi al, gereksizleri ele
        news_items = []
        for item in results[:5]:
            # Tarih formatı bazen karışık gelebilir, olduğu gibi alıyoruz
            news_items.append({
                'title': item['title'],
                'desc': item['desc'],
                'date': item['date'],
                'link': item['link'],
                'media': item['media']
            })
        return news_items
    except Exception as e:
        print(f"Haber çekme hatası: {e}")
        return None


def create_globe():
    """3D Küreyi oluşturur."""
    font_ailesi = "'007 GoldenEye', '007Goldeneye', 'GoldenEye', 'Courier New', monospace"

    fig = go.Figure(data=go.Choropleth(
        locations=df_geo['CODE'],
        z=[1] * len(df_geo),
        text=df_geo['COUNTRY'],
        colorscale=[[0, '#001a2c'], [1, '#00ccff']],
        autocolorscale=False,
        reversescale=False,
        marker_line_color='#00ffff',
        marker_line_width=0.5,
        showscale=False,
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))

    fig.update_layout(
        paper_bgcolor='black',
        clickmode='event+select',  # Tıklamayı algıla
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='orthographic',
            showland=True,
            landcolor="black",
            showocean=True,
            oceancolor="#020408",
            bgcolor='black'
        ),
        margin=dict(r=0, l=0, b=0, t=0),
        height=800,  # Başlangıç yüksekliği
        hoverlabel=dict(
            bgcolor="black",
            font_size=18,
            font_family=font_ailesi,
            font_color="#00ffff",
            bordercolor="#00ffff"
        )
    )
    return fig


# --- 3. ARAYÜZ (LAYOUT) ---
# CSS ile animasyon ve font ayarları
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Situation Room</title>
        {%favicon%}
        {%css%}
        <style>
            @font-face {
                font-family: 'GoldenEye';
                src: local('007 GoldenEye'), local('007Goldeneye');
            }
            body {
                background-color: black;
                margin: 0;
                overflow: hidden; /* Scroll barı gizle */
                font-family: 'GoldenEye', 'Courier New', monospace;
            }
            .container {
                display: flex;
                width: 100vw;
                height: 100vh;
                transition: all 0.5s ease-in-out;
            }
            .map-container {
                width: 100%;
                transition: width 0.8s cubic-bezier(0.25, 1, 0.5, 1);
            }
            .news-panel {
                width: 0%;
                background-color: #050505;
                border-left: 2px solid #00ffff;
                height: 100vh;
                overflow-y: auto;
                transition: width 0.8s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.5s ease;
                opacity: 0;
                padding: 0;
                box-shadow: -10px 0px 30px rgba(0, 255, 255, 0.1);
            }
            /* Haber Kartları Stili */
            .news-item {
                border-bottom: 1px solid #004444;
                padding: 20px;
                transition: background 0.3s;
                cursor: pointer;
            }
            .news-item:hover {
                background-color: #001111;
                border-left: 4px solid #00ffff;
            }
            .news-title {
                color: #00ffff;
                font-size: 1.2em;
                margin-bottom: 5px;
                text-transform: uppercase;
                text-shadow: 0 0 5px rgba(0,255,255,0.5);
            }
            .news-desc {
                color: #aaaaaa;
                font-size: 0.9em;
                font-family: 'Courier New', monospace; /* Okunabilirlik için */
            }
            .news-meta {
                color: #ff0000; /* Kritik tarih kırmızı */
                font-size: 0.8em;
                margin-top: 10px;
                text-align: right;
            }
            .panel-header {
                color: #00ffff;
                text-align: center;
                padding: 20px;
                font-size: 2em;
                border-bottom: 2px solid #00ffff;
                background: #001a2c;
            }
            /* Scrollbar tasarımı */
            ::-webkit-scrollbar { width: 8px; }
            ::-webkit-scrollbar-track { background: black; }
            ::-webkit-scrollbar-thumb { background: #004444; }
            ::-webkit-scrollbar-thumb:hover { background: #00ffff; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(className='container', children=[
    # SOL TARAF: KÜRE
    html.Div(id='map-container', className='map-container', children=[
        dcc.Graph(
            id='globe-graph',
            figure=create_globe(),
            config={'displayModeBar': False, 'scrollZoom': True},
            style={'height': '100vh'}
        )
    ]),

    # SAĞ TARAF: HABER PANELİ
    html.Div(id='news-panel', className='news-panel', children=[
        html.Div(id='news-content')
    ])
])


# --- 4. ETKİLEŞİM (CALLBACKS) ---

@app.callback(
    [Output('map-container', 'style'),
     Output('news-panel', 'style'),
     Output('news-content', 'children')],
    [Input('globe-graph', 'clickData')]
)
def display_click_data(clickData):
    # Başlangıç durumu (Tıklama yoksa)
    if clickData is None:
        return {'width': '100%'}, {'width': '0%', 'opacity': 0}, []

    # Tıklanan ülkenin kodunu ve ismini al
    country_name = clickData['points'][0]['text']

    print(f"Analiz ediliyor: {country_name}")

    # Haberleri çek
    news_data = get_news_for_country(country_name)

    # Panel İçeriğini Oluştur
    panel_content = []

    # Başlık
    panel_content.append(html.Div(f"INTEL: {country_name.upper()}", className='panel-header'))

    if news_data:
        for news in news_data:
            # Google Translate Linki Oluşturma
            # Kullanıcı tıkladığında haberi İngilizceye çevrilmiş arayüzde görecek.
            orijinal_link = news['link']
            translate_link = f"https://translate.google.com/translate?sl=auto&tl=en&u={orijinal_link}"

            item_html = html.A(
                href=translate_link,
                target="_blank",  # Yeni sekmede aç
                style={'textDecoration': 'none'},
                children=html.Div(className='news-item', children=[
                    html.Div(news['title'], className='news-title'),
                    html.Div(news['desc'], className='news-desc'),
                    html.Div(f"SOURCE: {news['media']} | DATE: {news['date']}", className='news-meta')
                ])
            )
            panel_content.append(item_html)
    else:
        # Haber bulunamazsa
        panel_content.append(html.Div(className='news-item', children=[
            html.Div("NO RECENT AI ACTIVITY DETECTED", className='news-title', style={'color': 'red'}),
            html.Div("Target country has no significant AI news in the last 7 days.", className='news-desc')
        ]))

    # Animasyon için stilleri güncelle: Harita %65, Haberler %35
    map_style = {'width': '65%'}
    panel_style = {'width': '35%', 'opacity': 1, 'padding': '0'}

    return map_style, panel_style, panel_content


# --- 5. UYGULAMAYI BAŞLAT ---
if __name__ == '__main__':
    print("SITUATION ROOM BAŞLATILIYOR...")
    print("Erişim Adresi: http://127.0.0.1:8050/")
    # app.run_server yerine app.run kullanıyoruz
    app.run(debug=True, use_reloader=False)