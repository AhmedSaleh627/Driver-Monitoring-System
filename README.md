# Driver Monitoring System

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Dataset](#dataset)
   - [Example Images](#example-images)
5. [Kaggle Code for Training](#kaggle-code-for-training)
4. [Model Metrics](#model-metrics)
   - [Model Metrics Graphs](#model-metrics-graphs)
6. [Technologies Used](#technologies-used)
7. [How It Works](#how-it-works)
8. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Clone the Repository](#clone-the-repository)
9. [Future Enhancements](#future-enhancements)

---

## Overview
The **Driver Monitoring System (DMS)** is an AI-powered solution designed to detect drowsy driving behavior in real-time. By leveraging a YOLOv8-based model, the system identifies signs of driver drowsiness and sends an alert if the driver remains unresponsive. This project integrates deep learning, computer vision, and IoT technologies to enhance road safety.

---

## Features
- Real-time drowsiness detection using a YOLOv8 custom-trained model.
- Audible alarm to notify the driver.
- Intuitive GUI for user interaction, allowing the driver to cancel the alert.
- Automated emergency alert system with location tracking and Twilio API integration for SMS or call notifications.
- Failsafe mechanism: Sends an alert with location details if the driver fails to respond.

---

## Dataset
The model was trained on a custom dataset of **10,000+ images**, including:
- **Drowsy driver images:** Captured under various lighting conditions and angles.
- **Non-drowsy driver images:** Covers a wide range of normal driving behaviors.

### Example Images
#### Drowsy Example:
![2023-09-22-17-51-12_mp4-199_jpg rf 73c6890a53bca0b9e616be64a09876b3](https://github.com/user-attachments/assets/b8e713a2-b44b-44c3-a638-512d5bbff01b)


#### Non-Drowsy Example:
![2023-09-22-17-51-12_mp4-58_jpg rf 56581a1ab83818eb3b32a9903cdd8355](https://github.com/user-attachments/assets/8f8b403b-dd26-401b-909b-f6584b41393e)


---
## Kaggle Code for Training
This code provides the training process using YOLOv8, You can view and run the code directly from this link:
https://www.kaggle.com/code/ahmedsaleh627/notebook001d26f6f9

## Model Metrics
The system was trained on the YOLOv8 architecture with the following metrics:
- **Precision:** 95%
- **Recall:** 95%
- **mAP@50:** 98%
---
### Model Metrics Graphs
Below are the graphs that illustrate the model's performance:

- **Training Results:**

  ![results](https://github.com/user-attachments/assets/aae37825-d29e-4435-ac32-24c691b123c0)

- **Precision - Recall Curve:**

  ![PR_curve](https://github.com/user-attachments/assets/63d96fca-fd03-4f2a-87a2-6f69a0d4814b)

- **Confusion Matrix:**

  ![confusion_matrix](https://github.com/user-attachments/assets/61fed1df-eb01-4b68-8d26-99fbb32616cb)

- **Validation Batch:**

  ![val_batch1_pred](https://github.com/user-attachments/assets/76e692bb-7c89-463d-a986-553584edc050)



---
## Technologies Used
- **YOLOv8:** For real-time object detection.
- **OpenCV:** To capture and process video frames.
- **Tkinter:** For GUI implementation.
- **Twilio API:** To send emergency alerts via calls/SMS.
- **LocationIQ API:** For reverse geocoding to get the driver's location.

---

## How It Works
1. **Real-Time Monitoring:** 
   The system captures video frames via webcam and runs inference using the YOLOv8 model.

2. **Drowsiness Detection:** 
   If drowsy behavior is detected for more than 3 seconds, an audible alarm is triggered.

3. **Driver Interaction:**
   - A GUI is displayed, allowing the driver to cancel the alert within 10 seconds.
   - If the driver fails to respond, an emergency alert with the location is sent via Twilio.

---

## Installation

### Prerequisites
- Python 3.8+
- Install the required libraries:
  ```bash
  pip install ultralytics opencv-python requests twilio Location
  ```
### Clone the Repository
```bash
  git clone https://github.com/<your-username>/Driver-Monitoring-System.git
  cd Driver-Monitoring-System  
```
Usage
Place your YOLOv8 model file (best.pt) in the root directory.
Run the script:
```bash
python DMS.py
```
Press q to quit the live inference.

## Future Enhancements
- Add support for multi-driver detection in shared vehicle scenarios.  
- Incorporate more robust environmental handling (e.g., low light, occlusions).  
- Extend to detect other dangerous behaviors (e.g., texting while driving).
- Handling Wearing Sun Glasses
- Integrating this into our Infotainment system
