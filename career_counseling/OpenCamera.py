import cv2

def open_camera():
    camera = cv2.VideoCapture(0)  # Open webcam

    if not camera.isOpened():
        print("🚨 Error: Could not open camera!")
        return

    while True:
        ret, frame = camera.read()
        if not ret:
            print("🚨 Error: Failed to grab frame!")
            break

        cv2.imshow("Python Camera", frame)  # OpenCV camera window

        # Press 'q' to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()  # Close OpenCV window

if __name__ == "__main__":
    open_camera()
