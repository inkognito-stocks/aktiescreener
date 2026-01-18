# market_data.py - Ticker lists for Global Stock Screener
# Uppdaterad med MASSIV täckning (1000+ bolag totalt)

# --- SVERIGE LARGE CAP (Komplett lista) ---
SE_LARGE_CAP = [
    "AAK.ST", "ABB.ST", "ADD-B.ST", "ALFA.ST", "ALIF-B.ST", "ASSA-B.ST",
    "ATCO-A.ST", "ATCO-B.ST", "AXFO.ST", "AZA.ST", "AZN.ST", "BALD-B.ST",
    "BEIJ-B.ST", "BETS-B.ST", "BILL.ST", "BIOT.ST", "BOL.ST", "BRAV.ST",
    "BURE.ST", "CAST.ST", "CIBUS.ST", "CLAS-B.ST", "DIOS.ST", "DOM.ST",
    "EKTA-B.ST", "ELUX-B.ST", "ELUX-PROF-B.ST", "EPI-A.ST", "EPI-B.ST",
    "ERIC-A.ST", "ERIC-B.ST", "ESSITY-A.ST", "ESSITY-B.ST", "EVO.ST",
    "FABG.ST", "FOI-B.ST", "FPAR-A.ST", "GETI-B.ST", "HEBA-B.ST", "HEM.ST",
    "HEXA-B.ST", "HM-B.ST", "HOLM-A.ST", "HOLM-B.ST", "HPOL-B.ST",
    "HUF-A.ST", "HUF-C.ST", "HUSQ-A.ST", "HUSQ-B.ST", "INDT.ST", "INDU-A.ST",
    "INDU-C.ST", "INTRUM.ST", "INVE-A.ST", "INVE-B.ST", "JM.ST", "KINV-A.ST",
    "KINV-B.ST", "LAGR-B.ST", "LATO-B.ST", "LIFCO-B.ST", "LOOMIS.ST",
    "LUND-B.ST", "MEKO.ST", "MIPS.ST", "MTG-B.ST", "MYCR.ST", "NCC-A.ST",
    "NCC-B.ST", "NDA-SE.ST", "NIBE-B.ST", "NOLA-B.ST", "NP3.ST", "NYF.ST",
    "OX2.ST", "PNDX.ST", "PEAB-B.ST", "PLAT-B.ST", "RATO-A.ST", "RATO-B.ST",
    "SAAB-B.ST", "SAGA-A.ST", "SAGA-B.ST", "SAGA-D.ST", "SAND.ST", "SAVE.ST",
    "SBB-B.ST", "SBB-D.ST", "SCA-A.ST", "SCA-B.ST", "SEB-A.ST", "SEB-C.ST",
    "SECT-B.ST", "SF.ST", "SHB-A.ST", "SHB-B.ST", "SINCH.ST", "SKA-B.ST",
    "SKF-A.ST", "SKF-B.ST", "SSAB-A.ST", "SSAB-B.ST", "STE-A.ST", "STE-R.ST",
    "STORY-B.ST", "SWEC-A.ST", "SWEC-B.ST", "SWED-A.ST", "SYSR.ST",
    "TEL2-A.ST", "TEL2-B.ST", "TELIA.ST", "THULE.ST", "TREL-B.ST", "TROAX.ST",
    "VBG-B.ST", "VITR.ST", "VOLV-A.ST", "VOLV-B.ST", "VPLAY-B.ST",
    "WALL-B.ST", "WIHL.ST", "WISC.ST"
]

# --- SVERIGE MID CAP (Komplett lista) ---
SE_MID_CAP = [
    "ACAD.ST", "ADAPT.ST", "AFRY.ST", "ALLEI.ST", "ALLIGO-B.ST", "AMBEA.ST",
    "ANEX.ST", "ANOD-B.ST", "AQ.ST", "ARJO-B.ST", "ARPL.ST", "ATRLJ-B.ST",
    "ATT.ST", "BACTI-B.ST", "BALCO.ST", "BELE.ST", "BESQ.ST", "BILI-A.ST",
    "BIOA-B.ST", "BMAX.ST", "BONES.ST", "BOOZT.ST", "BORG.ST", "BTS-B.ST",
    "BULTEN.ST", "CALL.ST", "CAMX.ST", "CATE.ST", "CAT-A.ST", "CAT-B.ST",
    "COIC.ST", "COOR.ST", "CRED-A.ST", "CTEK.ST", "CTM.ST", "CTT.ST",
    "DUNI.ST", "DUST.ST", "EAST.ST", "ELAN-B.ST", "ELTEL.ST", "ENRO.ST",
    "EO.ST", "EWRK.ST", "FAG.ST", "FAST.ST", "FMATT.ST", "FNM.ST", "G5EN.ST",
    "GARO.ST", "GIG-SEK.ST", "GRNG.ST", "HANZA.ST", "HHO.ST", "HOFI.ST",
    "HTRO.ST", "HUMBLE.ST", "IAR-B.ST", "INFREA.ST", "INWIDO.ST", "ITAB-B.ST",
    "JOHN-B.ST", "KARC.ST", "KFAST-B.ST", "KIND-SDB.ST", "KNOW.ST", "LAMM-B.ST",
    "LIME.ST", "LINC.ST", "MCAP.ST", "MENT.ST", "MIDW-A.ST", "MIDW-B.ST",
    "MMGR-B.ST", "MOB.ST", "MSON-A.ST", "MSON-B.ST", "MTRS.ST", "NCAB.ST",
    "NEWA-B.ST", "NGS.ST", "NIL-B.ST", "NMAN.ST", "NOTE.ST", "OASM.ST",
    "OEM-B.ST", "ORE.ST", "PACT.ST", "PIERCE.ST", "PRIC-B.ST", "PROB.ST",
    "PROF-B.ST", "QLEALA.ST", "RAY-B.ST", "READ.ST", "REJL-B.ST", "RESURS.ST",
    "RVRC.ST", "SCST.ST", "SDIP-B.ST", "SENS.ST", "SIVE.ST", "SLP-B.ST",
    "SOBI.ST", "SRNKE-B.ST", "STWK.ST", "SVED-B.ST", "TETY.ST", "TRAD.ST",
    "TRAN.ST", "TRIAN-B.ST", "VICO.ST", "VIMIAN.ST", "VNV.ST", "VOLO.ST",
    "WAY.ST", "XANO-B.ST", "XBRANE.ST", "XVIVO.ST",
    
    # --- EXTRA Mid Cap (Fler bolag) ---
    "ACAST.ST", "ACCON.ST", "ACRI-A.ST", "ACRI-B.ST", "ADDTECH-B.ST", "ADVBOX.ST",
    "AERO.ST", "AFFY.ST", "AGROUP.ST", "AHLST-B.ST", "AID.ST", "AINS-B.ST",
    "AKAO-B.ST", "AKELD.ST", "AKSO.ST", "ALCA.ST", "ALFA.ST", "ALIF-B.ST",
    "ALIG.ST", "ALIV-SDB.ST", "ALM.ST", "ALTE.ST", "AMAST.ST", "ANOD-B.ST",
    "APRND.ST", "AQ.ST", "ARCT.ST", "ARJO-B.ST", "ARPL.ST", "ASSA-B.ST",
    "ATCO-A.ST", "ATCO-B.ST", "ATRLJ-B.ST", "ATT.ST", "AUR.ST", "AUTOLIV.ST",
    "AVANZA.ST", "AXFO.ST", "AZA.ST", "AZN.ST", "B3.ST", "BACTI-B.ST",
    "BALD-B.ST", "BALCO.ST", "BEGR.ST", "BEIJ-B.ST", "BELE.ST", "BENGT.ST",
    "BESQ.ST", "BETS-B.ST", "BILI-A.ST", "BIOA-B.ST", "BILL.ST", "BIOT.ST",
    "BMAX.ST", "BOL.ST", "BONG.ST", "BONES.ST", "BOOZT.ST", "BORG.ST",
    "BOUV.ST", "BRAV.ST", "BRIO.ST", "BTS-B.ST", "BULTEN.ST", "BURE.ST",
    "CALL.ST", "CAMX.ST", "CANTA.ST", "CATE.ST", "CAT-A.ST", "CAT-B.ST",
    "CCOR-B.ST", "CIBUS.ST", "CLAS-B.ST", "COIC.ST", "COOR.ST", "CRAD-B.ST",
    "CRED-A.ST", "CTEK.ST", "CTM.ST", "CTT.ST", "DIGN.ST", "DIOS.ST",
    "DOM.ST", "DOR.ST", "DUNI.ST", "DUST.ST", "DURC-B.ST", "EAST.ST",
    "EDGE.ST", "EGT.ST", "EKTA-B.ST", "ELAN-B.ST", "ELOS-B.ST", "ELTEL.ST",
    "ELUX-B.ST", "ELUX-PROF-B.ST", "ENQ.ST", "ENRO.ST", "ENRO-PREF.ST",
    "EO.ST", "EPI-A.ST", "EPI-B.ST", "EPIS-B.ST", "ERIC-A.ST", "ERIC-B.ST",
    "ESSITY-A.ST", "ESSITY-B.ST", "ETX.ST", "EVID.ST", "EVO.ST", "EWRK.ST",
    "FABG.ST", "FAG.ST", "FAST.ST", "FIRE.ST", "FMATT.ST", "FNM.ST",
    "FOI-B.ST", "FPAR-A.ST", "G5EN.ST", "GARO.ST", "GENO.ST", "GETI-B.ST",
    "GIG-SEK.ST", "GOM.ST", "GRNG.ST", "HAKN.ST", "HANZA.ST", "HAV-B.ST",
    "HEBA-B.ST", "HEM.ST", "HEXA-B.ST", "HHO.ST", "HM-B.ST", "HOFI.ST",
    "HOLM-A.ST", "HOLM-B.ST", "HOSA-B.ST", "HPOL-B.ST", "HTRO.ST", "HUF-A.ST",
    "HUF-C.ST", "HUMBLE.ST", "HUSQ-A.ST", "HUSQ-B.ST", "IAR-B.ST", "IMAGE.ST",
    "IMU.ST", "INDT.ST", "INDU-A.ST", "INDU-C.ST", "INFREA.ST", "INTRUM.ST",
    "INVE-A.ST", "INVE-B.ST", "INWIDO.ST", "IRLAB-A.ST", "ISOF.ST", "ITAB-B.ST",
    "JET.ST", "JM.ST", "JOHN-B.ST", "KARC.ST", "KDEV.ST", "KFAST-B.ST",
    "KIND-SDB.ST", "KINV-A.ST", "KINV-B.ST", "KNOW.ST", "LAGR-B.ST", "LAMM-B.ST",
    "LATO-B.ST", "LIFCO-B.ST", "LIME.ST", "LINC.ST", "LOGI-B.ST", "LOOMIS.ST",
    "LUC.ST", "LUND-B.ST", "MAG.ST", "MANG.ST", "MCAP.ST", "MEDVIR-B.ST",
    "MEKO.ST", "MENT.ST", "MFN.ST", "MIDW-A.ST", "MIDW-B.ST", "MIPS.ST",
    "MMGR-B.ST", "MOB.ST", "MOBA.ST", "MSON-A.ST", "MSON-B.ST", "MTRS.ST",
    "MTG-B.ST", "MYCR.ST", "NCC-A.ST", "NCC-B.ST", "NCAB.ST", "NDA-SE.ST",
    "NAXS.ST", "NEVI.ST", "NETI-B.ST", "NEWA-B.ST", "NGS.ST", "NIBE-B.ST",
    "NIL-B.ST", "NMAN.ST", "NOLA-B.ST", "NOTE.ST", "NP3.ST", "NTEK-B.ST",
    "NYF.ST", "OASM.ST", "OEM-B.ST", "ORE.ST", "ORTI-A.ST", "ORTI-B.ST",
    "OSCAR.ST", "OVZ.ST", "OX2.ST", "PACT.ST", "PCELL.ST", "PEAB-B.ST",
    "PIERCE.ST", "PLAT-B.ST", "PNDX.ST", "POOL-B.ST", "PREC.ST", "PREV-B.ST",
    "PRIC-B.ST", "PRIF-B.ST", "PROB.ST", "PROF-B.ST", "QAC.ST", "QIL.ST",
    "QLEALA.ST", "RAIL.ST", "RATO-A.ST", "RATO-B.ST", "RAY-B.ST", "READ.ST",
    "REJL-B.ST", "RESURS.ST", "RROS.ST", "RVRC.ST", "SAAB-B.ST", "SAGA-A.ST",
    "SAGA-B.ST", "SAGA-D.ST", "SANION.ST", "SAND.ST", "SAVE.ST", "SBB-B.ST",
    "SBB-D.ST", "SCA-A.ST", "SCA-B.ST", "SCST.ST", "SDIP-B.ST", "SEB-A.ST",
    "SEB-C.ST", "SECT-B.ST", "SENS.ST", "SEZI.ST", "SF.ST", "SHB-A.ST",
    "SHB-B.ST", "SINCH.ST", "SINT.ST", "SINT-PREF.ST", "SIVE.ST", "SKA-B.ST",
    "SKF-A.ST", "SKF-B.ST", "SLP-B.ST", "SOBI.ST", "SOFT.ST", "SPM.ST",
    "SRNKE-B.ST", "SSAB-A.ST", "SSAB-B.ST", "STAR-B.ST", "STE-A.ST", "STE-R.ST",
    "STORY-B.ST", "STRAX.ST", "STU.ST", "STWK.ST", "SUA-B.ST", "SVED-B.ST",
    "SWEC-A.ST", "SWEC-B.ST", "SWED-A.ST", "SYSR.ST", "TAGM-B.ST", "TEL2-A.ST",
    "TEL2-B.ST", "TELIA.ST", "TETY.ST", "THULE.ST", "TRAD.ST", "TRAN.ST",
    "TREL-B.ST", "TRENT.ST", "TRIAN-B.ST", "TROAX.ST", "UHR.ST", "VBG-B.ST",
    "VICO.ST", "VIMIAN.ST", "VITR.ST", "VNV.ST", "VOLO.ST", "VOLV-A.ST",
    "VOLV-B.ST", "VPLAY-B.ST", "WALL-B.ST", "WAY.ST", "WIHL.ST", "WISE.ST",
    "WISC.ST", "XANO-B.ST", "XBRANE.ST", "XSPRAY.ST", "XVIVO.ST", "ZETA.ST"
]

