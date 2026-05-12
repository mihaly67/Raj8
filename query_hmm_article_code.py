import sqlite3
import re
conn = sqlite3.connect("/home/misi/MQL5_Theory/mql5_articles_brain2dev.db")
c = conn.cursor()
c.execute("SELECT content FROM rag_data WHERE filepath = 'article_16830.html'")
res = c.fetchone()
if res:
    idx = res[0].find("[START_ATTACHED_FILE:")
    if idx != -1:
        print("=== CSATOLT FÁJLOK ===")
        print(res[0][idx:idx+800])
    else:
        print("Nincs csatolt zip kód.")
