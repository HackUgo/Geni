# Geni: The AI Guardian 🛡️🤖
### *Real-Time Safety & Accessibility through Computer Vision*

Geni is an intelligent sensing layer designed to protect elderly independence. It turns standard home cameras into life-saving devices that detect falls and ensure medication adherence without compromising user privacy.

---

## 🚀 The Mission
Inspired by the need to protect our grandparents while respecting their desire for independent living, Geni bridges the gap between **Computer Vision** and **Social Impact**. It acts as a "silent guardian" that only intervenes when a crisis is detected.

## 🛠️ How It Works
Geni utilizes a high-speed pipeline to monitor and respond to emergencies in sub-4 seconds:

1. **Skeletal Tracking:** Uses `YOLOv8-Pose` to monitor 17 keypoints of the human body.
2. **Impact Calculus:** A custom Python state machine calculates vertical velocity to distinguish between sitting and a sudden fall:
   $$v = \frac{y_{current} - y_{previous}}{\Delta t}$$
3. **AI Reasoning:** The `Gemini API` analyzes the scene to verify if the user is in distress or handling the correct medication.
4. **Vocal Interaction:** `ElevenLabs` provides a natural, empathetic voice to check in on the user.
5. **Emergency Dispatch:** If the user is unresponsive, `Twilio` sends an immediate WhatsApp/SMS alert to caretakers.



## 🏗️ Technical Stack
* **Language:** Python 3.10+
* **Vision:** YOLOv8, OpenCV, Gemini Vision API
* **Communication:** Twilio API (WhatsApp/SMS)
* **Audio:** ElevenLabs AI (Text-to-Speech)
* **Frontend:** React & TypeScript (Caretaker Dashboard)

## ⚡ Engineering Challenges
* **Multimodal Integration:** Orchestrating three cloud APIs (Vision, Voice, Comms) to fire in a synchronized sequence without lagging the local vision engine.
* **Background Processing:** Implemented subprocess-level execution to ensure AI voice clips play invisibly without interrupting the real-time detection loop.

---

## 📈 Future Roadmap
- [ ] **Geni Hub:** Porting the logic to a dedicated hardware device (Jetson Nano / Raspberry Pi).
- [ ] **HealthSync:** Bluetooth integration with heart-rate wearables for 360-degree monitoring.
- [ ] **IoT Expansion:** Mesh network of ESP32-CAMs to cover an entire household.

---

## 👨‍💻 Developed By
**Ugonna Victor Emeka-Inegbu** *Electrical Engineering Student @ Central Michigan University* *Aspiring Robotics Engineer*

[LinkedIn](https://www.linkedin.com/in/ugonna-inegbu) | [Portfolio](https://github.com/HackUgo)