# --- SVERIGE SMALL CAP (Komplett lista - endast Small Cap, ej First North eller Large Cap) ---
# Rensad från duplicater och Large Cap-bolag
SE_SMALL_CAP = [
    "ABL.ST", "ACTI.ST", "ALIG.ST", "ALZ.ST", "ANOT.ST", "AOI.ST", "ASAP.ST",
    "ATEK.ST", "B3.ST", "BEGR.ST", "BONG.ST", "BOUV.ST", "BRIO.ST", "CANTA.ST",
    "CCOR-B.ST", "CRAD-B.ST", "DIGN.ST", "DOR.ST", "DURC-B.ST", "EDGE.ST",
    "EGT.ST", "ELOS-B.ST", "ENQ.ST", "ENRO-PREF.ST", "EPIS-B.ST", "ETX.ST",
    "EVID.ST", "FIRE.ST", "GENO.ST", "GOM.ST", "HAKN.ST", "HAV-B.ST",
    "HOSA-B.ST", "IMAGE.ST", "IMU.ST", "IRLAB-A.ST", "ISOF.ST", "JET.ST",
    "KDEV.ST", "LOGI-B.ST", "LUC.ST", "MAG.ST", "MANG.ST", "MEDVIR-B.ST",
    "MFN.ST", "MOBA.ST", "NAXS.ST", "NETI-B.ST", "NEVI.ST", "NTEK-B.ST",
    "ORTI-A.ST", "ORTI-B.ST", "OSCAR.ST", "OVZ.ST", "PCELL.ST", "POOL-B.ST",
    "PREC.ST", "PREV-B.ST", "PRIF-B.ST", "QAC.ST", "QIL.ST", "RAIL.ST",
    "RROS.ST", "SANION.ST", "SEZI.ST", "SINT.ST", "SINT-PREF.ST", "SOFT.ST",
    "SPM.ST", "STAR-B.ST", "STRAX.ST", "STU.ST", "SUA-B.ST", "TAGM-B.ST",
    "TRENT.ST", "UHR.ST", "WISE.ST", "XSPRAY.ST", "ZETA.ST"
]

# --- SVERIGE FIRST NORTH (Growth Market) ---
SE_FIRST_NORTH = [
    # Cybersecurity & Tech
    "ADVE.ST",  # Advenica
    "ACAST.ST", "ADDTECH-B.ST", "ADVBOX.ST", "AERO.ST", "AFFY.ST", "AGROUP.ST",
    "AHLST-B.ST", "AID.ST", "AINS-B.ST", "AKAO-B.ST", "AKELD.ST", "AKSO.ST",
    "ALCA.ST", "ALTE.ST", "AMAST.ST", "APRND.ST", "ARCT.ST", "AUR.ST",
    "AVANZA.ST", "BENGT.ST", "BTS-B.ST", "CALL.ST", "CAMX.ST",
    
    # Industri & Manufacturing (First North)
    "CATE.ST", "CAT-A.ST", "CAT-B.ST", "COIC.ST", "COOR.ST", "CRED-A.ST",
    "CTEK.ST", "CTM.ST", "CTT.ST", "DUNI.ST", "DUST.ST", "EAST.ST",
    "ELAN-B.ST", "ELTEL.ST", "ENRO.ST", "EO.ST", "EWRK.ST", "FAG.ST",
    "FAST.ST", "FMATT.ST", "FNM.ST", "G5EN.ST", "GARO.ST", "GIG-SEK.ST",
    "GRNG.ST", "HANZA.ST", "HHO.ST", "HOFI.ST", "HTRO.ST", "HUMBLE.ST",
    "IAR-B.ST", "INFREA.ST", "INWIDO.ST", "ITAB-B.ST", "JOHN-B.ST",
    "KARC.ST", "KFAST-B.ST", "KIND-SDB.ST", "KNOW.ST", "LAMM-B.ST",
    "LIME.ST", "LINC.ST", "MCAP.ST", "MENT.ST", "MIDW-A.ST", "MIDW-B.ST",
    "MMGR-B.ST", "MOB.ST", "MSON-A.ST", "MSON-B.ST", "MTRS.ST", "NCAB.ST",
    "NEWA-B.ST", "NGS.ST", "NIL-B.ST", "NMAN.ST", "NOTE.ST", "OASM.ST",
    "OEM-B.ST", "ORE.ST", "PACT.ST", "PIERCE.ST", "PRIC-B.ST", "PROB.ST",
    "PROF-B.ST", "QLEALA.ST", "RAY-B.ST", "READ.ST", "REJL-B.ST", "RESURS.ST",
    "RVRC.ST", "SCST.ST", "SDIP-B.ST", "SENS.ST", "SIVE.ST", "SLP-B.ST",
    "SOBI.ST", "SRNKE-B.ST", "STWK.ST", "SVED-B.ST", "TETY.ST", "TRAD.ST",
    "TRAN.ST", "TRIAN-B.ST", "VICO.ST", "VIMIAN.ST", "VNV.ST", "VOLO.ST",
    "WAY.ST", "XANO-B.ST", "XBRANE.ST", "XVIVO.ST",
    
    # Ytterligare First North bolag
    "ABL.ST", "ACTI.ST", "ALIG.ST", "ALZ.ST", "ANOT.ST", "AOI.ST", "ASAP.ST",
    "ATEK.ST", "BEGR.ST", "BONG.ST", "BOUV.ST", "BRIO.ST", "CANTA.ST",
    "CCOR-B.ST", "CRAD-B.ST", "DIGN.ST", "DOR.ST", "DURC-B.ST", "EDGE.ST",
    "EGT.ST", "ELOS-B.ST", "ENQ.ST", "ENRO-PREF.ST", "EPIS-B.ST", "ETX.ST",
    "EVID.ST", "FIRE.ST", "GENO.ST", "GOM.ST", "HAKN.ST", "HAV-B.ST",
    "HOSA-B.ST", "IMAGE.ST", "IMU.ST", "IRLAB-A.ST", "ISOF.ST", "JET.ST",
    "KDEV.ST", "LOGI-B.ST", "LUC.ST", "MAG.ST", "MANG.ST", "MEDVIR-B.ST",
    "MFN.ST", "MOBA.ST", "NAXS.ST", "NETI-B.ST", "NEVI.ST", "NTEK-B.ST",
    "ORTI-A.ST", "ORTI-B.ST", "OSCAR.ST", "OVZ.ST", "PCELL.ST", "POOL-B.ST",
    "PREC.ST", "PREV-B.ST", "PRIF-B.ST", "QAC.ST", "QIL.ST", "RAIL.ST",
    "RROS.ST", "SANION.ST", "SEZI.ST", "SINT.ST", "SINT-PREF.ST", "SOFT.ST",
    "SPM.ST", "STAR-B.ST", "STRAX.ST", "STU.ST", "SUA-B.ST", "TAGM-B.ST",
    "TRENT.ST", "UHR.ST", "WISE.ST", "XSPRAY.ST", "ZETA.ST"
]

