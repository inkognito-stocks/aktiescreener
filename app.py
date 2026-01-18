import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup

# --- IMPORT FRÅN MARKET_DATA.PY ---
try:
    from market_data import (
        SE_LARGE_CAP, 
        SE_MID_CAP, 
        SE_SMALL_CAP, 
        US_ALL_STAR, 
        CA_ALL_STAR
    )
except ImportError:
    st.error("⚠️ Hittade inte 'market_data.py'. Se till att filen ligger i samma mapp!")
    # Fallback-tomma listor så appen inte kraschar
    SE_LARGE_CAP, SE_MID_CAP, SE_SMALL_CAP, US_ALL_STAR, CA_ALL_STAR = [], [], [], [], []

# --- ORGANISERA LISTORNA ---
# Vi bygger ihop strukturen här så att menyn i appen fungerar snyggt
ticker_lists = {
    "Sverige 🇸🇪": {
        "Large Cap": SE_LARGE_CAP,
        "Mid Cap": SE_MID_CAP,
        "Small Cap": SE_SMALL_CAP
    },
    "USA 🇺🇸": {
        "S&P 100 / All Star": US_ALL_STAR
    },
    "Kanada 🇨🇦": {
        "TSX Top 40": CA_ALL_STAR
    }
}

# --- Inställningar ---
st.set_page_config(page_title="AktieScreener Global", layout="wide")

# --- Batch Download Functions ---

@st.cache_data(ttl=2700)  # Cache i 45 minuter
def download_batch_data(tickers_batch, batch_num, total_batches):
    """
    Laddar ner data för en batch av tickers samtidigt.
    """
    try:
        data = yf.download(
            tickers_batch,
            period="1mo",
            group_by='ticker',
            threads=True,
            progress=False
        )
        time.sleep(1)  # Rate limiting för att vara snäll mot Yahoo
        return data
    except Exception as e:
        return None

def calculate_streak(prices):
    """Beräknar antal dagar i rad aktien gått upp eller ner"""
    if len(prices) < 2:
        return 0
    
    streak = 0
    for i in range(len(prices) - 1, 0, -1):
        today = prices.iloc[i]
        yesterday = prices.iloc[i-1]
        
        if pd.isna(today) or pd.isna(yesterday):
            break
            
        if today > yesterday:
            if streak < 0: break
            streak += 1
        elif today < yesterday:
            if streak > 0: break
            streak -= 1
        else:
            break
    return streak

def get_market_from_ticker(ticker):
    """Identifierar marknad baserat på ticker-suffix"""
    if ticker.endswith('.ST'):
        return 'Sverige 🇸🇪'
    elif ticker.endswith('.TO') or ticker.endswith('.V') or ticker.endswith('.CN'):
        return 'Kanada 🇨🇦'
    else:
        return 'USA 🇺🇸'

