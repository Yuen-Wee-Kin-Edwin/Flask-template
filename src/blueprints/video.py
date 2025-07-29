# src/blueprints/video.py
from flask import Blueprint, Response, current_app
from src.utils import running_in_docker

video_bp = Blueprint("video", __name__, url_prefix="/video")


@video_bp.route("/video_feed")
def video_feed():
    if running_in_docker():
        # Disable webcam streaming inside Docker
        return "Webcam stream is currently disabled.", 403

    camera = current_app.extensions.get("camera")
    if not camera:
        return "Camera stream not available.", 503

    # To enable streaming, return:
    """Video streaming route. Use this in an <img> tag."""
    return Response(
        camera.generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )
