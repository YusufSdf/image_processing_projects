import cv2
import mediapipe as mp
import time
from ultralytics import YOLO

# --- MediaPipe Tasks Configuration ---
BaseOptions = mp.tasks.BaseOptions
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Set up Hand Landmarker options for video mode
hand_options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.3,
    min_hand_presence_confidence=0.3,
    min_tracking_confidence=0.3
)

# Initialize YOLOv8 Small model for better accuracy/speed balance
model = YOLO("yolov8s.pt")
class_name = model.names

# Variables for FPS calculation
prev_frame_time = 0
new_frame_time = 0

# Initialize MediaPipe Hand Landmarker
with HandLandmarker.create_from_options(hand_options) as landmarker:
    cap = cv2.VideoCapture(0) # Open default camera

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        frame = cv2.flip(frame, 1) # Mirror the frame for natural interaction
        h, w, _ = frame.shape

        # Reset coordinates each frame to prevent "ghost" detections
        cursor_x, cursor_y = -1, -1

        # --- YOLO Detection Area ---
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Predict only 'cell phone' class (ID 67) with optimized image size
        results = model.predict(source=frame, classes=[67], imgsz=320, verbose=False)

        # Prepare image for MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Calculate timestamp for video stream processing
        timestamp_ms = int(time.time() * 1000)

        # Execute hand landmark detection
        hand_results = landmarker.detect_for_video(mp_image, timestamp_ms)
        
        # Process hand landmarks if detected
        if hand_results.hand_landmarks:
            for hand_landmark in hand_results.hand_landmarks:
                # Landmark 8: Index Finger Tip | Landmark 4: Thumb Tip
                index_finger = hand_landmark[8]
                bas_finger = hand_landmark[4]

                # Convert normalized coordinates to pixel coordinates
                cursor_x = int(index_finger.x * w)
                cursor_y = int(index_finger.y * h)
                cursor_x_bas = int(bas_finger.x * w)
                cursor_y_bas = int(bas_finger.y * h)

                # Draw finger tips on frame
                cv2.circle(frame, (cursor_x, cursor_y), 10, (39, 245, 118), -1)
                cv2.circle(frame, (cursor_x_bas, cursor_y_bas), 10, (39, 49, 245), -1)

        # --- Object Processing and Collision Logic ---
        for r in results:
            for box in r.boxes:
                # Extract bounding box coordinates [x1, y1, x2, y2]
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                
                # Draw bounding box for the phone
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, "cell phone", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # COLLISION CHECK: Check if the index finger tip is inside the phone's box
                if x1 < cursor_x < x2 and y1 < cursor_y < y2:
                    cv2.putText(frame, "put the phone down!", (w//2 - 150, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            

        # --- FPS Calculation and Display ---
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(frame, fps_text, (w - 130, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2)
        
        # Show the processed frame
        cv2.imshow('FocusGuard AI - Anti-Distraction', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()