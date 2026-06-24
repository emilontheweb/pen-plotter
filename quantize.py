from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def load_image(path):
    img = Image.open(path).convert("RGB")
    return np.array(img)

def image_to_pixels(arr):
    return arr.reshape(-1, 3)

def quantize_colors(pixels, n_colors=5):
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    labels = kmeans.fit_predict(pixels)
    palette = kmeans.cluster_centers_.astype("uint8")
    return palette, labels

def quantize_image(arr, palette, labels):
    quantized_pixels = palette[labels]
    return quantized_pixels.reshape(arr.shape)

def build_masks(arr, labels, n_colors):
    label_map = labels.reshape(arr.shape[:2])
    masks = []
    for i in range(n_colors):
        mask = (label_map == i)
        masks.append(mask)
    return masks

if __name__ == "__main__":
    arr = load_image("images/counter.jpg")
    pixels = image_to_pixels(arr)
    palette, labels = quantize_colors(pixels, n_colors=5)
    
    masks = build_masks(arr, labels, n_colors=5)
    for i, mask in enumerate(masks):
        Image.fromarray((mask * 255).astype("uint8")).save(f"output/mask_{i}.png")
        print(f"Saved output/mask_{i}.png — {mask.sum()} pixels")
    
    """ quantized = quantize_image(arr, palette, labels)
    Image.fromarray(quantized).save("output/quantized.png")
    print("Saved output/quantized.png") """
    
    """ print("Palette (RGB):")
    print(palette)
    print("labels shape:", labels.shape) """

