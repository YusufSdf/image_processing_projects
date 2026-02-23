AI-Powered Brick Breaker 🕹️
A modern take on the classic Atari Breakout game, controlled entirely by your hand movements using AI-driven Computer Vision.

🚀 Features
Index Finger Control: Move the paddle by moving your finger in front of the webcam.

Real-time Detection: Powered by Mediapipe Tasks API for low-latency hand tracking.

Physics & Audio: Realistic ball bouncing logic with sound effects for collisions and victory.

Procedural Bricks: Colorful bricks generated at the start of each session.

🛠️ Requirements
Python 3.9+

A working Webcam.

hand_landmarker.task file (Place it in the project root).

📦 Installation
Clone the repository:

Bash
git clone https://github.com/yourusername/ai-brick-breaker.git
cd ai-brick-breaker
Install dependencies:

Bash
pip install opencv-python mediapipe pygame
Run the application:

Bash
python main.py
🎮 How to Play
Launch the script and position your hand in the camera view.

Move your index finger left and right to control the paddle.

Break all the bricks to win!

If the ball falls below the paddle, the game is over.
