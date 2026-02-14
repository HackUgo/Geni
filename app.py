import cv2
from ultralytics import YOLO
import time
import os
import requests
import subprocess
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

# --- 🔑 CONFIG ---
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_NUMBER")
TARGET_WHATSAPP = os.getenv("TARGET_PHONE_WHATSAPP")

def play_voice(text):
    """Plays AI voice via ElevenLabs."""
    print(f"🔊 AI VOICE: {text}")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"}
    data = {"text": text, "model_id": "eleven_monolingual_v1"}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("voice.mp3", "wb") as f:
                f.write(response.content)
            subprocess.Popen('start /min "" "voice.mp3"', shell=True)
    except Exception as e:
        print(f"Voice Error: {e}")

def send_emergency_msg():
    """Dispatches the emergency WhatsApp alert."""
    print("📱 SENDING EMERGENCY WHATSAPP...")
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        client.messages.create(
            body="🚨 *GENI EMERGENCY ALERT*\n\nA fall has been detected. The user is unresponsive.",
            from_=TWILIO_WHATSAPP_FROM,
            to=TARGET_WHATSAPP
        )
        print("✅ WHATSAPP SENT SUCCESSFULLY")
    except Exception as e:
        print(f"Twilio Error: {e}")

# --- VISION SETUP ---
os.environ['YOLO_VERBOSE'] = 'False'
model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

prev_nose_y, prev_hip_y = 0, 0
fall_primed = False
still_seconds = 0
alert_stage = 0 
last_time = time.time()

print("--- GENI MASTER SENSING: ACTIVE ---")

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model(frame, verbose=False)
    person_down = False

    for r in results:
        frame = r.plot(labels=False, boxes=False)
        if r.keypoints and len(r.keypoints.xy[0]) > 11:
            pts = r.keypoints.xy[0]
            try:
                nose_y = pts[0][1].item()
                shoulder_y = ((pts[5][1] + pts[6][1]) / 2).item()
                hip_y = pts[11][1].item()

                # Velocity calculations
                if prev_nose_y != 0:
                    nose_vel = nose_y - prev_nose_y
                    hip_vel = hip_y - prev_hip_y

                    if nose_vel > 35 or hip_vel > 45:
                        fall_primed = True
                        print("⚠️ IMPACT DETECTED")

                if (nose_y > shoulder_y + 40) or (abs(nose_y - hip_y) < 65):
                    person_down = True

                if nose_y < hip_y - 120:
                    fall_primed, still_seconds, alert_stage = False, 0, 0

                prev_nose_y, prev_hip_y = nose_y, hip_y
            except Exception as e:
                continue

    now = time.time()
    dt, last_time = now - last_time, now

    if fall_primed:
        still_seconds += dt
    else:
        still_seconds = 0

    if still_seconds > 2.0 and alert_stage == 0:
        alert_stage = 1
        play_voice("Hey, are you okay?")

    if still_seconds > 4.0 and alert_stage == 1:
        alert_stage = 2
        play_voice("I am notifying your caretaker now.")
        send_emergency_msg()

    # UI Rendering
    color = (0, 255, 0)
    status_text = "GENI: MONITORING"
    if alert_stage == 1:
        color = (0, 215, 255)
        status_text = f"CONFIRMING STATE: {round(still_seconds, 1)}s"
    elif alert_stage == 2:
        color = (0, 0, 255)
        status_text = "EMERGENCY: ALERT DISPATCHED"

    cv2.putText(frame, status_text, (20, 40), 2, 0.7, color, 2)
    cv2.imshow("Geni Master Sensing", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()