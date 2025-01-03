import cv2
import easyocr

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify the language(s) you need

# Capture video from the webcam (or use an image path)
cap = cv2.VideoCapture(0)  # Change to image path if needed

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Use EasyOCR to extract text from the frame
    results = reader.readtext(frame)

    # Draw bounding boxes and extracted text on the frame
    for (bbox, text, prob) in results:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        # Draw the box around the detected text
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # Display the text above the bounding box
        cv2.putText(frame, text, (top_left[0], top_left[1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video Feed', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()