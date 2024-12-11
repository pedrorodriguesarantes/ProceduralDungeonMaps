from PIL import Image
import numpy as np

def remove_white_pixels(image_path, tolerance=20):
    """
    Remove white pixels (and near-white pixels) from an image and make them transparent.
    The tolerance parameter defines how close a pixel must be to white to be considered white.
    Returns an image with transparency where white or near-white pixels were.
    """
    
    img = Image.open(image_path).convert('RGBA')
    data = np.array(img)

    if data.shape[2] != 4:
        raise ValueError("Image does not have 4 channels (RGBA).")

    white_pixels = np.all(
        (data[:, :, :3] >= (255 - tolerance)) & (data[:, :, :3] <= 255), 
        axis=-1
    )

    data[white_pixels, 3] = 0
    return Image.fromarray(data)