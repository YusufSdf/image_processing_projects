Hand Tracking Survival Game
Bu proje, MediaPipe Hand Landmarker (yeni nesil Tasks API) ve Pygame kullanılarak geliştirilmiş, işaret parmağı ile kontrol edilen gerçek zamanlı bir hayatta kalma oyunudur.

#🇹🇷 Türkçe Açıklama
Özellikler
Yapay Zeka Destekli Kontrol: İşaret parmağınızın konumuyla eşzamanlı hareket eden oyuncu karakteri.

Görüntü İşleme: CLAHE (Contrast Limited Adaptive Histogram Equalization) ile farklı ışık koşullarında daha stabil el takibi.

Oyun Mekanikleri: Rastgele üretilen düşmanlar, çarpışma algılama, can sistemi ve hasar sonrası dokunulmazlık süresi.

Performans: 60 FPS hedefli, optimize edilmiş kod yapısı.

Gereksinimler
Python 3.9+

Webcam (Kamera)

hand_landmarker.task dosyası (MediaPipe model dosyası)

Kurulum
Gerekli kütüphaneleri yükleyin:

Bash
pip install opencv-python mediapipe pygame
hand_landmarker.task dosyasını Google MediaPipe web sitesinden indirin ve proje ana dizinine koyun.

Oyunu çalıştırın:

Bash
python main.py


#🇺🇸 English Description
Features
AI-Powered Control: A player character that moves synchronously with your index finger position.

Image Processing: Stable hand tracking in various lighting conditions using CLAHE normalization.

Game Mechanics: Procedurally generated enemies, collision detection, health system, and invincibility frames.

Performance: Optimized code structure targeting a smooth 60 FPS experience.

Requirements
Python 3.9+

Webcam

hand_landmarker.task (MediaPipe model file)

Installation
Install the required libraries:

Bash
pip install opencv-python mediapipe pygame
Download the hand_landmarker.task file from the Google MediaPipe website and place it in the project root directory.

Run the game:

Bash
python main.py
🛠 Kullanılan Teknolojiler / Technologies Used
OpenCV: Video capturing and image preprocessing.

MediaPipe Tasks API: Hand landmark detection.

Pygame: Game engine, rendering, and collision logic.
