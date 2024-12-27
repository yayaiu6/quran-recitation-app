# utils/process_audio/transcription.py

# استيراد نموذج التعرف على الكلام من المجلد الأعلى
from ..models import asr_pipeline  # استخدام الاستيراد النسبي

def transcribe_audio(audio_filename):
    """
    تحويل الملف الصوتي إلى نص باستخدام نموذج Whisper للتعرف على الكلام.
    
    المعاملات:
    audio_filename: مسار الملف الصوتي المراد تحويله إلى نص
    
    المخرجات:
    str: النص المستخرج من الملف الصوتي
    
    يرفع:
    Exception: في حالة حدوث خطأ أثناء عملية التحويل
    """
    try:
        # استدعاء نموذج التعرف على الكلام
        transcription_result = asr_pipeline(audio_filename)
        
        # استخراج النص من نتيجة النموذج
        transcription = transcription_result['text']
        
        # طباعة رسالة نجاح مع النص المستخرج
        print(f"Transcription successful: {transcription}")
        
        # إرجاع النص
        return transcription
        
    except Exception as e:
        # في حالة حدوث خطأ، طباعة رسالة الخطأ
        print(f"Transcription error: {e}")
        # إعادة رفع الخطأ للتعامل معه في المستوى الأعلى
        raise