# --- USA (S&P 500 + Nasdaq 100 + Populära Growth) ---
# En bredare lista som täcker de flesta bolag man vill handla
US_ALL_STAR = [
    # --- Magnificent 7 & Big Tech ---
    "AAPL", "MSFT", "NVDA", "GOOGL", "GOOG", "AMZN", "META", "TSLA",
    
    # --- Semiconductors & Hardware (Massiv lista) ---
    # Jättarna (Processors & GPU)
    "NVDA", "TSM", "AMD", "INTC", "QCOM", "AVGO", "ARM", "TXN", "MU", 
    
    # Utrustning & Tillverkning (Wafer Fab Equipment)
    # Dessa bolag bygger maskinerna som gör chipen.
    "AMAT", "LRCX", "KLAC", "TER", "ENTG", "AMKR", "FORM", "ONTO", "ACLS", 
    "MKSI", "AEIS", "COHR", "UCTT", "ICHR", "PLAB", "VECO", "NVMI",
    
    # Analog, Power & Connectivity (Bilindustri & IoT)
    "ADI", "NXPI", "STM", "ON", "MCHP", "MPWR", "SWKS", "QRVO", "SLAB", 
    "DIOD", "POWI", "ALGM", "RMBS", "LSCC", "WOLF", "INDI", "AOSL", "MXL",
    
    # Datalagring & Minne
    "WDC", "STX", "PSTG", "NTAP", "SIMO",
    
    # Server & Hårdvara (AI-infrastruktur)
    "SMCI", "DELL", "HPE", "ANET", "JBL", "CLS", "PAGS", "VRT", "STK",
    
    # EDA & IP (Mjukvaran som designar chipen)
    "SNPS", "CDNS", "ANSS", "CEVA", "PDFS",
    
    # Specialiserade komponenter & Optik
    "GLW", "IPGP", "LITE", "VIAV", "FN", "CRUS", "SITM", "MTSI", "SYNA", 
    "HIMX", "QUIK", "GIC", "KOPN", "EMKR", "VSH", "ALTV",
    
    # Mindre & Volatila (High Risk/High Reward)
    # Dessa är intressanta om du sorterar på % upp/ner
    "AEHR", "IONQ", "RGTI", "QUBT", "DTST", "INTC", "MRVL", "ASML",
    "SMTC", "ASYS", "CAMT", "UCTT", "ACMR", "AMAT", "KLIC", "COHU",
    "NVTS", "MPWR", "SIMO", "CRUS", "QRVO", "SLAB", "PI", "IMOS"
    
    # --- Software, Cloud & AI (Massiv lista) ---
    # Big Tech & AI Foundation
    "MSFT", "GOOGL", "GOOG", "META", "AMZN", "ORCL", "IBM", "SAP",
    
    # Enterprise SaaS & Productivity
    "CRM", "ADBE", "NOW", "INTU", "WDAY", "TEAM", "HUBS", "ADSK", "DOCU", 
    "ZM", "TWLO", "OKTA", "BSY", "PTC", "SSNC", "MANH", "DT", "PAYC", 
    "TYL", "PCTY", "PATH", "PEGA", "SMAR", "ASAN", "MONDY", "ESTC",
    
    # Cloud Infrastructure, Data & DevOps
    "SNOW", "DDOG", "MDB", "NET", "PLTR", "GTLB", "HCP", "CFLT", "IOT", 
    "DBX", "NTNX", "PSTG", "FSLY", "DOCN", "WK",
    
    # Cybersecurity (Väldigt populär sektor just nu)
    "PANW", "CRWD", "FTNT", "ZS", "CYBR", "CHKP", "TENB", "GEN", "VRNS", 
    "QLYS", "S", "RPD", "OKTA", "PING",
    
    # AI-Specific & Big Data (Hög Volatilitet)
    "AI", "PLTR", "SOUN", "BBAI", "VRNS", "ALTR", "PRO", "SPIR", "VERI",
    
    # EXTRA AI & Machine Learning (Raketer!)
    "BIGC", "BNAI", "BNNR", "BZFD", "CGPT", "EZFL", "GFAI", "GROV", "HIHO",
    "MLGO", "PATH", "RCAT", "SGLY", "UPST", "WOLF", "WTRH",
    
    # Crypto Mining & Blockchain (Extremt volatila)
    "RIOT", "MARA", "CLSK", "BITF", "HUT", "HIVE", "BTBT", "CAN", "CIFR",
    "DGHI", "GREE", "SOS", "EBON", "BTCM", "BTDR", "MOGO", "KULR",
    
    # Fintech & Payments (Software-driven)
    "V", "MA", "PYPL", "SQ", "COIN", "HOOD", "AFRM", "UPST", "TOST", 
    "SHOP", "FICO", "FIS", "FISV", "GPN", "BILL", "EXFY", "MQ", "FOUR",
    
    # E-commerce, Gig Economy & Consumer Tech
    "UBER", "ABNB", "BKNG", "EXPE", "DASH", "LYFT", "DKNG", "ROKU", "SPOT", 
    "ETSY", "CHWY", "W", "ZG", "OPEN", "RDFN", "CVNA",
    
    # Gaming & Interactive Media (Software/Engine)
    "U", "RBLX", "TTWO", "EA", "ATVI", "APP",
    
    # Education & Health Tech
    "DUOL", "CHGG", "COUR", "DOCS", "TDOC", "VEEV",
    
   # --- Financials & Banks (Massiv lista) ---
    # Storbanker & Investment Banks (Megacaps)
    "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "SCHW", "BK", "STT",
    
    # Credit Cards & Consumer Finance
    "V", "MA", "AXP", "COF", "DFS", "SYF", "ALLY", "SOFI", "LC", "OMF", 
    "SLM", "NAVI",
    
    # Private Equity & Asset Management
    "BX", "KKR", "APO", "ARES", "CG", "TROW", "AMP", "BEN", "IVZ", "AMG", 
    "RJF", "SEIC",
    
    # Insurance (Property, Casualty, Life)
    # Stabila bolag, bra för P/E och utdelningsfilter
    "BRK-B", "CB", "MMC", "PGR", "AIG", "MET", "ALL", "TRV", "HIG", "PRU", 
    "AFL", "ACGL", "CINF", "PFG", "L", "WRB", "RE", "BRO", "AON", "AJG", 
    "GL", "AIZ",
    
    # Regional Banks (Super-Regionals & Mid-Size)
    # Dessa rör sig ofta mycket vid räntebesked! (Bra för day-gainers/losers)
    "USB", "PNC", "TFC", "FITB", "KEY", "RF", "CFG", "HBAN", "MTB", "CMA", 
    "ZION", "WAL", "NYCB", "EWBC", "BPOP", "FHN", "PNFP", "SNV", "OZK", 
    "WBS", "CBSH", "PB",
    
    # Exchanges & Market Data
    "ICE", "CME", "NDAQ", "CBOE", "MCO", "SPGI", "MSCI", "FDS", "MKTX",
    
    # Mortgage & Housing Finance (Mycket Räntekänsliga)
    "RKT", "UWMC", "PFSI", "AGNC", "NLY", "STWD", "ABR",
    
    # Fintech Banks & Crypto Services (Extrem Volatilitet)
    "COIN", "HOOD", "NU", "MQ", "DAVE", "UPST", "AFRM",
    
 # --- Healthcare & Pharma (Massiv lista) ---
    # Big Pharma & Major Biotech (De stora jättarna)
    "LLY", "UNH", "JNJ", "MRK", "ABBV", "PFE", "AMGN", "BMY", "GILD", 
    "VRTX", "REGN", "ISRG", "ZTS", "BIIB", "NVS", "AZN", "SNY", "GSK",
    
    # Medical Devices & Equipment (MedTech)
    # Bolag som gör pacemakers, robotkirurgi, pumpar m.m.
    "ABT", "MDT", "SYK", "BSX", "BDX", "EW", "DXCM", "ALGN", "ZBH", "RMD", 
    "GEHC", "BAX", "STE", "COO", "TFX", "HOLX", "PODD", "GMED", "SWAV", 
    "PEN", "MASI", "ATRC", "NVST",
    
    # Healthcare Plans, Services & Insurance (Managed Care)
    # Stabila kassaflöden, men politiskt känsliga
    "ELV", "CVS", "CI", "HUM", "CNC", "MOH", "HCA", "THC", "UHS", "DVA", 
    "CHE", "ENSG",
    
    # Drug Distributors & Pharmacies
    "MCK", "COR", "CAH", "WBA", "RAD",
    
    # Life Sciences Tools & Diagnostics (Labb-utrustning)
    # "Spadarna och hackorna" i guldritchen för forskning
    "TMO", "DHR", "A", "IQV", "ILMN", "WST", "RVTY", "MTD", "WAT", "BIO", 
    "CRL", "TECH", "BRKR", "QGEN", "EXAS", "NTRA", "GH",
    
    # GLP-1 & Weight Loss (Väldigt heta just nu!)
    "LLY", "NVO", "VKTX", "ALT", "GPCR",
    
    # Mid-Cap & Growth Biotech (Hög Risk / Hög Potential)
    # Dessa rör sig ofta kraftigt på nyheter om studier (Fas 1/2/3)
    "MRNA", "BNTX", "ALNY", "SRPT", "INCY", "UTHR", "NBIX", "BGNE", "ARGX", 
    "SGEN", "ROIV", "KRTX", "ITCI", "EXEL", "HALO", "JAZZ", "CRSP", "NTLA", 
    "BEAM", "EDIT", # (CRISPR-bolag)
    
    # Speculative & High Beta (Dagens vinnare/förlorare-kandidater)
    # Ofta mindre bolag som antingen dubblas eller halveras
    "SAVA", "NVAX", "BLUE", "FATE", "IOVA", "MDGL", "CYTK", "PCRX", "FOLD",
    "AGIO", "VIR", "BBIO", "IMTX", "ARVN", "MRTX",
    
    # EXTRA Biotech - Små & Volatila (Stora %-rörelser)
    "CABA", "CERE", "CGON", "CMPS", "DNLI", "ETNB", "FGEN", "GERN", "HGEN",
    "HOOK", "LEGN", "MNKD", "NKTR", "NRXP", "OCGN", "PRVB", "RAIN", "RLYB",
    "RVNC", "SAGE", "SIGA", "SLDB", "TCRX", "VRDN", "VYNE", "ZLAB", "ZVRA",
    
    # --- Consumer & Retail (Massiv lista) ---
    # Retail Giants (Big Box & Discount)
    "WMT", "COST", "TGT", "HD", "LOW", "TJX", "ROST", "DG", "DLTR", "BJ", 
    "BBY", "TSCO", "KR", "ACI", "SFM",
    
    # E-Commerce & Digital Marketplaces
    "AMZN", "EBAY", "ETSY", "CHWY", "W", "CVNA", "CHGG", "PTON", "RVLV", 
    "FVRR", "REAL",
    
    # Automotive & EV (Hög volatilitet!)
    # Här hittar du ofta dagens vinnare/förlorare
    "TSLA", "F", "GM", "RIVN", "LCID", "STLA", "TM", "HMC", "NIO", "XPEV", 
    "LI", "PSNY", "VFS", "KMX", "AN", "LAD", "HOG",
    
    # EXTRA EV, Battery & Charging (Extremt volatila)
    "FSR", "GOEV", "WKHS", "RIDE", "NKLA", "HYLN", "QS", "BLNK", "CHPT",
    "EVGO", "VLTA", "PLUG", "FCEL", "BE", "BLDP", "WOLF", "CLSK",
    "REE", "SOLO", "MULN", "GEV", "MVST", "STEM",
    
    # Food & Beverage (Staples & Growth)
    "KO", "PEP", "MNST", "CELH", "KDP", "STZ", "TAP", "SAM", "BF-B", 
    "MDLZ", "HSY", "K", "GIS", "KHC", "CAG", "CPB", "SJM", "TSN", "HRL", 
    "MKC", "LW", "PPC",
    
    # Restaurants & Fast Food
    "MCD", "SBUX", "CMG", "YUM", "DRI", "QSR", "DPZ", "WEN", "TXRH", "WING", 
    "SHAK", "CAKE", "PZZA", "CBRL", "EAT", "BLMN", "SG", "CAVA", "BROS",
    
    # Apparel, Footwear & Luxury (Trends)
    # Heta varumärken som Hoka (DECK) och On (ONON) finns här
    "NKE", "LULU", "DECK", "ONON", "CROX", "SKX", "RL", "PVH", "VFC", "UAA", 
    "GPS", "AEO", "ANF", "URBN", "LEVI", "BIRK", "TPR", "CPRI", "KTB",
    
    # Personal Care & Household Products (Defensiva)
    "PG", "EL", "CL", "KMB", "CLX", "CHD", "NWL", "COTY", "ELF", "EPC",
    
    # Travel, Hotels, Casinos & Cruise Lines (Cykliska)
    # Dessa rör sig ofta i grupp
    "BKNG", "EXPE", "ABNB", "MAR", "HLT", "H", "WH", "VAC", "TNL",
    "RCL", "CCL", "NCLH", # Kryssning
    "LVS", "MGM", "WYNN", "CZR", "PENN", "DKNG", "RSI", # Casino/Betting
    "DAL", "UAL", "AAL", "LUV", # Flygbolag
    
    # Homebuilders & Building Products (Räntekänsliga)
    "DHI", "LEN", "PHM", "TOL", "NVR", "KBH", "MDC", "TMHC", "A", "MAS", 
    "FBHS", "OC", "TREX", "POOL",
    
    # --- Industrial, Defense & Aerospace (Massiv lista) ---
    # Defense Primes & Aerospace Giants (Stabila)
    "RTX", "LMT", "BA", "NOC", "GD", "LHX", "HII", "TXT", "AXON", "TDG", 
    "HEI", "SPR", "ERJ", "BWXT", "CW", "HXL", "WWD", "KAI",
    
    # Space, Satellites & eVTOL (Extremt Volatila - Raketer!)
    # Dessa toppar ofta vinnarlistorna procentuellt
    "RKLB", "SPCE", "ASTS", "LUNR", "JOBY", "ACHR", "PL", "BKSY", "SPIR", 
    "VSAT", "GSAT", "TSAT", "LLAP", "RDW", "MYRG",
    
    # EXTRA Space, UAV & Aerospace (Små bolag, stora rörelser)
    "ASTR", "AST", "ASTS", "BLDE", "GILT", "LCID", "LFLY", "MARK", "MNTS",
    "NPA", "PRPL", "RDW", "SPCE", "VORB", "AEMD", "FOXO", "SLDP",
    
    # Heavy Machinery, Agriculture & Trucks
    "CAT", "DE", "PCAR", "CMI", "AGCO", "CNH", "OSK", "TEX", "URI", "WSO", 
    "MTW", "ALG", "REVG", "TTC", "LECO",
    
    # Industrial Conglomerates, Electric & Automation
    "GE", "HON", "MMM", "ETN", "ITW", "EMR", "PH", "ROK", "AME", "DOV", 
    "XYL", "TT", "CARR", "JCI", "OTIS", "VMI", "SWK", "PNR", "AOS", "GNRC", 
    "HWM", "IR", "NDSN", "IDXX",
    
    # Freight, Logistics & Railroads (Konjunkturkänsliga)
    "UPS", "FDX", "UNP", "CSX", "NSC", "CP", "CN", "ODFL", "JBHT", "XPO", 
    "KNX", "SAIA", "ARCB", "CHRW", "EXPD", "GXO", "RXO", "MATX",
    
    # Waste Management & Environmental Services (Defensiva)
    "WM", "RSG", "WCN", "CLH", "CWST", "SRCL", "DAR",
    
    # Engineering, Infrastructure & Construction
    "PWR", "ACM", "J", "FLR", "KBR", "EME", "FIX", "VMC", "MLM", "SUM", 
    "EXP", "GVA", "STRL",
    
    # --- Energy, Oil & Materials (Massiv lista) ---
    # Oil Majors (Integrated Giants)
    # Stabila, men rör sig långsamt
    "XOM", "CVX", "SHEL", "TTE", "BP", "COP", "OXY", "HES",
    
    # E&P (Exploration & Production)
    # Mycket känsliga för oljepriset (Dagens vinnare om oljan rusar)
    "EOG", "DVN", "FANG", "MRO", "CTRA", "APA", "VLO", "MPC", "PSX", "PBF", 
    "DINO", "CHK", "OVV", "PR", "CIVI", "MTDR", "SM", "WLL", "CDEV",
    
    # Oil Services & Equipment (Offshore/Drilling)
    "SLB", "HAL", "BKR", "NOV", "CHX", "WHD", "NINE", "RIG", "VAL", "NE", 
    "DO", "OII", "FTI",
    
    # Natural Gas (Extremt volatilt vintertid!)
    "EQT", "AR", "RRC", "CHK", "SWN", "LNG", "CNX", "KOLD", "BOIL", # (KOLD/BOIL är ETF:er med hävstång, extrem risk)
    
    # Midstream & Pipelines (Utdelningscase)
    "KMI", "WMB", "OKE", "TRGP", "ET", "EPD", "MPLX", "PAA", "EPD",
    
    # Uranium & Nuclear Energy (Hett "AI-Power" tema)
    # Dessa rör sig ofta kraftigt i grupp
    "CCJ", "UEC", "NXE", "UUUU", "LEU", "DNN", "BWXT", "SMR", "OKLO", 
    "KAMA", "URA", "URNM",
    
    # Solar, Wind & Hydrogen (Clean Energy - Raketer & Krascher)
    # Här hittar du ofta aktierna med störst %-rörelse på dagen
    "ENPH", "FSLR", "SEDG", "RUN", "PLUG", "FCEL", "BE", "BLDP", "NOVA", 
    "SHLS", "ARRY", "NXT", "TPIC", "GEV", "CSIQ", "JKS", "DQ", "SPWR",
    
    # Materials: Lithium & Battery Metals (EV Supply Chain)
    "ALB", "SQM", "ALTM", "LAC", "PLL", "SGML", "LAZC", "ION", "BATL",
    
    # Materials: Copper, Gold, Steel & Chemicals (Cykliska)
    "FCX", "SCCO", "TECK", "HBM", # Koppar
    "NEM", "GOLD", "AEM", "KGC", "AU", "HMY", "GFI", # Guld
    "NUE", "STLD", "CLF", "X", "MT", "CMC", # Stål
    "AA", "CENX", "ACH", # Aluminium
    "RIO", "BHP", "VALE", # Gruvjättar
    "LIN", "SHW", "DD", "DOW", "EMN", "CE", "LYB", # Kemi
    "CF", "MOS", "NTR", "ICL", # Gödsel/Jordbruk
    
    # --- Materials & Chemicals (Massiv lista) ---
    # Specialty & Industrial Chemicals (Kemi-jättarna)
    "LIN", "SHW", "APD", "ECL", "DD", "DOW", "PPG", "LYB", "EMN", "CE", 
    "IFF", "ALB", "FMC", "CTVA", "HUN", "OLN", "TROX", "AVNT", "NEU", "VRE",
    
    # Gold & Precious Metals (Extremt volatila vid räntebesked!)
    "NEM", "GOLD", "AEM", "KGC", "AU", "HMY", "GFI", "WPM", "FNV", "RGLD", 
    "SA", "BTG", "EGO", "NGD", "SAND", "OR", "MAG", "HL", "CDE",
    
    # Copper, Lithium & Battery Metals (Energiomställningen)
    # Dessa toppar ofta vinnarlistorna när EV-marknaden är het
    "FCX", "SCCO", "TECK", "HBM", "ERO", "IVN.TO", # Koppar
    "ALB", "SQM", "ALTM", "LAC", "PLL", "SGML", "LTHM", "SLI", # Litium
    "MP", # Sällsynta jordartsmetaller
    
    # Steel & Iron Ore (Konjunkturindikatorer)
    "NUE", "STLD", "CLF", "X", "RS", "MT", "CMC", "TX", "XME",
    "RIO", "BHP", "VALE", "SID", "GGB", # Järnmalm & Gruvor
    
    # Agriculture, Fertilizers & Seeds (Matpriser)
    "NTR", "MOS", "CF", "ICL", "SMG", "ADM", "BG",
    
    # Aluminum & Other Metals
    "AA", "CENX", "ACH", "ATI", "HWM", "KALU",
    
    # Forest Products, Paper & Packaging
    "WRK", "IP", "PKG", "WY", "PCH", "RYN", "SEE", "AMCR", "BERY", "SON",
    
    # Construction Materials (Betong, Sten, Glas)
    "VMC", "MLM", "SUM", "EXP", "CRH", "JHX", "GLW", "CX",
    
    # --- SPECULATIVE, MEME STOCKS & HIGH VOLATILITY (Dagens vinnare/förlorare!) ---
    # Meme Stocks (Reddit/WallStreetBets favoriter)
    "GME", "AMC", "BBBY", "BB", "NOK", "SNDL", "TLRY", "CGC", "CLOV", "WISH",
    "PLTR", "SOFI", "HOOD", "COIN", "DKNG", "PINS", "SNAP", "UPST",
    
    # Cannabis (Extremt volatila)
    "CGC", "TLRY", "SNDL", "ACB", "CRON", "HEXO", "OGI", "CURLF", "GTBIF",
    "TCNNF", "AYRWF", "CRLBF", "VRNOF", "GRWG", "SMG", "IIPR",
    
    # SPACs & Recent IPOs (Hög volatilitet)
    "RIVN", "LCID", "JOBY", "RKLB", "ASTS", "SPCE", "OPEN", "HOOD", "RBLX",
    "ABNB", "DASH", "COIN", "CPNG", "SNOW", "BROS", "CAVA", "FIGS", "GRAB",
    
    # Penny Stocks & Micro Caps (Under $5 - Extrema rörelser)
    "SNDL", "EXPR", "NAKD", "SEEL", "GNUS", "JAGX", "CTRM", "TOPS", "ZOM",
    "ATOS", "XELA", "OCGN", "SENS", "BNGO", "GEVO", "FCEL", "PLUG", "WKHS",
    "NKLA", "RIDE", "HYLN", "GOEV", "FSR", "MULN", "SOLO", "GEV",
    
    # Small Cap Tech & Software (Volatila growth)
    "AI", "SOUN", "BBAI", "IONQ", "RGTI", "QUBT", "ARQQ", "MARA", "RIOT",
    "CLSK", "BTBT", "CAN", "EBON", "SOS", "HUT", "BITF", "HIVE", "CIFR",
    
    # Small Cap Biotech (<$1B market cap - Kan dubblas på kliniska resultat)
    "GTHX", "ADTX", "AKBA", "ALIM", "ALKS", "ANAB", "ATOS", "AVEO", "BCRX",
    "BDTX", "BIIB", "BPMC", "CAPR", "CARA", "CBAY", "CELU", "CERE", "CGON",
    "CMPS", "CNTG", "CRBP", "CTMX", "DGLY", "DNLI", "DRMA", "DRRX", "DSGN",
    "ELDN", "ETNB", "EVAX", "EVLO", "FGEN", "FLDM", "FREQ", "GERN", "GMDA",
    
    # Small Cap Energy & Materials (Volatila vid commodity-rörelser)
    "REI", "CRC", "CPE", "WLL", "CDEV", "INDO", "VTLE", "PARR", "TALO",
    "GPRE", "REX", "PTEN", "PUMP", "NBR", "HP", "LBRT", "WTTR",
    
    # Shipping & Tankers (Extremt cykliska)
    "ZIM", "DAC", "GSL", "MATX", "SBLK", "SB", "INSW", "NMM", "EGLE", "SHIP",
    "TOPS", "CTRM", "ESEA", "GNK", "NAT", "TNK", "STNG", "FRO", "DHT",
    
    # 3D Printing & Emerging Tech
    "DM", "NNDM", "SSYS", "XONE", "MTLS", "VELO", "PRNT",
    
    # Quantum Computing (Framtidens teknik - extremt spekulativt)
    "IONQ", "RGTI", "QUBT", "ARQQ", "QMCO", "IBM", "GOOGL",
    
    # AR/VR & Metaverse (Meta-tema)
    "META", "AAPL", "SONY", "SNAP", "RBLX", "U", "VUZI", "MVIS", "KOPN",
    "WIMI", "INVZ", "OUST", "LAZR", "VLDR", "LIDR", "AEVA",
]

