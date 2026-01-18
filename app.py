import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# --- Inställningar ---
st.set_page_config(page_title="AktieScreener AI", layout="wide")

# "THE BEAST" - Uppdaterad med USA 🇺🇸
ticker_lists = {
    "Sverige 🇸🇪": {
        "Large Cap (OMXS30 & Co)": [
            "ABB.ST", "ALFA.ST", "ASSA-B.ST", "AZN.ST", "ATCO-A.ST", "ATCO-B.ST",
            "AXFO.ST", "BOL.ST", "CAST.ST", "ELUX-B.ST", "ERIC-B.ST", "ESSITY-B.ST",
            "EVO.ST", "GETI-B.ST", "HM-B.ST", "SHB-A.ST", "HEXA-B.ST", "HOLM-B.ST",
            "HUSQ-B.ST", "INDT.ST", "INVE-B.ST", "KINN-B.ST", "LATO-B.ST", "LIFCO-B.ST",
            "NIBE-B.ST", "NDA-SE.ST", "SAAB-B.ST", "SAND.ST", "SCA-B.ST", "SEB-A.ST",
            "SECU-B.ST", "SKA-B.ST", "SKF-B.ST", "SWED-A.ST", "TEL2-B.ST", "TELIA.ST",
            "TREL-B.ST", "VOLV-B.ST", "VOLCAR-B.ST", "EQT.ST", "EPI-A.ST", "BALD-B.ST",
            "AZA.ST", "VITR.ST", "THULE.ST", "SINCH.ST", "SBB-B.ST", "WALL-B.ST",
            "LUND-B.ST", "HUFV-A.ST", "BILL.ST", "AAK.ST", "AFRY.ST", "BRAV.ST"
        ],
        "Mid Cap & Small Cap (Blandat)": [
            "ACAD.ST", "ADVE.ST", "ANOD-B.ST", "AQ.ST", "ARJO-B.ST", "ATT.ST", "BACT-B.ST",
            "BEGR.ST", "BETCO.ST", "BHG.ST", "BILI-A.ST", "BIOA-B.ST", "BIOG-B.ST",
            "BIOT.ST", "BONG.ST", "BOOZT.ST", "BOUV.ST", "BTS-B.ST", "BUFAB.ST", "BULT.ST",
            "CALL.ST", "CAMX.ST", "CATE.ST", "CAT-B.ST", "CIBUS.ST", "CLAS-B.ST",
            "COIC.ST", "COLL.ST", "CORE-B.ST", "CTEEK.ST", "DIOS.ST", "DOME.ST", "DOR.ST",
            "DUST.ST", "EAST.ST", "ELOS-B.ST", "ELTEL.ST", "ENRO.ST", "ENQ.ST", "EOLU-B.ST",
            "EPIS-B.ST", "FAG.ST", "FAST.ST", "FING-B.ST", "FMART.ST", "FNM.ST", "GARO.ST",
            "G5EN.ST", "GRNG.ST", "HANZA.ST", "HEBA-B.ST", "HEM.ST", "HEXPOL-B.ST",
            "HMS.ST", "HOIST.ST", "HTRO.ST", "HUM.ST", "INSTAL.ST", "INTRUM.ST", "ITAB.ST",
            "JM.ST", "KABE-B.ST", "KAR.ST", "KNOX.ST", "LAGR-B.ST", "LAMM-B.ST", "LINC.ST",
            "LOOMIS.ST", "LVE.ST", "MEKO.ST", "MIPS.ST", "MQ.ST", "MTG-B.ST", "MYCR.ST",
            "NCC-B.ST", "NCAB.ST", "NETI-B.ST", "NOLA-B.ST", "NOTE.ST", "NP3.ST", "NYF.ST",
            "OEM-B.ST", "ORE.ST", "OX2.ST", "PNDX-B.ST", "PEAB-B.ST", "PLAZ-B.ST",
            "PRIC-B.ST", "PROF-B.ST", "RATO-B.ST", "RAY-B.ST", "READ.ST", "RESURS.ST",
            "SCST.ST", "SECT-B.ST", "SKIS-B.ST", "SSAB-B.ST", "STILL.ST", "STOR-B.ST",
            "SVED-B.ST", "SWEC-B.ST", "SYSR.ST", "TIETOS.ST", "TROAX.ST", "VBG-B.ST",
            "VPLAY-B.ST", "WIHL.ST", "XANO-B.ST", "XVIVO.ST"
        ],
        "First North (Tillväxt & Förhoppning)": [
            "ABLI.ST", "ACNE.ST", "ACTI.ST", "ADVER.ST", "AINO.ST", "ALIG.ST", "ALM.ST",
            "ANOT.ST", "APAB.ST", "ARPL.ST", "ASPIRE.ST", "BIM.ST", "BONE.ST", "BRG-B.ST",
            "CARY.ST", "CHECK.ST", "CINT.ST", "CLEAR.ST", "CLIME.ST", "CRAD-B.ST",
            "DEV.ST", "DIAD.ST", "DIGN.ST", "DIVIO.ST", "DRLN.ST", "ECO.ST", "EBR.ST",
            "ELLT.ST", "EMBRAC-B.ST", "ENEA.ST", "ENRO.ST", "ENVI.ST", "ESEN.ST",
            "EUROP.ST", "EVLI.ST", "EXPR.ST", "FINE.ST", "FIRE.ST", "FLOW.ST", "FPC-B.ST",
            "FRACT.ST", "GAPW-B.ST", "GENO.ST", "GOMR.ST", "HAYPP.ST", "HILD.ST",
            "IMPL-A.ST", "INWI.ST", "IRLAB-A.ST", "ISOFOL.ST", "JETTY.ST", "JOOL.ST",
            "KALLE.ST", "KDEV.ST", "LOGI.ST", "LYKO-A.ST", "MAGN.ST", "MANTEX.ST",
            "MBRS.ST", "MENT-B.ST", "MINT.ST", "MODEL-B.ST", "MOBA.ST", "NANESA.ST",
            "NEXT.ST", "NIV-B.ST", "NORD.ST", "NORVA.ST", "ODD.ST", "ONCO.ST", "OPT.ST",
            "OVZ.ST", "PAX.ST", "PEXA-B.ST", "PHYS.ST", "PIERCE.ST", "PLEJD.ST",
            "POLY.ST", "PREV-B.ST", "PROB.ST", "QLIFE.ST", "QUIA.ST", "RANA.ST", "RETO.ST",
            "RUG.ST", "RVRC.ST", "SALT-B.ST", "SAVOS.ST", "SDIP.ST", "SEZI.ST",
            "SIVERS.ST", "SLP-B.ST", "SMART.ST", "SMOL.ST", "SOLT.ST", "SPEQ.ST",
            "SPECTR.ST", "STORY-B.ST", "STRAX.ST", "SVEA-B.ST", "SYNC-B.ST", "TEQ.ST",
            "THQ.ST", "TOBII.ST", "TOUCH.ST", "TRNST.ST", "TRUE-B.ST", "USER.ST",
            "VESTUM.ST", "VNV.ST", "W5.ST", "WAY.ST", "XBRANE.ST", "XSPRAY.ST", "ZIGN.ST"
        ]
    },
    "Kanada 🇨🇦": {
        "TSX Energy (Oil/Gas Giants)": [
            "SU.TO", "CNQ.TO", "CVE.TO", "IMO.TO", "TRP.TO", "ENB.TO", "PPL.TO",
            "TOU.TO", "ARX.TO", "POW.TO", "VET.TO", "MEG.TO", "CPG.TO", "BTE.TO",
            "WCP.TO", "ERF.TO", "PEY.TO", "BIR.TO", "NVA.TO", "ATH.TO", "KEC.TO",
            "TVE.TO", "IPO.TO", "SES.TO", "CEU.TO", "CJ.TO", "GEI.TO", "KEY.TO",
            "PSI.TO", "MTL.TO", "ALA.TO"
        ],
        "TSX Mining (Global Majors)": [
            "ABX.TO", "AEM.TO", "TECK-B.TO", "IVN.TO", "FM.TO", "WPM.TO", "FNV.TO",
            "LUN.TO", "AGI.TO", "K.TO", "NGD.TO", "PAAS.TO", "SVM.TO", "MAG.TO",
            "DPM.TO", "EDV.TO", "ERO.TO", "LUG.TO", "ORA.TO", "SSRM.TO", "CG.TO",
            "ALS.TO", "TXG.TO", "OSK.TO", "AYA.TO", "ELD.TO", "IMG.TO", "BTO.TO",
            "LGO.TO", "EQX.TO", "YRI.TO", "SSRM.TO", "PVG.TO", "NG.TO"
        ],
        "TSX Venture (Junior Mining - The Goldmine)": [
            "MOG.V", "FIL.V", "LIO.V", "NFG.V", "GBR.V", "SGD.V", "ISO.V", "PMET.V",
            "LI.V", "EU.V", "VPT.V", "GLO.V", "DSV.V", "FL.V", "SKE.V", "PRYM.V",
            "MAX.V", "GIGA.V", "VGCX.V", "ARTG.V", "MAU.V", "FDR.V", "QTWO.V",
            "ATX.V", "ARIC.V", "NICU.V", "KRY.V", "PLSR.V", "FNM.V", "HSTR.V",
            "BFM.V", "DMX.V", "CVV.V", "FPC.V", "LBC.V", "AAG.V", "OGN.V", "EMO.V",
            "HMR.V", "LGC.V", "SHL.V", "GRZ.V", "HAMR.V", "MMY.V", "STD.V", "RRI.V",
            "DEC.V", "DV.V", "EPL.V", "GTT.V", "HIVE.V", "HSTR.V", "KNT.V", "LME.V",
            "NUG.V", "PGM.V", "QPM.V", "RIO.V", "RSLV.V", "RU.V", "SCOT.V", "SGN.V",
            "SIG.V", "SLL.V", "SO.V", "TAU.V", "TDG.V", "TEA.V", "TIG.V", "TUO.V",
            "VLE.V", "VZLA.V", "WM.V", "XTRA.V", "ZEN.V"
        ],
        "TSX Venture (Junior Energy/Tech/Misc)": [
            "SEI.V", "RECO.V", "JOY.V", "TAL.V", "STEP.V", "SDE.V", "TWM.V", "GXE.V",
            "OYL.V", "AAV.TO", "CR.TO", "YGR.TO", "SXE.TO", "VLE.TO", "CMC.V",
            "DM.V", "DOC.V", "ESE.V", "FOBI.V", "GRN.V", "HPQ.V", "PYR.V",
            "QYOU.V", "SOLR.V", "VO.V", "WELL.TO", "XBC.TO"
        ],
        "CSE (High Risk / Speculative)": [
            "KUYA.CN", "AMQ.CN", "API.CN", "ARS.CN", "ACDX.CN", "ACM.CN", "PMAX.CN",
            "NEXU.CN", "EMET.CN", "TUNG.CN", "MSM.CN", "QIMC.CN", "EATH.CN",
            "APXC.CN", "BLLG.CN", "SLV.CN", "CCI.CN", "UUU.CN", "ATMY.CN", "LFLR.CN",
            "AAB.CN", "ABR.CN", "ACT.CN", "AGB.CN", "BIG.CN", "BOSS.CN", "CANS.CN",
            "COOL.CN", "DIGI.CN", "DRUG.CN", "EGLX.TO", "FE.CN", "GLD.CN", "GTII.CN",
            "ION.CN", "JANE.CN", "LIFT.CN", "LITE.CN", "MEDV.CN", "MSET.CN",
            "NUMI.TO", "OPT.CN", "PLTH.CN", "RIV.CN", "RVV.CN", "THRM.CN",
            "TRIP.CN", "TRUL.CN", "VEXT.CN", "XPHY.CN"
        ]
    },
    "USA 🇺🇸": {
        "Small/Mid Tech & Growth (Volatile Favorites)": [
            "PLTR", "SOFI", "DKNG", "HOOD", "RIVN", "LCID", "PLUG", "ROKU", "U", "RBLX",
            "OPEN", "AFRM", "UPST", "AI", "PATH", "IOT", "MDB", "SNOW", "DDOG", "NET",
            "ZS", "CRWD", "TTD", "APP", "DUOL", "HIMS", "IONQ", "JOBY", "ACHR", "ASTS"
        ],
        "Crypto & Fintech (High Beta)": [
            "COIN", "MARA", "RIOT", "CLSK", "MSTR", "HUT", "BITF", "SQ", "PYPL", "SOFI",
            "AFRM", "UPST", "HOOD", "BAC", "C", "JPM"
        ],
        "Biotech & Pharma (Small/Mid)": [
            "DNA", "NVTA", "PACB", "CRSP", "NTLA", "BEAM", "EDIT", "FATE", "IOVA", "ITCI",
            "KRTX", "MDGL", "NVAX", "SAVA", "SRPT", "VRTX", "MRNA", "BNTX"
        ],
        "Energy, Uranium & Commodities (US Listings)": [
            "CCJ", "UUUU", "UEC", "DNN", "NXE", "URA", "URNM",
            "FCEL", "BE", "BLDP", "RUN", "ENPH", "SEDG", "FSLR",
            "XOM", "CVX", "COP", "OXY", "DVN", "EOG", "PXD", "HAL", "SLB"
        ],
        "Retail & Meme Favorites (High Volatility)": [
            "GME", "AMC", "KOSS", "BB", "NOK", "TLRY", "CGC", "SNDL", "SPCE", "NKLA",
            "MULLN", "FFIE", "CVNA", "CHWY", "PTON", "FUBO", "WISH"
        ]
    }
}

