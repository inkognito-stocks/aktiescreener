import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tickers import ticker_lists  # Importera ticker-lista från separat fil

# --- Inställningar ---
st.set_page_config(page_title="AktieScreener AI", layout="wide")

# --- Hjälpfunktioner ---

@st.cache_data(ttl=2700)  # Cache i 45 minuter (undvik Yahoo Finance rate limiting)
def get_cached_stock_data(ticker_symbol):
    """Hämtar grundläggande aktiedata och cachar det"""
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period="1d")
        info = stock.info
        
        price = hist['Close'].iloc[-1] if not hist.empty else 0
        
        return {
            'price': float(price),
            'pe': info.get('trailingPE', None),
            'pb': info.get('priceToBook', None),
            'ticker': ticker_symbol
        }
    except:
        return None

@st.cache_data(ttl=2700)  # Cache i 45 minuter (undvik Yahoo Finance rate limiting)
def get_streak(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1mo", progress=False)
        if len(df) < 5:
            return 0
        
        # Hantera dataformatet från yfinance
        closes = df['Close']
        if isinstance(closes, pd.DataFrame):
            closes = closes.iloc[:, 0]  # Välj första kolumnen om det är en DataFrame
            
        values = closes.values
        
        streak = 0
        for i in range(len(values) - 1, 0, -1):
            today = values[i]
            yesterday = values[i-1]
            
            if today > yesterday:
                if streak < 0: break
                streak += 1
            elif today < yesterday:
                if streak > 0: break
                streak -= 1
            else:
                break
        return streak
    except Exception as e:
        return 0

def check_yf_news(ticker_symbol, keywords_list, days_back=30):
    """
    Söker i Yahoo Finance press releases och nyheter för en ticker
    efter specifika nyckelord.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        news = stock.news
        
        if not news:
            return None
        
        # Filtrera nyheter från senaste X dagarna (gör båda timezone-aware eller naive)
        cutoff_date = datetime.now()
        
        for article in news:
            # Hantera både gamla och nya strukturer från yfinance
            content = article.get('content', article)
            
            # Kontrollera publiceringsdatum
            pub_timestamp = content.get('providerPublishTime', article.get('providerPublishTime', 0))
            if pub_timestamp == 0:
                # Försök hämta från pubDate om providerPublishTime saknas
                pub_date_str = content.get('pubDate', '')
                if pub_date_str:
                    try:
                        # Parse ISO date och ta bort timezone info för enklare jämförelse
                        pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                        pub_date = pub_date.replace(tzinfo=None)  # Gör naive för jämförelse
                    except:
                        continue
                else:
                    continue
            else:
                pub_date = datetime.fromtimestamp(pub_timestamp)
            
            # Kontrollera om nyheten är inom tidsperioden
            days_diff = (cutoff_date - pub_date).days
            if days_diff > days_back or days_diff < 0:
                continue
            
            # Hämta title och summary från rätt plats
            title = content.get('title', '').lower()
            summary = content.get('summary', '').lower()
            
            # Sök efter nyckelord i titel OCH summary för bättre träffsäkerhet
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


def get_valuation_metrics(ticker_symbol):
    """Hämtar värderingsdata för en aktie"""
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        return {
            'pe': info.get('trailingPE', None),
            'pb': info.get('priceToBook', None),
            'ps': info.get('priceToSalesTrailing12Months', None),
            'ev_ebitda': info.get('enterpriseToEbitda', None),
            'market_cap': info.get('marketCap', None)
        }
    except:
        return {'pe': None, 'pb': None, 'ps': None, 'ev_ebitda': None, 'market_cap': None}

def check_earnings_date(ticker_symbol, days_range=30):
    """Kontrollerar om rapport ska släppas inom X dagar eller släpptes nyligen"""
    try:
        stock = yf.Ticker(ticker_symbol)
        
        # Försök få rapportdatum
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

def process_single_ticker(symbol, price_range, use_pe_filter, pe_range, use_pb_filter, pb_range, 
                          streak_filter, check_vinstvarning, check_rapport, check_insider, check_ny_vd):
    """Processar en ticker och returnerar resultat eller None"""
    try:
        # Hämta grunddata (cachad)
        basic_data = get_cached_stock_data(symbol)
        if not basic_data:
            return None
        
        price = basic_data['price']
        
        # Filter: Pris (snabbt - skippa tidigt)
        if not (price_range[0] <= price <= price_range[1]):
            return None
        
        # Hämta streak
        streak = get_streak(symbol)
        
        # Filter: Trend (snabbt - skippa tidigt)
        min_streak, max_streak = streak_filter
        if not (min_streak <= streak <= max_streak):
            return None
        
        # Hämta värderingsdata
        pe = basic_data['pe']
        pb = basic_data['pb']
        
        # Filter: P/E
        if use_pe_filter and pe_range:
            if pe is None or not (pe_range[0] <= pe <= pe_range[1]):
                return None
        
        # Filter: P/B
        if use_pb_filter and pb_range:
            if pb is None or not (pb_range[0] <= pb <= pb_range[1]):
                return None
        
        # Nu hämtar vi bara nyheter om vi behöver (långsammast)
        news_hits = []
        is_swedish = symbol.endswith('.ST')
        is_canadian = symbol.endswith('.TO') or symbol.endswith('.V') or symbol.endswith('.CN')
        
        if check_vinstvarning:
            warning_keywords = []
            if is_swedish:
                # För svenska bolag: använd BÅDE svenska OCH engelska ord (Yahoo Finance ger ofta engelska artiklar)
                warning_keywords = [
                    'vinstvarning', 'sänker prognos', 'nedjusterar', 'varning', 'vinstvarning',
                    'profit warning', 'lowers', 'lower', 'cuts', 'reduces', 'downgrade', 
                    'warning', 'miss', 'disappoints', 'weak', 'below expectations'
                ]
            else:
                warning_keywords = [
                    'profit warning', 'lowers guidance', 'lower guidance', 'cuts guidance',
                    'downgrade', 'warning', 'miss', 'misses', 'disappoints', 'weak results',
                    'below expectations', 'reduces'
                ]
            
            yf_hit = check_yf_news(symbol, warning_keywords, days_back=30)
            if yf_hit:
                news_hits.append(f"⚠️ {yf_hit['title'][:50]}...")
            else:
                return None  # Vinstvarning krävdes men hittades inte
        
        if check_rapport:
            earnings_info = check_earnings_date(symbol, days_range=30)
            if earnings_info:
                news_hits.append(f"📊 {earnings_info}")
            else:
                report_keywords = []
                if is_swedish:
                    report_keywords = ['kvartalsrapport', 'delårsrapport', 'Q1', 'Q2', 'Q3', 'Q4', 'earnings']
                else:
                    report_keywords = ['earnings', 'quarterly results', 'reports', 'Q1', 'Q2', 'Q3', 'Q4']
                
                yf_hit = check_yf_news(symbol, report_keywords, days_back=30)
                if yf_hit:
                    news_hits.append(f"📊 Rapport")
        
        if check_insider:
            insider_keywords = []
            if is_swedish:
                insider_keywords = ['insider', 'köper', 'säljer', 'styrelse köp', 'vd köp', 'ledning köp', 
                                   'insiderhandel', 'förvärvat', 'avyttrat']
            else:
                insider_keywords = ['insider', 'insider buying', 'insider selling', 'CEO bought', 
                                   'director bought', 'executive bought', 'purchased', 'sold shares']
            
            yf_hit = check_yf_news(symbol, insider_keywords, days_back=30)
            if yf_hit:
                news_hits.append(f"👤 Insider: {yf_hit['title'][:40]}...")
        
        if check_ny_vd:
            vd_keywords = []
            if is_swedish:
                vd_keywords = ['ny vd', 'vd avgår', 'tillträder', 'utsedd vd', 'ny ledning', 
                               'ny ceo', 'ceo lämnar', 'styrelseordförande']
            else:
                vd_keywords = ['new ceo', 'ceo appointed', 'ceo resigns', 'ceo steps down', 
                               'new chief executive', 'executive changes', 'management change', 
                               'appointed ceo', 'named ceo']
            
            yf_hit = check_yf_news(symbol, vd_keywords, days_back=60)
            if yf_hit:
                news_hits.append(f"🎯 Ledning: {yf_hit['title'][:40]}...")
        
        # Avgör valuta
        if symbol.endswith('.ST'):
            currency = "SEK"
        elif symbol.endswith('.TO') or symbol.endswith('.V') or symbol.endswith('.CN'):
            currency = "CAD"
        else:
            currency = "USD"
        
        news_text = " | ".join(news_hits) if news_hits else "Ingen specifik händelse"
        
        return {
            "Ticker": symbol,
            f"Pris ({currency})": round(float(price), 2),
            "P/E": round(pe, 2) if pe else "N/A",
            "P/B": round(pb, 2) if pb else "N/A",
            "Trend (Dagar)": streak,
            "Händelser": news_text
        }
    except Exception as e:
        return None

# --- Huvudapplikation ---

def main():
    st.title("🔎 Börs-Sök (Prototyp)")
    st.markdown("Hitta bolag baserat på pris, trend, värdering och **nyhetshändelser**.")

    # --- SIDEBAR ---
    st.sidebar.header("🎯 Filterinställningar")

    # --- MARKNAD & KATEGORI ---
    st.sidebar.subheader("🌍 Välj Marknader")
    
    # Skapa en lista över alla tillgängliga marknader
    all_markets = list(ticker_lists.keys())
    selected_markets = st.sidebar.multiselect(
        "Marknader att scanna",
        options=all_markets,
        default=["Sverige 🇸🇪"],
        help="Välj vilka marknader du vill scanna"
    )
    
    # Välj kategorier baserat på valda marknader
    selected_categories = {}
    if selected_markets:
        for market in selected_markets:
            categories = list(ticker_lists[market].keys())
            selected_cats = st.sidebar.multiselect(
                f"Kategorier i {market}",
                options=categories,
                default=categories,
                key=f"cat_{market}"
            )
            selected_categories[market] = selected_cats
    
    st.sidebar.markdown("---")
    
    # --- PRISFILTER ---
    st.sidebar.subheader("💰 Pris")
    
    # Avgör valuta baserat på valda marknader
    has_swedish = any("Sverige" in m for m in selected_markets)
    has_canadian = any("Kanada" in m for m in selected_markets)
    has_us = any("USA" in m for m in selected_markets)
    
    price_range = st.sidebar.slider(
        "Prisintervall (alla valutor)", 
        min_value=0, 
        max_value=2000, 
        value=(0, 2000), 
        step=10,
        help="Välj prisintervall. OBS: Jämför SEK, CAD, USD direkt (1:1)"
    )

    # --- VÄRDERINGSFILTER ---
    st.sidebar.subheader("📊 Värdering")
    use_pe_filter = st.sidebar.checkbox("Använd P/E-filter")
    if use_pe_filter:
        pe_range = st.sidebar.slider("P/E-tal", 0.0, 50.0, (0.0, 50.0), 1.0)
    else:
        pe_range = None
    
    use_pb_filter = st.sidebar.checkbox("Använd P/B-filter")
    if use_pb_filter:
        pb_range = st.sidebar.slider("P/B-tal", 0.0, 10.0, (0.0, 10.0), 0.5)
    else:
        pb_range = None

    # --- HÄNDELSER ---
    st.sidebar.subheader("📰 Händelser (Press Releases)")
    check_vinstvarning = st.sidebar.checkbox(
        "⚠️ Vinstvarning / Profit Warning", 
        help="Söker i Yahoo Finance press releases efter vinstvarningar, nedgraderings etc."
    )
    check_rapport = st.sidebar.checkbox(
        "📊 Rapport släppt/på väg (30 dagar)",
        help="Söker efter kvartalsrapporter i Yahoo Finance news och rapportkalender"
    )
    check_insider = st.sidebar.checkbox(
        "👤 Insidertransaktioner",
        help="Söker efter insiderköp och insiderförsäljning i Yahoo Finance press releases"
    )
    check_ny_vd = st.sidebar.checkbox(
        "🎯 Ny VD/ledning",
        help="Söker efter VD-byten och ledningsförändringar i Yahoo Finance press releases"
    )
    
    # --- TEKNISK TREND ---
    st.sidebar.subheader("📈 Teknisk Trend")
    streak_filter = st.sidebar.slider("Trend (Dagar upp/ner)", -15, 15, (-15, 15))

    st.sidebar.markdown("---")
    start_btn = st.sidebar.button("🔍 Skanna Marknaden", type="primary", use_container_width=True)

    # --- LOGIK ---
    if start_btn:
        if not selected_markets:
            st.warning("⚠️ Välj minst en marknad att scanna!")
            return
            
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Bygg en lista över alla tickers att scanna
        tickers_to_scan = []
        for market in selected_markets:
            if market in selected_categories:
                for category in selected_categories[market]:
                    tickers_to_scan.extend(ticker_lists[market][category])
        
        total = len(tickers_to_scan)
        
        if total == 0:
            st.warning("⚠️ Inga kategorier valda. Välj minst en kategori att scanna!")
            return
        
        st.info(f"🚀 Skannar {total} aktier parallellt (mycket snabbare!)...")
        start_time = time.time()
        
        # Använd ThreadPoolExecutor för att processa flera aktier samtidigt
        completed = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Skicka alla jobs
            future_to_ticker = {
                executor.submit(
                    process_single_ticker, 
                    symbol, 
                    price_range, 
                    use_pe_filter, 
                    pe_range, 
                    use_pb_filter, 
                    pb_range,
                    streak_filter, 
                    check_vinstvarning, 
                    check_rapport, 
                    check_insider, 
                    check_ny_vd
                ): symbol for symbol in tickers_to_scan
            }
            
            # Samla resultat när de blir klara
            for future in as_completed(future_to_ticker):
                completed += 1
                symbol = future_to_ticker[future]
                progress_bar.progress(completed / total)
                status_text.text(f"⚡ Analyserat {completed}/{total} aktier...")
                
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    pass  # Skippa aktier som ger fel

        status_text.empty()
        progress_bar.empty()
        
        elapsed_time = time.time() - start_time

        if len(results) > 0:
            # Begränsa till max 40 resultat
            results = results[:40]
            
            st.success(f"✅ Hittade {len(results)} bolag som matchar dina kriterier på {elapsed_time:.1f} sekunder!")
            df_results = pd.DataFrame(results)
            
            # Visa statistik
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Antal bolag", len(results))
            with col2:
                # Hitta priskolumn (den kan heta olika saker beroende på valuta)
                price_cols = [col for col in df_results.columns if col.startswith('Pris (')]
                if price_cols:
                    avg_price = df_results[price_cols[0]].mean()
                    st.metric("Snitt pris", f"{avg_price:.2f}")
                else:
                    st.metric("Snitt pris", "N/A")
            with col3:
                positive_trend = len([r for r in results if r['Trend (Dagar)'] > 0])
                st.metric("Positiv trend", f"{positive_trend}/{len(results)}")
            
            st.dataframe(
                df_results, 
                use_container_width=True,
                height=600
            )
            
            # Exportknapp
            csv = df_results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Ladda ner resultat (CSV)",
                data=csv,
                file_name=f"aktier_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
        else:
            st.warning("⚠️ Inga bolag matchade dina filter. Prova att justera kriterierna.")

    else:
        st.info("Justera filtren till vänster och tryck på 'Skanna Marknaden'.")

if __name__ == "__main__":
    main()