import os
import numpy as np
from PIL import Image

def load_and_preprocess_image(image_path: str, target_size=(224, 224)) -> tuple:
    """
    Loads an image from disk, converts to RGB, resizes, and normalizes pixel values.
    Returns:
        processed_array: Normalized numpy array of shape (1, 224, 224, 3)
        image_metrics: Basic computer vision color distribution metrics
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    # Open using Pillow
    img = Image.open(image_path).convert("RGB")
    original_size = img.size

    # Resize to model input specification
    img_resized = img.resize(target_size)
    img_array = np.array(img_resized, dtype=np.float32)

    # Calculate basic CV color metrics (Chlorophyll green vs necrotic brown/yellow)
    r = img_array[:, :, 0]
    g = img_array[:, :, 1]
    b = img_array[:, :, 2]

    # Healthy green index: Green > Red and Green > Blue
    green_mask = (g > r * 1.1) & (g > b * 1.1)
    green_ratio = float(np.sum(green_mask)) / (target_size[0] * target_size[1])

    # Necrotic/blight spot index: Dark brown/yellow lesions where R and G are high or very dark lesions
    necrotic_mask = ((r > g * 1.1) & (r > b)) | ((r < 50) & (g < 50) & (b < 50))
    necrotic_ratio = float(np.sum(necrotic_mask)) / (target_size[0] * target_size[1])

    # Normalize to [0, 1] range for CNN inference
    normalized_array = img_array / 255.0
    batch_array = np.expand_dims(normalized_array, axis=0)

    image_metrics = {
        "original_width": original_size[0],
        "original_height": original_size[1],
        "target_size": target_size,
        "green_foliage_ratio": round(green_ratio, 3),
        "necrotic_lesion_ratio": round(necrotic_ratio, 3)
    }

    return batch_array, image_metrics