# --- Hjälpfunktioner ---

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
        
        # Filtrera nyheter från senaste X dagarna
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for article in news:
            # Kontrollera publiceringsdatum
            pub_timestamp = article.get('providerPublishTime', 0)
            pub_date = datetime.fromtimestamp(pub_timestamp)
            
            if pub_date < cutoff_date:
                continue
            
            title = article.get('title', '').lower()
            
            # Sök efter nyckelord i titeln
            for keyword in keywords_list:
                if keyword.lower() in title:
                    return {
                        'title': article.get('title', ''),
                        'link': article.get('link', ''),
                        'publisher': article.get('publisher', ''),
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
        
        st.info(f"🔍 Skannar {total} aktier...")
        
        for i, symbol in enumerate(tickers_to_scan):
            status_text.text(f"Analyserar {symbol}... ({i+1}/{total})")
            progress_bar.progress((i + 1) / total)
            
            stock = yf.Ticker(symbol)
            streak = get_streak(symbol)
            
            # Hämta pris
            try:
                hist = stock.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                else:
                    price = 0
            except:
                price = 0

            # Filter: Pris
            if not (price_range[0] <= price <= price_range[1]):
                continue

            # Hämta värderingsdata
            valuation = get_valuation_metrics(symbol)
            
            # Filter: P/E
            if use_pe_filter and pe_range:
                pe = valuation['pe']
                if pe is None or not (pe_range[0] <= pe <= pe_range[1]):
                    continue
            
            # Filter: P/B
            if use_pb_filter and pb_range:
                pb = valuation['pb']
                if pb is None or not (pb_range[0] <= pb <= pb_range[1]):
                    continue

            # Filter: Trend
            min_streak, max_streak = streak_filter
            if not (min_streak <= streak <= max_streak):
                continue

            # Filter: Nyheter och händelser (Yahoo Finance Press Releases)
            news_hits = []
            match = True
            
            # Avgör vilka nyckelord som är relevanta baserat på marknad
            is_swedish = symbol.endswith('.ST')
            is_canadian = symbol.endswith('.TO') or symbol.endswith('.V') or symbol.endswith('.CN')
            is_us = not (is_swedish or is_canadian)
            
            if check_vinstvarning:
                # Sök efter vinstvarning/profit warning i Yahoo Finance news
                warning_keywords = []
                if is_swedish:
                    warning_keywords = ['vinstvarning', 'sänker prognos', 'nedjusterar', 'varning']
                else:
                    warning_keywords = ['profit warning', 'lowers guidance', 'downgrade', 'warning', 'miss']
                
                yf_hit = check_yf_news(symbol, warning_keywords, days_back=30)
                if yf_hit:
                    news_hits.append(f"⚠️ {yf_hit['title'][:50]}...")
                else:
                    match = False

            if check_rapport:
                # Kontrollera rapportdatum (fungerar för alla marknader)
                earnings_info = check_earnings_date(symbol, days_range=30)
                if earnings_info:
                    news_hits.append(f"📊 {earnings_info}")
                else:
                    # Sök efter rapport i Yahoo Finance news
                    report_keywords = []
                    if is_swedish:
                        report_keywords = ['kvartalsrapport', 'delårsrapport', 'Q1', 'Q2', 'Q3', 'Q4', 'earnings']
                    else:
                        report_keywords = ['earnings', 'quarterly results', 'reports', 'Q1', 'Q2', 'Q3', 'Q4']
                    
                    yf_hit = check_yf_news(symbol, report_keywords, days_back=30)
                    if yf_hit:
                        news_hits.append(f"📊 Rapport")
            
            if check_insider:
                # Sök efter insidertransaktioner
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
                # Sök efter VD-byten och ledningsförändringar
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
            
            # Om vinstvarning var ikryssad men inte hittades, skippa bolaget
            if check_vinstvarning and not match:
                continue
            
            # Lägg till resultat
            news_text = " | ".join(news_hits) if news_hits else "Ingen specifik händelse"
            
            # Avgör valuta
            if symbol.endswith('.ST'):
                currency = "SEK"
            elif symbol.endswith('.TO') or symbol.endswith('.V') or symbol.endswith('.CN'):
                currency = "CAD"
            else:
                currency = "USD"
            
            results.append({
                "Ticker": symbol,
                f"Pris ({currency})": round(float(price), 2),
                "P/E": round(valuation['pe'], 2) if valuation['pe'] else "N/A",
                "P/B": round(valuation['pb'], 2) if valuation['pb'] else "N/A",
                "Trend (Dagar)": streak,
                "Händelser": news_text
            })

        status_text.empty()
        progress_bar.empty()

        if len(results) > 0:
            # Begränsa till max 40 resultat
            results = results[:40]
            
            st.success(f"✅ Hittade {len(results)} bolag som matchar dina kriterier!")
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