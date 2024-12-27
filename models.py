# utils/models.py

from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration
from config import WHISPER_MODEL

# إعداد نموذج Whisper مع التكوين المناسب
processor = WhisperProcessor.from_pretrained(WHISPER_MODEL)
model = WhisperForConditionalGeneration.from_pretrained(WHISPER_MODEL)

# تهيئة خط الأنابيب باستخدام النموذج والمعالج
asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    return_timestamps=False  # تعطيل الطوابع الزمنية بشكل صريح
)
