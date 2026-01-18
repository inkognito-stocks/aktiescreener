import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

# --- IMPORT FRÅN MARKET_DATA.PY ---
try:
    import market_data as md
    # Grundlistor
    SE_LARGE_CAP = getattr(md, 'SE_LARGE_CAP', [])
    SE_MID_CAP = getattr(md, 'SE_MID_CAP', [])
    SE_SMALL_CAP = getattr(md, 'SE_SMALL_CAP', [])
    SE_FIRST_NORTH = getattr(md, 'SE_FIRST_NORTH', [])
    US_ALL_STAR = getattr(md, 'US_ALL_STAR', [])
    CA_ALL_STAR = getattr(md, 'CA_ALL_STAR', [])
    # Kanada sektorer
    CA_ENERGY = getattr(md, 'CA_ENERGY', [])
    CA_MINING = getattr(md, 'CA_MINING', [])
    CA_TECH = getattr(md, 'CA_TECH', [])
    CA_FINANCIALS = getattr(md, 'CA_FINANCIALS', [])
    CA_CONSUMER = getattr(md, 'CA_CONSUMER', [])
    CA_INDUSTRIALS = getattr(md, 'CA_INDUSTRIALS', [])
    CA_TELECOM_UTILITIES = getattr(md, 'CA_TELECOM_UTILITIES', [])
    CA_REAL_ESTATE = getattr(md, 'CA_REAL_ESTATE', [])
    CA_HEALTHCARE = getattr(md, 'CA_HEALTHCARE', [])
    CA_FORESTRY = getattr(md, 'CA_FORESTRY', [])
    CA_SPECULATIVE = getattr(md, 'CA_SPECULATIVE', [])
    # USA sektorer
    US_TECH = getattr(md, 'US_TECH', [])
    US_FINANCIALS = getattr(md, 'US_FINANCIALS', [])
    US_ENERGY = getattr(md, 'US_ENERGY', [])
    US_HEALTHCARE = getattr(md, 'US_HEALTHCARE', [])
    US_CONSUMER = getattr(md, 'US_CONSUMER', [])
    US_INDUSTRIALS = getattr(md, 'US_INDUSTRIALS', [])
    US_MATERIALS = getattr(md, 'US_MATERIALS', [])
    # Sverige sektorer
    SE_TECH = getattr(md, 'SE_TECH', [])
    SE_FINANCIALS = getattr(md, 'SE_FINANCIALS', [])
    SE_INDUSTRIALS = getattr(md, 'SE_INDUSTRIALS', [])
    SE_CONSUMER = getattr(md, 'SE_CONSUMER', [])
    SE_HEALTHCARE = getattr(md, 'SE_HEALTHCARE', [])
    SE_ENERGY = getattr(md, 'SE_ENERGY', [])
    SE_REAL_ESTATE = getattr(md, 'SE_REAL_ESTATE', [])
except ImportError as e:
    st.error(f"⚠️ Hittade inte 'market_data.py': {e}")
    # Fallback-tomma listor så appen inte kraschar
    SE_LARGE_CAP, SE_MID_CAP, SE_SMALL_CAP, US_ALL_STAR, CA_ALL_STAR = [], [], [], [], []
    CA_ENERGY, CA_MINING, CA_TECH, CA_FINANCIALS, CA_CONSUMER, CA_INDUSTRIALS = [], [], [], [], [], []
    CA_TELECOM_UTILITIES, CA_REAL_ESTATE, CA_HEALTHCARE, CA_FORESTRY, CA_SPECULATIVE = [], [], [], [], []
    US_TECH, US_FINANCIALS, US_ENERGY, US_HEALTHCARE, US_CONSUMER, US_INDUSTRIALS, US_MATERIALS = [], [], [], [], [], [], []
    SE_TECH, SE_FINANCIALS, SE_INDUSTRIALS, SE_CONSUMER, SE_HEALTHCARE, SE_ENERGY, SE_REAL_ESTATE = [], [], [], [], [], [], []

# --- ORGANISERA LISTORNA ---
# Vi bygger ihop strukturen här så att menyn i appen fungerar snyggt
ticker_lists = {
    "Sverige 🇸🇪": {
        "Alla bolag": SE_LARGE_CAP + SE_MID_CAP + SE_SMALL_CAP + SE_FIRST_NORTH,
        "Large Cap": SE_LARGE_CAP,
        "Mid Cap": SE_MID_CAP,
        "Small Cap": SE_SMALL_CAP,
        "First North": SE_FIRST_NORTH,
        "Tech & Software": SE_TECH,
        "Financials & Banks": SE_FINANCIALS,
        "Industrials & Manufacturing": SE_INDUSTRIALS,
        "Consumer & Retail": SE_CONSUMER,
        "Healthcare & Biotech": SE_HEALTHCARE,
        "Energy & Utilities": SE_ENERGY,
        "Real Estate": SE_REAL_ESTATE
    },
    "USA 🇺🇸": {
        "Alla bolag": US_ALL_STAR,
        "Tech & Software": US_TECH,
        "Financials & Banks": US_FINANCIALS,
        "Energy & Oil": US_ENERGY,
        "Healthcare & Biotech": US_HEALTHCARE,
        "Consumer & Retail": US_CONSUMER,
        "Industrials": US_INDUSTRIALS,
        "Materials & Mining": US_MATERIALS
    },
    "Kanada 🇨🇦": {
        "Alla bolag": CA_ALL_STAR,
        "Energy & Pipelines": CA_ENERGY,
        "Mining & Materials": CA_MINING,
        "Tech & Software": CA_TECH,
        "Financials & Banks": CA_FINANCIALS,
        "Consumer & Retail": CA_CONSUMER,
        "Industrials & Transportation": CA_INDUSTRIALS,
        "Telecom & Utilities": CA_TELECOM_UTILITIES,
        "Real Estate (REITs)": CA_REAL_ESTATE,
        "Healthcare & Cannabis": CA_HEALTHCARE,
        "Forestry & Paper": CA_FORESTRY,
        "Speculative & Crypto": CA_SPECULATIVE
    }
}

# --- Inställningar ---
st.set_page_config(
    page_title="AktieScreener Global", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS för bättre UI
st.markdown("""
<style>
    /* Förbättra sidebar */
    .css-1d391kg {
        padding-top: 1.5rem;
    }
    
    /* Kompaktare spacing */
    .stMarkdown {
        margin-bottom: 0.5rem;
    }
    
    /* Bättre tabell-läsbarhet */
    .dataframe {
        font-size: 0.85rem;
    }
    
    .dataframe th {
        background-color: #f0f2f6;
        font-weight: 600;
        padding: 0.5rem;
    }
    
    .dataframe td {
        padding: 0.4rem;
    }
    
    /* Tydligare knappar */
    .stButton > button {
        width: 100%;
        font-weight: 600;
        padding: 0.5rem 1rem;
        margin-top: 0.5rem;
    }
    
    /* Fixerad knapp längst ner på skärmen */
    .fixed-scan-button-container {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: white !important;
        padding: 1rem !important;
        border-top: 2px solid #e0e0e0 !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1) !important;
        z-index: 999 !important;
        width: 100% !important;
    }
    
    /* Justera padding för huvudinnehållet när fixerad knapp finns */
    .main .block-container {
        padding-bottom: 100px !important;
    }
    
    /* Fixerad knapp styling */
    .fixed-scan-button-container .stButton > button {
        width: 100% !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    .fixed-scan-button-container .stButton > button:hover {
        box-shadow: 0 6px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* Kompaktare multiselect */
    .stMultiSelect > div {
        padding: 0.25rem 0;
    }
    
    /* Bättre info-boxes */
    .stInfo {
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stSuccess {
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    
    /* Tydligare headers */
    h3 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Kompaktare metrics */
    .stMetric {
        padding: 0.5rem;
    }
    
    /* Snabbare transitions */
    * {
        transition: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- REDDIT TRENDING TICKERS ---

@st.cache_data(ttl=1800)  # Cache i 30 minuter
def get_reddit_trending_tickers(limit=100):
    """
    Hämtar de mest diskuterade tickers från Reddit.
    Söker i populära finans-subreddits.
    """
    try:
        # Samla alla tickers från våra listor för att validera
        all_tickers = set()
        for market_data in ticker_lists.values():
            for category_tickers in market_data.values():
                # Ta bort .TO, .ST suffix för att matcha Reddit-format
                for ticker in category_tickers:
                    clean_ticker = ticker.replace('.TO', '').replace('.ST', '').replace('-', '')
                    if len(clean_ticker) <= 5 and clean_ticker.isalpha():
                        all_tickers.add(clean_ticker.upper())
        
        # Lägg till vanliga tickers som kan saknas
        common_tickers = {'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD', 'NFLX', 
                         'DIS', 'BAC', 'JPM', 'WFC', 'GS', 'MS', 'V', 'MA', 'PYPL', 'SQ', 'COIN',
                         'GME', 'AMC', 'BB', 'NOK', 'PLTR', 'RKT', 'CLOV', 'WISH', 'SPCE', 'SNDL'}
        all_tickers.update(common_tickers)
        
        # Subreddits att söka i
        subreddits = ['stocks', 'investing', 'wallstreetbets', 'StockMarket', 'pennystocks', 
                     'CanadianInvestor', 'stocks', 'SecurityAnalysis']
        
        ticker_counts = Counter()
        
        for subreddit in subreddits[:3]:  # Begränsa till 3 för att undvika för många requests
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit//len(subreddits[:3])}"
                headers = {'User-Agent': 'StockScreener/1.0'}
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts:
                        post_data = post.get('data', {})
                        title = post_data.get('title', '')
                        selftext = post_data.get('selftext', '')
                        combined_text = f"{title} {selftext}".upper()
                        
                        # Hitta ticker-symboler (2-5 bokstäver, stora bokstäver, omgivna av whitespace eller specialtecken)
                        ticker_pattern = r'\$?([A-Z]{2,5})\b'
                        found_tickers = re.findall(ticker_pattern, combined_text)
                        
                        for ticker in found_tickers:
                            # Filtrera bort vanliga ord som inte är tickers
                            if ticker not in {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                                            'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 
                                            'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW',
                                            'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'ITS',
                                            'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE', 'YEAR', 'YOUR',
                                            'THIS', 'THAT', 'WITH', 'FROM', 'HAVE', 'WILL', 'WHAT',
                                            'WHEN', 'WHERE', 'WHICH', 'WHILE', 'AFTER', 'BEFORE',
                                            'ABOUT', 'ABOVE', 'ACROSS', 'AGAIN', 'AGAINST', 'ALONG',
                                            'AMONG', 'AROUND', 'BECAUSE', 'BECOME', 'BECAME', 'BEHIND',
                                            'BELOW', 'BESIDE', 'BETWEEN', 'BEYOND', 'DURING', 'EXCEPT',
                                            'INSIDE', 'OUTSIDE', 'THROUGH', 'THROUGHOUT', 'TOWARD',
                                            'UNDER', 'UNDERNEATH', 'UNLESS', 'UNTIL', 'UPON', 'WITHIN',
                                            'WITHOUT', 'THERE', 'THESE', 'THOSE', 'THEIR', 'THEM',
                                            'THERE', 'THESE', 'THOSE', 'THEIR', 'THEM', 'THERE', 'THESE',
                                            'THOSE', 'THEIR', 'THEM', 'THERE', 'THESE', 'THOSE'}:
                                if ticker in all_tickers or len(ticker) >= 3:  # Acceptera kända tickers eller 3+ bokstäver
                                    ticker_counts[ticker] += 1
            except Exception as e:
                # Fortsätt med nästa subreddit om en misslyckas
                continue
        
        # Returnera top 10 mest nämnda tickers
        top_tickers = [ticker for ticker, count in ticker_counts.most_common(10) if count >= 2]
        return top_tickers[:10]
    
    except Exception as e:
        # Om Reddit-hämtning misslyckas, returnera en tom lista eller fallback-tickers
        return []

def render_trending_ticker_banner(tickers):
    """
    Skapar en scrolling banner med trending tickers.
    """
    if not tickers:
        return
    
    # Skapa HTML för scrolling banner
    ticker_html = " • ".join([f"<span style='color: #FF6B6B; font-weight: bold;'>{ticker}</span>" for ticker in tickers])
    
    banner_html = f"""
    <div style="
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 12px 0;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        overflow: hidden;
        position: relative;
    ">
        <div style="
            display: flex;
            align-items: center;
            white-space: nowrap;
            animation: scroll 30s linear infinite;
        ">
            <span style="margin-right: 20px; font-weight: bold; color: #FFD700;">🔥 TRENDING:</span>
            <span style="margin-right: 50px;">{ticker_html}</span>
            <span style="margin-right: 50px;">{ticker_html}</span>
        </div>
    </div>
    
    <style>
        @keyframes scroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
    </style>
    """
    
    st.markdown(banner_html, unsafe_allow_html=True)

# --- Batch Download Functions ---

@st.cache_data(ttl=2700)  # Cache i 45 minuter
def download_batch_data(tickers_batch, batch_num, total_batches):
    """
    Laddar ner data för en batch av tickers samtidigt.
    Hämtar 5 års historik för att stödja alla utvecklingsperioder.
    """
    try:
        data = yf.download(
            tickers_batch,
            period="5y",  # 5 års historik för att stödja alla perioder
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

def detect_volume_spike(volumes, days_lookback=252):
    """
    Detekterar volymspikar och returnerar metadata.
    Returns: dict med 'spike_ratio', 'is_record', 'spike_category'
    """
    if len(volumes) < 30:
        return None
    
    recent_volume = float(volumes.iloc[-1])
    
    # Genomsnittlig volym över 90 dagar
    if len(volumes) > 90:
        avg_volume_90d = float(volumes.iloc[-91:-1].mean())
    else:
        avg_volume_90d = float(volumes.iloc[:-1].mean())
    
    # 52-veckors högsta volym (252 handelsdagar)
    lookback_days = min(days_lookback, len(volumes) - 1)
    if lookback_days > 0:
        max_volume_52w = float(volumes.iloc[-lookback_days-1:-1].max())
    else:
        max_volume_52w = avg_volume_90d
    
    if avg_volume_90d == 0:
        return None
    
    spike_ratio = recent_volume / avg_volume_90d
    is_record = recent_volume >= max_volume_52w
    
    # Kategorisera spiken
    if spike_ratio >= 10:
        spike_category = "EXTREMT"
    elif spike_ratio >= 5:
        spike_category = "MYCKET HÖG"
    elif spike_ratio >= 3:
        spike_category = "HÖG"
    elif spike_ratio >= 2:
        spike_category = "MÅTTLIG"
    else:
        spike_category = "NORMAL"
    
    return {
        'spike_ratio': spike_ratio,
        'is_record': is_record,
        'spike_category': spike_category,
        'recent_volume': recent_volume,
        'avg_volume_90d': avg_volume_90d,
        'max_volume_52w': max_volume_52w
    }

def detect_gap(prices):
    """
    Detekterar gap i priset (gap upp eller gap ner).
    Returns: dict med 'gap_pct', 'gap_type', 'gap_size'
    """
    if len(prices) < 2:
        return None
    
    today_close = float(prices.iloc[-1])
    yesterday_close = float(prices.iloc[-2])
    
    # För gap behöver vi öppningspriset, men vi har bara Close
    # Vi approximerar gap genom att jämföra dagens close med gårdagens close
    # Ett riktigt gap skulle kräva Open data, men vi kan identifiera stora rörelser
    
    # Om vi har High/Low data kan vi bättre uppskatta gap
    # För nu, låt oss använda close-to-close som proxy
    
    # Ett gap upp: dagens lägsta är högre än gårdagens högsta
    # Ett gap ner: dagens högsta är lägre än gårdagens lägsta
    
    # För enkelhet, låt oss använda close-to-close för stora rörelser
    price_change_pct = ((today_close - yesterday_close) / yesterday_close) * 100
    
    # Ett gap är vanligtvis >2% rörelse
    if abs(price_change_pct) >= 2:
        if price_change_pct > 0:
            gap_type = "GAP UPP"
        else:
            gap_type = "GAP NER"
        
        return {
            'gap_pct': abs(price_change_pct),
            'gap_type': gap_type,
            'gap_size': 'STOR' if abs(price_change_pct) >= 5 else 'MÅTTLIG'
        }
    
    return None

def detect_breakout(prices, volumes=None):
    """
    Detekterar breakout genom viktiga prisnivåer.
    Returns: dict med 'breakout_type', 'breakout_level', 'strength'
    """
    if len(prices) < 20:
        return None
    
    current_price = float(prices.iloc[-1])
    
    # 52-veckors hög/låg (252 handelsdagar)
    lookback_days = min(252, len(prices) - 1)
    if lookback_days > 0:
        high_52w = float(prices.iloc[-lookback_days-1:-1].max())
        low_52w = float(prices.iloc[-lookback_days-1:-1].min())
    else:
        high_52w = float(prices.max())
        low_52w = float(prices.min())
    
    # 20-dagars moving average
    if len(prices) >= 20:
        ma_20 = float(prices.iloc[-20:].mean())
    else:
        ma_20 = current_price
    
    # 50-dagars moving average
    if len(prices) >= 50:
        ma_50 = float(prices.iloc[-50:].mean())
    else:
        ma_50 = current_price
    
    breakouts = []
    
    # Breakout till 52-veckors hög
    if current_price >= high_52w * 0.98:  # 98% av högsta = nära breakout
        breakouts.append({
            'breakout_type': '52-VECKORS HÖG',
            'breakout_level': high_52w,
            'strength': 'MYCKET STARK' if current_price >= high_52w else 'STARK'
        })
    
    # Breakout över MA20
    if current_price > ma_20 and len(prices) >= 2:
        prev_price = float(prices.iloc[-2])
        if prev_price <= ma_20:  # Korsade precis över
            breakouts.append({
                'breakout_type': 'MA20',
                'breakout_level': ma_20,
                'strength': 'MÅTTLIG'
            })
    
    # Breakout över MA50
    if current_price > ma_50 and len(prices) >= 2:
        prev_price = float(prices.iloc[-2])
        if prev_price <= ma_50:  # Korsade precis över
            breakouts.append({
                'breakout_type': 'MA50',
                'breakout_level': ma_50,
                'strength': 'STARK'
            })
    
    if breakouts:
        # Returnera den starkaste breakouten
        return max(breakouts, key=lambda x: 3 if 'MYCKET STARK' in x['strength'] else (2 if 'STARK' in x['strength'] else 1))
    
    return None

def calculate_momentum_score(relative_volume, daily_change_pct, streak, has_news, 
                            volume_spike_data=None, gap_data=None, breakout_data=None):
    """
    Beräknar ett momentum-score (0-100) baserat på flera faktorer.
    Högre score = starkare momentum.
    """
    score = 0.0
    
    # 1. Relativ volym (30% vikt)
    if relative_volume is not None:
        if relative_volume >= 5:
            vol_score = 30
        elif relative_volume >= 3:
            vol_score = 25
        elif relative_volume >= 2:
            vol_score = 20
        elif relative_volume >= 1.5:
            vol_score = 15
        elif relative_volume >= 1.2:
            vol_score = 10
        else:
            vol_score = 5
        score += vol_score
    
    # 2. Prisförändring (25% vikt)
    if daily_change_pct is not None:
        if daily_change_pct >= 10:
            price_score = 25
        elif daily_change_pct >= 5:
            price_score = 20
        elif daily_change_pct >= 3:
            price_score = 15
        elif daily_change_pct >= 1:
            price_score = 10
        elif daily_change_pct >= 0:
            price_score = 5
        else:
            price_score = 0
        score += price_score
    
    # 3. Trend-streak (15% vikt)
    if streak is not None:
        if streak >= 7:
            streak_score = 15
        elif streak >= 5:
            streak_score = 12
        elif streak >= 3:
            streak_score = 10
        elif streak >= 1:
            streak_score = 7
        else:
            streak_score = 3
        score += streak_score
    
    # 4. Nyhetsaktivitet (10% vikt)
    if has_news:
        score += 10
    
    # 5. Volymspik bonus (10% vikt)
    if volume_spike_data:
        if volume_spike_data.get('is_record'):
            score += 10
        elif volume_spike_data.get('spike_ratio', 0) >= 5:
            score += 8
        elif volume_spike_data.get('spike_ratio', 0) >= 3:
            score += 5
    
    # 6. Gap bonus (5% vikt)
    if gap_data:
        if gap_data.get('gap_size') == 'STOR':
            score += 5
        else:
            score += 3
    
    # 7. Breakout bonus (5% vikt)
    if breakout_data:
        if 'MYCKET STARK' in breakout_data.get('strength', ''):
            score += 5
        elif 'STARK' in breakout_data.get('strength', ''):
            score += 3
        else:
            score += 2
    
    return min(100, max(0, score))  # Begränsa till 0-100

def get_market_from_ticker(ticker):
    """Identifierar marknad baserat på ticker-suffix"""
    if ticker.endswith('.ST'):
        return 'Sverige 🇸🇪'
    elif ticker.endswith('.TO') or ticker.endswith('.V') or ticker.endswith('.CN'):
        return 'Kanada 🇨🇦'
    else:
        return 'USA 🇺🇸'

def get_yahoo_finance_url(ticker):
    """
    Genererar Yahoo Finance URL för en ticker.
    """
    # Yahoo Finance använder samma ticker-format som yfinance
    # T.ex. AAPL, AAK.ST, RY.TO
    encoded_ticker = ticker.replace('.', '-')  # Yahoo Finance använder - istället för . i URL:en
    return f"https://finance.yahoo.com/quote/{ticker}"

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

def process_batch_results(data, tickers_in_batch, market_cap_range, streak_filter, 
                          check_vinstvarning, check_rapport, check_insider, check_ny_vd, 
                          use_price_change, price_change_period, price_change_range, 
                          volume_threshold, development_period):
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
            
            # Senaste pris (behålls för visning)
            price = float(closes.iloc[-1])
            
            # Hämta börsvärde (market cap) från yfinance info
            market_cap = None
            try:
                ticker_obj = yf.Ticker(ticker)
                info = ticker_obj.info
                market_cap = info.get('marketCap', None)
            except Exception:
                pass
            
            # Börsvärde-filter (om market cap är tillgängligt och filter är aktivt)
            if market_cap_range and len(market_cap_range) == 2:
                if market_cap is None:
                    # Om börsvärde saknas och filter är aktivt, hoppa över (eller tillåt om båda är 0-1000)
                    if market_cap_range[0] > 0 or market_cap_range[1] < 1000_000_000_000:
                        continue
                elif not (market_cap_range[0] <= market_cap <= market_cap_range[1]):
                    continue
            
            # Beräkna streak
            streak = calculate_streak(closes)
            
            # Streak-filter
            min_streak, max_streak = streak_filter
            if not (min_streak <= streak <= max_streak):
                continue
            
            # Beräkna volym alltid (för att visa relativ volym)
            relative_volume = None
            volume_spike_data = None
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
                    
                    # Detektera volymspikar
                    volume_spike_data = detect_volume_spike(volumes)
            
            # Beräkna dagens stängning (positivt/negativt)
            daily_change_pct = None
            daily_change_direction = None
            if len(closes) >= 2:
                today_price = float(closes.iloc[-1])
                yesterday_price = float(closes.iloc[-2])
                daily_change_pct = ((today_price - yesterday_price) / yesterday_price) * 100
                if daily_change_pct > 0:
                    daily_change_direction = "positivt"
                elif daily_change_pct < 0:
                    daily_change_direction = "negativt"
                else:
                    daily_change_direction = "oförändrat"
            
            # Detektera gap
            gap_data = detect_gap(closes)
            
            # Detektera breakout
            breakout_data = None
            if 'Volume' in ticker_data.columns:
                volumes = ticker_data['Volume'].dropna()
                breakout_data = detect_breakout(closes, volumes)
            else:
                breakout_data = detect_breakout(closes)
            
            # Beräkna utveckling för vald period
            development_pct = None
            development_days = {
                "1 dag": 1,
                "1 vecka": 5,
                "1 månad": 20,
                "3 månader": 60,
                "6 månader": 120,
                "12 månader": 250,
                "3 år": 750,
                "5 år": 1250
            }
            days_back = development_days.get(development_period, 1)
            
            if len(closes) > days_back:
                old_price = float(closes.iloc[-days_back-1])
                current_price = float(closes.iloc[-1])
                development_pct = ((current_price - old_price) / old_price) * 100
            
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
            has_news = len(news_hits) > 0
            
            # Beräkna momentum-score
            momentum_score = calculate_momentum_score(
                relative_volume, daily_change_pct, streak, has_news,
                volume_spike_data, gap_data, breakout_data
            )
            
            # Generera Yahoo Finance länk
            yahoo_url = get_yahoo_finance_url(ticker)
            
            # Bygg resultat-dictionary
            result_dict = {
                "Momentum": momentum_score,  # Lägg först för sortering
                "Ticker": ticker,  # Vi formaterar detta senare som länk
                "Ticker_URL": yahoo_url,  # Spara URL separat för formatering
                "Marknad": market,
                f"Pris ({currency})": round(price, 2),
                "Trend (Dagar)": streak,
            }
            
            # Lägg till dagens stängning (positivt/negativt)
            if daily_change_direction and daily_change_pct is not None:
                if daily_change_direction == "positivt":
                    result_dict["Dagens stängning"] = f"+{daily_change_pct:.2f}%"
                elif daily_change_direction == "negativt":
                    result_dict["Dagens stängning"] = f"{daily_change_pct:.2f}%"
                else:
                    result_dict["Dagens stängning"] = f"{daily_change_pct:.2f}%"
            else:
                result_dict["Dagens stängning"] = "N/A"
            
            # Lägg till utveckling för vald period
            if development_pct is not None:
                if development_pct > 0:
                    result_dict[f"Utveckling ({development_period})"] = f"+{development_pct:.2f}%"
                elif development_pct < 0:
                    result_dict[f"Utveckling ({development_period})"] = f"{development_pct:.2f}%"
                else:
                    result_dict[f"Utveckling ({development_period})"] = f"{development_pct:.2f}%"
            else:
                result_dict[f"Utveckling ({development_period})"] = "N/A"
            
            # Lägg till relativ volym alltid (om tillgängligt)
            if relative_volume is not None:
                # Formatera som 1.5 för 50% mer, 0.5 för 50% lägre
                result_dict["Relativ Volym"] = f"{relative_volume:.2f}"
            else:
                result_dict["Relativ Volym"] = "N/A"
            
            # Lägg till volymspik-info
            if volume_spike_data:
                spike_emoji = "🔥" if volume_spike_data.get('is_record') else "📈"
                spike_text = f"{spike_emoji} {volume_spike_data.get('spike_category', 'NORMAL')}"
                if volume_spike_data.get('is_record'):
                    spike_text += " (REKORD)"
                result_dict["Volymspik"] = spike_text
            else:
                result_dict["Volymspik"] = "N/A"
            
            # Lägg till gap-info
            if gap_data:
                gap_emoji = "🚀" if gap_data.get('gap_type') == "GAP UPP" else "📉"
                result_dict["Gap"] = f"{gap_emoji} {gap_data.get('gap_type', '')} {gap_data.get('gap_pct', 0):.1f}%"
            else:
                result_dict["Gap"] = "Ingen"
            
            # Lägg till breakout-info
            if breakout_data:
                breakout_emoji = "💥"
                result_dict["Breakout"] = f"{breakout_emoji} {breakout_data.get('breakout_type', '')}"
            else:
                result_dict["Breakout"] = "Ingen"
            
            # Lägg till prisförändring om filtret är aktivt
            if use_price_change and price_change_pct is not None:
                result_dict[f"Förändring ({price_change_period})"] = f"{price_change_pct:+.2f}%"
            
            result_dict["Händelser"] = news_text
            
            results.append(result_dict)
            
        except Exception:
            continue
    
    return results

# --- RÅVAROR, OLJA & KRYPTO ---

@st.cache_data(ttl=300)  # Cache i 5 minuter
def get_commodities_data():
    """Hämtar priser för råvaror (koppar, guld, silver, etc.)"""
    commodities = {
        "Guld": "GC=F",  # Gold Futures
        "Silver": "SI=F",  # Silver Futures
        "Koppar": "HG=F",  # Copper Futures
        "Platina": "PL=F",  # Platinum Futures
        "Palladium": "PA=F",  # Palladium Futures
        "Aluminium": "ALI=F",  # Aluminum Futures
        "Zink": "ZN=F",  # Zinc Futures
        "Nickel": "NI=F",  # Nickel Futures
        "Vete": "ZW=F",  # Wheat Futures
        "Majs": "ZC=F",  # Corn Futures
        "Sojabönor": "ZS=F",  # Soybean Futures
        "Kaffe": "KC=F",  # Coffee Futures
        "Socker": "SB=F",  # Sugar Futures
        "Kakao": "CC=F",  # Cocoa Futures
        "Bomull": "CT=F",  # Cotton Futures
    }
    
    results = []
    for name, ticker in commodities.items():
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.history(period="2d")
            if not info.empty:
                current_price = info['Close'].iloc[-1]
                prev_price = info['Close'].iloc[-2] if len(info) > 1 else current_price
                change_pct = ((current_price - prev_price) / prev_price) * 100
                
                results.append({
                    "Råvara": name,
                    "Pris": f"${current_price:.2f}",
                    "Förändring (%)": f"{change_pct:+.2f}%",
                    "Ticker": ticker,
                    "URL": f"https://finance.yahoo.com/quote/{ticker}"
                })
        except Exception as e:
            continue
    
    return results

@st.cache_data(ttl=300)  # Cache i 5 minuter
def get_oil_data():
    """Hämtar oljepriser"""
    oil_types = {
        "WTI Crude": "CL=F",  # WTI Crude Oil
        "Brent Crude": "BZ=F",  # Brent Crude Oil
        "Heating Oil": "HO=F",  # Heating Oil
        "RBOB Gasoline": "RB=F",  # RBOB Gasoline
        "Natural Gas": "NG=F",  # Natural Gas
    }
    
    results = []
    for name, ticker in oil_types.items():
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.history(period="2d")
            if not info.empty:
                current_price = info['Close'].iloc[-1]
                prev_price = info['Close'].iloc[-2] if len(info) > 1 else current_price
                change_pct = ((current_price - prev_price) / prev_price) * 100
                
                results.append({
                    "Oljetyp": name,
                    "Pris": f"${current_price:.2f}",
                    "Förändring (%)": f"{change_pct:+.2f}%",
                    "Ticker": ticker,
                    "URL": f"https://finance.yahoo.com/quote/{ticker}"
                })
        except Exception as e:
            continue
    
    return results

@st.cache_data(ttl=300)  # Cache i 5 minuter
def get_crypto_data():
    """Hämtar kryptopriser"""
    cryptocurrencies = {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
        "Binance Coin": "BNB-USD",
        "Solana": "SOL-USD",
        "Cardano": "ADA-USD",
        "XRP": "XRP-USD",
        "Polkadot": "DOT-USD",
        "Dogecoin": "DOGE-USD",
        "Avalanche": "AVAX-USD",
        "Chainlink": "LINK-USD",
        "Polygon": "MATIC-USD",
        "Litecoin": "LTC-USD",
        "Bitcoin Cash": "BCH-USD",
        "Uniswap": "UNI-USD",
        "Ethereum Classic": "ETC-USD",
    }
    
    results = []
    for name, ticker in cryptocurrencies.items():
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.history(period="2d")
            if not info.empty:
                current_price = info['Close'].iloc[-1]
                prev_price = info['Close'].iloc[-2] if len(info) > 1 else current_price
                change_pct = ((current_price - prev_price) / prev_price) * 100
                
                # Formatera pris beroende på storlek
                if current_price < 1:
                    price_str = f"${current_price:.4f}"
                elif current_price < 1000:
                    price_str = f"${current_price:.2f}"
                else:
                    price_str = f"${current_price:,.2f}"
                
                results.append({
                    "Krypto": name,
                    "Pris": price_str,
                    "Förändring (%)": f"{change_pct:+.2f}%",
                    "Ticker": ticker,
                    "URL": f"https://finance.yahoo.com/quote/{ticker}"
                })
        except Exception as e:
            continue
    
    return results

@st.cache_data(ttl=600)  # Cache i 10 minuter
def get_commodities_news():
    """Hämtar nyheter om råvaror"""
    tickers = ["GC=F", "SI=F", "HG=F", "PL=F", "PA=F"]
    
    all_news = []
    seen_titles = set()  # För att undvika duplicater
    
    for ticker in tickers:
        try:
            ticker_obj = yf.Ticker(ticker)
            news = ticker_obj.news[:5]  # Hämta top 5 nyheter
            for article in news:
                title = article.get('title', '')
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    all_news.append(article)
        except Exception:
            continue
    
    # Sortera efter datum (nyaste först)
    all_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
    return all_news[:10]  # Returnera top 10

@st.cache_data(ttl=600)  # Cache i 10 minuter
def get_oil_news():
    """Hämtar nyheter om olja"""
    tickers = ["CL=F", "BZ=F", "NG=F"]
    
    all_news = []
    seen_titles = set()  # För att undvika duplicater
    
    for ticker in tickers:
        try:
            ticker_obj = yf.Ticker(ticker)
            news = ticker_obj.news[:5]
            for article in news:
                title = article.get('title', '')
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    all_news.append(article)
        except Exception:
            continue
    
    all_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
    return all_news[:10]

@st.cache_data(ttl=600)  # Cache i 10 minuter
def get_crypto_news():
    """Hämtar nyheter om krypto"""
    tickers = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"]
    
    all_news = []
    seen_titles = set()  # För att undvika duplicater
    
    for ticker in tickers:
        try:
            ticker_obj = yf.Ticker(ticker)
            news = ticker_obj.news[:5]
            for article in news:
                title = article.get('title', '')
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    all_news.append(article)
        except Exception:
            continue
    
    all_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
    return all_news[:10]

def display_commodities():
    """Visar råvaror-priser och nyheter"""
    st.header("📦 Råvaror")
    
    # Hämta data
    with st.spinner("Hämtar råvaror-priser..."):
        commodities_data = get_commodities_data()
    
    if commodities_data:
        # Visa priser i en tabell
        df = pd.DataFrame(commodities_data)
        
        # Färgkoda förändringar
        def color_change(val):
            if isinstance(val, str) and '%' in val:
                if '+' in val:
                    return 'background-color: #d4edda; color: #155724; font-weight: bold;'
                elif '-' in val:
                    return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
            return ''
        
        styled_df = df.style.applymap(color_change, subset=['Förändring (%)'])
        
        # Lägg till länkar
        column_config = {}
        if 'URL' in df.columns:
            try:
                df['🔗'] = df['URL']
                column_config['🔗'] = st.column_config.LinkColumn(
                    "Länk",
                    help="Öppna på Yahoo Finance",
                    display_text="Öppna"
                )
                df = df.drop(columns=['URL', 'Ticker'])
            except AttributeError:
                df['🔗 Länk'] = df.apply(
                    lambda row: f"[Öppna]({row['URL']})",
                    axis=1
                )
                df = df.drop(columns=['URL', 'Ticker'])
        
        st.dataframe(styled_df, use_container_width=True, height=400, column_config=column_config if column_config else None)
        
        # Visa nyheter
        st.markdown("### 📰 Senaste nyheterna om råvaror")
        with st.spinner("Hämtar nyheter..."):
            news = get_commodities_news()
        
        if news:
            for article in news[:5]:
                pub_time = datetime.fromtimestamp(article.get('providerPublishTime', 0))
                st.markdown(f"""
                **{article.get('title', 'Ingen titel')}**
                - *{article.get('publisher', 'Okänd källa')}* - {pub_time.strftime('%Y-%m-%d %H:%M')}
                - [Läs mer]({article.get('link', '#')})
                """)
                st.markdown("---")
        else:
            st.info("Inga nyheter hittades.")
    else:
        st.warning("Kunde inte hämta råvaror-data.")

def display_oil():
    """Visar oljepriser och nyheter"""
    st.header("🛢️ Olja & Energi")
    
    with st.spinner("Hämtar oljepriser..."):
        oil_data = get_oil_data()
    
    if oil_data:
        df = pd.DataFrame(oil_data)
        
        def color_change(val):
            if isinstance(val, str) and '%' in val:
                if '+' in val:
                    return 'background-color: #d4edda; color: #155724; font-weight: bold;'
                elif '-' in val:
                    return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
            return ''
        
        styled_df = df.style.applymap(color_change, subset=['Förändring (%)'])
        
        column_config = {}
        if 'URL' in df.columns:
            try:
                df['🔗'] = df['URL']
                column_config['🔗'] = st.column_config.LinkColumn("Länk", help="Öppna på Yahoo Finance", display_text="Öppna")
                df = df.drop(columns=['URL', 'Ticker'])
            except AttributeError:
                df['🔗 Länk'] = df.apply(lambda row: f"[Öppna]({row['URL']})", axis=1)
                df = df.drop(columns=['URL', 'Ticker'])
        
        st.dataframe(styled_df, use_container_width=True, height=300, column_config=column_config if column_config else None)
        
        st.markdown("### 📰 Senaste nyheterna om olja")
        with st.spinner("Hämtar nyheter..."):
            news = get_oil_news()
        
        if news:
            for article in news[:5]:
                pub_time = datetime.fromtimestamp(article.get('providerPublishTime', 0))
                st.markdown(f"""
                **{article.get('title', 'Ingen titel')}**
                - *{article.get('publisher', 'Okänd källa')}* - {pub_time.strftime('%Y-%m-%d %H:%M')}
                - [Läs mer]({article.get('link', '#')})
                """)
                st.markdown("---")
        else:
            st.info("Inga nyheter hittades.")
    else:
        st.warning("Kunde inte hämta oljepriser.")

def display_crypto():
    """Visar kryptopriser och nyheter"""
    st.header("₿ Krypto")
    
    with st.spinner("Hämtar kryptopriser..."):
        crypto_data = get_crypto_data()
    
    if crypto_data:
        df = pd.DataFrame(crypto_data)
        
        def color_change(val):
            if isinstance(val, str) and '%' in val:
                if '+' in val:
                    return 'background-color: #d4edda; color: #155724; font-weight: bold;'
                elif '-' in val:
                    return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
            return ''
        
        styled_df = df.style.applymap(color_change, subset=['Förändring (%)'])
        
        column_config = {}
        if 'URL' in df.columns:
            try:
                df['🔗'] = df['URL']
                column_config['🔗'] = st.column_config.LinkColumn("Länk", help="Öppna på Yahoo Finance", display_text="Öppna")
                df = df.drop(columns=['URL', 'Ticker'])
            except AttributeError:
                df['🔗 Länk'] = df.apply(lambda row: f"[Öppna]({row['URL']})", axis=1)
                df = df.drop(columns=['URL', 'Ticker'])
        
        st.dataframe(styled_df, use_container_width=True, height=500, column_config=column_config if column_config else None)
        
        st.markdown("### 📰 Senaste nyheterna om krypto")
        with st.spinner("Hämtar nyheter..."):
            news = get_crypto_news()
        
        if news:
            for article in news[:5]:
                pub_time = datetime.fromtimestamp(article.get('providerPublishTime', 0))
                st.markdown(f"""
                **{article.get('title', 'Ingen titel')}**
                - *{article.get('publisher', 'Okänd källa')}* - {pub_time.strftime('%Y-%m-%d %H:%M')}
                - [Läs mer]({article.get('link', '#')})
                """)
                st.markdown("---")
        else:
            st.info("Inga nyheter hittades.")
    else:
        st.warning("Kunde inte hämta kryptopriser.")

# --- TOP VINNARE/FÖRLORARE ---

@st.cache_data(ttl=300)  # Cache i 5 minuter
def get_top_gainers_losers(limit=10):
    """
    Hämtar top 10 vinnare och förlorare från alla aktier i market_data.
    """
    try:
        # Samla alla tickers från alla marknader
        all_tickers = []
        for market_data in ticker_lists.values():
            for category_tickers in market_data.values():
                all_tickers.extend(category_tickers)
        
        # Ta bort duplicater
        all_tickers = list(set(all_tickers))
        
        if not all_tickers:
            return [], []
        
        # Hämta data för alla aktier i batch (använd större batches för snabbare hämtning)
        BATCH_SIZE = 50
        batches = [all_tickers[i:i + BATCH_SIZE] for i in range(0, len(all_tickers), BATCH_SIZE)]
        
        gainers = []
        losers = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for batch_idx, batch in enumerate(batches, 1):
            status_text.caption(f"⚡ Hämtar data för batch {batch_idx}/{len(batches)} ({len(batch)} aktier)...")
            progress_bar.progress(batch_idx / len(batches))
            
            try:
                # Hämta data för batch
                data = yf.download(batch, period="5d", group_by='ticker', threads=True, progress=False, timeout=10)
                
                if data.empty:
                    continue
                
                # Processa varje ticker i batchen
                for ticker in batch:
                    try:
                        # Hämta data för denna ticker
                        if len(batch) == 1:
                            ticker_data = data
                        else:
                            if ticker not in data.columns.levels[0]:
                                continue
                            ticker_data = data[ticker]
                        
                        if 'Close' not in ticker_data.columns:
                            continue
                        
                        closes = ticker_data['Close'].dropna()
                        if len(closes) < 2:
                            continue
                        
                        # Beräkna dagens förändring
                        today_price = float(closes.iloc[-1])
                        yesterday_price = float(closes.iloc[-2])
                        
                        # Skip om pris är 0 eller NaN
                        if today_price == 0 or pd.isna(today_price) or yesterday_price == 0 or pd.isna(yesterday_price):
                            continue
                        
                        change_pct = ((today_price - yesterday_price) / yesterday_price) * 100
                        
                        # Hämta marknad och valuta
                        market = get_market_from_ticker(ticker)
                        currency = "SEK" if market == 'Sverige 🇸🇪' else ("CAD" if market == 'Kanada 🇨🇦' else "USD")
                        
                        # Generera Yahoo Finance länk
                        yahoo_url = get_yahoo_finance_url(ticker)
                        
                        result = {
                            "Ticker": ticker,
                            "Ticker_URL": yahoo_url,
                            "Marknad": market,
                            f"Pris ({currency})": round(today_price, 2),
                            "Förändring (%)": round(change_pct, 2)
                        }
                        
                        if change_pct > 0:
                            gainers.append(result)
                        elif change_pct < 0:
                            losers.append(result)
                    
                    except Exception:
                        continue
            
            except Exception:
                continue
        
        progress_bar.empty()
        status_text.empty()
        
        # Sortera och ta top 10
        top_gainers = sorted(gainers, key=lambda x: x['Förändring (%)'], reverse=True)[:limit]
        top_losers = sorted(losers, key=lambda x: x['Förändring (%)'])[:limit]
        
        return top_gainers, top_losers
    
    except Exception as e:
        return [], []

def display_winners_losers():
    """Visar top vinnare och förlorare"""
    st.header("🏆 Vinnare/Förlorare Globalt")
    st.markdown("Top 10 bästa vinnare och förlorare baserat på **dagens prisförändring** från alla aktier i databasen.")
    
    # Info om uppdatering
    col_info1, col_info2 = st.columns([2, 1])
    with col_info1:
        st.caption("💡 Data hämtas från alla aktier i market_data.py och uppdateras automatiskt var 5:e minut.")
    with col_info2:
        if st.button("🔄 Uppdatera", use_container_width=True):
            # Rensa cache för get_top_gainers_losers
            get_top_gainers_losers.clear()
            st.rerun()
    
    st.markdown("---")
    
    # Hämta data
    top_gainers, top_losers = get_top_gainers_losers(limit=10)
    
    if not top_gainers and not top_losers:
        st.warning("⚠️ Kunde inte hämta data. Försök igen om en stund.")
        return
    
    # Visa i två kolumner
    col_gainers, col_losers = st.columns(2)
    
    with col_gainers:
        st.subheader("📈 Top 10 Vinnare")
        if top_gainers:
            df_gainers = pd.DataFrame(top_gainers)
            
            # Formatera förändring med färg
            def format_change(val):
                if isinstance(val, (int, float)):
                    if val > 0:
                        return f"+{val:.2f}%"
                    else:
                        return f"{val:.2f}%"
                return val
            
            df_gainers['Förändring (%)'] = df_gainers['Förändring (%)'].apply(format_change)
            
            # Sortera kolumner - viktigaste först
            priority_cols = ['Ticker', 'Förändring (%)', 'Marknad', 'Pris']
            existing_cols = list(df_gainers.columns)
            ordered_cols = []
            for col in priority_cols:
                matches = [c for c in existing_cols if col.lower() in c.lower() or c.startswith(col)]
                if matches:
                    ordered_cols.extend(matches)
                    existing_cols = [c for c in existing_cols if c not in matches]
            ordered_cols.extend([c for c in existing_cols if c not in ordered_cols and c != 'Ticker_URL'])
            df_gainers = df_gainers[ordered_cols]
            
            # Lägg till länkar
            column_config_gainers = {}
            if 'Ticker_URL' in df_gainers.columns:
                try:
                    df_gainers['🔗'] = df_gainers['Ticker_URL']
                    column_config_gainers['🔗'] = st.column_config.LinkColumn(
                        "Länk",
                        help="Öppna på Yahoo Finance",
                        display_text="Öppna"
                    )
                    df_gainers = df_gainers.drop(columns=['Ticker_URL'])
                    # Lägg till länk-kolumnen efter Ticker
                    if 'Ticker' in ordered_cols:
                        ticker_idx = ordered_cols.index('Ticker')
                        ordered_cols.insert(ticker_idx + 1, '🔗')
                    # Filtrera ordered_cols så att bara kolumner som finns i df_gainers används
                    ordered_cols = [col for col in ordered_cols if col in df_gainers.columns]
                    df_gainers = df_gainers[ordered_cols]
                except AttributeError:
                    df_gainers['🔗 Länk'] = df_gainers.apply(
                        lambda row: f"[Öppna]({row['Ticker_URL']})",
                        axis=1
                    )
                    df_gainers = df_gainers.drop(columns=['Ticker_URL'])
                    if 'Ticker' in ordered_cols:
                        ticker_idx = ordered_cols.index('Ticker')
                        ordered_cols.insert(ticker_idx + 1, '🔗 Länk')
                    # Filtrera ordered_cols så att bara kolumner som finns i df_gainers används
                    ordered_cols = [col for col in ordered_cols if col in df_gainers.columns]
                    df_gainers = df_gainers[ordered_cols]
            
            # Färgkoda förändring
            def color_gainers(val):
                if isinstance(val, str) and '%' in val:
                    if '+' in val:
                        return 'background-color: #d4edda; color: #155724; font-weight: bold;'
                return ''
            
            styled_gainers = df_gainers.style.applymap(
                color_gainers,
                subset=['Förändring (%)']
            )
            
            if column_config_gainers:
                st.dataframe(styled_gainers, use_container_width=True, height=400, column_config=column_config_gainers)
            else:
                st.dataframe(styled_gainers, use_container_width=True, height=400)
        else:
            st.info("Inga vinnare hittades.")
    
    with col_losers:
        st.subheader("📉 Top 10 Förlorare")
        if top_losers:
            df_losers = pd.DataFrame(top_losers)
            
            # Formatera förändring
            def format_change(val):
                if isinstance(val, (int, float)):
                    if val > 0:
                        return f"+{val:.2f}%"
                    else:
                        return f"{val:.2f}%"
                return val
            
            df_losers['Förändring (%)'] = df_losers['Förändring (%)'].apply(format_change)
            
            # Sortera kolumner - viktigaste först
            priority_cols = ['Ticker', 'Förändring (%)', 'Marknad', 'Pris']
            existing_cols = list(df_losers.columns)
            ordered_cols = []
            for col in priority_cols:
                matches = [c for c in existing_cols if col.lower() in c.lower() or c.startswith(col)]
                if matches:
                    ordered_cols.extend(matches)
                    existing_cols = [c for c in existing_cols if c not in matches]
            ordered_cols.extend([c for c in existing_cols if c not in ordered_cols and c != 'Ticker_URL'])
            df_losers = df_losers[ordered_cols]
            
            # Lägg till länkar
            column_config_losers = {}
            if 'Ticker_URL' in df_losers.columns:
                try:
                    df_losers['🔗'] = df_losers['Ticker_URL']
                    column_config_losers['🔗'] = st.column_config.LinkColumn(
                        "Länk",
                        help="Öppna på Yahoo Finance",
                        display_text="Öppna"
                    )
                    df_losers = df_losers.drop(columns=['Ticker_URL'])
                    # Lägg till länk-kolumnen efter Ticker
                    if 'Ticker' in ordered_cols:
                        ticker_idx = ordered_cols.index('Ticker')
                        ordered_cols.insert(ticker_idx + 1, '🔗')
                    # Filtrera ordered_cols så att bara kolumner som finns i df_losers används
                    ordered_cols = [col for col in ordered_cols if col in df_losers.columns]
                    df_losers = df_losers[ordered_cols]
                except AttributeError:
                    df_losers['🔗 Länk'] = df_losers.apply(
                        lambda row: f"[Öppna]({row['Ticker_URL']})",
                        axis=1
                    )
                    df_losers = df_losers.drop(columns=['Ticker_URL'])
                    if 'Ticker' in ordered_cols:
                        ticker_idx = ordered_cols.index('Ticker')
                        ordered_cols.insert(ticker_idx + 1, '🔗 Länk')
                    # Filtrera ordered_cols så att bara kolumner som finns i df_losers används
                    ordered_cols = [col for col in ordered_cols if col in df_losers.columns]
                    df_losers = df_losers[ordered_cols]
            
            # Färgkoda förändring
            def color_losers(val):
                if isinstance(val, str) and '%' in val:
                    if '+' not in val:
                        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
                return ''
            
            styled_losers = df_losers.style.applymap(
                color_losers,
                subset=['Förändring (%)']
            )
            
            if column_config_losers:
                st.dataframe(styled_losers, use_container_width=True, height=400, column_config=column_config_losers)
            else:
                st.dataframe(styled_losers, use_container_width=True, height=400)
        else:
            st.info("Inga förlorare hittades.")
    
    st.markdown("---")
    st.caption("💡 Data uppdateras automatiskt var 5:e minut. Klicka på länken för att se mer detaljer på Yahoo Finance.")

# --- Huvudapplikation ---

def main():
    # Visa trending tickers banner
    try:
        trending_tickers = get_reddit_trending_tickers()
        if trending_tickers:
            render_trending_ticker_banner(trending_tickers)
    except Exception as e:
        # Om något går fel, fortsätt utan banner
        pass
    
    # Branschknappar/flikar ovanför huvudrubriken
    st.markdown("### Branscher")
    
    # Initiera session_state för vald bransch
    if 'selected_industry' not in st.session_state:
        st.session_state.selected_industry = 'stocks'
    
    industry_cols = st.columns(4)
    
    # Hantera knapp-klick med on_click callbacks för att undvika rerun-problem
    def set_industry(industry):
        st.session_state.selected_industry = industry
    
    with industry_cols[0]:
        st.button("📦 Råvaror", use_container_width=True, key="commodities_btn", 
                 type="primary" if st.session_state.selected_industry == 'commodities' else "secondary",
                 on_click=set_industry, args=('commodities',))
    with industry_cols[1]:
        st.button("🛢️ Olja", use_container_width=True, key="oil_btn",
                 type="primary" if st.session_state.selected_industry == 'oil' else "secondary",
                 on_click=set_industry, args=('oil',))
    with industry_cols[2]:
        st.button("₿ Krypto", use_container_width=True, key="crypto_btn",
                 type="primary" if st.session_state.selected_industry == 'crypto' else "secondary",
                 on_click=set_industry, args=('crypto',))
    with industry_cols[3]:
        st.button("📈 Aktier", use_container_width=True, key="stocks_btn",
                 type="primary" if st.session_state.selected_industry == 'stocks' else "secondary",
                 on_click=set_industry, args=('stocks',))
    
    st.markdown("---")
    
    # Visa rätt innehåll baserat på vald bransch
    if st.session_state.selected_industry == 'commodities':
        display_commodities()
    elif st.session_state.selected_industry == 'oil':
        display_oil()
    elif st.session_state.selected_industry == 'crypto':
        display_crypto()
    else:
        # Standard: Visa aktier
        # Huvudrubrik med kompakt layout
        col_title, col_info = st.columns([3, 1])
        with col_title:
            st.title("🌍 Global AktieScreener")
        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("Sverige 🇸🇪 • Kanada 🇨🇦 • USA 🇺🇸")
        
        st.markdown("---")
        
        # Skapa flikar
        tab1, tab2 = st.tabs(["🔍 Screener", "🏆 Vinnare/Förlorare Globalt"])
        
        with tab1:
            show_screener()
        
        with tab2:
            display_winners_losers()

def show_screener():
    """Huvudfunktion för screener-fliken"""
    # --- MARKNADSVAL ---
    st.sidebar.markdown("### 🌍 Marknader")
    
    all_markets = list(ticker_lists.keys())
    selected_markets = st.sidebar.multiselect(
        "Marknader att scanna",
        options=all_markets,
        default=["Sverige 🇸🇪"],
        help="Välj vilka marknader du vill scanna. Du kan välja flera samtidigt (Sverige, USA, Kanada)."
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
                key=f"cat_{market}",
                help=f"Välj vilka kategorier från {market} du vill inkludera. Exempel: Large Cap, Mid Cap, Small Cap för Sverige."
            )
            selected_categories[market] = selected_cats
            
            for cat in selected_cats:
                if cat in ticker_lists[market]:
                    total_tickers_estimated += len(ticker_lists[market][cat])
    
    # Beräkna faktiskt antal unika aktier (tar bort duplicater)
    if selected_markets and selected_categories:
        unique_tickers = set()
        for market in selected_markets:
            if market in selected_categories and selected_categories[market]:
                for category in selected_categories[market]:
                    if category in ticker_lists[market]:
                        unique_tickers.update(ticker_lists[market][category])
        total_unique = len(unique_tickers)
        
        if total_unique > 0:
            st.sidebar.success(f"📊 {total_unique} aktier kommer att scannas")
    elif total_tickers_estimated > 0:
        st.sidebar.success(f"📊 ~{total_tickers_estimated} aktier valda")
    
    st.sidebar.markdown("---")
    
    # --- BÖRSVÄRDE & FILTER ---
    st.sidebar.markdown("### 💰 Filter")
    
    # Initiera session_state för börsvärde-intervall (i miljarder USD)
    if 'market_cap_min' not in st.session_state:
        st.session_state.market_cap_min = 0
    if 'market_cap_max' not in st.session_state:
        st.session_state.market_cap_max = 1000  # 1000 miljarder = 1 triljon
    
    # Skapa två kolumner för min och max input
    col_mcap_min, col_mcap_max = st.sidebar.columns(2)
    
    with col_mcap_min:
        market_cap_min_input = st.number_input(
            "Min börsvärde (M)",
            min_value=0.0,
            max_value=1000.0,
            value=float(st.session_state.market_cap_min),
            step=10.0,
            key="market_cap_min_input",
            help="Minsta börsvärde i miljarder USD (t.ex. 1 = $1B, 100 = $100B)"
        )
        st.session_state.market_cap_min = float(market_cap_min_input)
    
    with col_mcap_max:
        market_cap_max_input = st.number_input(
            "Max börsvärde (M)",
            min_value=0.0,
            max_value=1000.0,
            value=float(st.session_state.market_cap_max),
            step=10.0,
            key="market_cap_max_input",
            help="Största börsvärde i miljarder USD (t.ex. 100 = $100B, 1000 = $1T)"
        )
        st.session_state.market_cap_max = float(market_cap_max_input)
    
    # Konvertera till faktiska värden (miljarder -> faktiskt värde)
    market_cap_min_value = st.session_state.market_cap_min * 1_000_000_000
    market_cap_max_value = st.session_state.market_cap_max * 1_000_000_000
    
    market_cap_range = st.sidebar.slider(
        "Börsvärde-intervall (Miljarder USD)", 
        0.0, 1000.0, 
        (st.session_state.market_cap_min, st.session_state.market_cap_max), 
        10.0,
        key="market_cap_range_slider",
        help="Dra slidern eller använd textfälten ovanför för att ange börsvärde-intervall. Exempel: 1-100 för att hitta aktier med börsvärde mellan $1B och $100B."
    )
    
    # Uppdatera session_state när slidern ändras (säkerställ float-typ)
    st.session_state.market_cap_min = float(market_cap_range[0])
    st.session_state.market_cap_max = float(market_cap_range[1])
    
    # Konvertera till faktiska värden för filtrering
    market_cap_range_values = (market_cap_range[0] * 1_000_000_000, market_cap_range[1] * 1_000_000_000)
    
    st.sidebar.markdown("---")
    
    # Prisförändring filter
    use_price_change = st.sidebar.checkbox(
        "Använd prisförändring-filter",
        help="Aktivera för att filtrera aktier baserat på hur mycket de har gått upp eller ner över en vald tidsperiod. Perfekt för att hitta momentum-aktier eller dippar."
    )
    
    if use_price_change:
        price_change_period = st.sidebar.selectbox(
            "Tidsperiod",
            ["1 dag", "1 vecka", "1 månad", "3 månader"],
            help="Hur långt bakåt ska prisförändringen beräknas? '1 dag' = jämför med igår, '1 vecka' = jämför med för 5 handelsdagar sedan, '1 månad' = jämför med för ~20 handelsdagar sedan."
        )
        
        # Initiera session_state för prisförändring om det inte finns
        if 'price_change_min' not in st.session_state:
            st.session_state.price_change_min = 0.0
        if 'price_change_max' not in st.session_state:
            st.session_state.price_change_max = 20.0
        
        # Skapa två kolumner för min och max input
        col_min, col_max = st.sidebar.columns(2)
        
        with col_min:
            min_change_input = st.number_input(
                "Min (%)",
                min_value=-50.0,
                max_value=100.0,
                value=st.session_state.price_change_min,
                step=0.5,
                key="price_change_min_input",
                help="Skriv in eller ändra minsta prisförändring (t.ex. -10 för -10%)"
            )
            st.session_state.price_change_min = min_change_input
        
        with col_max:
            max_change_input = st.number_input(
                "Max (%)",
                min_value=-50.0,
                max_value=100.0,
                value=st.session_state.price_change_max,
                step=0.5,
                key="price_change_max_input",
                help="Skriv in eller ändra största prisförändring (t.ex. +20 för +20%)"
            )
            st.session_state.price_change_max = max_change_input
        
        # Slider som synkroniseras med textfälten
        price_change_range = st.sidebar.slider(
            "Prisförändring (%)",
            -50.0, 100.0, 
            (st.session_state.price_change_min, st.session_state.price_change_max),
            step=0.5,
            key="price_change_slider",
            help="Dra slidern eller använd textfälten ovanför för att ange intervall. Exempel: 5-15% = aktier som gått upp 5-15%, -10% till -5% = aktier som fallit 5-10%."
        )
        
        # Uppdatera session_state när slidern ändras
        st.session_state.price_change_min = price_change_range[0]
        st.session_state.price_change_max = price_change_range[1]
        
        # Volymfilter (valfritt)
        use_volume_filter = st.sidebar.checkbox(
            "📊 Filtrera på volym",
            help="Aktivera för att bara visa aktier med ovanlig volym. Hög volym + uppgång = stark signal, låg volym + uppgång = svag signal. Perfekt för att hitta breakouts på hög volym."
        )
        
        if use_volume_filter:
            # Initiera session_state för volym om det inte finns
            if 'volume_threshold_value' not in st.session_state:
                st.session_state.volume_threshold_value = 100
            
            volume_threshold_input = st.sidebar.number_input(
                "Min. relativ volym (%)",
                min_value=0,
                max_value=500,
                value=st.session_state.volume_threshold_value,
                step=10,
                key="volume_threshold_input",
                help="Skriv in eller ändra minimum relativ volym (t.ex. 150 för 150%)"
            )
            st.session_state.volume_threshold_value = volume_threshold_input
            
            volume_threshold = st.sidebar.slider(
                "Min. relativ volym (%)",
                0, 500, 
                st.session_state.volume_threshold_value,
                step=10,
                key="volume_threshold_slider",
                help="Dra slidern eller använd textfältet ovanför. 100% = normal volym, 150% = 50% mer än normalt, 200% = dubbel volym. Högre värden = bara aktier med ovanligt hög omsättning (breakouts, nyheter)."
            )
            
            # Uppdatera session_state när slidern ändras
            st.session_state.volume_threshold_value = volume_threshold
        else:
            volume_threshold = None
    else:
        price_change_period = None
        price_change_range = None
        volume_threshold = None
    
    st.sidebar.markdown("---")
    
    # Snabb sökning-läge
    st.sidebar.markdown("### ⚡ Prestanda")
    snabb_sokning = st.sidebar.checkbox(
        "Snabb sökning (skippa händelser)", 
        value=False,
        help="Mycket snabbare (10-20x) men ingen nyhetssökning. Perfekt för explorativ sökning!"
    )
    
    st.sidebar.markdown("---")
    
    # Händelser (expanderbar sektion)
    st.sidebar.markdown("### 📰 Händelser")
    with st.sidebar.expander("Visa händelsefilter", expanded=False):
        # Inaktivera händelsefilter om snabb sökning är på
        if snabb_sokning:
            st.info("🚀 Snabb sökning aktiverad - händelsefilter inaktiverade")
            check_vinstvarning = False
            check_rapport = False
            check_insider = False
            check_ny_vd = False
        else:
            check_vinstvarning = st.checkbox(
                "⚠️ Vinstvarning",
                help="Hitta aktier som har varnat för sämre resultat eller sänkt prognos. Inkluderar både hårda varningar och mjukare 'resultatuppdateringar'."
            )
            check_rapport = st.checkbox(
                "📊 Rapport (30 dagar)",
                help="Hitta aktier som har eller kommer att släppa kvartals-/årsrapport inom de närmaste 30 dagarna. Bra för att hitta aktier inför earnings."
            )
            check_insider = st.checkbox(
                "👤 Insider",
                help="Hitta aktier där insiders (VD, styrelse, större ägare) har köpt eller sålt aktier. Insiderköp kan vara ett positivt tecken."
            )
            check_ny_vd = st.checkbox(
                "🎯 Ny VD",
                help="Hitta aktier som har fått ny VD eller ledningsändringar. Nya ledare kan innebära strategiförändringar och aktiekursrörelser."
            )
    
    st.sidebar.subheader("📈 Teknisk Trend")
    
    # Initiera session_state för trend
    if 'trend_min' not in st.session_state:
        st.session_state.trend_min = -15
    if 'trend_max' not in st.session_state:
        st.session_state.trend_max = 15
    
    # Skapa två kolumner för min och max input
    col_trend_min, col_trend_max = st.sidebar.columns(2)
    
    with col_trend_min:
        trend_min_input = st.number_input(
            "Min (dagar)",
            min_value=-15,
            max_value=15,
            value=st.session_state.trend_min,
            step=1,
            key="trend_min_input",
            help="Skriv in minsta antal dagar (t.ex. -5 för -5 dagar)"
        )
        st.session_state.trend_min = int(trend_min_input)
    
    with col_trend_max:
        trend_max_input = st.number_input(
            "Max (dagar)",
            min_value=-15,
            max_value=15,
            value=st.session_state.trend_max,
            step=1,
            key="trend_max_input",
            help="Skriv in största antal dagar (t.ex. +10 för +10 dagar)"
        )
        st.session_state.trend_max = int(trend_max_input)
    
    streak_filter = st.sidebar.slider(
        "Trend (Dagar upp/ner)", 
        -15, 15, 
        (st.session_state.trend_min, st.session_state.trend_max),
        key="trend_slider",
        help="Dra slidern eller använd textfälten ovanför. Exempel: +3 till +10 = aktier som stängt uppåt 3-10 dagar i rad. -5 till -1 = aktier som stängt nedåt 1-5 dagar i rad."
    )
    
    # Uppdatera session_state när slidern ändras
    st.session_state.trend_min = streak_filter[0]
    st.session_state.trend_max = streak_filter[1]
    
    # Utvecklingsperiod (alltid synlig)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Utveckling")
    development_period = st.sidebar.selectbox(
        "Tidsperiod",
        ["1 dag", "1 vecka", "1 månad", "3 månader", "6 månader", "12 månader", "3 år", "5 år"],
        index=0,
        help="Välj tidsperiod för utvecklingskolumnen i resultaten. Visar hur mycket aktien har gått upp/ner över den valda perioden. Exempel: '1 månad' visar utveckling senaste månaden, '3 år' visar långsiktig utveckling."
    )
    
    st.sidebar.markdown("---")
    start_btn_sidebar = st.sidebar.button("🔍 Skanna Marknaden", type="primary", use_container_width=True)
    
    # --- SÖKLOGIK ---
    if start_btn_sidebar:
        if not selected_markets:
            st.warning("⚠️ Välj minst en marknad!")
            return
        
        # Beräkna antal aktier baserat på valda marknader och kategorier
        all_tickers = []
        for market in selected_markets:
            if market in selected_categories and selected_categories[market]:
                for category in selected_categories[market]:
                    if category in ticker_lists[market]:
                        all_tickers.extend(ticker_lists[market][category])
        
        # Ta bort duplicater (samma ticker kan finnas i flera kategorier)
        all_tickers = list(set(all_tickers))
        total = len(all_tickers)
        
        if total == 0:
            st.warning("⚠️ Inga kategorier valda! Välj minst en kategori från valda marknader.")
            return
        
        # Estimera scanningstid baserat på filter
        has_events = check_vinstvarning or check_rapport or check_insider or check_ny_vd
        if has_events:
            estimated_time = f"~{total//10}-{total//5}s"
            mode_text = "Händelsesök"
        else:
            estimated_time = f"~{total//50}-{total//25}s"
            mode_text = "Snabb sökning"
        
        # Kompakt status-header
        col_status1, col_status2, col_status3 = st.columns([2, 1, 1])
        with col_status1:
            st.info(f"🔍 Skannar {total} aktier ({mode_text})")
        with col_status2:
            st.metric("Estimerad tid", estimated_time)
        with col_status3:
            st.metric("Batches", f"{(total-1)//50 + 1}")
        
        BATCH_SIZE = 50
        batches = [all_tickers[i:i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]
        num_batches = len(batches)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.empty()
        all_results = []
        start_time = time.time()
        
        for batch_idx, batch in enumerate(batches, 1):
            status_text.caption(f"⚡ Batch {batch_idx}/{num_batches} ({len(batch)} aktier)...")
            progress_bar.progress(batch_idx / num_batches)
            
            batch_data = download_batch_data(batch, batch_idx, num_batches)
            
            if batch_data is not None:
                batch_results = process_batch_results(
                    batch_data, batch, market_cap_range_values, streak_filter,
                    check_vinstvarning, check_rapport, check_insider, check_ny_vd,
                    use_price_change, price_change_period, price_change_range,
                    volume_threshold, development_period
                )
                all_results.extend(batch_results)
                
                if all_results:
                    elapsed_so_far = time.time() - start_time
                    results_container.info(f"✅ Hittills: {len(all_results)} matchande ({elapsed_so_far:.1f}s)")
        
        status_text.empty()
        progress_bar.empty()
        results_container.empty()
        elapsed_time = time.time() - start_time
        
        if len(all_results) > 0:
            # Sortera efter momentum-score (högst först)
            all_results_sorted = sorted(all_results, key=lambda x: x.get('Momentum', 0), reverse=True)
            display_results = all_results_sorted[:100]
            
            # Visa resultat med bättre layout
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("Hittade aktier", len(all_results))
            with col_stats2:
                st.metric("Visas", min(100, len(all_results)))
            with col_stats3:
                st.metric("Tid", f"{elapsed_time:.1f}s")
            
            st.info(f"📊 Sorterade efter momentum-score (högst först). Top {min(100, len(all_results))} visas.")
            st.markdown("---")
            
            df_results = pd.DataFrame(display_results)
            
            # Förbättra kolumnordning - viktigaste först
            priority_order = ['Ticker', 'Momentum', 'Marknad', 'Pris', 'Dagens stängning', 
                            'Utveckling', 'Relativ Volym', 'Volymspik', 'Gap', 'Breakout', 
                            'Trend (Dagar)', 'Förändring', 'Händelser']
            
            # Sortera kolumner enligt prioritet, lägg resten i slutet
            existing_cols = list(df_results.columns)
            ordered_cols = []
            for col in priority_order:
                # Hitta matchande kolumner (kan vara med valuta eller period)
                matches = [c for c in existing_cols if col.lower() in c.lower() or c.startswith(col)]
                if matches:
                    ordered_cols.extend(matches)
                    existing_cols = [c for c in existing_cols if c not in matches]
            
            # Lägg till resterande kolumner (exkludera Ticker_URL från visningen)
            ordered_cols.extend([c for c in existing_cols if c not in ordered_cols and c != 'Ticker_URL'])
            # Filtrera ordered_cols så att bara kolumner som finns i df_results används
            ordered_cols = [col for col in ordered_cols if col in df_results.columns]
            df_results = df_results[ordered_cols]
            
            # Förbered Yahoo Finance länkar för ticker-kolumnen
            # Vi behåller Ticker_URL för att använda med column_config
            
            # Färgkoda kolumner med stängning/utveckling
            def color_cells(val):
                if pd.isna(val) or val == "N/A":
                    return ''
                if isinstance(val, str) and '%' in val:
                    try:
                        # Extrahera numeriskt värde
                        num_str = val.replace('%', '').replace('+', '').strip()
                        num_val = float(num_str)
                        
                        # Grönt för positiva värden
                        if num_val > 0:
                            return 'background-color: #d4edda; color: #155724;'  # Grönt
                        # Rött för negativa värden
                        elif num_val < 0:
                            return 'background-color: #f8d7da; color: #721c24;'  # Rött
                        # Grått för oförändrat
                        else:
                            return 'background-color: #e2e3e5; color: #383d41;'  # Grått
                    except:
                        return ''
                # Färgkoda Momentum-score
                if isinstance(val, (int, float)):
                    if val >= 70:
                        return 'background-color: #d4edda; color: #155724; font-weight: bold;'  # Mörkgrönt för högt momentum
                    elif val >= 50:
                        return 'background-color: #c3e6cb; color: #155724;'  # Ljusgrönt för medelhögt
                    elif val >= 30:
                        return 'background-color: #fff3cd; color: #856404;'  # Gul för medel
                    else:
                        return 'background-color: #f8d7da; color: #721c24;'  # Rött för lågt
                return ''
            
            # Lägg till klickbara länkar till Yahoo Finance
            column_config = {}
            if 'Ticker' in df_results.columns and 'Ticker_URL' in df_results.columns:
                try:
                    # Försök använda Streamlit's LinkColumn (Streamlit >= 1.23.0)
                    df_results['🔗'] = df_results['Ticker_URL']
                    column_config['🔗'] = st.column_config.LinkColumn(
                        "Yahoo Finance",
                        help="Klicka för att öppna på Yahoo Finance",
                        display_text="Öppna"
                    )
                    # Ta bort Ticker_URL från visningen och ordered_cols
                    df_results = df_results.drop(columns=['Ticker_URL'])
                    ordered_cols = [col for col in ordered_cols if col != 'Ticker_URL']
                    # Uppdatera ordered_cols - lägg till länk-kolumnen efter Ticker
                    if 'Ticker' in ordered_cols:
                        ticker_idx = ordered_cols.index('Ticker')
                        ordered_cols.insert(ticker_idx + 1, '🔗')
                    else:
                        ordered_cols.insert(0, '🔗')
                    # Filtrera ordered_cols så att bara kolumner som finns i df_results används
                    ordered_cols = [col for col in ordered_cols if col in df_results.columns]
                    df_results = df_results[ordered_cols]
                except AttributeError:
                    # Fallback för äldre Streamlit-versioner: Lägg till länkar i en separat kolumn
                    df_results['🔗 Länk'] = df_results.apply(
                        lambda row: f"[Öppna]({row['Ticker_URL']})",
                        axis=1
                    )
                    df_results = df_results.drop(columns=['Ticker_URL'])
                    # Ta bort Ticker_URL från ordered_cols
                    ordered_cols = [col for col in ordered_cols if col != 'Ticker_URL']
                    # Uppdatera ordered_cols
                    if 'Ticker' in ordered_cols:
                        ticker_idx = ordered_cols.index('Ticker')
                        ordered_cols.insert(ticker_idx + 1, '🔗 Länk')
                    else:
                        ordered_cols.insert(0, '🔗 Länk')
                    # Filtrera ordered_cols så att bara kolumner som finns i df_results används
                    ordered_cols = [col for col in ordered_cols if col in df_results.columns]
                    df_results = df_results[ordered_cols]
            
            # Applicera styling på relevanta kolumner
            color_columns = [col for col in df_results.columns if 'stängning' in col or 'Utveckling' in col or 'Förändring' in col or col == 'Momentum']
            if color_columns:
                styled_df = df_results.style.applymap(
                    color_cells,
                    subset=color_columns
                ).format({
                    'Momentum': '{:.0f}'  # Visa momentum som heltal
                }, na_rep='N/A')
                # Använd column_config om det finns länkar
                if column_config:
                    st.dataframe(styled_df, use_container_width=True, height=600, column_config=column_config)
                else:
                    st.dataframe(styled_df, use_container_width=True, height=600)
            else:
                if column_config:
                    st.dataframe(df_results, use_container_width=True, height=600, column_config=column_config)
                else:
                    st.dataframe(df_results, use_container_width=True, height=600)
            
            st.markdown("---")
            csv = df_results.to_csv(index=False).encode('utf-8')
            col_dl1, col_dl2 = st.columns([1, 4])
            with col_dl1:
                st.download_button("📥 Ladda ner CSV", csv, "resultat.csv", "text/csv", use_container_width=True)
        else:
            st.warning("⚠️ Inga aktier matchade dina filter. Prova att ändra filterinställningarna.")
    else:
        st.info("👈 **Kom igång:** Välj marknad och kategorier i sidebar, sedan klicka på 'Skanna Marknaden'")
        st.markdown("""
        ### 💡 Snabbtips:
        - **Snabb sökning** = 10-20x snabbare (rekommenderas för första sökningen)
        - **Momentum-score** = Automatisk sortering efter starkaste signaler
        - **Volymspikar** = Identifierar ovanligt hög omsättning
        - **Breakouts** = Hitta aktier som bryter genom viktiga prisnivåer
        """)
    

if __name__ == "__main__":
    main()