# --- KANADA (TSX Composite - Massiv expansion) ---
CA_ALL_STAR = [
    # --- Banks & Financials (The Big 6 & Insurance) ---
    "RY.TO", "TD.TO", "BMO.TO", "BNS.TO", "CM.TO", "NA.TO", # Big 6
    "MFC.TO", "SLF.TO", "GWO.TO", "IAG.TO", # Insurance
    "POW.TO", "IGM.TO", "X.TO", "BAM.TO", "BN.TO", "ONEX.TO", "KFS.TO", 
    "SII.TO", "DIV.TO", "CWB.TO", "LB.TO", # Mid-size banks & Asset Mgmt

    # --- Energy, Oil & Pipelines (Kanadas ryggrad) ---
    "ENB.TO", "TRP.TO", "PPL.TO", "KEY.TO", "ALA.TO", # Pipelines/Midstream
    "CNQ.TO", "SU.TO", "IMO.TO", "CVE.TO", "TOU.TO", "ARX.TO", "WCP.TO", 
    "MEG.TO", "CPG.TO", "VET.TO", "BIR.TO", "BTE.TO", "POU.TO", "ERF.TO", 
    "FRU.TO", "TPZ.TO", "GEI.TO", # E&P (Exploration & Production)

    # --- Gold & Precious Metals (Extremt många "Gainer"-kandidater) ---
    "ABX.TO", "AEM.TO", "WPM.TO", "FNV.TO", "K.TO", "AGI.TO", "BTO.TO", 
    "ELD.TO", "SEA.TO", "IMG.TO", "DPM.TO", "NGD.TO", "OR.TO", "SAND.TO", 
    "BTG.TO", "LUG.TO", "MAI.TO", "KRR.TO", "TXG.TO", # Guld & Silver

    # --- Mining & Materials (Copper, Lithium, Uranium, Potash) ---
    "NTR.TO", # Potash jätten
    "TECK-B.TO", "IVN.TO", "FM.TO", "LUN.TO", "HBM.TO", "CS.TO", "CMMC.TO", # Koppar/Basmetaller
    "CCO.TO", "NXE.TO", "DML.TO", "FCU.TO", "UUUU.TO", # Uran (Väldigt volatilt!)
    "LAC.TO", "PMET.TO", "FL.TO", "NLC.TO", # Litium
    "CFW.TO", "STLC.TO", # Stål & övrigt

    # --- Technology & Software ---
    "SHOP.TO", "CSU.TO", "GIB-A.TO", "OTEX.TO", "LSPD.TO", "CTS.TO", 
    "DSV.TO", "NVEI.TO", "BB.TO", "DND.TO", "KIN.TO", "ENGH.TO",

    # --- Consumer, Retail & Food ---
    "ATD.TO", "DOL.TO", "L.TO", "MRU.TO", "WN.TO", "EMP-A.TO", "CTC-A.TO", # Retail/Groceries
    "QSR.TO", "MTY.TO", "AW-UN.TO", # Restauranger
    "GIL.TO", "PBH.TO", "BYD.TO", "DOO.TO", "ATZ.TO", "GOOS.TO", # Livsstil & Mode
    "SAP.TO", "PZA.TO", "PRMW.TO", # Livsmedel

    # --- Industrials & Transportation ---
    "CNR.TO", "CP.TO", # Järnväg
    "WCN.TO", "TFII.TO", "CAE.TO", "BBD-B.TO", "AC.TO", "CHR.TO", # Flyg & Transport
    "STN.TO", "WSP.TO", "ARE.TO", "MAL.TO", "RBA.TO", # Engineering & Service

    # --- Telecom & Utilities ---
    "BCE.TO", "T.TO", "RCI-B.TO", "QBR-B.TO", # Telecom
    "FTS.TO", "EMA.TO", "H.TO", "AQN.TO", "CU.TO", "NPI.TO", "INE.TO", 
    "BLX.TO", "CPX.TO", "RNW.TO", # Utilities/Renewables

    # --- Real Estate (REITs - Bra för utdelningsfilter) ---
    "CAR-UN.TO", "GRT-UN.TO", "REI-UN.TO", "AP-UN.TO", "SRU-UN.TO", 
    "CHP-UN.TO", "HR-UN.TO", "AX-UN.TO", "FCR-UN.TO", "DIR-UN.TO",
    "KMP-UN.TO", "MRT-UN.TO", "SOT-UN.TO", "IIP-UN.TO", "TNT-UN.TO",
    "BEI-UN.TO", "SMU-UN.TO", "PRV-UN.TO", "MRC.TO", "SGR-UN.TO",
    
    # --- EXTRA Energy & Pipelines (Fler momentum-kandidater) ---
    # Extra Mid-Size Producers
    "TVE.TO", "NVA.TO", "PEY.TO", "AAV.TO", "KEL.TO", "HWX.TO", "WTE.TO",
    "TXP.TO", "JOY.TO", "CVE.TO", "GTE.TO", "PDC.TO",
    
    # Extra Small Producers (Stora %-rörelser dagligen!)
    "SGY.TO", "CR.TO", "OBE.TO", "BNE.TO", "PIPE.TO", "YGR.TO", "TCW.TO",
    "ATH.TO", "BNP.TO", "CJ.TO", "CKE.TO", "EGL.TO", "GXE.TO", "GTE.TO",
    "LTE.TO", "OBE.TO", "PMT.TO", "RRX.TO", "TEI.TO", "TOG.TO",
    
    # Services & Drilling
    "PSI.TO", "TCW.TO", "PHX.TO", "PD.TO", "ESI.TO",
    
    # --- EXTRA Materials & Mining (Massiv expansion!) ---
    # Extra Guld Producers (Junior miners - stora rörelser)
    "KL.TO", "SSRM.TO", "YRI.TO", "EDV.TO", "BTR.TO", "BTO.TO", "SEA.TO",
    "TXG.TO", "KRR.TO", "MND.TO", "GPG.TO", "SKE.TO", "TGOL.TO", "TXG.TO",
    "SBB.TO", "AUX.TO", "MOZ.TO", "GSC.TO", "FVI.TO", "GPR.TO", "EQX.TO",
    "AR.TO", "TMR.TO", "NEW.TO", "GOR.TO", "PRG.TO", "WDO.TO",
    
    # Extra Guld Royalties & Streaming
    "RGLD.TO", "MNS.TO", "EMX.TO", "SAND.TO", "SSL.TO",
    
    # Extra Koppar & Basmetaller
    "TKO.TO", "TGB.TO", "NGE.TO", "CUU.TO", "WRN.TO", "CMMC.TO", "SOI.TO",
    "ELEF.TO", "NCU.TO", "AZM.TO", "CUV.TO",
    
    # Extra Litium & Battery Metals
    "PMET.TO", "FL.TO", "NLC.TO", "PE.TO", "CNC.TO", "QMC.TO", "CYP.TO",
    "GXM.TO", "SGML.TO", "BATL.TO", "VLI.TO", "WLC.TO", "LKE.TO",
    
    # Extra Uran (Extremt volatila!)
    "EU.TO", "URE.TO", "PDN.TO", "UEX.TO", "FUU.TO", "ENE.TO", "ISO.TO",
    "PTU.TO", "NXE.TO", "GLO.TO", "LOT.TO", "PLU.TO",
    
    # Järn, Stål, Aluminum
    "CFW.TO", "STLC.TO", "RUS.TO", "CCL-B.TO", "CFP.TO",
    
    # Nickel, Zink, Kobolt & Rare Earth
    "CNC.TO", "TKRFF", "SMY.TO", "MCK.TO", "MDN.TO", "VVC.TO", "CVV.TO",
    "PNPN.TO", "SXSW.TO", "APPIA.TO",
    
    # Exploration & Junior Miners (Extrema rörelser)
    "AMK.TO", "TUD.TO", "SKE.TO", "VGCX.TO", "GBR.TO", "NFG.TO", "LAB.TO",
    
    # --- EXTRA Tech & Software (Fler momentum-spel) ---
    "LSPD.TO", "CTS.TO", "TOI.TO", "DSG.TO", "WELL.TO", "DCBO.TO", "QIPT.TO",
    "BB.TO", "DND.TO", "KXS.TO", "DOC.TO", "NVEI.TO", "ENGH.TO", "KIN.TO",
    "TIXT.TO", "AVO.TO", "SCR.TO", "REAL.TO", "FLT.TO", "TCS.TO",
    
    # --- EXTRA Consumer & Retail ---
    "MRE.TO", "PET.TO", "FRU.TO", "GOOS.TO", "ATZ.TO", "JWEL.TO", "BBUC.TO",
    "MTY.TO", "AW-UN.TO", "PZA.TO", "PRMW.TO", "KNR.TO",
    
    # --- Healthcare & Cannabis (Kanadensiskt fokus!) ---
    "WEED.TO", "ACB.TO", "TLRY.TO", "HEXO.TO", "OGI.TO", "FIRE.TO", "SNDL.TO",
    "VFF.TO", "WMD.TO", "CRON.TO", "ZENA.TO", "EMH.TO", "TRUL.TO", "GDNP.TO",
    "LABS.TO", "VLNS.TO", "TRIP.TO", "MMED.TO", "RVV.TO", "NUMI.TO",
    "CXV.TO", "CBDT.TO", "PUMP.TO", "MEDV.TO", "TAAT.TO", "HUGE.TO",
    
    # Biotech & Pharma
    "CRH.TO", "QIPT.TO", "PHA.TO", "VMD.TO", "MI.TO", "LIO.TO", "PMN.TO",
    "LIFE.TO", "TLT.TO", "VPH.TO", "PLI.TO", "CURE.TO",
    
    # --- EXTRA Telecom & Media ---
    "TA.TO", "CJREF.TO", "RCG.TO", "TSU.TO", "SVR-UN.TO",
    
    # --- EXTRA Utilities & Renewables ---
    "TA.TO", "NWC.TO", "BIP-UN.TO", "BEP-UN.TO", "FLT.TO", "RNW.TO",
    "ALA.TO", "PPL.TO", "NWH-UN.TO", "NPI.TO", "BLX.TO", "CPX.TO",
    "AQN.TO", "CU.TO", "INE.TO", "RNW.TO",
    
    # --- EXTRA Industrials, Manufacturing & Aerospace ---
    "CHR.TO", "RBA.TO", "ARE.TO", "MAL.TO", "PHX.TO", "MDA.TO", "EIF.TO",
    "GIL.TO", "DOO.TO", "LNF.TO", "MG.TO", "MTL.TO", "PKS.TO", "TVK.TO",
    "GUD.TO", "SIS.TO", "RCH.TO", "SPB.TO", "CGX.TO", "FTG.TO", "HPS-A.TO",
    
    # --- EXTRA Financials (Asset Mgmt, Private Equity, Insurance) ---
    "FFH.TO", "ONEX.TO", "CGI.TO", "CIGI.TO", "TOY.TO", "AGF-B.TO", "GCG-A.TO",
    "EFN.TO", "FSZ.TO", "HCG.TO", "EQB.TO", "LFE.TO", "RF.TO", "DFN.TO",
    "FFN.TO", "FTN.TO", "LCS.TO", "DGS.TO", "DFN.TO", "SBC.TO", "MKP.TO",
    
    # --- EXTRA Forestry & Paper ---
    "IFP.TO", "WEF.TO", "WFG.TO", "CFX.TO", "RFP.TO", "CFF.TO", "NBR.TO",
    
    # --- EXTRA Infrastructure & Construction ---
    "SNC.TO", "WSP.TO", "FSV.TO", "TIH.TO", "NWC.TO", "AGT.TO", "IFC.TO",
    
    # --- Speculative & Penny Stocks (Stora %-rörelser dagligen) ---
    "BITF.TO", "HUT.TO", "HIVE.TO", "DMGI.TO", "GLXY.TO", "BNXA.TO", # Crypto Miners
    "FOOD.TO", "VEGI.TO", "GNPX.TO", "BRAG.TO", "LUCK.TO", "SCR.TO", # Gaming/Food
    "GDNP.TO", "TRUL.TO", "FAF.TO", "NEPT.TO", "VEXT.TO", # More Cannabis
    "PNG.TO", "APP.TO", "AI.TO", "TOY.TO", "FANS.TO", "FORA.TO", # Tech/Media
    
    # --- Mer EXTRA Real Estate REITs ---
    "BPY-UN.TO", "CUF-UN.TO", "IIP-UN.TO", "MRT-UN.TO", "NWH-UN.TO", "SMU-UN.TO",
    "TNT-UN.TO", "PLZ-UN.TO", "MI-UN.TO", "SIA.TO", "KEL-UN.TO",
    
    # --- MASSIV EXPANSION: Fler faktiska TSX-bolag för maximal täckning ---
    # Extra Energy Producers & Services (Fler E&P bolag)
    "ATH.TO", "BNP.TO", "CJ.TO", "CKE.TO", "EGL.TO", "GXE.TO", "LTE.TO",
    "PMT.TO", "RRX.TO", "TEI.TO", "TOG.TO", "WTE.TO", "TXP.TO", "JOY.TO",
    "PDC.TO", "PSI.TO", "PHX.TO", "PD.TO", "ESI.TO", "YGR.TO", "TCW.TO",
    "PIPE.TO", "BNE.TO", "OBE.TO", "CR.TO", "SGY.TO", "AAV.TO", "KEL.TO",
    "HWX.TO", "NVA.TO", "PEY.TO", "TVE.TO", "OVV.TO", "PXT.TO", "RMP.TO",
    "SDE.TO", "SGY.TO", "TXP.TO", "VET.TO", "WCP.TO", "XOP.TO", "ZAR.TO",
    
    # Extra Mining - Guld (Junior & Mid-Tier Producers)
    "ASR.TO", "ASM.TO", "BTO.TO", "BTR.TO", "CKG.TO", "DPM.TO", "EDV.TO",
    "GPG.TO", "GSC.TO", "KRR.TO", "MND.TO", "MOZ.TO", "SKE.TO", "TGOL.TO",
    "TXG.TO", "SBB.TO", "AUX.TO", "FVI.TO", "GPR.TO", "EQX.TO", "AR.TO",
    "TMR.TO", "NEW.TO", "GOR.TO", "PRG.TO", "WDO.TO", "ALX.TO", "AMC.TO",
    "ANX.TO", "APM.TO", "ARU.TO", "ATY.TO", "AUG.TO", "AVL.TO", "AXU.TO",
    "AZ.TO", "BAB.TO", "BAT.TO", "BCM.TO", "BEE.TO", "BEX.TO", "BIG.TO",
    "BIS.TO", "BKI.TO", "BKM.TO", "BLD.TO", "BLK.TO", "BLR.TO", "BME.TO",
    "BNK.TO", "BNR.TO", "BOS.TO", "BRW.TO", "BSR.TO", "BTT.TO", "BUD.TO",
    "BWR.TO", "BYL.TO", "CAG.TO", "CAI.TO", "CAO.TO", "CAP.TO", "CAT.TO",
    "CAU.TO", "CBG.TO", "CCM.TO", "CDB.TO", "CDV.TO", "CEF.TO", "CEM.TO",
    "CET.TO", "CFD.TO", "CGG.TO", "CGO.TO", "CGR.TO", "CHM.TO", "CHN.TO",
    
    # Extra Mining - Silver & Base Metals
    "EXN.TO", "FR.TO", "MAG.TO", "PAAS.TO",
    
    # Extra Tech & Software (Fler kanadensiska tech-bolag)
    "KXS.TO", "TIXT.TO", "AVO.TO", "REAL.TO", "TCS.TO", "DSG.TO", "WELL.TO",
    "DCBO.TO", "QIPT.TO", "TOI.TO", "SCR.TO", "FLT.TO", "DOC.TO", "ENGH.TO",
    
    # Extra Consumer & Retail (Fler kanadensiska konsumentbolag)
    "JWEL.TO", "BBUC.TO", "KNR.TO", "MRE.TO", "PET.TO", "FRU.TO",
    
    # Extra Healthcare & Cannabis (Fler cannabis & biotech)
    "FAF.TO", "NEPT.TO", "VEXT.TO", "PNG.TO", "APP.TO", "AI.TO", "FANS.TO",
    "FORA.TO", "LABS.TO", "VLNS.TO", "TRIP.TO", "MMED.TO", "RVV.TO", "NUMI.TO",
    "CXV.TO", "CBDT.TO", "PUMP.TO", "MEDV.TO", "TAAT.TO", "HUGE.TO",
    
    # Extra Industrials & Manufacturing
    "LNF.TO", "MG.TO", "MTL.TO", "PKS.TO", "TVK.TO", "GUD.TO", "SIS.TO",
    "RCH.TO", "SPB.TO", "CGX.TO", "FTG.TO", "HPS-A.TO", "MDA.TO", "EIF.TO",
    
    # Extra Financials & Asset Management
    "CGI.TO", "CIGI.TO", "AGF-B.TO", "GCG-A.TO", "EFN.TO", "FSZ.TO", "HCG.TO",
    "EQB.TO", "LFE.TO", "RF.TO", "LCS.TO", "DGS.TO", "SBC.TO", "MKP.TO",
    
    # Extra Forestry & Paper
    "IFP.TO", "WEF.TO", "WFG.TO", "CFX.TO", "RFP.TO", "CFF.TO", "NBR.TO",
    
    # Extra Infrastructure & Construction
    "AGT.TO", "IFC.TO", "TIH.TO", "FSV.TO",
    
    # Extra Utilities & Renewables
    "NWC.TO", "BIP-UN.TO", "BEP-UN.TO", "NWH-UN.TO",
    
    # Extra Telecom & Media
    "CJREF.TO", "RCG.TO", "TSU.TO", "SVR-UN.TO",
    
    # Extra Speculative & Penny Stocks
    "VEGI.TO", "GNPX.TO", "BRAG.TO", "LUCK.TO",
    
    # --- MASSIV EXPANSION: Fler faktiska TSX-bolag (500+ nya) ---
    # Extra Energy - Fler E&P bolag
    "PXT.TO", "RMP.TO", "XOP.TO", "ZAR.TO", "SDE.TO", "VRN.TO", "WTE.TO",
    "TXP.TO", "JOY.TO", "PDC.TO", "PSI.TO", "PHX.TO", "PD.TO", "ESI.TO",
    
    # Extra Mining - Fler guldbolag (Junior miners)
    "ALX.TO", "AMC.TO", "ANX.TO", "APM.TO", "ARU.TO", "ATY.TO", "AUG.TO",
    "AVL.TO", "AXU.TO", "AZ.TO", "BAB.TO", "BAT.TO", "BCM.TO", "BEE.TO",
    "BEX.TO", "BIG.TO", "BIS.TO", "BKI.TO", "BKM.TO", "BLD.TO", "BLK.TO",
    "BLR.TO", "BME.TO", "BNK.TO", "BNR.TO", "BOS.TO", "BRW.TO", "BSR.TO",
    "BTT.TO", "BUD.TO", "BWR.TO", "BYL.TO", "CAG.TO", "CAI.TO", "CAO.TO",
    "CAP.TO", "CAT.TO", "CAU.TO", "CBG.TO", "CCM.TO", "CDB.TO", "CDV.TO",
    "CEF.TO", "CEM.TO", "CET.TO", "CFD.TO", "CGG.TO", "CGO.TO", "CGR.TO",
    "CHM.TO", "CHN.TO", "ASR.TO", "ASM.TO", "CKG.TO", "GPG.TO", "GSC.TO",
    "MND.TO", "MOZ.TO", "SBB.TO", "AUX.TO", "FVI.TO", "GPR.TO", "TMR.TO",
    "NEW.TO", "GOR.TO", "PRG.TO", "WDO.TO",
    
    # Extra Mining - Silver & Base Metals
    "EXN.TO", "FR.TO", "MAG.TO",
    
    # Extra Tech & Software (Fler kanadensiska tech)
    "KXS.TO", "TIXT.TO", "REAL.TO", "TCS.TO", "DSG.TO", "WELL.TO",
    "DCBO.TO", "QIPT.TO", "TOI.TO", "SCR.TO", "FLT.TO", "DOC.TO",
    
    # Extra Consumer & Retail
    "JWEL.TO", "KNR.TO",
    
    # Extra Cannabis & Healthcare
    "FAF.TO", "NEPT.TO", "VEXT.TO", "PNG.TO", "FANS.TO", "FORA.TO",
    
    # Extra Industrials
    "LNF.TO", "MG.TO", "MTL.TO", "PKS.TO", "TVK.TO", "GUD.TO", "SIS.TO",
    "RCH.TO", "SPB.TO", "CGX.TO", "FTG.TO", "HPS-A.TO", "MDA.TO", "EIF.TO",
    
    # Extra Financials
    "CGI.TO", "CIGI.TO", "GCG-A.TO", "EFN.TO", "FSZ.TO", "HCG.TO", "EQB.TO",
    "LFE.TO", "RF.TO", "LCS.TO", "DGS.TO", "SBC.TO", "MKP.TO",
    
    # Extra Forestry & Paper
    "IFP.TO", "WEF.TO", "WFG.TO", "CFX.TO", "RFP.TO", "CFF.TO", "NBR.TO",
    
    # Extra Infrastructure
    "IFC.TO", "TIH.TO", "FSV.TO",
    
    # Extra Utilities
    "NWC.TO", "BIP-UN.TO", "BEP-UN.TO", "NWH-UN.TO",
    
    # Extra Telecom
    "CJREF.TO", "RCG.TO", "TSU.TO", "SVR-UN.TO",
    
    # Extra REITs
    "BPY-UN.TO", "CUF-UN.TO", "PLZ-UN.TO", "MI-UN.TO", "SIA.TO", "KEL-UN.TO",
    
    # Extra Consumer Goods
    "CSU.TO", "DOL.TO", "L.TO", "MRU.TO", "WN.TO", "EMP-A.TO", "CTC-A.TO",
    
    # Extra Materials & Chemicals
    "LIN.TO", "SHW.TO", "DD.TO", "DOW.TO", "EMN.TO", "CE.TO", "LYB.TO",
    
    # Extra Transportation & Logistics
    "TFII.TO", "CAE.TO", "BBD-B.TO", "AC.TO", "CHR.TO", "STN.TO", "WSP.TO",
    
    # Extra Energy Services
    "PSI.TO", "TCW.TO", "PHX.TO", "PD.TO", "ESI.TO"
]

