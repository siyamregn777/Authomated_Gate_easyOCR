import cv2
import easyocr
import requests
import time

# Replace with your IP webcam URL
url = "http://10.6.156.17:8080/video"

def extract_license_plate(frame):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(frame)
    
    # Filter results to find a potential license plate
    for (bbox, text, prob) in results:
        if len(text) >= 5:  # Adjust this condition based on your license plate format
            return text.strip()  # Return the detected license plate text
    return None

def check_plate_in_database(plate):
    response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
    return response.json()

def main():
    max_retries = 5
    cap = None
    # Attempt to connect to the webcam
    for attempt in range(max_retries):
        cap = cv2.VideoCapture(url)
        if cap.isOpened():
            print("Successfully connected to the webcam.")
            break
        print(f"Attempt {attempt + 1} failed, retrying...")
        time.sleep(2)  # Wait before retrying

    if not cap or not cap.isOpened():
        print("Failed to connect to the webcam after multiple attempts.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        # Extract license plate from the current frame
        license_plate = extract_license_plate(frame)
        print(f"Detected License Plate: {license_plate}")

        if license_plate:
            result = check_plate_in_database(license_plate)
            if result.get("registered"):
                print("Access Granted")
            else:
                print("Access Denied")

        time.sleep(1)  # Adjust delay as needed

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()