# utils/get_ayahs.py

import sqlite3
from config import DATABASE_PATH
from flask import jsonify

def get_ayahs(surah_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT aya_no, aya_text FROM ayahs WHERE surah_id = ? ORDER BY aya_no", (surah_id,))
        ayahs = [{"aya_no": row[0], "aya_text": row[1]} for row in cursor.fetchall()]
        conn.close()
        return jsonify({"ayahs": ayahs})
    except Exception as e:
        print(f"Error retrieving ayahs: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