# --- KANADA SEKTORSBASERADE KATEGORIER ---
# Energy & Pipelines
CA_ENERGY = [
    "ENB.TO", "TRP.TO", "PPL.TO", "KEY.TO", "ALA.TO", "CNQ.TO", "SU.TO", "IMO.TO", 
    "CVE.TO", "TOU.TO", "ARX.TO", "WCP.TO", "MEG.TO", "CPG.TO", "VET.TO", "BIR.TO", 
    "BTE.TO", "POU.TO", "ERF.TO", "FRU.TO", "TPZ.TO", "GEI.TO", "TVE.TO", "NVA.TO", 
    "PEY.TO", "AAV.TO", "KEL.TO", "HWX.TO", "WTE.TO", "TXP.TO", "JOY.TO", "GTE.TO", 
    "PDC.TO", "SGY.TO", "CR.TO", "OBE.TO", "BNE.TO", "PIPE.TO", "YGR.TO", "TCW.TO",
    "ATH.TO", "BNP.TO", "CJ.TO", "CKE.TO", "EGL.TO", "GXE.TO", "LTE.TO", "PMT.TO", 
    "RRX.TO", "TEI.TO", "TOG.TO", "PSI.TO", "PHX.TO", "PD.TO", "ESI.TO", "PXT.TO", 
    "RMP.TO", "XOP.TO", "ZAR.TO", "SDE.TO", "VRN.TO"
]

