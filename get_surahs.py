# utils/get_surahs.py

import sqlite3
from config import DATABASE_PATH, SURAHS_NAMES
from flask import jsonify

def get_surahs():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT surah_id FROM ayahs ORDER BY surah_id")
        surahs = [{"surah_id": row[0], "surah_name": SURAHS_NAMES.get(row[0], "غير معروف")} for row in cursor.fetchall()]
        conn.close()
        print(f"Retrieved surahs: {surahs}")  # إضافة سجل للسور المسترجعة
        return jsonify(surahs)
    except Exception as e:
        print(f"Error retrieving surahs: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
