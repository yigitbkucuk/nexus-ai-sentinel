from GoogleNews import GoogleNews
import pandas as pd

# Yapay Zeka Süper Güçleri
TIER_1_COUNTRIES = ['United States', 'China', 'United Kingdom', 'Russia', 'Japan', 'Germany', 'France', 'Israel',
                    'India', 'Canada', 'South Korea']

RISK_KEYWORDS = ['military', 'nuclear', 'weapon', 'war', 'army', 'kill', 'attack', 'hack', 'spy', 'surveillance',
                 'danger', 'threat', 'missile', 'soldier', 'death', 'virus', 'bioweapon', 'cyber', 'drone']


def analyze_risk(text):
    text_lower = text.lower()
    for word in RISK_KEYWORDS:
        if word in text_lower:
            return True
    return False


def get_country_news(country_name):
    # Hedefimiz temiz 12 haber. O yüzden ham olarak daha fazlasını çekiyoruz.
    limit = 25 if country_name in TIER_1_COUNTRIES else 15

    googlenews = GoogleNews(lang='en', period='7d')
    googlenews.clear()

    try:
        googlenews.search(f'Artificial Intelligence {country_name}')
        results = googlenews.result()

        # Eğer çok az haber varsa 2. sayfayı da zorla
        if len(results) < 10:
            googlenews.get_page(2)
            results = googlenews.result()

        clean_results = []
        seen_titles = set()

        if results:
            for item in results:
                title = item['title']
                if not title or title in seen_titles:
                    continue
                seen_titles.add(title)

                is_risky = analyze_risk(title) or analyze_risk(item.get('desc', ''))

                clean_results.append({
                    'title': title,
                    'desc': item.get('desc', ''),
                    'date': item.get('date', 'Recent'),
                    'link': item.get('link', '#'),
                    'media': item.get('media', 'Unknown Source'),
                    'risk': is_risky
                })

                # 15 tane temiz haber topladıysak duralım (Bize 12 lazım)
                if len(clean_results) >= 15:
                    break

            return clean_results
        return None
    except Exception as e:
        print(f"Haber hatası: {e}")
        return None


def get_geo_data():
    """Dünya haritası verilerini çeker ve eksikleri tamamlar."""
    url = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv'
    try:
        df = pd.read_csv(url)

        # EKSİK ÜLKELERİ TANIMLA (Manuel Enjeksiyon)
        missing_countries = [
            {'CODE': 'ESH', 'COUNTRY': 'Western Sahara', 'GDP (BILLIONS)': 0},
            {'CODE': 'GUF', 'COUNTRY': 'French Guiana', 'GDP (BILLIONS)': 0},
            {'CODE': 'PSE', 'COUNTRY': 'Palestine', 'GDP (BILLIONS)': 0}
        ]

        # Listede yoklarsa ekle
        rows_to_add = []
        for item in missing_countries:
            if item['COUNTRY'] not in df['COUNTRY'].values:
                rows_to_add.append(item)

        if rows_to_add:
            df = pd.concat([df, pd.DataFrame(rows_to_add)], ignore_index=True)

        return df
    except:
        # İnternet yoksa dummy data
        return pd.DataFrame({'CODE': ['TUR'], 'COUNTRY': ['Turkey']})


def get_country_coordinates(country_name):
    return None, None