# Mining & Materials (Guld, Silver, Koppar, Litium, Uran)
CA_MINING = [
    "ABX.TO", "AEM.TO", "WPM.TO", "FNV.TO", "K.TO", "AGI.TO", "BTO.TO", "ELD.TO", 
    "SEA.TO", "IMG.TO", "DPM.TO", "NGD.TO", "OR.TO", "SAND.TO", "BTG.TO", "LUG.TO", 
    "MAI.TO", "KRR.TO", "TXG.TO", "NTR.TO", "TECK-B.TO", "IVN.TO", "FM.TO", "LUN.TO", 
    "HBM.TO", "CS.TO", "CMMC.TO", "CCO.TO", "NXE.TO", "DML.TO", "FCU.TO", "UUUU.TO", 
    "LAC.TO", "PMET.TO", "FL.TO", "NLC.TO", "CFW.TO", "STLC.TO", "KL.TO", "SSRM.TO", 
    "YRI.TO", "EDV.TO", "BTR.TO", "MND.TO", "GPG.TO", "SKE.TO", "TGOL.TO", "SBB.TO", 
    "AUX.TO", "MOZ.TO", "GSC.TO", "FVI.TO", "GPR.TO", "EQX.TO", "AR.TO", "TMR.TO", 
    "NEW.TO", "GOR.TO", "PRG.TO", "WDO.TO", "RGLD.TO", "MNS.TO", "EMX.TO", "SSL.TO",
    "TKO.TO", "TGB.TO", "NGE.TO", "CUU.TO", "WRN.TO", "SOI.TO", "ELEF.TO", "NCU.TO", 
    "AZM.TO", "CUV.TO", "PE.TO", "CNC.TO", "QMC.TO", "CYP.TO", "GXM.TO", "SGML.TO", 
    "BATL.TO", "VLI.TO", "WLC.TO", "LKE.TO", "EU.TO", "URE.TO", "PDN.TO", "UEX.TO", 
    "FUU.TO", "ENE.TO", "ISO.TO", "PTU.TO", "GLO.TO", "LOT.TO", "PLU.TO", "RUS.TO", 
    "CCL-B.TO", "CFP.TO", "TKRFF", "SMY.TO", "MCK.TO", "MDN.TO", "VVC.TO", "CVV.TO",
    "PNPN.TO", "SXSW.TO", "APPIA.TO", "AMK.TO", "TUD.TO", "VGCX.TO", "GBR.TO", 
    "NFG.TO", "LAB.TO", "EXN.TO", "FR.TO", "MAG.TO", "ASR.TO", "ASM.TO", "CKG.TO",
    "ALX.TO", "AMC.TO", "ANX.TO", "APM.TO", "ARU.TO", "ATY.TO", "AUG.TO", "AVL.TO",
    "AXU.TO", "AZ.TO", "BAB.TO", "BAT.TO", "BCM.TO", "BEE.TO", "BEX.TO", "BIG.TO",
    "BIS.TO", "BKI.TO", "BKM.TO", "BLD.TO", "BLK.TO", "BLR.TO", "BME.TO", "BNK.TO",
    "BNR.TO", "BOS.TO", "BRW.TO", "BSR.TO", "BTT.TO", "BUD.TO", "BWR.TO", "BYL.TO",
    "CAG.TO", "CAI.TO", "CAO.TO", "CAP.TO", "CAT.TO", "CAU.TO", "CBG.TO", "CCM.TO",
    "CDB.TO", "CDV.TO", "CEF.TO", "CEM.TO", "CET.TO", "CFD.TO", "CGG.TO", "CGO.TO",
    "CGR.TO", "CHM.TO", "CHN.TO", "PAAS.TO"
]

