# utils/process_audio/process_audio.py
import os
import tempfile
from flask import jsonify
from config import SURAHS_NAMES
from .audio_processing import convert_audio
from .transcription import transcribe_audio
from .database import get_ayahs
from .analysis import find_best_match, analyze_transcription

def process_audio(request):
    """
    معالجة الملف الصوتي وتحليله للمطابقة مع الآيات القرآنية.
    
    المعاملات:
    request: طلب HTTP يحتوي على الملف الصوتي ورقم السورة
    
    المخرجات:
    JSON يحتوي على نتائج التحليل والنص المنقول
    """
    
    # التحقق من وجود الملف الصوتي في الطلب
    if 'audio' not in request.files:
        return jsonify({"error": "No audio data provided"}), 400

    # استخراج الملف الصوتي ورقم السورة من الطلب
    audio_file = request.files['audio']
    surah_id = request.form.get('surah_id')

    # التحقق من وجود رقم السورة
    if not surah_id:
        return jsonify({"error": "No surah_id provided"}), 400

    # إنشاء ملف مؤقت لحفظ الصوت
    with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
        temp_file_name = temp_file.name
        audio_file.save(temp_file_name)

    converted_filename = None

    try:
        # تحويل الملف الصوتي إلى صيغة WAV
        converted_filename = temp_file_name + '_converted.wav'
        convert_audio(temp_file_name, converted_filename)

        # تحويل الصوت إلى نص
        transcription = transcribe_audio(converted_filename)

        # جلب آيات السورة المحددة
        ayahs = get_ayahs(surah_id)

        # البحث عن أفضل مطابقة بين النص والآيات
        best_match = find_best_match(transcription, ayahs)

        if best_match:
            # تحليل النص ومقارنته مع الآية
            analysis = analyze_transcription(transcription, best_match)

            # إرجاع النتائج
            return jsonify({
                'analysis': analysis,          # نتائج التحليل
                'transcription': transcription # النص المنقول
            })
        else:
            # في حالة عدم وجود مطابقة
            return jsonify({"error": "No matching ayah found"}), 400

    except Exception as e:
        # معالجة الأخطاء
        print(f"Error processing audio: {e}")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        # تنظيف الملفات المؤقتة
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
        if converted_filename and os.path.exists(converted_filename):
            os.remove(converted_filename)