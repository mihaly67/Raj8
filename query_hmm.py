import sqlite3
conn = sqlite3.connect("/home/misi/MQL5_Theory/mql5_articles_brain2dev.db")
c = conn.cursor()
c.execute("SELECT filepath, content FROM rag_data WHERE content LIKE '%Hidden Markov Model%' OR content LIKE '%HMM%' LIMIT 5")
results = c.fetchall()
if results:
    for res in results:
        print(f"[TALÁLAT]\nFájl: {res[0]}")
        # A cím a content elején van, kiprinteljük az első kb. 300 karaktert
        print(f"{res[1][:300]}...\n")
else:
    print("Nincs találat.")
