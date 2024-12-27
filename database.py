# utils/process_audio/database.py

import sqlite3
from config import DATABASE_PATH

def get_ayahs(surah_id):
    """
    يجلب الآيات من قاعدة البيانات بناءً على معرف السورة.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT aya_no, aya_text FROM ayahs WHERE surah_id = ? ORDER BY aya_no", (surah_id,))
        ayahs = cursor.fetchall()
        conn.close()
        return ayahs
    except Exception as e:
        print(f"Error retrieving ayahs from database: {e}")
        raise