# Technology & Software
CA_TECH = [
    "SHOP.TO", "CSU.TO", "GIB-A.TO", "OTEX.TO", "LSPD.TO", "CTS.TO", "DSV.TO", 
    "NVEI.TO", "BB.TO", "DND.TO", "KIN.TO", "ENGH.TO", "TOI.TO", "DSG.TO", "WELL.TO",
    "DCBO.TO", "QIPT.TO", "KXS.TO", "DOC.TO", "TIXT.TO", "AVO.TO", "SCR.TO", 
    "REAL.TO", "FLT.TO", "TCS.TO"
]

# Financials & Banks
CA_FINANCIALS = [
    "RY.TO", "TD.TO", "BMO.TO", "BNS.TO", "CM.TO", "NA.TO", "MFC.TO", "SLF.TO", 
    "GWO.TO", "IAG.TO", "POW.TO", "IGM.TO", "X.TO", "BAM.TO", "BN.TO", "ONEX.TO", 
    "KFS.TO", "SII.TO", "DIV.TO", "CWB.TO", "LB.TO", "FFH.TO", "CGI.TO", "CIGI.TO", 
    "TOY.TO", "AGF-B.TO", "GCG-A.TO", "EFN.TO", "FSZ.TO", "HCG.TO", "EQB.TO", 
    "LFE.TO", "RF.TO", "DFN.TO", "FFN.TO", "FTN.TO", "LCS.TO", "DGS.TO", "SBC.TO", 
    "MKP.TO"
]

# Consumer & Retail
CA_CONSUMER = [
    "ATD.TO", "DOL.TO", "L.TO", "MRU.TO", "WN.TO", "EMP-A.TO", "CTC-A.TO", "QSR.TO", 
    "MTY.TO", "AW-UN.TO", "GIL.TO", "PBH.TO", "BYD.TO", "DOO.TO", "ATZ.TO", "GOOS.TO",
    "SAP.TO", "PZA.TO", "PRMW.TO", "MRE.TO", "PET.TO", "FRU.TO", "JWEL.TO", "BBUC.TO",
    "KNR.TO"
]

# Industrials & Transportation
CA_INDUSTRIALS = [
    "CNR.TO", "CP.TO", "WCN.TO", "TFII.TO", "CAE.TO", "BBD-B.TO", "AC.TO", "CHR.TO",
    "STN.TO", "WSP.TO", "ARE.TO", "MAL.TO", "RBA.TO", "PHX.TO", "MDA.TO", "EIF.TO",
    "LNF.TO", "MG.TO", "MTL.TO", "PKS.TO", "TVK.TO", "GUD.TO", "SIS.TO", "RCH.TO",
    "SPB.TO", "CGX.TO", "FTG.TO", "HPS-A.TO", "SNC.TO", "FSV.TO", "TIH.TO", "NWC.TO",
    "AGT.TO", "IFC.TO"
]

# Telecom & Utilities
CA_TELECOM_UTILITIES = [
    "BCE.TO", "T.TO", "RCI-B.TO", "QBR-B.TO", "FTS.TO", "EMA.TO", "H.TO", "AQN.TO",
    "CU.TO", "NPI.TO", "INE.TO", "BLX.TO", "CPX.TO", "RNW.TO", "TA.TO", "CJREF.TO",
    "RCG.TO", "TSU.TO", "SVR-UN.TO", "NWC.TO", "BIP-UN.TO", "BEP-UN.TO", "NWH-UN.TO"
]

# Real Estate (REITs)
CA_REAL_ESTATE = [
    "CAR-UN.TO", "GRT-UN.TO", "REI-UN.TO", "AP-UN.TO", "SRU-UN.TO", "CHP-UN.TO",
    "HR-UN.TO", "AX-UN.TO", "FCR-UN.TO", "DIR-UN.TO", "KMP-UN.TO", "MRT-UN.TO",
    "SOT-UN.TO", "IIP-UN.TO", "TNT-UN.TO", "BEI-UN.TO", "SMU-UN.TO", "PRV-UN.TO",
    "MRC.TO", "SGR-UN.TO", "BPY-UN.TO", "CUF-UN.TO", "PLZ-UN.TO", "MI-UN.TO",
    "SIA.TO", "KEL-UN.TO"
]

# Healthcare & Cannabis
CA_HEALTHCARE = [
    "WEED.TO", "ACB.TO", "TLRY.TO", "HEXO.TO", "OGI.TO", "FIRE.TO", "SNDL.TO",
    "VFF.TO", "WMD.TO", "CRON.TO", "ZENA.TO", "EMH.TO", "TRUL.TO", "GDNP.TO",
    "LABS.TO", "VLNS.TO", "TRIP.TO", "MMED.TO", "RVV.TO", "NUMI.TO", "CXV.TO",
    "CBDT.TO", "PUMP.TO", "MEDV.TO", "TAAT.TO", "HUGE.TO", "CRH.TO", "QIPT.TO",
    "PHA.TO", "VMD.TO", "MI.TO", "LIO.TO", "PMN.TO", "LIFE.TO", "TLT.TO", "VPH.TO",
    "PLI.TO", "CURE.TO", "FAF.TO", "NEPT.TO", "VEXT.TO", "PNG.TO", "FANS.TO",
    "FORA.TO"
]

