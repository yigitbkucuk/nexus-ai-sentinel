import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
from news_backend import get_country_news, get_geo_data

# Verileri Yükle
df_geo = get_geo_data()

app = dash.Dash(__name__)
server = app.server


# --- YARDIMCI FONKSİYONLAR ---
def clean_text_for_bond(text):
    if not text: return ""
    replacements = {
        'ğ': 'g', 'Ğ': 'G', 'ş': 's', 'Ş': 'S', 'ı': 'i', 'İ': 'I',
        'ç': 'c', 'Ç': 'C', 'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O'
    }
    for tr, en in replacements.items():
        text = text.replace(tr, en)
    return text


def translate_content(text, target_lang):
    if target_lang == 'en': return text
    try:
        safe_text = text[:499] if len(text) > 500 else text
        return GoogleTranslator(source='auto', target=target_lang).translate(safe_text)
    except:
        return text


# --- MANUEL KOORDİNATLAR ---
MANUAL_COORDS = {
    'United States': (37.0902, -95.7129), 'China': (35.8617, 104.1954), 'Russia': (61.5240, 105.3188),
    'Turkey': (38.9637, 35.2433), 'Mexico': (23.6345, -102.5528), 'Canada': (56.1304, -106.3468),
    'Brazil': (-14.2350, -51.9253), 'Australia': (-25.2744, 133.7751), 'India': (20.5937, 78.9629),
    'United Kingdom': (55.3781, -3.4360), 'France': (46.2276, 2.2137), 'Germany': (51.1657, 10.4515),
    'Japan': (36.2048, 138.2529),

    # YENİ EKLENENLER
    'French Guiana': (3.9339, -53.1258),  # Güney Amerika'da
    'Palestine': (31.9522, 35.2332),  # Orta Doğu'da
    'Western Sahara': (24.2155, -12.8858)  # Afrika'da
}

def get_safe_coordinates(country_name):
    if country_name in MANUAL_COORDS: return MANUAL_COORDS[country_name]
    return (None, None)


# --- HARİTA OLUŞTURMA ---
def create_globe(selected_country=None, uirevision='constant', zoom_level=1.0):
    # Varsayılan: Mat Turkuaz (#004466)
    z_values = [0.3] * len(df_geo)

    if selected_country:
        match = df_geo.index[df_geo['COUNTRY'] == selected_country].tolist()
        if match:
            # Seçilen: Neon Cyan (1.0), Diğerleri: Mat Turkuaz (0.3)
            z_values = [0.3 if i != match[0] else 1.0 for i in range(len(df_geo))]

    fig = go.Figure(data=go.Choropleth(
        locations=df_geo['CODE'],
        z=z_values,
        text=df_geo['COUNTRY'],
        colorscale=[
            [0, '#004466'],
            [0.5, '#004466'],
            [0.6, '#00ffff'],
            [1, '#00ffff']
        ],
        autocolorscale=False, showscale=False,
        marker_line_color='#00cccc',
        marker_line_width=0.5,
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))

    font_ailesi = "'GoldenEye', 'Share Tech Mono', monospace"

    fig.update_layout(
        title={
            'text': "NEXUS: GLOBAL AI SENTINEL",
            'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',
            'font': {'size': 32, 'color': '#00ffff', 'family': font_ailesi, 'shadow': '0px 0px 10px #00ffff'}
        },
        paper_bgcolor='black',
        clickmode='event+select',
        uirevision=uirevision,

        geo=dict(
            showframe=False, showcoastlines=False,
            projection_type='orthographic',
            projection_scale=zoom_level,

            showland=True, landcolor="#002233",  # Verisiz yerler
            showocean=True, oceancolor="black",  # SİYAH OKYANUS (ONAYLANDI)

            bgcolor='black'
        ),
        margin=dict(r=0, l=0, b=0, t=80),
        autosize=True,
        hoverlabel=dict(bgcolor="black", font_size=18, font_family=font_ailesi, font_color="#00ffff")
    )
    return fig


app.layout = html.Div(className='container', children=[

    html.Div(id='map-container', className='map-container', style={'width': '100%'}, children=[
        dcc.Graph(
            id='globe-graph',
            figure=create_globe(),
            config={'displayModeBar': False, 'scrollZoom': True, 'responsive': True},
            style={'height': '100vh', 'width': '100%'}
        ),
        # ZOOM BUTONLARI
        html.Div(className='zoom-controls', children=[
            html.Button('+', id='zoom-in', className='zoom-btn'),
            html.Button('-', id='zoom-out', className='zoom-btn'),
        ])
    ]),

    html.Div(id='news-panel', className='news-panel', style={'width': '0%', 'opacity': 0}, children=[
        html.Div(className='control-header', children=[
            html.Div(className='lang-box', children=[
                dcc.Dropdown(
                    id='language-selector',
                    options=[
                        {'label': 'ENGLISH (ORIGINAL)', 'value': 'en'}, {'label': 'TURKISH (TÜRKÇE)', 'value': 'tr'},
                        {'label': 'SPANISH (ESPAÑOL)', 'value': 'es'}, {'label': 'GERMAN (DEUTSCH)', 'value': 'de'},
                        {'label': 'RUSSIAN (РУССКИЙ)', 'value': 'ru'}, {'label': 'FRENCH (FRANÇAIS)', 'value': 'fr'},
                    ],
                    value='en', clearable=False, searchable=False, placeholder="SELECT LANGUAGE"
                )
            ]),
            html.Button(["CLOSE ", html.Span("[", className="punct-red"), "X", html.Span("]", className="punct-red")],
                        id='close-btn', className='close-btn'),
        ]),

        # SCROLL İÇİN ÖNEMLİ: Panel içeriği burada
        dcc.Loading(
            id="loading-news", type="cube", color="#00ffff",
            parent_style={'flex': '1', 'position': 'relative', 'display': 'flex', 'flexDirection': 'column',
                          'height': '100%'},
            children=html.Div(id='news-content', className='panel-content-scroll')
        )
    ]),

    dcc.Store(id='selected-country-store'),
    dcc.Store(id='zoom-level-store', data=1.0)
])


