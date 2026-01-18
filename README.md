# 🔎 Börs-Sök - Aktiescreener

En kraftfull sökmotor för svenska aktier med avancerade filter för pris, värdering, trend och händelser.

## 🚀 Funktioner

### Prisfilter
- Välj prisintervall precis som på Blocket
- Från 0 till 1000 SEK

### Värderingsfilter
- **P/E-tal** (Price/Earnings) - Värdering i förhållande till vinst
- **P/B-tal** (Price/Book) - Pris i förhållande till bokfört värde

### Händelsefilter (Yahoo Finance Press Releases)
- ⚠️ **Vinstvarning / Profit Warning** - Söker i Yahoo Finance press releases efter vinstvarningar, nedgraderingar och varningar
- 📊 **Rapport** - Visar om kvartalsrapport släpptes nyligen eller ska släppas inom 30 dagar (kontrollerar både rapportkalender och press releases)
- 👤 **Insidertransaktioner** - Söker efter insiderköp och insiderförsäljning (t.ex. VD, styrelseledamöter)
- 🎯 **Ny VD/ledning** - Söker efter VD-byten och ledningsförändringar

**Fördel med Yahoo Finance:** Mer träffsäkert än att söka på företagsnamn - hämtar nyheter direkt kopplade till ticker-symbolen!

### Teknisk Trend
- Filtrera på antal dagar aktien gått upp eller ner i rad
- -15 till +15 dagar

### Resultat
- Visar 5-40 bolag som matchar dina kriterier
- Statistik över resultat
- Exportera till CSV

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

## ⚡ Performance

- **Parallell processing:** 10 aktier analyseras samtidigt
- **Caching:** 45 minuters cache (undviker Yahoo Finance rate limiting)
- **Smart filtrering:** Filtrerar bort aktier tidigt för snabbare resultat
- **Hastighet:** Large Cap (51 aktier) ~20-30 sekunder

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
