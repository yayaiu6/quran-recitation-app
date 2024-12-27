// static/script.js

document.addEventListener("DOMContentLoaded", () => {
    const surahSelect = document.getElementById("surahSelect");
    const ayahContainer = document.getElementById("ayahContainer");
    const startListeningBtn = document.getElementById("startListeningBtn");
    const realTimeTextBox = document.getElementById("realTimeTextBox"); // إضافة العنصر الجديد

    let isListening = false;
    let mediaRecorder = null;
    let audioChunks = [];
    let currentSurahId = null;
    let recordingIntervalId = null;

    const API_BASE = ""; // يمكنك تحديد قاعدة URL إذا كان هناك مسار أساسي

    const fetchJSON = async (url, options = {}) => {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`Error: ${response.statusText}`);
        return response.json();
    };

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

    const loadAyahs = async (surahId) => {
        try {
            currentSurahId = surahId;
            const data = await fetchJSON(`${API_BASE}/ayahs/${surahId}`);
            displayAyahs(data.ayahs);
        } catch (error) {
            console.error("Error loading ayahs:", error);
        }
    };

    const displayAyahs = (ayahs) => {
        ayahContainer.innerHTML = ayahs.map(ayah => 
            `<div class="ayah" data-aya-no="${ayah.aya_no}">
                ${ayah.aya_text.split(" ").map((word, index) => 
                    `<span class="word" data-word-index="${index}">${word} </span>`
                ).join('')}
            </div>`
        ).join('');
    };

    // مجموعة لتخزين الكلمات التي تم تمييزها بالفعل
    const highlightedWords = new Set();

    // مؤشر للكلمة الحالية
    let currentWordIndex = 0;

    const updateWordColors = ({ aya_no, word_matches }) => {
        const ayahElement = document.querySelector(`[data-aya-no="${aya_no}"]`);
        if (!ayahElement) return;

        // إعادة تعيين الألوان لجميع الكلمات
        ayahElement.querySelectorAll('.word').forEach(word => {
            word.style.color = 'black';
            // إذا لم يتم تمييز الكلمة بالفعل، قم بإزالة الخلفية
            if (!highlightedWords.has(word.textContent.trim())) {
                word.style.backgroundColor = 'transparent';
            }
        });

        word_matches.forEach(({ index, similarity }) => {
            const wordElement = ayahElement.querySelector(`.word[data-word-index="${index}"]`);
            if (wordElement) {
                const wordText = wordElement.textContent.trim();
                if (similarity >= 0.7 && !highlightedWords.has(wordText)) {
                    wordElement.style.backgroundColor = '#90EE90'; // أخضر
                    highlightedWords.add(wordText);
                    
                    // تسليط الضوء على الكلمة التالية
                    currentWordIndex = index + 1;
                    const nextWordElement = ayahElement.querySelector(`.word[data-word-index="${currentWordIndex}"]`);
                    if (nextWordElement && !highlightedWords.has(nextWordElement.textContent.trim())) {
                        nextWordElement.style.backgroundColor = '#ADD8E6'; // أزرق فاتح للكلمة التالية
                    }
                }
            }
        });

        // تمرير الآية إلى وسط الشاشة
        ayahElement.scrollIntoView({ behavior: "smooth", block: "center" });
        ayahElement.style.backgroundColor = "#FFFFCC";
        setTimeout(() => ayahElement.style.backgroundColor = "transparent", 2000);
    };

    // تحديث النص المنطوق في الوقت الفعلي
    const updateRealTimeText = (text) => {
        realTimeTextBox.style.display = "block"; // إظهار الصندوق
        realTimeTextBox.innerText = text;
    };

    const processAudio = async (audioBlob) => {
        const formData = new FormData();
        formData.append("audio", audioBlob);
        formData.append("surah_id", currentSurahId);

        try {
            const data = await fetchJSON(`${API_BASE}/process-audio`, {
                method: "POST",
                body: formData
            });
            if (data.transcription) {
                updateRealTimeText(data.transcription); // تحديث النص المنطوق
            }
            data.analysis && updateWordColors(data.analysis);
        } catch (error) {
            alert("حدث خطأ أثناء معالجة الصوت. الرجاء المحاولة مرة أخرى.");
            console.error("Error processing audio:", error);
        }
    };

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
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
        }
        if (recordingIntervalId) {
            clearInterval(recordingIntervalId);
        }
    };

    startListeningBtn.addEventListener("click", toggleListening);
    surahSelect.addEventListener("change", e => e.target.value && loadAyahs(e.target.value));

    loadSurahs();
});