@app.callback(
    [Output('map-container', 'style'),
     Output('news-panel', 'style'),
     Output('news-content', 'children'),
     Output('selected-country-store', 'data'),
     Output('globe-graph', 'figure'),
     Output('globe-graph', 'clickData'),
     Output('zoom-level-store', 'data')],
    [Input('globe-graph', 'clickData'),
     Input('close-btn', 'n_clicks'),
     Input('language-selector', 'value'),
     Input('zoom-in', 'n_clicks'),
     Input('zoom-out', 'n_clicks')],
    [State('selected-country-store', 'data'),
     State('globe-graph', 'figure'),
     State('zoom-level-store', 'data')]
)
def update_situation_room(clickData, close_clicks, lang_code, zoom_in, zoom_out,
                          current_country, current_fig, current_zoom):
    triggered_id = ctx.triggered_id

    # --- ZOOM MANTIĞI ---
    if triggered_id == 'zoom-in':
        new_zoom = min(current_zoom + 0.2, 3.0)
        fig = go.Figure(current_fig)
        fig.update_layout(geo=dict(projection_scale=new_zoom), uirevision='constant')
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, fig, dash.no_update, new_zoom

    if triggered_id == 'zoom-out':
        new_zoom = max(current_zoom - 0.2, 0.5)
        fig = go.Figure(current_fig)
        fig.update_layout(geo=dict(projection_scale=new_zoom), uirevision='constant')
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, fig, dash.no_update, new_zoom

    # 1. KAPATMA
    if triggered_id == 'close-btn' or (triggered_id is None and clickData is None):
        if current_fig:
            fig = go.Figure(current_fig)
            fig.update_traces(z=[0.3] * len(df_geo))
            return {'width': '100%'}, {'width': '0%', 'opacity': 0}, [], None, fig, None, current_zoom
        else:
            return {'width': '100%'}, {'width': '0%', 'opacity': 0}, [], None, create_globe(
                zoom_level=current_zoom), None, current_zoom

    # 2. AÇMA
    country_name = None
    if triggered_id == 'globe-graph' and clickData:
        country_name = clickData['points'][0]['text']
    elif triggered_id == 'language-selector' and current_country:
        country_name = current_country

    if country_name is None:
        return {'width': '100%'}, {'width': '0%', 'opacity': 0}, [], None, dash.no_update, dash.no_update, current_zoom

    # Haberleri Çek
    news_data = get_country_news(country_name)
    panel_content = []

    display_country = country_name.upper()
    if lang_code != 'en':
        translated_country = translate_content(country_name, lang_code).upper()
        display_country = clean_text_for_bond(translated_country)

    panel_content.append(
        html.Div(["INTEL", html.Span(":", className="punct"), f" {display_country}"], className='panel-header'))

    if news_data:
        # MAX 12 HABER KURALI
        visible_news = news_data[:12]

        for news in visible_news:
            risk_label = []
            item_class = 'news-item-safe'
            title_class = 'news-title title-safe'

            if news['risk']:
                item_class = 'news-item-critical'
                title_class = 'news-title title-critical'
                risk_text = "CRITICAL"
                if lang_code != 'en':
                    risk_text = clean_text_for_bond(translate_content("CRITICAL", lang_code).upper())
                risk_label = [html.Span(" [", className="punct-red"), risk_text, html.Span("]", className="punct-red")]

            raw_title = news['title'];
            raw_desc = news['desc']
            if lang_code != 'en':
                raw_title = translate_content(news['title'], lang_code)
                raw_desc = translate_content(news['desc'], lang_code)

            translate_link = f"https://translate.google.com/translate?sl=auto&tl={lang_code}&u={news['link']}"
            item_html = html.A(href=translate_link, target="_blank", style={'textDecoration': 'none'}, children=
            html.Div(className=item_class, children=[
                html.Div([clean_text_for_bond(raw_title)] + risk_label, className=title_class),
                html.Div(raw_desc, className='news-desc'),
                html.Div(f"SOURCE: {news['media']} | {news['date']}", className='news-meta')
            ]))
            panel_content.append(item_html)

    else:
        no_data_title = "NO DATA DETECTED"
        no_data_desc = f"No recent AI intelligence found for {country_name}."
        if lang_code != 'en':
            no_data_title = clean_text_for_bond(translate_content(no_data_title, lang_code))
            no_data_desc = translate_content(no_data_desc, lang_code)
        panel_content.append(html.Div(className='news-item-safe', children=[
            html.Div(no_data_title, className='news-title', style={'color': 'gray'}),
            html.Div(no_data_desc, className='news-desc')
        ]))

    new_fig = go.Figure(current_fig) if current_fig else create_globe(zoom_level=current_zoom)
    z_values = [0.3] * len(df_geo)
    match = df_geo.index[df_geo['COUNTRY'] == country_name].tolist()
    if match: z_values = [0.3 if i != match[0] else 1.0 for i in range(len(df_geo))]
    new_fig.update_traces(z=z_values)
    new_fig.update_layout(uirevision='constant')

    return {'width': '60%'}, {'width': '40%',
                              'opacity': 1}, panel_content, country_name, new_fig, dash.no_update, current_zoom


if __name__ == '__main__':
    print("NEXUS: GLOBAL AI SENTINEL (STABLE 12-MAX) BAŞLATILIYOR...")
    app.run(debug=True, use_reloader=False, dev_tools_ui=False)