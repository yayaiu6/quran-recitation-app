# utils/process_audio/audio_processing.py

from pydub import AudioSegment  # استيراد مكتبة pydub للتعامل مع الملفات الصوتية
import os  # استيراد مكتبة os للتعامل مع نظام التشغيل ومسارات الملفات

def convert_audio(input_filename, output_filename, frame_rate=16000, channels=1):
    """
    تحويل الملف الصوتي إلى صيغة WAV مع خصائص محددة.
    
    المعاملات:
    input_filename: مسار الملف الصوتي المدخل
    output_filename: مسار الملف الناتج بعد التحويل
    frame_rate: معدل الإطارات (التردد)، القيمة الافتراضية 16000 هرتز
    channels: عدد القنوات الصوتية، القيمة الافتراضية 1 (أحادي القناة)
    
    المخرجات:
    لا يوجد مخرجات مباشرة، ولكن يتم إنشاء ملف صوتي جديد
    """
    try:
        # قراءة الملف الصوتي المدخل
        audio = AudioSegment.from_file(input_filename)
        
        # ضبط خصائص الملف الصوتي
        audio = audio.set_frame_rate(frame_rate)  # تعيين معدل الإطارات
        audio = audio.set_channels(channels)      # تعيين عدد القنوات
        
        # حفظ الملف بالصيغة الجديدة
        audio.export(output_filename, format='wav')
        
        # طباعة رسالة نجاح
        print(f"Audio converted successfully: {output_filename}")
        
    except Exception as e:
        # في حالة حدوث خطأ، طباعة رسالة الخطأ
        print(f"Error converting audio: {e}")
        raise  # إعادة رفع الاستثناء للتعامل معه في المستوى الأعلى