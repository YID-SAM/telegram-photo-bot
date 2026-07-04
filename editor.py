from PIL import Image
import mediapipe as mp
import numpy as np
from config import Config

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection.FaceDetection(
    model_selection=1,
    min_detection_confidence=0.5
)


def crop_square(img):
    width, height = img.size

    rgb = np.array(img.convert("RGB"))
    results = mp_face_detection.process(rgb)

    size = min(width, height)

    if results.detections:
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box

        face_x = int((bbox.xmin + bbox.width / 2) * width)
        face_y = int((bbox.ymin + bbox.height / 2) * height)
    else:
        face_x = width // 2
        face_y = height // 2

    # Center horizontally
    left = face_x - size // 2

    # Keep the face slightly above center
    top = face_y - int(size * 0.35)

    # Keep crop inside image
    left = max(0, min(left, width - size))
    top = max(0, min(top, height - size))

    right = left + size
    bottom = top + size

    return img.crop((left, top, right, bottom))


def edit_image(input_path, output_path):

    # Open user photo
    photo = Image.open(input_path).convert("RGBA")

    # Face-aware crop
    photo = crop_square(photo)

    # Resize
    photo = photo.resize((1080, 1080), Image.LANCZOS)

    # Open overlay
    overlay = Image.open(Config.OVERLAY_PATH).convert("RGBA")
    overlay = overlay.resize((1080, 1080), Image.LANCZOS)

    # Create transparent canvas
    overlay_canvas = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))

    # Move overlay DOWN by 30 pixels
    # Change 30 to 40 or 50 if you want it lower
    overlay_canvas.paste(overlay, (0, 30), overlay)

    # Merge
    final = Image.alpha_composite(photo, overlay_canvas)

    # Save
    final.convert("RGB").save(output_path, quality=100)