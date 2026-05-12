import sqlite3
import re
conn = sqlite3.connect("/home/misi/MQL5_Theory/mql5_articles_brain2dev.db")
c = conn.cursor()
c.execute("SELECT filepath, content FROM rag_data WHERE content LIKE '%Hidden Markov Model%' LIMIT 3")
results = c.fetchall()
if results:
    for res in results:
        print(f"[Cikk]: {res[0]}")
        # Megkeressük hol van benne a "Hidden Markov Model" és kinyerjük a kontextusát
        match = re.search(r'(.{0,100}Hidden Markov Model.{0,100})', res[1], re.IGNORECASE | re.DOTALL)
        if match:
            print(f"Kontextus:\n...{match.group(1)}...\n")
else:
    print("Nincs egyértelmű Hidden Markov Model találat.")
