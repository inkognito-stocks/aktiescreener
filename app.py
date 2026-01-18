import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
from tickers import ticker_lists

# --- Inställningar ---
st.set_page_config(page_title="AktieScreener Global", layout="wide")

# --- Batch Download Functions ---

@st.cache_data(ttl=2700)  # Cache i 45 minuter
def download_batch_data(tickers_batch, batch_num, total_batches):
    """
    Laddar ner data för en batch av tickers samtidigt.
    Mycket snabbare än att hämta en i taget!
    """
    try:
        # Download price data for all tickers in batch
        data = yf.download(
            tickers_batch,
            period="1mo",
            group_by='ticker',
            threads=True,
            progress=False
        )
        
        time.sleep(1)  # Rate limiting
        return data
    except Exception as e:
        st.warning(f"Batch {batch_num}/{total_batches} failed: {e}")
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
    Söker i Yahoo Finance press releases och nyheter för en ticker
    efter specifika nyckelord.
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

def process_batch_results(data, tickers_in_batch, price_range, pe_range, pb_range, 
                          use_pe, use_pb, streak_filter, check_vinstvarning, check_rapport,
                          check_insider, check_ny_vd):
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
            
            # Hämta valuation metrics (behöver enskild request, men bara för filtrerade)
            pe, pb = None, None
            if use_pe or use_pb:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    pe = info.get('trailingPE', None)
                    pb = info.get('priceToBook', None)
                except:
                    pass
            
            # P/E filter
            if use_pe and pe_range:
                if pe is None or not (pe_range[0] <= pe <= pe_range[1]):
                    continue
            
            # P/B filter
            if use_pb and pb_range:
                if pb is None or not (pb_range[0] <= pb <= pb_range[1]):
                    continue
            
            # --- HÄNDELSE-FILTRERING ---
            news_hits = []
            is_swedish = ticker.endswith('.ST')
            
            if check_vinstvarning:
                warning_keywords = []
                if is_swedish:
                    warning_keywords = [
                        'vinstvarning', 'sänker prognos', 'nedjusterar', 'varning',
                        'profit warning', 'lowers', 'lower', 'cuts', 'reduces', 'downgrade', 
                        'warning', 'miss', 'disappoints', 'weak', 'below expectations'
                    ]
                else:
                    warning_keywords = [
                        'profit warning', 'lowers guidance', 'lower guidance', 'cuts guidance',
                        'downgrade', 'warning', 'miss', 'misses', 'disappoints', 'weak results',
                        'below expectations', 'reduces'
                    ]
                
                yf_hit = check_yf_news(ticker, warning_keywords, days_back=30)
                if yf_hit:
                    news_hits.append(f"⚠️ Vinstvarning")
                else:
                    continue  # Vinstvarning krävdes men hittades inte
            
            if check_rapport:
                earnings_info = check_earnings_date(ticker, days_range=30)
                if earnings_info:
                    news_hits.append(f"📊 {earnings_info}")
                else:
                    report_keywords = []
                    if is_swedish:
                        report_keywords = ['kvartalsrapport', 'delårsrapport', 'Q1', 'Q2', 'Q3', 'Q4', 'earnings']
                    else:
                        report_keywords = ['earnings', 'quarterly results', 'reports', 'Q1', 'Q2', 'Q3', 'Q4']
                    
                    yf_hit = check_yf_news(ticker, report_keywords, days_back=30)
                    if yf_hit:
                        news_hits.append(f"📊 Rapport")
            
            if check_insider:
                insider_keywords = []
                if is_swedish:
                    insider_keywords = ['insider', 'köper', 'säljer', 'styrelse köp', 'vd köp']
                else:
                    insider_keywords = ['insider', 'insider buying', 'CEO bought', 'director bought']
                
                yf_hit = check_yf_news(ticker, insider_keywords, days_back=30)
                if yf_hit:
                    news_hits.append(f"👤 Insider")
            
            if check_ny_vd:
                vd_keywords = []
                if is_swedish:
                    vd_keywords = ['ny vd', 'vd avgår', 'utsedd vd', 'ny ceo']
                else:
                    vd_keywords = ['new ceo', 'ceo appointed', 'ceo resigns', 'management change']
                
                yf_hit = check_yf_news(ticker, vd_keywords, days_back=60)
                if yf_hit:
                    news_hits.append(f"🎯 Ledning")
            
            # Avgör valuta och marknad
            market = get_market_from_ticker(ticker)
            if market == 'Sverige 🇸🇪':
                currency = "SEK"
            elif market == 'Kanada 🇨🇦':
                currency = "CAD"
            else:
                currency = "USD"
            
            news_text = " | ".join(news_hits) if news_hits else "Ingen händelse"
            
            # Lägg till resultat
            results.append({
                "Ticker": ticker,
                "Marknad": market,
                f"Pris ({currency})": round(price, 2),
                "P/E": round(pe, 2) if pe else "N/A",
                "P/B": round(pb, 2) if pb else "N/A",
                "Trend (Dagar)": streak,
                "Händelser": news_text
            })
            
        except Exception as e:
            continue
    
    return results

# --- Huvudapplikation ---

def main():
    st.title("🌍 Global AktieScreener")
    st.markdown("Scanna aktier från **Sverige, Kanada och USA** med avancerade filter")
    
    # --- SIDEBAR ---
    st.sidebar.header("🎯 Filterinställningar")
    
    # --- MARKNADSVAL ---
    st.sidebar.subheader("🌍 Välj Marknader")
    
    all_markets = list(ticker_lists.keys())
    selected_markets = st.sidebar.multiselect(
        "Marknader att scanna",
        options=all_markets,
        default=["Sverige 🇸🇪"],
        help="Välj vilka marknader du vill scanna. Fler marknader = längre scanningstid"
    )
    
    # Välj kategorier baserat på valda marknader
    selected_categories = {}
    total_tickers_estimated = 0
    
    if selected_markets:
        for market in selected_markets:
            categories = list(ticker_lists[market].keys())
            
            # Default: välj bara första kategorin för varje marknad (för snabbhet)
            default_cats = [categories[0]] if categories else []
            
            selected_cats = st.sidebar.multiselect(
                f"Kategorier i {market}",
                options=categories,
                default=default_cats,
                key=f"cat_{market}",
                help=f"Välj kategorier från {market}"
            )
            selected_categories[market] = selected_cats
            
            # Räkna antal tickers
            for cat in selected_cats:
                total_tickers_estimated += len(ticker_lists[market][cat])
    
    if total_tickers_estimated > 0:
        st.sidebar.info(f"📊 Kommer scanna ~{total_tickers_estimated} aktier")
    
    st.sidebar.markdown("---")
    
    # --- PRISFILTER ---
    st.sidebar.subheader("💰 Pris")
    price_range = st.sidebar.slider(
        "Prisintervall (alla valutor)", 
        min_value=0, 
        max_value=2000, 
        value=(0, 2000), 
        step=10,
        help="Jämför SEK, CAD, USD direkt (1:1 för enkelhetens skull)"
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
        help="Söker i Yahoo Finance press releases efter vinstvarningar"
    )
    check_rapport = st.sidebar.checkbox(
        "📊 Rapport släppt/på väg (30 dagar)",
        help="Söker efter kvartalsrapporter i Yahoo Finance"
    )
    check_insider = st.sidebar.checkbox(
        "👤 Insidertransaktioner",
        help="Söker efter insiderköp och insiderförsäljning"
    )
    check_ny_vd = st.sidebar.checkbox(
        "🎯 Ny VD/ledning",
        help="Söker efter VD-byten och ledningsförändringar"
    )
    
    # --- TEKNISK TREND ---
    st.sidebar.subheader("📈 Teknisk Trend")
    streak_filter = st.sidebar.slider("Trend (Dagar upp/ner)", -15, 15, (-15, 15))
    
    st.sidebar.markdown("---")
    start_btn = st.sidebar.button("🔍 Skanna Marknaden", type="primary", use_container_width=True)
    
    # --- SÖKLOGIK ---
    if start_btn:
        if not selected_markets:
            st.warning("⚠️ Välj minst en marknad att scanna!")
            return
        
        # Bygg lista över alla tickers
        all_tickers = []
        for market in selected_markets:
            if market in selected_categories:
                for category in selected_categories[market]:
                    all_tickers.extend(ticker_lists[market][category])
        
        # Ta bort duplicates
        all_tickers = list(set(all_tickers))
        total = len(all_tickers)
        
        if total == 0:
            st.warning("⚠️ Inga kategorier valda!")
            return
        
        st.info(f"🚀 Skannar {total} aktier med batch-download (snabbt!)...")
        
        # Dela upp i batches
        BATCH_SIZE = 50
        batches = [all_tickers[i:i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]
        num_batches = len(batches)
        
        st.write(f"📦 Delar upp i {num_batches} batches (max {BATCH_SIZE} aktier/batch)")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.empty()
        
        all_results = []
        start_time = time.time()
        
        # Processa varje batch
        for batch_idx, batch in enumerate(batches, 1):
            status_text.text(f"⚡ Processar batch {batch_idx}/{num_batches} ({len(batch)} aktier)...")
            progress_bar.progress(batch_idx / num_batches)
            
            # Download data för denna batch
            batch_data = download_batch_data(batch, batch_idx, num_batches)
            
            if batch_data is not None:
                # Processa resultaten
                batch_results = process_batch_results(
                    batch_data, 
                    batch,
                    price_range,
                    pe_range,
                    pb_range,
                    use_pe_filter,
                    use_pb_filter,
                    streak_filter,
                    check_vinstvarning,
                    check_rapport,
                    check_insider,
                    check_ny_vd
                )
                all_results.extend(batch_results)
                
                # Visa preliminära resultat
                if all_results:
                    results_container.success(f"✅ Hittills: {len(all_results)} matchande aktier")
        
        status_text.empty()
        progress_bar.empty()
        results_container.empty()
        
        elapsed_time = time.time() - start_time
        
        # --- VISA RESULTAT ---
        if len(all_results) > 0:
            # Begränsa till max 100 resultat
            display_results = all_results[:100]
            
            st.success(f"✅ Hittade {len(all_results)} aktier som matchar på {elapsed_time:.1f} sekunder!")
            
            if len(all_results) > 100:
                st.info(f"📌 Visar topp 100 av {len(all_results)} resultat")
            
            df_results = pd.DataFrame(display_results)
            
            # Visa statistik
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Antal aktier", len(all_results))
            with col2:
                markets_found = df_results['Marknad'].nunique()
                st.metric("Marknader", markets_found)
            with col3:
                positive_trend = len([r for r in all_results if r['Trend (Dagar)'] > 0])
                st.metric("Positiv trend", f"{positive_trend}")
            with col4:
                st.metric("Scanningstid", f"{elapsed_time:.1f}s")
            
            # Visa tabell
            st.dataframe(
                df_results,
                use_container_width=True,
                height=600
            )
            
            # Export
            csv = df_results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Ladda ner resultat (CSV)",
                data=csv,
                file_name=f"global_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
        else:
            st.warning("⚠️ Inga aktier matchade dina filter. Prova att justera kriterierna.")
    
    else:
        st.info("👈 Justera filtren till vänster och tryck på 'Skanna Marknaden'")
        
        # Visa info om marknader
        st.markdown("### 📊 Tillgängliga Marknader")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Sverige 🇸🇪")
            for cat, tickers in ticker_lists["Sverige 🇸🇪"].items():
                st.write(f"• {cat}: {len(tickers)} aktier")
        
        with col2:
            st.markdown("#### Kanada 🇨🇦")
            for cat, tickers in ticker_lists["Kanada 🇨🇦"].items():
                st.write(f"• {cat}: {len(tickers)} aktier")
        
        with col3:
            st.markdown("#### USA 🇺🇸")
            for cat, tickers in ticker_lists["USA 🇺🇸"].items():
                st.write(f"• {cat}: {len(tickers)} aktier")

if __name__ == "__main__":
    main()
