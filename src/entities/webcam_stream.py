import cv2


class WebcamStream:
    def __init__(self, stream_url=None):
        """
       Initialise the video capture.
       If stream_url is None, use default local camera (index 0).
       Otherwise, use the provided URL to open an MJPEG stream.
       """
        if stream_url:
            self.camera = cv2.VideoCapture(stream_url)
        else:
            self.camera = cv2.VideoCapture(0)

    def generate_frames(self):
        """
        Generator that reads frames from the video capture,
        encodes them as JPEG, and yields them as byte sequences
        suitable for multipart HTTP response streaming.
        """
        while True:
            success, frame = self.camera.read()
            if not success:
                break

            ret, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            # Yield multipart HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def release(self):
        """
        Release the video capture device.
        """
        if self.camera.isOpened():
            self.camera.release()
