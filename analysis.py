# utils/process_audio/analysis.py

from difflib import SequenceMatcher

def find_best_match(transcription, ayahs):
    """
    يبحث عن أفضل مطابقة بين النص المنقول والآيات الموجودة.
    
    المعاملات:
    transcription: النص المنقول الذي نريد البحث عن مطابقة له
    ayahs: قائمة من الآيات، كل عنصر يحتوي على (رقم الآية، نص الآية)
    
    المخرجات:
    قاموس يحتوي على أفضل مطابقة تم العثور عليها
    """
    # تهيئة متغيرات لحفظ أفضل نتيجة
    best_match = None
    best_score = 0.0
    
    # البحث في كل الآيات
    for aya_no, aya_text in ayahs:
        # حساب نسبة التشابه بين النص المنقول والآية الحالية
        similarity = SequenceMatcher(None, transcription, aya_text).ratio()
        
        # إذا كانت نسبة التشابه أعلى من السابقة، نحفظ هذه النتيجة
        if similarity > best_score:
            best_score = similarity
            best_match = {
                'aya_no': aya_no,        # رقم الآية
                'aya_text': aya_text,    # نص الآية
                'similarity': similarity  # نسبة التشابه
            }
    
    return best_match

def analyze_transcription(transcription, best_match):
    """
    يحلل النص المنقول ويقارنه مع أفضل آية مطابقة.
    
    المعاملات:
    transcription: النص المنقول المراد تحليله
    best_match: أفضل آية مطابقة (من نتيجة find_best_match)
    
    المخرجات:
    قاموس يحتوي على تحليل تفصيلي للتطابق
    """
    # التحقق من وجود مطابقة
    if not best_match:
        return None

    # استخراج الكلمات الرئيسية (أول 5 كلمات) من الآية
    words = best_match['aya_text'].split()
    key_words = words[:5] if len(words) >= 5 else words

    # تقسيم النصوص إلى كلمات
    transcription_words = transcription.split()
    aya_words = best_match['aya_text'].split()
    
    # تحليل تطابق كل كلمة
    word_matches = []
    for i in range(len(aya_words)):
        if aya_words[i] in key_words:  # نتحقق فقط من الكلمات الرئيسية
            # حساب نسبة تطابق الكلمة إذا كانت موجودة في النص المنقول
            if i < len(transcription_words):
                t_word = transcription_words[i]
                a_word = aya_words[i]
                word_similarity = SequenceMatcher(None, t_word, a_word).ratio()
            else:
                word_similarity = 0.0  # الكلمة غير موجودة في النص المنقول
                
            # إضافة نتيجة تحليل الكلمة
            word_matches.append({
                'index': i,                  # موقع الكلمة في الآية
                'similarity': word_similarity # نسبة تطابق الكلمة
            })
    
    # تجميع نتائج التحليل
    analysis = {
        'aya_no': best_match['aya_no'],      # رقم الآية
        'word_matches': word_matches          # نتائج تحليل الكلمات
    }
    
    return analysis