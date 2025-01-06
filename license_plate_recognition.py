
import cv2
import easyocr
import requests
import time

# Use 0 for the default webcam on your PC
video_source = 0  

# Initialize EasyOCR reader globally to avoid reloading on each frame
reader = easyocr.Reader(['en'])

def extract_license_plate(frame):
    """
    Extract potential license plate text from a video frame using EasyOCR.
    """
    # Convert to grayscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply adaptive thresholding
    thresh_image = cv2.adaptiveThreshold(blurred_image, 255, 
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY_INV, 
                                         11, 2)

    # Perform morphological operations (dilation)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated_image = cv2.dilate(thresh_image, kernel, iterations=1)

    # Perform OCR on the preprocessed image
    results = reader.readtext(dilated_image)
    
    for (bbox, text, prob) in results:
        if len(text) >= 3:  # Adjust based on your needs
            return text.strip()
    
    return None

def check_plate_in_database(plate):
    """
    Check if the license plate exists in the database by sending a request to the API.
    """
    try:
        response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error checking plate in database: {e}")
        return {"registered": False}

def main():
    max_retries = 5
    cap = None

    # Attempt to connect to the webcam
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Failed to connect to the webcam.")
        return

    last_capture_time = time.time()  # Track the last time an image was captured

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        # Display the video feed
        cv2.imshow("Live Feed", frame)

        current_time = time.time()
        
        # Capture an image every 10 seconds
        if current_time - last_capture_time >= 10:
            last_capture_time = current_time
            
            # Extract text from the captured frame
            license_plate = extract_license_plate(frame)
            if license_plate:
                print(f"Detected License Plate: {license_plate}")

                # Check database
                result = check_plate_in_database(license_plate)
                if result.get("registered"):
                    print("Access Granted")
                else:
                    print("Access Denied")
            else:
                print("No license plate detected.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




















# import cv2
# import easyocr
# import requests
# import time

# # Use your IP webcam URL
# video_source = "http://10.5.242.131:8080/video"  # Replace <your_ip> with the IP address of your phone

# # Initialize EasyOCR reader globally to avoid reloading on each frame
# reader = easyocr.Reader(['en'])

# def extract_license_plate(frame):
#     """
#     Extract potential license plate text from a video frame using EasyOCR.
#     """
#     # Convert to grayscale
#     gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Apply Gaussian Blur to reduce noise
#     blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

#     # Apply adaptive thresholding
#     thresh_image = cv2.adaptiveThreshold(blurred_image, 255, 
#                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                                          cv2.THRESH_BINARY_INV, 
#                                          11, 2)

#     # Perform morphological operations (dilation)
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     dilated_image = cv2.dilate(thresh_image, kernel, iterations=1)

#     # Perform OCR on the preprocessed image
#     results = reader.readtext(dilated_image)
    
#     for (bbox, text, prob) in results:
#         if len(text) >= 3:  # Adjust based on your needs
#             return text.strip()
    
#     return None

# def check_plate_in_database(plate):
#     """
#     Check if the license plate exists in the database by sending a request to the API.
#     """
#     try:
#         response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"Error checking plate in database: {e}")
#         return {"registered": False}

# def main():
#     max_retries = 5
#     cap = None

#     # Attempt to connect to the IP webcam
#     cap = cv2.VideoCapture(video_source)
#     if not cap.isOpened():
#         print("Failed to connect to the IP webcam.")
#         return

#     last_capture_time = time.time()  # Track the last time an image was captured

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to read frame from IP webcam.")
#             break

#         # Display the video feed
#         cv2.imshow("Live Feed", frame)

#         current_time = time.time()
        
#         # Capture an image every 10 seconds
#         if current_time - last_capture_time >= 10:
#             last_capture_time = current_time
            
#             # Extract text from the captured frame
#             license_plate = extract_license_plate(frame)
#             if license_plate:
#                 print(f"Detected License Plate: {license_plate}")

#                 # Check database
#                 result = check_plate_in_database(license_plate)
#                 if result.get("registered"):
#                     print("Access Granted")
#                 else:
#                     print("Access Denied")
#             else:
#                 print("No license plate detected.")

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

