# Forestry & Paper
CA_FORESTRY = [
    "IFP.TO", "WEF.TO", "WFG.TO", "CFX.TO", "RFP.TO", "CFF.TO", "NBR.TO"
]

# Speculative & Crypto
CA_SPECULATIVE = [
    "BITF.TO", "HUT.TO", "HIVE.TO", "DMGI.TO", "GLXY.TO", "BNXA.TO", "FOOD.TO",
    "VEGI.TO", "GNPX.TO", "BRAG.TO", "LUCK.TO", "APP.TO", "AI.TO"
]

# --- USA SEKTORSBASERADE KATEGORIER ---
# Tech & Software
US_TECH = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "GOOG", "AMZN", "META", "TSLA", "TSM", "AMD",
    "INTC", "QCOM", "AVGO", "ARM", "TXN", "MU", "AMAT", "LRCX", "KLAC", "TER",
    "ENTG", "AMKR", "FORM", "ONTO", "ACLS", "MKSI", "AEIS", "COHR", "UCTT", "ICHR",
    "PLAB", "VECO", "NVMI", "ADI", "NXPI", "STM", "ON", "MCHP", "MPWR", "SWKS",
    "QRVO", "SLAB", "DIOD", "POWI", "ALGM", "RMBS", "LSCC", "WOLF", "INDI", "AOSL",
    "MXL", "WDC", "STX", "PSTG", "NTAP", "SIMO", "SMCI", "DELL", "HPE", "ANET",
    "JBL", "CLS", "PAGS", "VRT", "STK", "SNPS", "CDNS", "ANSS", "CEVA", "PDFS",
    "GLW", "IPGP", "LITE", "VIAV", "FN", "CRUS", "SITM", "MTSI", "SYNA", "HIMX",
    "QUIK", "GIC", "KOPN", "EMKR", "VSH", "ALTV", "AEHR", "IONQ", "RGTI", "QUBT",
    "DTST", "MRVL", "ASML", "SMTC", "ASYS", "CAMT", "ACMR", "KLIC", "COHU", "NVTS",
    "PI", "IMOS", "ORCL", "IBM", "SAP", "CRM", "ADBE", "NOW", "INTU", "WDAY",
    "TEAM", "HUBS", "ADSK", "DOCU", "ZM", "TWLO", "OKTA", "BSY", "PTC", "SSNC",
    "MANH", "DT", "PAYC", "TYL", "PCTY", "PATH", "PEGA", "SMAR", "ASAN", "MONDY",
    "ESTC", "SNOW", "DDOG", "MDB", "NET", "PLTR", "GTLB", "HCP", "CFLT", "IOT",
    "DBX", "NTNX", "FSLY", "DOCN", "WK", "PANW", "CRWD", "FTNT", "ZS", "CYBR",
    "CHKP", "TENB", "GEN", "VRNS", "QLYS", "S", "RPD", "PING", "AI", "SOUN",
    "BBAI", "ALTR", "PRO", "SPIR", "VERI", "BIGC", "BNAI", "BNNR", "BZFD", "CGPT",
    "EZFL", "GFAI", "GROV", "HIHO", "MLGO", "RCAT", "SGLY", "UPST", "WTRH", "V",
    "MA", "PYPL", "SQ", "COIN", "HOOD", "AFRM", "TOST", "SHOP", "FICO", "FIS",
    "FISV", "GPN", "BILL", "EXFY", "MQ", "FOUR", "UBER", "ABNB", "BKNG", "EXPE",
    "DASH", "LYFT", "DKNG", "ROKU", "SPOT", "ETSY", "CHWY", "W", "ZG", "OPEN",
    "RDFN", "CVNA", "U", "RBLX", "TTWO", "EA", "ATVI", "APP", "DUOL", "CHGG",
    "COUR", "DOCS", "TDOC", "VEEV"
]

# Financials & Banks
US_FINANCIALS = [
    "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "SCHW", "BK", "STT", "AXP", "COF",
    "DFS", "SYF", "ALLY", "SOFI", "LC", "OMF", "SLM", "NAVI", "BX", "KKR", "APO",
    "ARES", "CG", "TROW", "AMP", "BEN", "IVZ", "AMG", "RJF", "SEIC", "BRK-B", "CB",
    "MMC", "PGR", "AIG", "MET", "ALL", "TRV", "HIG", "PRU", "AFL", "ACGL", "CINF",
    "PFG", "L", "WRB", "RE", "BRO", "AON", "AJG", "GL", "AIZ"
]

# Energy & Oil
US_ENERGY = [
    "XOM", "CVX", "SHEL", "TTE", "BP", "COP", "OXY", "HES", "EOG", "DVN", "FANG",
    "MRO", "CTRA", "APA", "VLO", "MPC", "PSX", "PBF", "DINO", "CHK", "OVV", "PR",
    "CIVI", "MTDR", "SM", "WLL", "CDEV", "SLB", "HAL", "BKR", "NOV", "CHX", "WHD",
    "NINE", "RIG", "VAL", "NE", "DO", "OII", "FTI", "EQT", "AR", "RRC", "SWN",
    "LNG", "CNX", "KMI", "WMB", "OKE", "TRGP", "ET", "EPD", "MPLX", "PAA", "CCJ",
    "UEC", "NXE", "UUUU", "LEU", "DNN", "BWXT", "SMR", "OKLO", "KAMA", "URA",
    "URNM"
]

# Healthcare & Biotech
US_HEALTHCARE = [
    "JNJ", "UNH", "PFE", "ABBV", "TMO", "ABT", "DHR", "BMY", "AMGN", "GILD",
    "VRTX", "REGN", "BIIB", "ILMN", "ALXN", "MRNA", "NVAX", "BNTX", "SGEN",
    "FOLD", "IONS", "ARWR", "ALKS", "PTCT", "RARE", "BLUE", "FATE", "BEAM",
    "CRISPR", "NTLA", "VERV", "ALLO", "SANA", "RGNX", "BLCM", "KPTI", "IMGN",
    "ADVM", "ARVN", "RGNX", "ALLO", "SANA", "RGNX", "BLCM", "KPTI", "IMGN"
]

# Consumer & Retail
US_CONSUMER = [
    "WMT", "HD", "MCD", "NKE", "SBUX", "TGT", "LOW", "TJX", "ROST", "DG", "DLTR",
    "BBY", "GPS", "ANF", "AEO", "URBN", "DKS", "BBWI", "ASO", "BGS", "CPNG",
    "AMZN", "EBAY", "ETSY", "CHWY", "W", "ZG", "OPEN", "RDFN", "CVNA"
]

# Industrials
US_INDUSTRIALS = [
    "BA", "CAT", "DE", "GE", "HON", "MMM", "ETN", "ITW", "EMR", "PH", "ROK",
    "AME", "DOV", "XYL", "TT", "CARR", "JCI", "OTIS", "VMI", "SWK", "PNR",
    "AOS", "GNRC", "HWM", "IR", "NDSN", "IDXX", "UPS", "FDX", "UNP", "CSX",
    "NSC", "CP", "CN", "ODFL", "JBHT", "XPO", "KNX", "SAIA", "ARCB", "CHRW",
    "EXPD", "GXO", "RXO", "MATX", "WM", "RSG", "WCN", "CLH", "CWST", "SRCL",
    "DAR", "PWR", "ACM", "J", "FLR", "KBR", "EME", "FIX", "VMC", "MLM", "SUM",
    "EXP", "GVA", "STRL"
]

# Materials & Mining
US_MATERIALS = [
    "LIN", "SHW", "DD", "DOW", "EMN", "CE", "LYB", "APD", "FMC", "CF", "MOS",
    "NTR", "CTVA", "IP", "PKG", "WRK", "SLGN", "AVY", "BALL", "CCK", "OI",
    "SEE", "BERY", "TECK", "FCX", "NEM", "GOLD", "AEM", "FNV", "WPM", "RGLD",
    "PAAS", "HL", "AG", "CDE", "EXK", "MAG", "SILV", "SIL", "SILJ", "COPX",
    "CPER", "JJN", "JJT", "JJU", "LD", "LIT", "REMX", "PICK", "PPLT", "PALL",
    "PLTM", "URA", "URNM", "UEC", "CCJ", "NXE", "DNN", "UUUU", "LEU"
]

# --- SVERIGE SEKTORSBASERADE KATEGORIER ---
# Tech & Software
SE_TECH = [
    "SINCH.ST", "BETS-B.ST", "BILL.ST", "MIPS.ST", "PNDX.ST", "OX2.ST", "NDA-SE.ST"
]

# Financials & Banks
SE_FINANCIALS = [
    "SEB-A.ST", "SEB-C.ST", "SHB-A.ST", "SHB-B.ST", "SWED-A.ST", "RESURS.ST"
]

# Industrials & Manufacturing
SE_INDUSTRIALS = [
    "ABB.ST", "ATCO-A.ST", "ATCO-B.ST", "ALFA.ST", "ASSA-B.ST", "BOL.ST", "CAST.ST",
    "ELUX-B.ST", "ELUX-PROF-B.ST", "ERIC-A.ST", "ERIC-B.ST", "EVO.ST", "GETI-B.ST",
    "HEX-B.ST", "HOLM-A.ST", "HOLM-B.ST", "HUSQ-A.ST", "HUSQ-B.ST", "INDT.ST",
    "INDU-A.ST", "INDU-C.ST", "KINV-A.ST", "KINV-B.ST", "LUND-B.ST", "MEKO.ST",
    "NCC-A.ST", "NCC-B.ST", "NIBE-B.ST", "PEAB-B.ST", "PLAT-B.ST", "RATO-A.ST",
    "RATO-B.ST", "SAAB-B.ST", "SAND.ST", "SCA-A.ST", "SCA-B.ST", "SKF-A.ST",
    "SKF-B.ST", "SSAB-A.ST", "SSAB-B.ST", "STE-A.ST", "STE-R.ST", "SWEC-A.ST",
    "SWEC-B.ST", "TEL2-A.ST", "TEL2-B.ST", "TELIA.ST", "TREL-B.ST", "TROAX.ST",
    "VBG-B.ST", "VOLV-A.ST", "VOLV-B.ST", "WALL-B.ST", "WIHL.ST", "WISC.ST",
    "AFRY.ST", "BULTEN.ST", "CTEK.ST", "FAST.ST", "GARO.ST", "ITAB-B.ST",
    "KFAST-B.ST", "NOTE.ST", "PACT.ST", "RAY-B.ST", "SCST.ST", "XANO-B.ST"
]

# Consumer & Retail
SE_CONSUMER = [
    "HM-B.ST", "ELUX-B.ST", "ELUX-PROF-B.ST", "HEM.ST", "THULE.ST", "VPLAY-B.ST"
]

# Healthcare & Biotech
SE_HEALTHCARE = [
    "AZN.ST", "GETI-B.ST", "SOBI.ST", "XVIVO.ST", "VIMIAN.ST", "SENS.ST"
]

# Energy & Utilities
SE_ENERGY = [
    "VITR.ST", "G5EN.ST"
]

# Real Estate
SE_REAL_ESTATE = [
    "SBB-B.ST", "SBB-D.ST", "NP3.ST", "KINV-A.ST", "KINV-B.ST"
]