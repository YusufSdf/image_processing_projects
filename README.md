📱 FocusGuard AI: Anti-Distraction System
This project provides a real-time computer vision solution to prevent distractions by monitoring smartphone usage during study or work.

🌐 Language / Dil
English

Türkçe

<a name="english"></a>

🇺🇸 English
🚀 Overview
FocusGuard AI uses YOLOv8 for object detection and MediaPipe for hand tracking to detect when a user's hand touches or reaches for their phone. It serves as a digital study assistant to keep you focused.

🛠️ How It Works
Object Detection: YOLOv8 identifies the coordinates of the "cell phone" (COCO class 67).

Hand Tracking: MediaPipe identifies 21 hand landmarks, specifically focusing on the index finger tip.

Collision Logic: The system checks if the finger's coordinates are within the phone's bounding box.

Warning: If contact is detected, a visual "Put the phone down!" alert appears.

📦 Installation
Install dependencies:

Bash
pip install opencv-python mediapipe ultralytics
Download hand_landmarker.task from MediaPipe and place it in the project folder.

Run the script:

Bash
python no_phone.py
<a name="türkçe"></a>

🇹🇷 Türkçe
🚀 Proje Hakkında
FocusGuard AI, çalışma veya odaklanma süreleri boyunca akıllı telefon kullanımını denetleyen bir yapay zeka sistemidir. YOLOv8 nesne tespiti ve MediaPipe el takibi kütüphanelerini birleştirerek kullanıcının elinin telefona değip değmediğini gerçek zamanlı olarak kontrol eder.

🛠️ Nasıl Çalışır?
Nesne Tespiti: YOLOv8, "cep telefonu" (sınıf 67) koordinatlarını belirler.

El Takibi: MediaPipe, el üzerindeki 21 eklem noktasını tarar ve işaret parmağı ucuna odaklanır.

Çakışma Mantığı: Yazılım, parmak ucunun telefonun etrafındaki kutunun (bounding box) içinde olup olmadığını kontrol eder.

Uyarı: Temas algılandığında ekranda "Telefonu bırak!" uyarısı çıkar.

📦 Kurulum
Gerekli kütüphaneleri yükleyin:

Bash
pip install opencv-python mediapipe ultralytics
MediaPipe'ın hand_landmarker.task dosyasını indirin ve proje klasörüne ekleyin.

Kodu çalıştırın:

Bash
python no_phone.py
📊 Technical Specifications / Teknik Detaylar
Model: YOLOv8s (Small) for balanced performance.

Input Resolution: Optimized at imgsz=320 for higher FPS.

Hand Detection: Supports up to 2 hands simultaneously.

📜 License
This project is open-source and available under the MIT License.
