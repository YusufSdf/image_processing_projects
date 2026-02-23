import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame
import random

# --- 1. CONFIGURATION AND MODEL LOADING ---
model_path = 'hand_landmarker.task' 
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Tracking Survival Game")
clock = pygame.time.Clock()

# MediaPipe Task API Setup
BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1, # Optimized for single hand performance
    min_hand_detection_confidence=0.5
)

# --- 2. GAME OBJECTS AND VARIABLES ---
player_pos = [WIDTH//2, HEIGHT//2]
health = 100
last_hit_time = 0 
enemies = [] 
spawn_delay = 20 
spawn_timer = 0

cap = cv2.VideoCapture(0)

# Main context manager for MediaPipe
with HandLandmarker.create_from_options(options) as landmarker:
    running = True

    while running:
        # Clear the Pygame screen with a dark background
        screen.fill((20, 20, 20)) 
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        success, frame = cap.read()
        if not success: break

        # Preprocessing: Flip and resize frame for display matching
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        # --- LIGHT NORMALIZATION (CLAHE) ---
        # Enhances detection in varying lighting conditions
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        merged = cv2.merge((cl, a, b))
        frame = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

        # Convert image for MediaPipe processing
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        timestamp_ms = int(time.time() * 1000)
        result = landmarker.detect_for_video(mp_image, timestamp_ms)

        # --- 1. HAND TRACKING LOGIC ---
        if result.hand_landmarks:
            hand_landmarks = result.hand_landmarks[0]
            index_finger = hand_landmarks[8] # Tracking index finger tip
            player_pos[0] = int(index_finger.x * WIDTH)
            player_pos[1] = int(index_finger.y * HEIGHT)

        # --- 2. ENEMY SPAWNING ---
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            enemies.append({
                "x": random.randint(0, WIDTH - 50),
                "y": -50,
                "speed": random.randint(5, 10),
                "w": random.randint(40, 60)
            })
            spawn_timer = 0

        # --- 3. COLLISION AND UPDATE LOOP ---
        current_time = time.time()
        player_rect = pygame.Rect(player_pos[0]-15, player_pos[1]-15, 30, 30)
        
        for enemy in enemies[:]:
            enemy["y"] += enemy["speed"] # Move enemy down
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy["w"], enemy["w"])
            
            # Collision Check with Invincibility Frames (0.7s)
            if player_rect.colliderect(enemy_rect):
                if current_time - last_hit_time > 0.7: 
                    health -= 10
                    last_hit_time = current_time
                    if enemy in enemies: enemies.remove(enemy)
                    continue 

            # Memory Management: Remove off-screen enemies
            if enemy["y"] > HEIGHT:
                if enemy in enemies: enemies.remove(enemy)
            else:
                # Draw the enemy
                pygame.draw.rect(screen, (255, 50, 50), enemy_rect)

        # --- 4. UI AND PLAYER RENDERING ---
        # Draw player (finger tip representation)
        pygame.draw.circle(screen, (0, 255, 0), player_pos, 15)
        
        # Draw Health Bar
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, health * 2, 20))
        
        # Check Game Over status
        if health <= 0:
            print("GAME OVER")
            running = False

        # Update Pygame display
        pygame.display.flip()
        clock.tick(60) # Maintain 60 FPS

        # --- DEBUG VIEW (OpenCV) ---
        cv2.putText(frame, f"Health: {health}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Debug View', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
cap.release()
pygame.quit()
cv2.destroyAllWindows()