def check_yf_news(ticker_symbol, keywords_list, days_back=30):
    """
    Söker i Yahoo Finance press releases och nyheter.
    Används för USA och Kanada.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        news = stock.news
        
        if not news:
            return None
        
        cutoff_date = datetime.now()
        
        for article in news:
            content = article.get('content', article)
            
            pub_timestamp = content.get('providerPublishTime', article.get('providerPublishTime', 0))
            if pub_timestamp == 0:
                pub_date_str = content.get('pubDate', '')
                if pub_date_str:
                    try:
                        pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                        pub_date = pub_date.replace(tzinfo=None)
                    except:
                        continue
                else:
                    continue
            else:
                pub_date = datetime.fromtimestamp(pub_timestamp)
            
            days_diff = (cutoff_date - pub_date).days
            if days_diff > days_back or days_diff < 0:
                continue
            
            title = content.get('title', '').lower()
            summary = content.get('summary', '').lower()
            search_text = f"{title} {summary}"
            
            for keyword in keywords_list:
                if keyword.lower() in search_text:
                    return {
                        'title': content.get('title', 'No title'),
                        'link': content.get('canonicalUrl', {}).get('url', ''),
                        'publisher': content.get('provider', {}).get('displayName', 'Unknown'),
                        'date': pub_date
                    }
        return None
    except Exception as e:
        return None

@st.cache_data(ttl=7200)  # Cache i 2 timmar (snabbare, nyheter ändras inte så ofta)
def check_placera_news(ticker_symbol, keywords_list, days_back=30):
    """
    Söker på Placera.se med enkel sökstrategi.
    """
    try:
        # Ta bort .ST och formatera
        clean_ticker = ticker_symbol.replace('.ST', '').replace('-', '')
        
        # KOMPLETT mappning: ticker -> Placera-bolagsnamn
        # Skapad från market_data.py för alla svenska Large/Mid/Small Cap
        company_names = {
            # Large Cap - Stora välkända bolag
            'AAK': 'aak', 'ABB': 'abb', 'ADDB': 'addtech', 'ALFA': 'alfa-laval',
            'ALIFB': 'alimak', 'ASSAB': 'assa-abloy', 'ATCOA': 'atlas-copco',
            'ATCOB': 'atlas-copco', 'AXFO': 'axfood', 'AZA': 'azelio', 
            'AZN': 'astrazeneca', 'BALDB': 'balder', 'BEIJB': 'beijer-ref',
            'BETSB': 'betsson', 'BILL': 'billerud', 'BIOT': 'biotage',
            'BOL': 'boliden', 'BRAV': 'bravida', 'BURE': 'bure',
            'CAST': 'castellum', 'CIBUS': 'cibus', 'CLASB': 'clas-ohlson',
            'DIOS': 'dios', 'DOM': 'dometic', 'EKTAB': 'ekta',
            'ELUXB': 'electrolux', 'ELUXPROFB': 'electrolux-professional',
            'EPIA': 'epiroc', 'EPIB': 'epiroc', 'ERICA': 'ericsson',
            'ERICB': 'ericsson', 'ESSITYA': 'essity', 'ESSITYB': 'essity',
            'EVO': 'evolution', 'FABG': 'fabege', 'FOIB': 'fortum',
            'FPARA': 'fastpartner', 'GETIB': 'getinge', 'HEBAB': 'heba',
            'HEM': 'hemfosa', 'HEXAB': 'hexagon', 'HMB': 'h-m',
            'HOLMA': 'holmen', 'HOLMB': 'holmen', 'HPOLB': 'hexpol',
            'HUFA': 'hufvudstaden', 'HUFC': 'hufvudstaden',
            'HUSQA': 'husqvarna', 'HUSQB': 'husqvarna', 'INDT': 'indutrade',
            'INDUA': 'industrivarden', 'INDUC': 'industrivarden',
            'INTRUM': 'intrum', 'INVEA': 'investor', 'INVEB': 'investor',
            'JM': 'jm', 'KINVA': 'kinnevik', 'KINVB': 'kinnevik',
            'LAGRB': 'lagercrantz', 'LATOB': 'latour', 'LIFCOB': 'lifco',
            'LOOMIS': 'loomis', 'LUNDB': 'lundberg', 'MEKO': 'mekonomen',
            'MIPS': 'mips', 'MTGB': 'mtg', 'MYCR': 'mycronics',
            'NCCA': 'ncc', 'NCCB': 'ncc', 'NDASE': 'nda', 'NIBEB': 'nibe',
            'NOLAB': 'nolato', 'NP3': 'np3', 'NYF': 'new-wave',
            'OX2': 'ox2', 'PNDX': 'pandox', 'PEABB': 'peab',
            'PLATB': 'platzer', 'RATOA': 'ratos', 'RATOB': 'ratos',
            'SAABB': 'saab', 'SAGAA': 'sagax', 'SAGAB': 'sagax',
            'SAGAD': 'sagax', 'SAND': 'sandvik', 'SAVE': 'samhallsbyggnadsbolaget',
            'SBBB': 'sbb', 'SBBD': 'sbb', 'SCAA': 'sca', 'SCAB': 'sca',
            'SEBA': 'seb', 'SEBC': 'seb', 'SECTB': 'sector-alarm',
            'SF': 'stillfront', 'SHBA': 'handelsbanken', 'SHBB': 'handelsbanken',
            'SINCH': 'sinch', 'SKAB': 'skanska', 'SKFA': 'skf', 'SKFB': 'skf',
            'SSABA': 'ssab', 'SSABB': 'ssab', 'STEA': 'storskogen',
            'STER': 'storskogen', 'STORYB': 'storytel', 'SWECA': 'sweco',
            'SWECB': 'sweco', 'SWEDA': 'swedbank', 'SYSR': 'systemair',
            'TEL2A': 'tele2', 'TEL2B': 'tele2', 'TELIA': 'telia',
            'THULE': 'thule', 'TRELB': 'trelleborg', 'TROAX': 'troax',
            'VBGB': 'vbg', 'VITR': 'vitrolife', 'VOLVA': 'volvo',
            'VOLVB': 'volvo', 'VPLAYB': 'viaplay', 'WALLB': 'wallenstam',
            'WIHL': 'wihlborgs', 'WISC': 'wesc',
            
            # Mid Cap - Viktiga medelstora bolag
            'ACAD': 'academedia', 'ADAPT': 'adapta', 'AFRY': 'afry',
            'ALLEI': 'allego', 'ALLIGOB': 'alligo', 'AMBEA': 'ambea',
            'ANEX': 'annexet', 'ANODB': 'anod', 'AQ': 'aq', 'ARJOB': 'arjo',
            'ARPL': 'aroundtown', 'ATRLJB': 'atrium-ljungberg', 'ATT': 'attendo',
            'BACTIB': 'bactiguard', 'BALCO': 'balco', 'BELE': 'bele',
            'BESQ': 'besqab', 'BILIA': 'bilia', 'BIOAB': 'bioarctic',
            'BMAX': 'betsson', 'BONES': 'ependion', 'BOOZT': 'boozt',
            'BORG': 'borg', 'BTSB': 'bts', 'BULTEN': 'bulten',
            'CALL': 'callino', 'CAMX': 'camurus', 'CATE': 'cint',
            'CATA': 'catena', 'CATB': 'catena', 'COIC': 'coeli',
            'COOR': 'coor', 'CREDA': 'credento', 'CTEK': 'ctek',
            'CTM': 'cantargia', 'CTT': 'ctt-systems', 'DUNI': 'duni',
            'DUST': 'dustin', 'EAST': 'eastnine', 'ELANB': 'elanders',
            'ELTEL': 'eltel', 'ENRO': 'ework', 'EO': 'elekta',
            'EWRK': 'ework', 'FAG': 'fagerhult', 'FAST': 'fastighets',
            'FMATT': 'fortnox', 'FNM': 'fenix-outdoor', 'G5EN': 'g5-entertainment',
            'GARO': 'garo', 'GIGSEK': 'gigger', 'GRNG': 'grange',
            'HANZA': 'hanza', 'HHO': 'hoist', 'HOFI': 'homeq',
            'HTRO': 'hydro66', 'HUMBLE': 'humble', 'IARB': 'iar',
            'INFREA': 'infrea', 'INWIDO': 'inwido', 'ITABB': 'itab',
            'JOHNB': 'john-mattson', 'KARC': 'karo', 'KFASTB': 'kungsleden',
            'KINDSDB': 'kindred', 'KNOW': 'knowit', 'LAMMB': 'lammhults',
            'LIME': 'lime', 'LINC': 'lindab', 'MCAP': 'midcap',
            'MENT': 'mentice', 'MIDWA': 'midwinter', 'MIDWB': 'midwinter',
            'MMGRB': 'momentum', 'MOB': 'moberg', 'MSONA': 'malmbergs',
            'MSONB': 'malmbergs', 'MTRS': 'matterport', 'NCAB': 'ncab',
            'NEWAB': 'newbody', 'NGS': 'ngs', 'NILB': 'nilorn',
            'NMAN': 'newman', 'NOTE': 'note', 'OASM': 'oresund',
            'OEMB': 'oem', 'ORE': 'orexo', 'PACT': 'pactum',
            'PIERCE': 'pierce', 'PRICB': 'price', 'PROB': 'probi',
            'PROFB': 'profoto', 'QLEALA': 'qlinea', 'RAYB': 'raykola',
            'READ': 'readly', 'REJLB': 'rejlers', 'RESURS': 'resurs',
            'RVRC': 'rovio', 'SCST': 'scandi', 'SDIPB': 'sdip',
            'SENS': 'sensec', 'SIVE': 'sivers', 'SLPB': 'samhall',
            'SOBI': 'sobi', 'SRNKEB': 'sevenday', 'STWK': 'stillwell',
            'SVEDB': 'svedbergs', 'TETY': 'techtank', 'TRAD': 'tradedoubler',
            'TRAN': 'transcom', 'TRIANB': 'trianon', 'VICO': 'vicore',
            'VIMIAN': 'vimian', 'VNV': 'vnv', 'VOLO': 'volati',
            'WAY': 'waystream', 'XANOB': 'xano', 'XBRANE': 'xbrane',
            'XVIVO': 'xvivo'
        }
        
        # Få bolagsnamn för sökning
        search_name = company_names.get(clean_ticker.upper())
        
        if not search_name:
            # Fallback: använd första delen av tickern
            search_name = clean_ticker[:4].lower()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Strategi: Sök brett efter bolagsnamn + något nyckelord
        # Ta det mest relevanta nyckelordet för initial sökning
        primary_keywords = ['resultat', 'vinstvarning', 'uppdatering', 'warning', 'update']
        
        for primary_keyword in primary_keywords:
            # Försök söka på Placera
            search_url = f"https://www.placera.se/search?query={search_name}+{primary_keyword}"
            
            try:
                response = requests.get(search_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Hitta alla länkar
                    all_links = soup.find_all('a', href=True)
                    
                    for link in all_links[:40]:
                        href = link.get('href', '')
                        link_text = link.get_text(strip=True)
                        
                        # Måste vara ett pressmeddelande
                        if '/pressmeddelanden/' not in href:
                            continue
                        
                        # Måste innehålla bolagsnamn
                        if search_name not in href.lower() and search_name not in link_text.lower():
                            continue
                        
                        # Kolla alla nyckelord
                        link_text_lower = link_text.lower()
                        for keyword in keywords_list:
                            if keyword.lower() in link_text_lower:
                                # Bygg fullständig URL
                                full_url = href if href.startswith('http') else f"https://www.placera.se{href}"
                                
                                return {
                                    'title': link_text,
                                    'link': full_url,
                                    'publisher': 'Placera',
                                    'date': datetime.now()
                                }
            except:
                continue
        
        return None
        
    except Exception as e:
        return None

def check_earnings_date(ticker_symbol, days_range=30):
    """Kontrollerar om rapport ska släppas inom X dagar eller släpptes nyligen"""
    try:
        stock = yf.Ticker(ticker_symbol)
        calendar = stock.calendar
        
        if calendar is not None and 'Earnings Date' in calendar:
            earnings_date = calendar['Earnings Date']
            if isinstance(earnings_date, pd.Series) and len(earnings_date) > 0:
                earnings_date = earnings_date.iloc[0]
            
            if pd.notna(earnings_date):
                today = datetime.now()
                days_diff = (earnings_date - today).days
                
                if -days_range <= days_diff <= days_range:
                    if days_diff < 0:
                        return f"Släpptes för {abs(days_diff)} dagar sedan"
                    else:
                        return f"Släpps om {days_diff} dagar"
        return None
    except:
        return None

def process_batch_results(data, tickers_in_batch, price_range, streak_filter, 
                          check_vinstvarning, check_rapport, check_insider, check_ny_vd, 
                          use_price_change, price_change_period, price_change_range, 
                          volume_threshold):
    """
    Processar resultatet från en batch-download
    """
    results = []
    
    for ticker in tickers_in_batch:
        try:
            # Hämta data för denna ticker
            if len(tickers_in_batch) == 1:
                ticker_data = data
            else:
                if ticker not in data.columns.levels[0]:
                    continue
                ticker_data = data[ticker]
            
            # Kontrollera att vi har Close data
            if 'Close' not in ticker_data.columns:
                continue
                
            closes = ticker_data['Close'].dropna()
            if len(closes) < 2:
                continue
            
            # Senaste pris
            price = float(closes.iloc[-1])
            
            # Pris-filter
            if not (price_range[0] <= price <= price_range[1]):
                continue
            
            # Beräkna streak
            streak = calculate_streak(closes)
            
            # Streak-filter
            min_streak, max_streak = streak_filter
            if not (min_streak <= streak <= max_streak):
                continue
            
            # Beräkna volym alltid (för att visa relativ volym)
            relative_volume = None
            if 'Volume' in ticker_data.columns:
                volumes = ticker_data['Volume'].dropna()
                
                if len(volumes) > 90:
                    # Genomsnittlig volym över 90 dagar (baseline/snitt)
                    avg_volume = float(volumes.iloc[-91:-1].mean())
                    
                    # Senaste dagens volym
                    recent_volume = float(volumes.iloc[-1])
                    
                    # Relativ volym (1.0 = normal, 1.5 = 50% mer än snittet, 0.5 = 50% lägre än snittet)
                    if avg_volume > 0:
                        relative_volume = recent_volume / avg_volume
            
            # Prisförändring-filter
            price_change_pct = None
            if use_price_change:
                # Bestäm hur många dagar tillbaka baserat på period
                period_map = {
                    "1 dag": 1,
                    "1 vecka": 5,
                    "1 månad": 20,
                    "3 månader": 60
                }
                days_back = period_map.get(price_change_period, 1)
                
                # Beräkna prisförändring
                if len(closes) > days_back:
                    old_price = float(closes.iloc[-days_back-1])
                    current_price = float(closes.iloc[-1])
                    price_change_pct = ((current_price - old_price) / old_price) * 100
                    
                    # Filtrera baserat på användarens intervall
                    min_change, max_change = price_change_range
                    if not (min_change <= price_change_pct <= max_change):
                        continue
                    
                    # Filtrera på relativ volym om aktiverat
                    if volume_threshold is not None and relative_volume is not None:
                        if (relative_volume * 100) < volume_threshold:
                            continue
                else:
                    # Inte tillräckligt med historik, skippa denna aktie
                    continue
            
            
            # --- HÄNDELSE-FILTRERING (HYBRID: Cision för SE, Yahoo för US/CA) ---
            news_hits = []
            is_swedish = ticker.endswith('.ST')
            
            # Tillfälligt: Använd Yahoo Finance för ALLA marknader (enklare och fungerar)
            # Placera-scraping är opålitlig, väntar på Börsdata API
            news_checker = check_yf_news
            
            if check_vinstvarning:
                warning_keywords = []
                if is_swedish:
                    warning_keywords = [
                        'vinstvarning', 'sänker prognos', 'nedjusterar', 'varning',
                        'nedrevidera', 'justerar ned', 'sänker',
                        'resultatuppdatering', 'reviderad prognos', 'omvärderar',
                        'försämrad', 'svagare', 'lägre än väntat', 'utmaning',
                        'preliminärt resultat', 'handelsuppdatering',
                        'uppdatering av finansiella mål', 'prognosjustering',
                        'results update', 'uppdatering för', 'resultat för',
                        'förväntas uppgå', 'rörelseresultat', 'ebit'
                    ]
                else:
                    warning_keywords = [
                        'profit warning', 'lowers guidance', 'downgrade', 
                        'misses', 'weak results', 'below expectations',
                        'result update', 'revised guidance', 'challenges',
                        'trading update', 'preliminary results',
                        'guidance update', 'financial update',
                        'results update', 'expected to amount', 'operating income'
                    ]
                
                news_hit = news_checker(ticker, warning_keywords, days_back=30)
                if news_hit:
                    news_hits.append(f"⚠️ Vinstvarning")
                else:
                    continue  # Filter aktivt men ingen träff -> hoppa över
            
            if check_rapport:
                earnings_info = check_earnings_date(ticker, days_range=30)
                if earnings_info:
                    news_hits.append(f"📊 {earnings_info}")
                else:
                    # Fallback på nyhetssök om kalender saknas
                    if is_swedish:
                        report_keywords = ['kvartalsrapport', 'delårsrapport', 'bokslutskommuniké', 'Q1', 'Q2', 'Q3', 'Q4']
                    else:
                        report_keywords = ['earnings', 'quarterly results', 'reports']
                    
                    news_hit = news_checker(ticker, report_keywords, days_back=30)
                    if news_hit:
                        news_hits.append(f"📊 Rapport")
            
            if check_insider:
                if is_swedish:
                    insider_keywords = ['insider', 'köper', 'säljer', 'förvärvat', 'avyttrat', 'insiderhandel']
                else:
                    insider_keywords = ['insider buying', 'insider selling', 'director bought', 'CEO bought']
                
                news_hit = news_checker(ticker, insider_keywords, days_back=30)
                if news_hit:
                    news_hits.append(f"👤 Insider")
            
            if check_ny_vd:
                if is_swedish:
                    vd_keywords = ['ny vd', 'vd avgår', 'tillträder som vd', 'ny ceo', 'ledningsändring', 'ny styrelse']
                else:
                    vd_keywords = ['new ceo', 'ceo resigns', 'ceo appointed', 'management change']
                
                news_hit = news_checker(ticker, vd_keywords, days_back=60)
                if news_hit:
                    news_hits.append(f"🎯 Ledning")
            
            # Avgör valuta
            market = get_market_from_ticker(ticker)
            currency = "SEK" if market == 'Sverige 🇸🇪' else ("CAD" if market == 'Kanada 🇨🇦' else "USD")
            
            news_text = " | ".join(news_hits) if news_hits else "Ingen händelse"
            
            # Bygg resultat-dictionary
            result_dict = {
                "Ticker": ticker,
                "Marknad": market,
                f"Pris ({currency})": round(price, 2),
                "Trend (Dagar)": streak,
            }
            
            # Lägg till relativ volym alltid (om tillgängligt)
            if relative_volume is not None:
                # Formatera som 1.5 för 50% mer, 0.5 för 50% lägre
                result_dict["Relativ Volym"] = f"{relative_volume:.2f}"
            else:
                result_dict["Relativ Volym"] = "N/A"
            
            # Lägg till prisförändring om filtret är aktivt
            if use_price_change and price_change_pct is not None:
                result_dict[f"Förändring ({price_change_period})"] = f"{price_change_pct:+.2f}%"
            
            result_dict["Händelser"] = news_text
            
            results.append(result_dict)
            
        except Exception:
            continue
    
    return results

# --- Huvudapplikation ---

def main():
    st.title("🌍 Global AktieScreener")
    st.markdown("Scanna aktier från **Sverige, Kanada och USA** (Listor från `market_data.py`)")
    
    # --- SIDEBAR ---
    st.sidebar.header("🎯 Filterinställningar")
    
    # --- MARKNADSVAL ---
    st.sidebar.subheader("🌍 Välj Marknader")
    
    all_markets = list(ticker_lists.keys())
    selected_markets = st.sidebar.multiselect(
        "Marknader att scanna",
        options=all_markets,
        default=["Sverige 🇸🇪"],
        help="Välj marknader."
    )
    
    selected_categories = {}
    total_tickers_estimated = 0
    
    if selected_markets:
        for market in selected_markets:
            categories = list(ticker_lists[market].keys())
            default_cats = [categories[0]] if categories else []
            
            selected_cats = st.sidebar.multiselect(
                f"Kategorier i {market}",
                options=categories,
                default=default_cats,
                key=f"cat_{market}"
            )
            selected_categories[market] = selected_cats
            
            for cat in selected_cats:
                total_tickers_estimated += len(ticker_lists[market][cat])
    
    if total_tickers_estimated > 0:
        st.sidebar.info(f"📊 Totalt ~{total_tickers_estimated} aktier valda")
    
    st.sidebar.markdown("---")
    
    # --- PRIS & FILTER ---
    price_range = st.sidebar.slider("Prisintervall (Nominellt)", 0, 2000, (0, 2000), 10)
    
    st.sidebar.markdown("---")
    
    # Snabb sökning-läge
    snabb_sokning = st.sidebar.checkbox(
        "⚡ Snabb sökning (skippa händelser)", 
        value=False,
        help="Mycket snabbare (10-20x) men ingen nyhetssökning. Perfekt för explorativ sökning!"
    )
    
    st.sidebar.subheader("📰 Händelser")
    
    # Inaktivera händelsefilter om snabb sökning är på
    if snabb_sokning:
        st.sidebar.info("🚀 Snabb sökning aktiverad - händelsefilter inaktiverade")
        check_vinstvarning = False
        check_rapport = False
        check_insider = False
        check_ny_vd = False
    else:
        check_vinstvarning = st.sidebar.checkbox("⚠️ Vinstvarning")
        check_rapport = st.sidebar.checkbox("📊 Rapport (30 dagar)")
        check_insider = st.sidebar.checkbox("👤 Insider")
        check_ny_vd = st.sidebar.checkbox("🎯 Ny VD")
    
    st.sidebar.subheader("📈 Teknisk Trend")
    streak_filter = st.sidebar.slider("Trend (Dagar upp/ner)", -15, 15, (-15, 15))
    
    # Prisförändring filter
    st.sidebar.markdown("---")
    use_price_change = st.sidebar.checkbox("Använd prisförändring-filter")
    
    if use_price_change:
        price_change_period = st.sidebar.selectbox(
            "Tidsperiod",
            ["1 dag", "1 vecka", "1 månad", "3 månader"],
            help="Hur långt bakåt ska prisförändringen beräknas?"
        )
        
        price_change_range = st.sidebar.slider(
            "Prisförändring (%)",
            -50.0, 100.0, (0.0, 20.0),
            step=0.5,
            help="Filtrera bolag som gått upp/ner inom detta intervall"
        )
        
        # Volymfilter (valfritt)
        use_volume_filter = st.sidebar.checkbox(
            "📊 Filtrera på volym",
            help="Välj bara aktier med ovanlig volym (högre/lägre än normalt)"
        )
        
        if use_volume_filter:
            volume_threshold = st.sidebar.slider(
                "Min. relativ volym (%)",
                0, 500, 100,
                step=10,
                help="100% = normal volym, 200% = dubbel volym, 50% = halv volym"
            )
        else:
            volume_threshold = None
    else:
        price_change_period = None
        price_change_range = None
        volume_threshold = None
    
    st.sidebar.markdown("---")
    start_btn = st.sidebar.button("🔍 Skanna Marknaden", type="primary", use_container_width=True)
    
    # --- SÖKLOGIK ---
    if start_btn:
        if not selected_markets:
            st.warning("⚠️ Välj minst en marknad!")
            return
        
        all_tickers = []
        for market in selected_markets:
            if market in selected_categories:
                for category in selected_categories[market]:
                    all_tickers.extend(ticker_lists[market][category])
        
        all_tickers = list(set(all_tickers))
        total = len(all_tickers)
        
        if total == 0:
            st.warning("⚠️ Inga kategorier valda!")
            return
        
        # Estimera scanningstid baserat på filter
        has_events = check_vinstvarning or check_rapport or check_insider or check_ny_vd
        if has_events:
            estimated_time = f"~{total//10}-{total//5} sekunder"
            st.info(f"🚀 Skannar {total} aktier med händelsesök... Estimerad tid: {estimated_time}")
            st.caption("💡 Tips: Aktivera '⚡ Snabb sökning' för 10-20x snabbare resultat")
        else:
            estimated_time = f"~{total//50}-{total//25} sekunder"
            st.info(f"⚡ Snabb sökning: {total} aktier... Estimerad tid: {estimated_time}")
        
        BATCH_SIZE = 50
        batches = [all_tickers[i:i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]
        num_batches = len(batches)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.empty()
        all_results = []
        start_time = time.time()
        
        for batch_idx, batch in enumerate(batches, 1):
            status_text.text(f"⚡ Processar batch {batch_idx}/{num_batches} ({len(batch)} st)...")
            progress_bar.progress(batch_idx / num_batches)
            
            batch_data = download_batch_data(batch, batch_idx, num_batches)
            
            if batch_data is not None:
                batch_results = process_batch_results(
                    batch_data, batch, price_range, streak_filter,
                    check_vinstvarning, check_rapport, check_insider, check_ny_vd,
                    use_price_change, price_change_period, price_change_range,
                    volume_threshold
                )
                all_results.extend(batch_results)
                
                if all_results:
                    results_container.success(f"✅ Hittills: {len(all_results)} matchande")
        
        status_text.empty()
        progress_bar.empty()
        results_container.empty()
        elapsed_time = time.time() - start_time
        
        if len(all_results) > 0:
            display_results = all_results[:100]
            st.success(f"✅ Klar! Hittade {len(all_results)} aktier på {elapsed_time:.1f}s")
            
            df_results = pd.DataFrame(display_results)
            st.dataframe(df_results, use_container_width=True, height=600)
            
            csv = df_results.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Ladda ner CSV", csv, "resultat.csv", "text/csv")
        else:
            st.warning("⚠️ Inga aktier matchade dina filter.")
    else:
        st.info("👈 Välj marknad och klicka på 'Skanna Marknaden'")

if __name__ == "__main__":
    main()