import os
import cv2
from src.utils import running_in_docker


class WebcamStream:
    def __init__(self, stream_url=None):
        """
        Initialise the video capture.
        If stream_url is None, use default local camera (index 0).
        Otherwise, use the provided URL to open an MJPEG stream.
        """
        self.camera = None

        # Do not attempt to use the webcam if inside Docker
        if running_in_docker():
            print("Running inside Docker. Webcam access is disabled.")
            return

        # Try stream URL first if provided
        if stream_url:
            self.camera = cv2.VideoCapture(stream_url)
            if not self.camera.isOpened():
                print(
                    f"Warning: Unable to open stream at {stream_url}. Falling back to local camera."
                )
                self.camera.release()
                self.camera = None

        # Fallback to local webcam if stream not available
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise RuntimeError("Error: Unable to open local camera.")

    def generate_frames(self):
        """
        Generator that reads frames from the video capture,
        encodes them as JPEG, and yields them as byte sequences
        suitable for multipart HTTP response streaming.
        """
        # If webcam is disabled or unavailable, stop streaming
        if self.camera is None or not self.camera.isOpened():
            return

        while True:
            success, frame = self.camera.read()
            if not success:
                break

            ret, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            # Yield multipart HTTP response
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

    def release(self):
        """
        Release the video capture device.
        """
        if self.camera.isOpened():
            self.camera.release()
