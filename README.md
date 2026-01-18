# 🌍 Global AktieScreener

En kraftfull sökmotor för aktier från **Sverige, Kanada och USA** med avancerade filter för pris, värdering och trend.

## 🚀 Funktioner

### 🌍 Multi-Market Support
- **Sverige 🇸🇪** - OMXS30, Mid Cap, Small Cap, First North
- **Kanada 🇨🇦** - TSX Energy, TSX Mining, Venture, CSE
- **USA 🇺🇸** - Tech, Crypto, Biotech, Energy, Meme stocks
- **546+ aktier** totalt

### ⚡ Batch-Download (SUPERSNABBT!)
- Laddar ner **50 aktier samtidigt** med `yf.download`
- **10-20x snabbare** än individuell nedladdning
- Exempel: 250 aktier på ~30 sekunder (vs 3-5 minuter tidigare)
- Progress tracking per batch

### 💰 Prisfilter
- Välj prisintervall från 0-2000 (SEK/CAD/USD)
- Jämför valutor direkt

### 📊 Värderingsfilter
- **P/E-tal** (Price/Earnings) - Värdering i förhållande till vinst
- **P/B-tal** (Price/Book) - Pris i förhållande till bokfört värde
- Valfria filter som kan aktiveras/inaktiveras

### 📰 Händelsefilter (HYBRID-LÖSNING!)
- ⚠️ **Vinstvarning / Profit Warning** - Söker efter vinstvarningar och nedgraderingar
- 📊 **Rapport** - Kvartalsrapporter (släppta eller kommande inom 30 dagar)
- 👤 **Insidertransaktioner** - Insiderköp och insiderförsäljning
- 🎯 **Ny VD/ledning** - VD-byten och ledningsförändringar

**🔥 SMART NYHETSKÄLLOR:**
- **Svenska bolag** → Cision (officiella pressmeddelanden, real-time!)
- **USA/Kanada** → Yahoo Finance (bra täckning för internationella marknader)

Detta ger dig bästa möjliga träffsäkerhet för varje marknad!

### 📈 Teknisk Trend
- Filtrera på antal dagar aktien gått upp eller ner i rad
- -15 till +15 dagar
- Beräknas direkt från prishistorik

### 📊 Resultat
- Visar upp till 100 matchande aktier
- **Marknad-kolumn** visar vilket land aktien kommer från
- Realtidsstatistik (antal aktier, marknader, trend)
- Exportera till CSV
- Scanningstid visas

## 💻 Installation

1. Installera Python-paket:
```bash
pip install -r requirements.txt
```

2. Kör appen:
```bash
streamlit run app.py
```

## 📋 Uppdatera Aktier

Ticker-listan finns i `tickers.py` - uppdatera den filen för att lägga till/ta bort aktier!

Se [TICKER_GUIDE.md](TICKER_GUIDE.md) för detaljerad guide.

## ⚡ Performance (Nya Batch-systemet)

- **Batch-download:** 50 aktier per batch med `yf.download`
- **10-20x snabbare** än tidigare version
- **Caching:** 45 minuters cache (undviker Yahoo Finance rate limiting)
- **Hastighet:**
  - 50 aktier: ~5-10 sekunder
  - 250 aktier: ~15-30 sekunder  
  - 500 aktier: ~30-60 sekunder

**Gamla versionen** (`app_old.py`): 250 aktier = 3-5 minuter
**Nya versionen** (`app.py`): 250 aktier = 15-30 sekunder ⚡

## 📖 Användning

1. Justera filtren i sidopanelen
2. Tryck på "🔍 Skanna Marknaden"
3. Vänta medan appen analyserar bolagen
4. Få resultat med 5-40 bolag som matchar

## 🎯 Tips

- Börja brett och smalna av filtren steg för steg
- Kombinera pris + trend för teknisk analys
- Använd värderingsfilter för fundamentalanalys
- Händelsefilter för att hitta katalysatorer

## ⚠️ Obs

Detta är en prototyp för analysändamål. Gör alltid egen due diligence innan investeringar!
