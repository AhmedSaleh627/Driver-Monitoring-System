from ultralytics import YOLO
import cv2
import requests
from twilio.rest import Client
import time
import threading
import winsound  # For playing alarm sounds
import tkinter as tk  # GUI library

# Location and Twilio configuration
LATITUDE = 31.248818720920042
LONGITUDE = 29.969674052607445
LOCATIONIQ_API_KEY = 'xxxxxxxxx'
account_sid = 'xxxxxxxxx'
auth_token = 'xxxxxxxxx'
to_number = 'xxxxxxxxx'
from_number = 'xxxxxxxxx'

# Load the  YOLOv8 model 
model = YOLO("D:/best.pt") 

# Function to get address from latitude and longitude
def get_address(lat, lon):
    url = f'https://us1.locationiq.com/v1/reverse.php?key={LOCATIONIQ_API_KEY}&lat={lat}&lon={lon}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('display_name', 'Unknown location')
    else:
        print("Error:", response.status_code, response.text)
        return 'Unknown location'

# Twilio function to send an alert call
def send_alert_call(address):
    client = Client(account_sid, auth_token)
    twiml_message = f'<Response><Say voice="alice">Driver has been in an accident or is in a drowsy state. Please hurry to the following location: {address}</Say></Response>'
    call = client.calls.create(
        twiml=twiml_message,
        to=to_number,
        from_=from_number
    )
    print("Call placed with location:", address)

# Function to play alarm sound
def play_alarm():
    for _ in range(3):  # Repeat the alarm sound 3 times
        winsound.Beep(frequency=1000, duration=1000)  # Beep at 1000 Hz for 1 second

# Function to display GUI
def show_gui(cancel_callback, timeout_callback):
    root = tk.Tk()
    root.title("Driver Alert")

    label = tk.Label(root, text="Drowsiness detected! Press the button to cancel the alert.", font=("Helvetica", 12))
    label.pack(pady=20)

    cancel_button = tk.Button(root, text="Cancel Alert", font=("Helvetica", 12), command=lambda: [cancel_callback(), root.destroy()])
    cancel_button.pack(pady=10)

    status_label = tk.Label(root, text="", font=("Helvetica", 12))
    status_label.pack(pady=10)

    def timeout_action():
        status_label.config(text="Sending alert...")
        root.update()  # Update the GUI to show the status change
        timeout_callback()
        root.destroy()

    # Automatically trigger timeout_callback after 10 seconds if not canceled
    root.after(10000, timeout_action)

    root.mainloop()

# Open the webcam (camera index 0 for the default webcam)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

drowsy_start_time = None
alert_sent = False

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image from webcam.")
        break

    # Run inference on the current frame
    results = model(frame)

    # Check for drowsiness in the results
    drowsy_detected = False
    for result in results:
        for box in result.boxes:
            # Assuming '1' is the class ID for drowsiness (adjust based on your model's labels)
            if box.cls == 1 and box.conf >= 0.7:  # Only trigger if confidence is above 0.7
                drowsy_detected = True
                break

    # Handle drowsiness detection timing
    if drowsy_detected:
        if drowsy_start_time is None:
            drowsy_start_time = time.time()  # Start timing
        elif time.time() - drowsy_start_time >= 3:  # Check if 3 seconds have passed
            if not alert_sent:
                print("Drowsiness detected for 3 seconds! Alerting driver...")
                threading.Thread(target=play_alarm).start()  # Play alarm in a separate thread

                gui_canceled = [False]

                def cancel_alert():
                    print("Driver responded! Alert canceled.")
                    gui_canceled[0] = True

                def timeout_alert():
                    if not gui_canceled[0]:
                        address = get_address(LATITUDE, LONGITUDE)
                        print("Sending ALERT! Parking Car!")
                        send_alert_call(address)
                        global alert_sent
                        alert_sent = True
                        cap.release()
                        cv2.destroyAllWindows()
                        exit()  # Exit after sending the alert

                # Show GUI for driver interaction
                show_gui(cancel_alert, timeout_alert)

    else:
        drowsy_start_time = None  # Reset timing if no drowsiness is detected

    # Show the frame with bounding boxes in a window
    frame_with_boxes = results[0].plot()  # Add bounding boxes to the frame
    cv2.imshow("YOLOv8 Live Inference", frame_with_boxes)

    # Check if 'q' is pressed to stop the webcam feed manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam capture and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
