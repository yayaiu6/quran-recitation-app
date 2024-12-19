document.addEventListener("DOMContentLoaded", () => {
    const surahSelect = document.getElementById("surahSelect");
    const ayahContainer = document.getElementById("ayahContainer");
    const startListeningBtn = document.getElementById("startListeningBtn");

    let isListening = false;
    let mediaRecorder = null;
    let audioChunks = [];
    let currentSurahId = null;
    let recordingIntervalId = null;

    const API_BASE = "http://523c-34-75-67-44.ngrok-free.app";


    // دالة مساعدة للقيام بالطلبات بـ fetch واستخدام async/await
    const fetchJSON = async (url, options = {}) => {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`Error: ${response.statusText}`);
        return response.json();
    };

    // تحميل قائمة السور
    const loadSurahs = async () => {
        try {
            const surahs = await fetchJSON(`${API_BASE}/surahs`);
            surahSelect.innerHTML = '<option value="">-- اختر السورة --</option>';
            surahs.forEach(({ surah_id, surah_name }) => {
                const option = document.createElement("option");
                option.value = surah_id;
                option.textContent = surah_name;
                surahSelect.appendChild(option);
            });
        } catch (error) {
            console.error("Error loading surahs:", error);
        }
    };

    // تحميل الآيات بناءً على السورة المحددة
    const loadAyahs = async (surahId) => {
        try {
            currentSurahId = surahId;
            const data = await fetchJSON(`${API_BASE}/ayahs/${surahId}`);
            displayAyahs(data.ayahs);
        } catch (error) {
            console.error("Error loading ayahs:", error);
        }
    };

    // عرض الآيات وكلماتها
    const displayAyahs = (ayahs) => {
        ayahContainer.innerHTML = ayahs.map(ayah => `
            <div class="ayah" data-aya-no="${ayah.aya_no}">
                ${ayah.aya_text.split(" ").map((word, index) => `
                    <span class="word" data-word-index="${index}">${word} </span>
                `).join('')}
            </div>
        `).join('');
    };

    // تحديث ألوان الكلمات بناءً على التحليل
    const updateWordColors = ({ aya_no, word_matches }) => {
        document.querySelectorAll('.word').forEach(word => {
            word.style.color = 'black';
            word.style.backgroundColor = 'transparent';
        });

        const ayahElement = document.querySelector(`[data-aya-no="${aya_no}"]`);
        if (!ayahElement) return;

        word_matches.forEach(({ index, similarity }) => {
            const wordElement = ayahElement.querySelector(`.word[data-word-index="${index}"]`);
            if (wordElement) {
                wordElement.style.backgroundColor = similarity >= 0.7 ? '#90EE90' : '#FFB6C1';
            }
        });
    };

    // معالجة الصوت المرسل من الميكروفون
    const processAudio = async (audioBlob) => {
        const formData = new FormData();
        formData.append("audio", audioBlob);
        formData.append("surah_id", currentSurahId);

        try {
            console.log("FormData:", Array.from(formData.entries()));
            const data = await fetchJSON(`${API_BASE}/process-audio`, {
                method: "POST",
                body: formData
            });
            console.log("Server response:", data);
            data.analysis && updateWordColors(data.analysis);
        } catch (error) {
            alert("حدث خطأ أثناء معالجة الصوت. الرجاء المحاولة مرة أخرى.");
            console.error("Error processing audio:", error);
        }
    };

    // بدء أو إيقاف الاستماع
    const toggleListening = () => {
        if (!isListening) {
            if (!currentSurahId) {
                alert("الرجاء اختيار السورة أولاً");
                return;
            }
            startListening();
        } else {
            stopListening();
        }
    };

    const startListening = () => {
        isListening = true;
        startListeningBtn.textContent = "إيقاف التسميع";
        audioChunks = [];

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm; codecs=opus' });
                    processAudio(audioBlob);
                };

                mediaRecorder.start();
                recordingIntervalId = setInterval(() => {
                    if (mediaRecorder.state === "recording") {
                        mediaRecorder.stop();
                        mediaRecorder.start();
                    }
                }, 3000);
            })
            .catch(error => {
                alert("يرجى السماح بالوصول إلى الميكروفون");
                console.error("Error accessing microphone:", error);
            });
    };

    const stopListening = () => {
        isListening = false;
        startListeningBtn.textContent = "بدء التسميع";
        mediaRecorder?.state === "recording" && mediaRecorder.stop();
        recordingIntervalId && clearInterval(recordingIntervalId);
    };

    // إعداد الأحداث
    startListeningBtn.addEventListener("click", toggleListening);
    surahSelect.addEventListener("change", e => e.target.value && loadAyahs(e.target.value));

    // تحميل السور عند تحميل الصفحة
    loadSurahs();
});
