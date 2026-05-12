import sqlite3
import re
conn = sqlite3.connect("/home/misi/MQL5_Theory/mql5_articles_brain2dev.db")
c = conn.cursor()
c.execute("SELECT filepath, content FROM rag_data WHERE filepath = 'article_16830.html'")
res = c.fetchone()
if res:
    print(res[1][:1500])
