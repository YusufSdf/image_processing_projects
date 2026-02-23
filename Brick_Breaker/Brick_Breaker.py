import cv2
import mediapipe as mp
import time
import pygame
import random
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- 1. AYARLAR ---
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH = 140
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30

pygame.init()
pygame.mixer.init() # Ses sistemi
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Brick Breaker - Level 1")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 64)

# --- 2. SESLERİ YÜKLE ---
try:
    hit_sound = pygame.mixer.Sound("hit.wav") # Tuğla ve raket sesi
    win_sound = pygame.mixer.Sound("win.wav") # Kazanma sesi
except:
    hit_sound = None
    win_sound = None
    print("Ses dosyaları bulunamadı, sessiz devam ediliyor.")

# --- 3. MEDIAPIPE ---
model_path = 'hand_landmarker.task'
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1
)

# --- 4. OYUN NESNELERİ ---
paddle = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball_pos = [WIDTH//2, HEIGHT//2]
ball_speed = [5, -5]
game_over = False
win = False

bricks = []
for r in range(BRICK_ROWS):
    for c in range(BRICK_COLS):
        # Renkli tuğlalar için rastgele renkler
        color = (random.randint(100, 255), random.randint(50, 150), random.randint(50, 150))
        brick_rect = pygame.Rect(c * BRICK_WIDTH + 2, r * BRICK_HEIGHT + 50, BRICK_WIDTH - 4, BRICK_HEIGHT - 4)
        bricks.append({"rect": brick_rect, "color": color})

# --- 5. ANA DÖNGÜ ---
cap = cv2.VideoCapture(0)
with vision.HandLandmarker.create_from_options(options) as landmarker:
    running = True
    while running:
        screen.fill((20, 20, 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        if not game_over and not win:
            success, frame = cap.read()
            if not success: break
            frame = cv2.flip(frame, 1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            result = landmarker.detect_for_video(mp_image, int(time.time() * 1000))

            # RAKET KONTROLÜ
            if result.hand_landmarks:
                index_x = result.hand_landmarks[0][8].x
                paddle.centerx = int(index_x * WIDTH)
                paddle.clamp_ip(screen.get_rect())

            # TOP HAREKETİ
            ball_pos[0] += ball_speed[0]
            ball_pos[1] += ball_speed[1]

            # DUVAR SEKMELERİ
            if ball_pos[0] <= 10 or ball_pos[0] >= WIDTH - 10: 
                ball_speed[0] *= -1
                if hit_sound: hit_sound.play()
            if ball_pos[1] <= 10: 
                ball_speed[1] *= -1
                if hit_sound: hit_sound.play()

            # RAKET SEKME
            ball_rect = pygame.Rect(ball_pos[0]-BALL_RADIUS, ball_pos[1]-BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
            if ball_rect.colliderect(paddle):
                ball_speed[1] *= -1
                ball_pos[1] = paddle.top - BALL_RADIUS
                if hit_sound: hit_sound.play()

            # TUĞLA KIRMA
            for b in bricks[:]:
                if ball_rect.colliderect(b["rect"]):
                    ball_speed[1] *= -1
                    bricks.remove(b)
                    if hit_sound: hit_sound.play()
                    break

            # KAZANMA KONTROLÜ
            if len(bricks) == 0:
                win = True
                if win_sound: win_sound.play()

            # KAYBETME KONTROLÜ
            if ball_pos[1] >= HEIGHT:
                game_over = True

        # --- ÇİZİMLER ---
        pygame.draw.rect(screen, (0, 255, 127), paddle)
        pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
        for b in bricks:
            pygame.draw.rect(screen, b["color"], b["rect"])

        # EKRAN MESAJLARI
        if win:
            msg = font.render("YOU WIN!", True, (0, 255, 0))
            screen.blit(msg, (WIDTH//2 - 140, HEIGHT//2))
        elif game_over:
            msg = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(msg, (WIDTH//2 - 160, HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

cap.release()
pygame.quit()