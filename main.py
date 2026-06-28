from hatch import hatch_mask
from quantize import load_image, image_to_pixels, quantize_colors, build_masks
from svg_builder import build_svg
from gcode_writer import write_gcode

INPUT_PATH = "images/test_pattern.png"
OUTPUT_SVG = "output/album.svg"
OUTPUT_GCODE = "output/album.gcode"
N_COLORS = 5
SPACING = 4
WHITE_CUTOFF = 230

def build_layers(masks, palette, spacing=4, skip=None):
    skip = skip or []
    layers = []
    for i in range(len(masks)):
        if i in skip:
            continue
        lines = hatch_mask(masks[i], spacing)
        color = tuple(int(c) for c in palette[i])
        layers.append({"color": color, "lines": lines})
    return layers

def is_paper(color, cutoff):
    return min(color) >= cutoff

if __name__ == "__main__":
    arr = load_image(INPUT_PATH)
    pixels = image_to_pixels(arr)
    palette, labels = quantize_colors(pixels, N_COLORS)
    skip = []
    for i in range(len(palette)):
        if is_paper(palette[i], WHITE_CUTOFF):
            skip.append(i)
    masks = build_masks(arr, labels, N_COLORS)
    layers = build_layers(masks, palette, SPACING, skip)
    size = (arr.shape[1], arr.shape[0])
    build_svg(layers, size, OUTPUT_SVG)
    write_gcode(layers, arr.shape[1], OUTPUT_GCODE)