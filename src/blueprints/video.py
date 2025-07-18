# src/blueprints/video.py
from flask import Blueprint, Response, current_app

video_bp = Blueprint("video", __name__, url_prefix="/video")


@video_bp.route("/video_feed")
def video_feed():
    camera = current_app.extensions.get("camera")

    return "Webcam stream is currently disabled.", 403
    # To enable streaming, return:
    # """Video streaming route. Use this in an <img> tag."""
    # return Response(camera.generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
