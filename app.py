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

@st.cache_data(ttl=1800)  # Cache i 30 minuter
def check_cision_news(ticker_symbol, keywords_list, days_back=30):
    """
    Söker i Cision press releases för SVENSKA bolag.
    Mycket mer pålitlig än Yahoo Finance för svenska pressmeddelanden!
    """
    try:
        # Ta bort .ST från ticker för att få bolagsnamn
        company_code = ticker_symbol.replace('.ST', '')
        
        # Cision URL för svenska pressmeddelanden
        # Format: https://news.cision.com/se/[företag]/r/
        # Vi söker via deras search API
        search_url = f"https://news.cision.com/se/search/pressreleases?keywords={company_code}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Hitta pressmeddelanden
        press_releases = soup.find_all('div', class_='feed-item')
        
        cutoff_date = datetime.now()
        
        for release in press_releases[:15]:  # Kolla senaste 15
            try:
                # Hitta titel
                title_elem = release.find('h3') or release.find('a', class_='title')
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True).lower()
                
                # Hitta även beskrivning/summary om den finns
                summary_elem = release.find('p') or release.find('div', class_='description')
                summary = summary_elem.get_text(strip=True).lower() if summary_elem else ""
                
                # Kombinera titel + summary för sökning
                search_text = f"{title} {summary}"
                
                # Hitta datum
                date_elem = release.find('time') or release.find('span', class_='date')
                if date_elem:
                    date_str = date_elem.get('datetime', date_elem.get_text(strip=True))
                    try:
                        if 'T' in date_str:
                            pub_date = datetime.fromisoformat(date_str.replace('Z', ''))
                        else:
                            # Försök parse svenska datum
                            pub_date = datetime.strptime(date_str, '%Y-%m-%d')
                    except:
                        continue
                    
                    days_diff = (cutoff_date - pub_date).days
                    if days_diff > days_back or days_diff < 0:
                        continue
                else:
                    continue
                
                # Sök efter nyckelord i både titel OCH summary
                for keyword in keywords_list:
                    if keyword.lower() in search_text:
                        link_elem = release.find('a')
                        link = link_elem.get('href', '') if link_elem else ''
                        if link and not link.startswith('http'):
                            link = f"https://news.cision.com{link}"
                        
                        return {
                            'title': title_elem.get_text(strip=True),
                            'link': link,
                            'publisher': 'Cision',
                            'date': pub_date
                        }
            except Exception as e:
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
            
            # Hämta valuation metrics (om valt)
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
            
            # --- HÄNDELSE-FILTRERING (HYBRID: Cision för SE, Yahoo för US/CA) ---
            news_hits = []
            is_swedish = ticker.endswith('.ST')
            
            # Välj rätt nyhetskälla baserat på marknad
            news_checker = check_cision_news if is_swedish else check_yf_news
            
            if check_vinstvarning:
                warning_keywords = []
                if is_swedish:
                    warning_keywords = [
                        'vinstvarning', 'sänker prognos', 'nedjusterar', 'varning',
                        'nedrevidera', 'justerar ned', 'sänker',
                        'resultatuppdatering', 'reviderad prognos', 'omvärderar',
                        'försämrad', 'svagare', 'lägre än väntat', 'utmaning',
                        'preliminärt resultat', 'handelsuppdatering',
                        'uppdatering av finansiella mål', 'prognosjustering'
                    ]
                else:
                    warning_keywords = [
                        'profit warning', 'lowers guidance', 'downgrade', 
                        'misses', 'weak results', 'below expectations',
                        'result update', 'revised guidance', 'challenges',
                        'trading update', 'preliminary results',
                        'guidance update', 'financial update'
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
            
            results.append({
                "Ticker": ticker,
                "Marknad": market,
                f"Pris ({currency})": round(price, 2),
                "P/E": round(pe, 2) if pe else "N/A",
                "P/B": round(pb, 2) if pb else "N/A",
                "Trend (Dagar)": streak,
                "Händelser": news_text
            })
            
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
    
    use_pe_filter = st.sidebar.checkbox("Använd P/E-filter")
    pe_range = st.sidebar.slider("P/E-tal", 0.0, 50.0, (0.0, 50.0)) if use_pe_filter else None
    
    use_pb_filter = st.sidebar.checkbox("Använd P/B-filter")
    pb_range = st.sidebar.slider("P/B-tal", 0.0, 10.0, (0.0, 10.0)) if use_pb_filter else None
    
    st.sidebar.subheader("📰 Händelser")
    check_vinstvarning = st.sidebar.checkbox("⚠️ Vinstvarning")
    check_rapport = st.sidebar.checkbox("📊 Rapport (30 dagar)")
    check_insider = st.sidebar.checkbox("👤 Insider")
    check_ny_vd = st.sidebar.checkbox("🎯 Ny VD")
    
    st.sidebar.subheader("📈 Teknisk Trend")
    streak_filter = st.sidebar.slider("Trend (Dagar upp/ner)", -15, 15, (-15, 15))
    
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
        
        st.info(f"🚀 Skannar {total} aktier...")
        
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
                    batch_data, batch, price_range, pe_range, pb_range,
                    use_pe_filter, use_pb_filter, streak_filter,
                    check_vinstvarning, check_rapport, check_insider, check_ny_vd
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