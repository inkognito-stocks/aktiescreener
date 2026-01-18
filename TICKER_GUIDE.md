# 📋 Guide: Uppdatera Ticker-Lista

Ticker-listan är nu separerad i en egen fil (`tickers.py`) för enkel uppdatering!

## 🔧 Hur du lägger till/tar bort aktier:

### 1. Öppna `tickers.py`

### 2. Hitta rätt marknad och kategori:
```python
"Sverige 🇸🇪": {
    "Large Cap (OMXS30 & Co)": [
        "ABB.ST", "ALFA.ST", ...
    ],
    ...
}
```

### 3. Lägg till eller ta bort ticker-symboler:

**Exempel: Lägg till Spotify till Sverige Large Cap:**
```python
"Large Cap (OMXS30 & Co)": [
    "ABB.ST", "ALFA.ST", ..., "SPOT.ST"  # <-- Lägg till här
]
```

**Exempel: Ta bort en aktie:**
```python
# Ta bara bort ticker-symbolen från listan
```

### 4. Pusha till GitHub:
```bash
git add tickers.py
git commit -m "Uppdaterade ticker-lista"
git push
```

### 5. Appen uppdateras automatiskt!
Streamlit Cloud upptäcker ändringarna och rebuildar appen (~2-3 min)

---

## 📝 Format för ticker-symboler:

- **Sverige:** Suffix `.ST` (ex: `VOLV-B.ST`)
- **Kanada TSX:** Suffix `.TO` (ex: `SU.TO`)
- **Kanada Venture:** Suffix `.V` (ex: `NFG.V`)
- **Kanada CSE:** Suffix `.CN` (ex: `KUYA.CN`)
- **USA:** Ingen suffix (ex: `PLTR`, `AAPL`)

---

## ➕ Lägg till ny kategori:

```python
"Sverige 🇸🇪": {
    "Large Cap (OMXS30 & Co)": [...],
    "Min Nya Kategori": [  # <-- Ny kategori
        "TICKER1.ST",
        "TICKER2.ST"
    ]
}
```

---

## ➕ Lägg till nytt land:

```python
ticker_lists = {
    "Sverige 🇸🇪": {...},
    "Kanada 🇨🇦": {...},
    "USA 🇺🇸": {...},
    "Tyskland 🇩🇪": {  # <-- Nytt land
        "DAX 40": [
            "SAP.DE",
            "VOW3.DE"
        ]
    }
}
```

---

## ⚠️ Viktigt:

- **Syntax:** Se till att komman är rätt placerade
- **Testkör lokalt först:** `py -m streamlit run app.py`
- **Backup:** Git sparar all historik, så du kan alltid ångra ändringar

---

## 💡 Tips:

- Du behöver INTE ändra `app.py` - bara `tickers.py`!
- Hitta ticker-symboler på [Yahoo Finance](https://finance.yahoo.com/)
- Använd Cursor/VS Code för syntax highlighting

**Lycka till! 🚀**
